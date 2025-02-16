import streamlit as st
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from the .env file
load_dotenv()

# Get the MongoDB URI from environment variables
mongodb_uri = os.getenv("MONGODB_URI")

# Connect to MongoDB
client = MongoClient(mongodb_uri)
db = client.get_database()  # Default to the database specified in the URI

# Access your collections
patients_collection = db.patients