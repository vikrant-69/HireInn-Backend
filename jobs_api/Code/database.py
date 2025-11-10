from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

mongo_uri = os.getenv("MONGODB_URI")
db_name = os.getenv("DB_NAME")

if not mongo_uri:
    raise ValueError("MONGODB_URI environment variable is not set.")

if "?" not in mongo_uri:
    mongo_uri = f"{mongo_uri}?retryWrites=true&w=majority&appName=jobs"

client = MongoClient(mongo_uri)
db = client[db_name]

def get_db():
    return db
																											