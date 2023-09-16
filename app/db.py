import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
database_name: str = os.getenv("DB_NAME")
database_user: str = os.getenv("DB_USERNAME")
database_pass: str = os.getenv("DB_PASSWORD")
database_host: str = os.getenv("DB_HOST")
database_port: str = os.getenv("DB_PORT")


db_client = psycopg2.connect(database=database_name, user = database_user, 
                        host= database_host,
                        password = database_pass,
                        port = database_port)