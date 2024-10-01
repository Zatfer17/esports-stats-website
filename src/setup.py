import os
import hashlib
import pandas as pd

from dotenv import load_dotenv
from lib.download import download_data
from lib.database import setup_database, generate_create_statement, generate_insert_statement 


# Setup environment variables
load_dotenv()
DATA_PATH            = os.environ['DATA_PATH']
DATA_URL             = os.environ['DATA_URL']
DATA_DOWNLOAD_PATH   = os.environ['DATA_DOWNLOAD_PATH']
DATABASE_PATH        = os.environ['DATABASE_PATH']
LEAGUE_MAPPINGS_PATH = os.environ['LEAGUE_MAPPINGS_PATH']

# Download latest data from Oracle's Elixir
download_data(DATA_URL, DATA_DOWNLOAD_PATH, quiet=False)

# Setup database
connection = setup_database(DATA_PATH, DATABASE_PATH)

# Load match stats
## Load league mappings
mappings = pd.read_csv(LEAGUE_MAPPINGS_PATH, keep_default_na=False, na_values='')
mappings_league = {league: maps_to for league, maps_to in zip(mappings.league, mappings.maps_to)}
mappings_region = {league: region for league, region in zip(mappings.league, mappings.region)}
## Create and insert into player_stats and team_stats
FILTERS = [
    'year',
    'region',
    'league',
    'split',
    'playoffs',
    'date',
    'game'
]
INDIVIDUAL_STATS = [
    'patch',
    'teamname',
    'side',

    'position',
    'playername',
    'champion',

    'kills',
    'deaths',
    'assists',
    'firstbloodkill',
    'firstbloodassist',
    'pentakills',

    'dpm',
    'cspm',

    'killsat15',
    'assistsat15',
    'deathsat15',
    'goldat15',
    'xpat15',
    'csat15',
    'golddiffat15',
    'xpdiffat15',
    'csdiffat15',

    'gamelength',
    'result'
]
TEAM_STATS = [
    'patch',
    'teamname',
    'side',
    
    'kills',
    'deaths',
    'assists',
    'firstblood',

    'firstdragon',
    'dragons',
    'firstherald',
    'heralds',
    'firstbaron',
    'barons',
    'elders',
    
    'firsttower',
    'towers',
    'firstmidtower',
    'firsttothreetowers',
    'turretplates',
    'inhibitors',

    'killsat15',
    'assistsat15',
    'deathsat15',
    'goldat15',
    'golddiffat15',

    'gamelength',
    'result'
]
for i, file in enumerate(os.listdir(DATA_DOWNLOAD_PATH)):
    print(f'Processing file: {file}')
    df = pd.read_csv(os.path.join(DATA_DOWNLOAD_PATH, file), low_memory=False)
    df['league'] = df['league'].map(mappings_league)
    df['region'] = df['league'].map(mappings_region)
    df['gameid'] = df.apply(lambda x: hashlib.sha256(str([x[column] for column in FILTERS]).encode('utf-8')).hexdigest(), axis=1)
    individual_df = df.loc[df.position != 'team', ['gameid']+FILTERS+INDIVIDUAL_STATS]
    team_df       = df.loc[df.position == 'team', ['gameid']+FILTERS+TEAM_STATS]
    if i == 0:
        connection.execute(generate_create_statement(table_name='player_stats', df=individual_df))
        connection.execute(generate_create_statement(table_name='team_stats',   df=team_df))
    connection.executemany(generate_insert_statement(table_name='player_stats', df=individual_df), list(individual_df.values))
    connection.executemany(generate_insert_statement(table_name='team_stats',   df=team_df),       list(team_df.values))
connection.commit()
connection.close()