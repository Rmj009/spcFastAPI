# ...
# from app import routes, models, errors

#!/usr/bin/env python
#encoding=utf8
"""
model/__init__.py contains the table definitions, the ORM classes and an init_model() function. 
This init_model() function must be called at application startup. 
"""
import os
from os.path import join, dirname
from dotenv import load_dotenv
from dotenv import dotenv_values
print('Before load_dotenv()', os.getenv('PG_URL')) #DBCONN_STR or SERVER IP
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
print('After load_dotenv()', os.getenv('PG_URL'))

# config = dotenv_values(".env")
# SECRET_KEY = os.environ.get("SECRET_KEY")
# DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
