import streamlit as st
import pandas as pd

from lib.utils import setup_session_state
from lib.spider import plot_radar_comparison

setup_session_state(st.session_state)

st.set_page_config(
    page_icon='📈',
    layout='wide'
)

st.title("📈 Compare two players")

positions = pd.read_sql("SELECT DISTINCT(position) FROM player_stats", st.session_state['connection'])
position = st.selectbox('Choose a role:', positions.position)
col1, col2, col3 = st.columns([2,2,3])
with col1:
    years_left = pd.read_sql(f"SELECT DISTINCT(year) FROM player_stats WHERE position='{position}' ORDER BY year ASC", st.session_state['connection'])
    year_left = st.selectbox('Choose a year:', years_left.year, key='year_left')

    regions_left = pd.read_sql(f"SELECT DISTINCT(region) FROM player_stats WHERE position='{position}' AND year={year_left} ORDER BY region ASC", st.session_state['connection'])
    region_left = st.selectbox('Choose a region:', regions_left.region, key='region_left')

    leagues_left = pd.read_sql(f"SELECT DISTINCT(league) FROM player_stats WHERE position='{position}' AND year={year_left} AND region='{region_left}' ORDER BY league ASC", st.session_state['connection'])
    league_left = st.selectbox('Choose a league:', leagues_left.league, key='league_left')

    teams_left = pd.read_sql(f"SELECT DISTINCT(teamname) FROM player_stats WHERE position='{position}' AND year={year_left} AND region='{region_left}' AND league='{league_left}' ORDER BY LOWER(teamname) ASC", st.session_state['connection'])
    team_left = st.selectbox('Choose a team:', teams_left.teamname, key='team_left')
    
    players_left = pd.read_sql(f"SELECT DISTINCT(playername) FROM player_stats WHERE position='{position}' AND year={year_left} AND region='{region_left}' AND league='{league_left}' AND teamname='{team_left}' ORDER BY LOWER(playername) ASC", st.session_state['connection'])
    player_left = st.selectbox('Choose a player:', players_left.playername, key='player_left')

with col2:

    years_right = pd.read_sql(f"SELECT DISTINCT(year) FROM player_stats WHERE position='{position}' ORDER BY year ASC", st.session_state['connection'])
    year_right = st.selectbox('Choose a year:', years_right.year, key='year_right')

    regions_right = pd.read_sql(f"SELECT DISTINCT(region) FROM player_stats WHERE position='{position}' AND year={year_right} ORDER BY region ASC", st.session_state['connection'])
    region_right = st.selectbox('Choose a region:', regions_right.region, key='region_right')

    leagues_right = pd.read_sql(f"SELECT DISTINCT(league) FROM player_stats WHERE position='{position}' AND year={year_right} AND region='{region_right}' ORDER BY league ASC", st.session_state['connection'])
    league_right= st.selectbox('Choose a league:', leagues_right.league, key='league_right')

    teams_right = pd.read_sql(f"SELECT DISTINCT(teamname) FROM player_stats WHERE position='{position}' AND year={year_right} AND region='{region_right}' AND league='{league_right}' ORDER BY LOWER(teamname) ASC", st.session_state['connection'])
    team_right = st.selectbox('Choose a team:', teams_right.teamname, key='team_right')
    
    players_right = pd.read_sql(f"SELECT DISTINCT(playername) FROM player_stats WHERE position='{position}' AND year={year_right} AND region='{region_right}' AND league='{league_right}' AND teamname='{team_right}'ORDER BY LOWER(playername) ASC", st.session_state['connection'])
    player_right = st.selectbox('Choose a player:', players_right.playername, key='player_right')

with col3:

    stats_left = pd.read_sql(f'''
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
    FROM player_stats
    WHERE
        position='{position}' AND
        year={year_left} AND
        region='{region_left}' AND
        league='{league_left}' AND
        teamname='{team_left}' AND
        playername='{player_left}'  
    ''',
    st.session_state['connection']
    )

    stats_right = pd.read_sql(f'''
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
    FROM player_stats
    WHERE
        position='{position}' AND
        year={year_right} AND
        region='{region_right}' AND
        league='{league_right}' AND
        teamname='{team_right}' AND
        playername='{player_right}'  
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
        FROM player_stats
        WHERE
            position='{position}' AND
            league IN ('LCK', 'LPL', 'LEC', 'LCS')
        GROUP BY playername
        ''',
        st.session_state['connection']
    )
    try:
        st.pyplot(plot_radar_comparison(stats_left, stats_right, stats_comparison, player_left, league_left, team_left, year_left, player_right, league_right, team_right, year_right), use_container_width=True)
    except Exception as e:
        st.warning('Try with another selection...', icon="⚠️")