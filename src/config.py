import os
from dotenv import load_dotenv
from src.db.db import new_database

load_dotenv()

def env_or_throw(key):
    env_variable = os.getenv(key)
    if not env_variable:
        raise Exception(f"{key} variable must be set on env variables.")
    return env_variable

db_path = env_or_throw('DB_PATH')
db = new_database(db_path)
cfg = {
    'db': db
}