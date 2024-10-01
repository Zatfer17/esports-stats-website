import os
import pandas as pd

from dotenv import load_dotenv
from lib.database import connect

def setup_session_state(session_state):
    load_dotenv()
    if 'connection' not in session_state:
        session_state['connection'] = connect(os.environ['DATABASE_PATH'])
