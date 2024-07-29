# extract_data.py
import sqlite3
import pandas as pd
from config import get_postgresql_engine

engine_postgres = get_postgresql_engine()
query           = "SELECT * FROM municipal_waste_management"
df              = pd.read_sql(query, engine_postgres)
conn_sqlite     = sqlite3.connect('datawarehouse.db')

df.to_sql('municipal_waste_management', conn_sqlite, if_exists='replace', index=False)
conn_sqlite.close()
