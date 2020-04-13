import sqlalchemy
from flask import Flask, g, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pickle
import datetime

import pandas as pd
import json
import pymysql
from pandas._libs import json

dbhost = 'bikesdata.cnqobaauuxez.us-east-1.rds.amazonaws.com'  # host name
dbuser = 'admin'  # mysql username
dbpass = 'rootadmin'  # mysql password
dbname = 'dbikes'  # database name
port = 3306
DB_URI = 'mysql+pymysql://' + dbuser + ':' + dbpass + '@' + dbhost + '/' + dbname

engine = sqlalchemy.create_engine(
    'mysql+pymysql://' + dbuser + ':' + dbpass + '@' + dbhost + ':' + DB_URI + '/' + dbname)  # connect to server

"""
 used pymsql, pymysql is pure python port of mysqldb (mysql-python) package. So, pymysql can be installed on any system without needing a C compiler.
# Installing mysqldb may need a compiler and in windows can produce error(error: Unable to find vcvarsall.bat) if you do not have one
# pymsql is a database connectors
"""

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

db = SQLAlchemy(app)


def connect_to_database():
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://' + dbuser + ':' + dbpass + '@' + dbhost + '/' + dbname)  # connect to server
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

    return jsonify(bikes_available=data)


@app.route("/occupancy/<int:station_id>")
def get_occupancy(station_id):
    engine = get_db()
    data = []
    rows = engine.execute("SELECT * From Bike where number={} order by last_update limit 1;".format(station_id))
    for row in rows:
        data.append(dict(row))
    print(data)
    return jsonify(bikes_available=data)


@app.route("/data/<int:station_id>")
def graph(station_id):
    engine = get_db()
    data = []
    rows = engine.execute("SELECT available_bikes, hour( last_update ) as hour FROM  Bike where number={}  group by hour( last_update ) asc;".format(station_id))
    #rows = engine.execute("SELECT available_bikes, dayname( last_update ) as day,hour( last_update ) as hour From Bike where number={} group by dayname( last_update ),hour( last_update );".format(station_id))
    for row in rows:
        data.append(dict(row))
    print(data)
    return jsonify(bikes_available=data)







# Load the trained ML pickel file
monday = pickle.load(open('monday_station.pkl', 'rb'))
tuesday = pickle.load(open("tuesday_station.pkl", "rb"))
wednesday = pickle.load(open("wednesday_station.pkl", "rb"))
thursday = pickle.load(open("thursday_station.pkl", "rb"))
friday = pickle.load(open("friday_station.pkl", "rb"))
saturday = pickle.load(open("saturday_station.pkl", "rb"))
sunday = pickle.load(open("sunday_station.pkl", "rb"))
import numpy as np


@app.route("/prediction", methods=['GET', 'POST'])
def prediction_model():
    import numpy as np

    # Store the request from JS
    data = request.args.get('post', 0, type=str)
    data = data.split()
    main_temp = float(data[0])
    main_pressure = int(data[1])
    main_humidity = int(data[2])
    wind_speed = float(data[3])
    date = (data[4])
    d = datetime.datetime.strptime(date, "%Y-%m-%d")
    date = d.strftime("%A")
    minute = (data[5])
    station = int(data[6])
    d = datetime.datetime.strptime(minute, "%H:%M")
    hours = int(d.hour)
    minute = int(d.minute)

    print("Data to be sent to the prediction model ", data)
    print(type(data))
    prediction_input = [[station, main_temp, main_pressure, main_humidity, wind_speed, hours, minute]]
    if date == "Monday":
        x = monday.predict(prediction_input)
    elif date == "Tuesday":
        x = tuesday.predict(prediction_input)
    elif date == "Wednesday":
        x = wednesday.predict(prediction_input)
    elif date == "Thurday":
        x = thursday.predict(prediction_input)
    elif date == "Friday":
        x = friday.predict(prediction_input)
    elif date == "Saturday":
        x = saturday.predict(prediction_input)
    elif date == "Sunday":
        x = sunday.predict(prediction_input)

    print("Predicted available bikes for selected station is", int(x[0]))

    # Fetch the ML model output and return as JSON to client
    prediction = [int(x[0])]
    return json.dumps(prediction);


# Run Server
if __name__ == "__main__":
    app.run(debug=True)
