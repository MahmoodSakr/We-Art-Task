import os 
DEBUG = True
SECRET_KEY= 'we-art-@#$%'
DB_USER='postgres'
DB_PASSWORD='root'
DB_HOST='customers-db'
DB_PORT=5432
DB_NAME='customers'
SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False