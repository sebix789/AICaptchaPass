from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os

DATABASE_URI = os.environ.get('DATABASE_URI', '')
DATABASE_NAME = os.environ.get('DATABASE_NAME', '')


# Create global mongo client

uri = DATABASE_URI
# TODO: tlsAllowInvalidCertificates have to be removed in production code ⬇️
client = MongoClient(uri, server_api=ServerApi('1'), tlsAllowInvalidCertificates=True)

# get database
db = client[DATABASE_NAME]

def get_db():
    return db

def close_db():
    pass