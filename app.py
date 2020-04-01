import sqlalchemy
from flask import Flask, g, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pandas as pd
import json
import pymysql
from pandas._libs import json

dbhost = 'bikesdata.cnqobaauuxez.us-east-1.rds.amazonaws.com' #host name
dbuser = 'admin' #mysql username
dbpass = 'rootadmin' #mysql password
dbname = 'dbikes' #database name
port=3306
DB_URI = 'mysql+pymysql://' + dbuser + ':' + dbpass + '@' + dbhost + '/' + dbname

engine = sqlalchemy.create_engine('mysql+pymysql://'+dbuser+':'+dbpass+'@'+dbhost+ ':' + DB_URI + '/'+dbname ) # connect to server

"""
 used pymsql, pymysql is pure python port of mysqldb (mysql-python) package. So, pymysql can be installed on any system without needing a C compiler.
# Installing mysqldb may need a compiler and in windows can produce error(error: Unable to find vcvarsall.bat) if you do not have one
# pymsql is a database connectors
"""

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI']=DB_URI

db = SQLAlchemy(app)

def connect_to_database():
    engine = sqlalchemy.create_engine('mysql+pymysql://' + dbuser + ':' + dbpass + '@' + dbhost + '/' +dbname)  # connect to server
    return engine

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()


# below retrieves all information the table station in the database and displays it as a json format
@app.route("/stations")
# @functools.lru_cache(maxsize=128)
def get_stations():
    engine = get_db()
    station = []
    rows = engine.execute("SELECT * from station;")
    for row in rows:
        station.append(dict(row))

    return jsonify(station=station)

# below retrieves all information about the table bikes_available in the database and displays it as a json format

@app.route("/bikes_available")
def get_bikes_available():
    engine = get_db()
    data = []
    rows = engine.execute("SELECT * From bikes_available")
    for row in rows:
        data.append(dict(row))

    return jsonify(bikes_available = data)

@app.route("/occupancy/<int:station_id>")
def get_occupancy(station_id):
    engine = get_db()
    df = pd.read_sql_query("select * from bikes_available where number=%(number)s", engine, params={"number":station_id})
    df['last_update'] = pd.to_datetime(df.last_update)
    df.set_index('last_update', inplace=True)
    res = df['available_bike_stands'].resample('1d').mean()

    print(res)
    return jsonify(data=json.dumps(list(zip(map(lambda x: x.isoformat(), res.index), res.values))))
# below creates a table in the database to test the connection

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     username = db.Column(db.String(80), unique = True)
#     email = db.Column(db.String(80), unique=True)
#
#     def __init__(self, username, email):
#         self.username = username
#         self.email = email
#
#
# db.create_all()



# Run Server
if __name__ == "__main__":
    app.run(debug=True)