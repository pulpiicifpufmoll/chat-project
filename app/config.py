import os


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY')

class Database(object):
    driver = os.getenv("DB_SQL_DRIVER")
    server = os.getenv("DB_HOST")
    database = os.getenv("DB_NAME")
    connString = f"DRIVER={driver};SERVER={server};DATABASE={database};TrustServerCertificate=yes;Trusted_connection=yes;"
    user = None
    password = None

