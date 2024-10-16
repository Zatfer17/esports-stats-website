import streamlit as st
import pandas as pd

from lib.utils import setup_session_state
from scipy.stats import percentileofscore

setup_session_state(st.session_state)

st.set_page_config(
    page_icon='📈',
    layout='wide'
)

st.title("📈 Inspect a player or a team")

mode = st.selectbox('Player or Team?', ['player', 'team'])

col1, col2 = st.columns(2)
with col1:
    if mode == 'player':
        positions = pd.read_sql(f"SELECT DISTINCT(position) FROM {mode}_stats", st.session_state['connection'])
        position = st.selectbox('Choose a role:', positions.position)
        
        years = pd.read_sql(f"SELECT DISTINCT(year) FROM {mode}_stats WHERE position='{position}' ORDER BY year ASC", st.session_state['connection'])
        year = st.selectbox('Choose a year:', years.year)

        regions = pd.read_sql(f"SELECT DISTINCT(region) FROM {mode}_stats WHERE position='{position}' AND year={year} ORDER BY region ASC", st.session_state['connection'])
        region = st.selectbox('Choose a region:', regions.region)

        leagues = pd.read_sql(f"SELECT DISTINCT(league) FROM {mode}_stats WHERE position='{position}' AND year={year} AND region='{region}' ORDER BY league ASC", st.session_state['connection'])
        league = st.selectbox('Choose a league:', leagues.league)

        teams = pd.read_sql(f"SELECT DISTINCT(teamname) FROM {mode}_stats WHERE position='{position}' AND year={year} AND region='{region}' AND league='{league}' ORDER BY LOWER(teamname) ASC", st.session_state['connection'])
        team = st.selectbox('Choose a team:', teams.teamname)
        
        players = pd.read_sql(f"SELECT DISTINCT(playername) FROM {mode}_stats WHERE position='{position}' AND year={year} AND region='{region}' AND league='{league}' AND teamname='{team}' ORDER BY LOWER(playername) ASC", st.session_state['connection'])
        player = st.selectbox('Choose a player:', players.playername)
    else:
        years = pd.read_sql(f"SELECT DISTINCT(year) FROM {mode}_stats ORDER BY year ASC", st.session_state['connection'])
        year = st.selectbox('Choose a year:', years.year)

        regions = pd.read_sql(f"SELECT DISTINCT(region) FROM {mode}_stats WHERE year={year} ORDER BY region ASC", st.session_state['connection'])
        region = st.selectbox('Choose a region:', regions.region)

        leagues = pd.read_sql(f"SELECT DISTINCT(league) FROM {mode}_stats WHERE year={year} AND region='{region}' ORDER BY league ASC", st.session_state['connection'])
        league = st.selectbox('Choose a league:', leagues.league)

        teams = pd.read_sql(f"SELECT DISTINCT(teamname) FROM {mode}_stats WHERE year={year} AND region='{region}' AND league='{league}' ORDER BY LOWER(teamname) ASC", st.session_state['connection'])
        team = st.selectbox('Choose a team:', teams.teamname)

