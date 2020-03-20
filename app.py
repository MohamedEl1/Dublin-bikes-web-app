import sqlalchemy
from flask import Flask, g, jsonify
from flask_sqlalchemy import SQLAlchemy
import pymysql

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
@app.route("/station")
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