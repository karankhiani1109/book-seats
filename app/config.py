import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
# Enable debug mode.
DEBUG = True
# Connect to the database
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@mysql/book_seats?charset=utf8mb4'

SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_COMMIT_ON_TEARDOWN = True