with col2:

    if mode == 'player':

        stats_raw = pd.read_sql(f'''
        SELECT
            AVG(kills) AS K,
            AVG(deaths) AS D,
            AVG(assists) AS A,
            AVG(dpm) AS DPM,
            AVG(cspm) AS CSPM,
            AVG(killsat15) AS 'K@15',
            AVG(deathsat15) AS 'D@15',
            AVG(assistsat15) AS 'A@15',
            AVG(goldat15) AS 'G@15',
            AVG(golddiffat15) AS 'GDIFF@15',
            AVG(xpat15) AS 'XP@15',
            AVG(xpdiffat15) AS 'XPDIFF@15',
            AVG(csat15) AS 'CS@15',
            AVG(csdiffat15) AS 'CSDIFF@15'
        FROM {mode}_stats
        WHERE
            position='{position}' AND
            year={year} AND
            region='{region}' AND
            league='{league}' AND
            teamname='{team}' AND
            playername='{player}'  
        ''',
        st.session_state['connection']
        )

        stats_comparison = pd.read_sql(f'''
        SELECT
            AVG(kills) AS K,
            AVG(deaths) AS D,
            AVG(assists) AS A,
            AVG(dpm) AS DPM,
            AVG(cspm) AS CSPM,
            AVG(killsat15) AS 'K@15',
            AVG(deathsat15) AS 'D@15',
            AVG(assistsat15) AS 'A@15',
            AVG(goldat15) AS 'G@15',
            AVG(golddiffat15) AS 'GDIFF@15',
            AVG(xpat15) AS 'XP@15',
            AVG(xpdiffat15) AS 'XPDIFF@15',
            AVG(csat15) AS 'CS@15',
            AVG(csdiffat15) AS 'CSDIFF@15'
        FROM {mode}_stats
        WHERE
            position='{position}' AND
            year={year} AND
            league IN ('LCK', 'LPL', 'LEC', 'LCS')
        GROUP BY playername
        ''',
        st.session_state['connection']
        )

    else:

        stats_raw = pd.read_sql(f'''
        SELECT
            AVG(kills) AS K,
            AVG(deaths) AS D,
            AVG(assists) AS A,
            AVG(dragons) AS Dragons,
            AVG(heralds) AS Heralds,
            AVG(barons) AS Barons,                    
            AVG(elders) AS Elders,
            AVG(towers) AS Towers,
            AVG(inhibitors) AS Inhibitors,
            AVG(turretplates) AS TurretPlates,
            AVG(killsat15) AS 'K@15',
            AVG(deathsat15) AS 'D@15',
            AVG(assistsat15) AS 'A@15',
            AVG(goldat15) AS 'G@15',
            AVG(golddiffat15) AS 'GDIFF@15',
            AVG(gamelength) AS GameLength                    
        FROM {mode}_stats
        WHERE
            year={year} AND
            region='{region}' AND
            league='{league}' AND
            teamname='{team}'
        ''',
        st.session_state['connection']
        )

        stats_comparison = pd.read_sql(f'''
        SELECT
            AVG(kills) AS K,
            AVG(deaths) AS D,
            AVG(assists) AS A,
            AVG(dragons) AS Dragons,
            AVG(heralds) AS Heralds,
            AVG(barons) AS Barons,                    
            AVG(elders) AS Elders,
            AVG(towers) AS Towers,
            AVG(inhibitors) AS Inhibitors,
            AVG(turretplates) AS TurretPlates,
            AVG(killsat15) AS 'K@15',
            AVG(deathsat15) AS 'D@15',
            AVG(assistsat15) AS 'A@15',
            AVG(goldat15) AS 'G@15',
            AVG(golddiffat15) AS 'GDIFF@15',
            AVG(gamelength) AS GameLength                    
        FROM {mode}_stats
        WHERE
            year={year} AND
            league IN ('LCK', 'LPL', 'LEC', 'LCS')
        GROUP BY teamname
        ''',
        st.session_state['connection']
        )

    stats = pd.DataFrame(data=None, columns=['Metric', 'Average']).reset_index(drop=True)
    stats['Metric'] = stats_raw.columns
    stats['Average'] = stats_raw.values[0]
    stats['Percentile'] = stats.apply(lambda x: percentileofscore(stats_comparison[x['Metric']], x['Average'], nan_policy='omit', kind='weak'), axis=1)
    stats.loc[stats['Metric'].isin(['D', 'D@15']), 'Percentile'] = 100 - stats.loc[stats['Metric'].isin(['D', 'D@15']), 'Percentile']
    n_rows = len(stats_raw.columns)
    st.dataframe(
        stats,
        hide_index=True,
        use_container_width=True,
        height=int(35.2*(n_rows+1)),
        column_config={
            "Percentile": st.column_config.ProgressColumn(
                help=f"Percentile with respect to other {position if mode=='player' else mode}s in the top 4 leagues (LCK, LPL, LEC, LCS)",
                format="%.2f",
                min_value=0,
                max_value=100,
            ),
        }
    )