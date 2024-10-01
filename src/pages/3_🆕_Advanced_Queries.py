import streamlit as st
import pandas as pd

from lib.utils import setup_session_state
from streamlit_ace import st_ace

setup_session_state(st.session_state)

def prohibit_query(query):
    for keyword in [
        'ALTER TABLE',
        'ANALYZE',
        'ATTACH DATABASE',
        'BEGIN TRANSACTION',
        'COMMIT TRANSACTION',
        'CREATE INDEX',
        'CREATE TABLE',
        'CREATE TRIGGER',
        'CREATE VIEW',
        'CREATE VIRTUAL TABLE',
        'DELETE',
        'DETACH DATABASE',
        'DROP INDEX',
        'DROP TABLE',
        'DROP TRIGGER',
        'DROP VIEW',
        'END TRANSACTION',
        'EXPLAIN',
        'INDEXED BY',
        'INSERT',
        'ON CONFLICT',
        'PRAGMA',
        'REINDEX',
        'RELEASE SAVEPOINT',
        'REPLACE',
        'RETURNING',
        'ROLLBACK TRANSACTION',
        'SAVEPOINT',
        'UPDATE',
        'UPSERT',
        'VACUUM',
        'sqlite_master'
    ]:
        if keyword.lower() in query.lower():
            return True
    return False

st.set_page_config(
    page_icon='📈',
    layout='wide'
)

st.title("📈 Advanced queries")

tab1, tab2 = st.tabs(['Query', 'Guide'])

with tab1:
    content = st_ace()
    if content:
        if not prohibit_query(content):
            try:
                result = pd.read_sql(content, st.session_state['connection'])
                st.dataframe(result.head(50))
            except Exception as e:
                st.warning(e, icon="⚠️")
        else:
            st.warning('You are not allowed to run this SQL statement...', icon="⚠️")

with tab2:
    st.markdown('Below the tables you can query:')
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", st.session_state['connection'])
    st.dataframe(tables, hide_index=True)
    st.markdown('With their columns:')
    tabs = st.tabs(list(tables.name))
    for tab, table in zip(tabs, list(tables.name)):
        tab.markdown(f'The *{table}* table has the following columns:')
        columns = pd.read_sql(f"PRAGMA table_info({table})", st.session_state['connection'])
        tab.write(list(columns.name))