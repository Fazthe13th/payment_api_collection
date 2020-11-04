import os
from dotenv import load_dotenv
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

load_dotenv()

Base = automap_base()

# engine, suppose it has two tables 'user' and 'address' set up
url = 'mysql+pymysql://{}:{}@{}:{}/{}'
user = os.getenv('mariadb_user')
password = os.getenv('mariadb_pwd')
host = os.getenv('mariadb_host')
port = os.getenv('mariadb_port')
database = os.getenv('mariadb_database')
url = url.format(user, password, host, port, database)
engine = create_engine(url)

# reflect the tables
Base.prepare(engine, reflect=True, schema='payment_test')

# mapped classes are now created with names by default
# matching that of the table name.
Users = Base.classes.rm_users
# ActivityLogs = Base.classes.activity_logs
# # CountryDistricts = Base.classes.country_districts
# CountryDivisions = Base.classes.country_divisions
# CountryThanas = Base.classes.country_thanas
# PMPS = Base.classes.pmps
# POPS = Base.classes.pops
# Wimaxs = Base.classes.wimaxs
# session = Session(engine)

# # rudimentary relationships are produced
# session.add(Address(email_address="foo@bar.com", user=User(name="foo")))
# session.commit()

# collection-based relationships are by default named
# "<classname>_collection"
# print(u1.address_collection)


# db = SQLAlchemy()
session = Session(engine)
