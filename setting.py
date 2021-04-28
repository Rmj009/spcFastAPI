import os
from os.path import join, dirname
from dotenv import dotenv_values,load_dotenv

print('Before load_dotenv()', os.getenv('DOMAIN')) #DBCONN_STR or SERVER IP
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
print('After load_dotenv()', os.getenv('DOMAIN'))


# SECRET_KEY = os.environ.get("SECRET_KEY")
# DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
