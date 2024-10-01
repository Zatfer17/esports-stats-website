import os
import sqlite3
import pandas as pd

def connect(db_path):
    return sqlite3.connect(db_path, check_same_thread=False)

def setup_database(data_path, db_path):
    database = [f for f in os.listdir(data_path) if '.db' in f]
    for file in database:
        os.remove(os.path.join(data_path, file))
    return connect(db_path)

def reset_table(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f'DROP table IF EXISTS {table_name}')
    conn.commit()

def reset_database(conn):
    df = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
    for table in df.name:
        reset_table(conn, table)

def generate_create_statement(table_name, df):
    columns = str(list(df.columns)).replace('[', '(').replace(']', ')').replace("'", '')
    return f'CREATE TABLE IF NOT EXISTS {table_name} {columns}'

def generate_insert_statement(table_name, df):
    columns = str(list(df.columns)).replace('[', '(').replace(']', ')').replace("'", '')
    values = str(['?' for _ in df.columns]).replace('[', '(').replace(']', ')').replace("'", '')
    return f'INSERT INTO {table_name} {columns} VALUES {values}'

