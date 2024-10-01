import streamlit as st

from lib.utils import setup_session_state
from streamlit_extras.badges import badge

setup_session_state(st.session_state)

st.set_page_config(
    page_icon='👋',
    layout='wide'
)

st.title('👋 Welcome')