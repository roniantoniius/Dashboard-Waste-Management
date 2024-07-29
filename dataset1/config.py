# config.py
from sqlalchemy import create_engine

POSTGRESQL_CONFIG = {
    'database' : 'waste_management1',
    'user'     : 'postgres',
    'password' : 'admin',
    'host'     : 'localhost',
    'port'     : 5432
}

def get_postgresql_engine():
    connection_string = f"postgresql://{POSTGRESQL_CONFIG['user']}:{POSTGRESQL_CONFIG['password']}@{POSTGRESQL_CONFIG['host']}:{POSTGRESQL_CONFIG['port']}/{POSTGRESQL_CONFIG['database']}"
    engine = create_engine(connection_string)
    return engine
