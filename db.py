import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

def get_connection():
    try:
        connection = psycopg2.connect(
            user=os.getenv("user"),
            password=os.getenv("password"),
            host=os.getenv("host"),
            port=os.getenv("port"),
            dbname=os.getenv("dbname")
        )
        return connection
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise
