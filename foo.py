from dotenv import dotenv_values,load_dotenv
import os

config = dotenv_values(".env")  
# config = {"USER": "foo", "EMAIL": "foo@example.org"}

# app.config['SQLALCHEMY_DATABASE_URI']

config = {
    **dotenv_values(".env.shared"),  # load shared development variables
    **dotenv_values(".env.secret"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}


print('Before load_dotenv()', os.getenv('DBCONN_STR'))

load_dotenv()

print('After load_dotenv()', os.getenv('DBCONN_STR'))

