from pymongo import MongoClient
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

# Get credentials from environment variables
username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")
cluster_url = os.getenv("MONGODB_CLUSTER_URL")
db_name = os.getenv("MONGODB_DB_NAME")

# URL encode the username and password
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

print(f"Connecting to MongoDB with username: {encoded_username} and password: {encoded_password}")
# Construct the connection string
mongo_uri = f"mongodb+srv://{encoded_username}:{encoded_password}@{cluster_url}/?retryWrites=true&w=majority&appName=jobs"

# mongodb+srv://dsaprep9785:<db_password>@jobs.uoymdwe.mongodb.net/?retryWrites=true&w=majority&appName=jobs

client = MongoClient(mongo_uri)
db = client[db_name]

def get_db():
    return db   


																											