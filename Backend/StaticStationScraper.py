# scraper that scrapes static station data about dublin bikes

import requests
import json
import time
import threading
import mysql.connector
import  sys

# Setup the database connection
try:
    mydb = mysql.connector.connect(host="bikesdata.cnqobaauuxez.us-east-1.rds.amazonaws.com", user="admin",
                                   passwd="rootadmin", database= "dbikes")
except mysql.connector.Error as err:
    print("Unable to connect to database: {}".format(err))
    sys.exit(1)

# Get the data from the API
bikes_url="https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=b0979801c4ff351dc53e4bf7120f76de43e10959"


try:
    response_bikes = requests.get(bikes_url)
    data_bikes = response_bikes.json()

except requests.exceptions.RequestException as e:
    print(e)
    sys.exit(1)


sql_bikes = "INSERT INTO station (address, banking, bike_stands, " \
            "bonus, contract_name, name, number, status, position_lat, position_lng) " \
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"


try:
    mycursor = mydb.cursor()

# Iterate through the data response object and perform inserts
    for elem in range(0, len(data_bikes)):
        val = (data_bikes[elem]["address"], data_bikes[elem]["banking"], data_bikes[elem]["bike_stands"],
               data_bikes[elem]["bonus"], data_bikes[elem]["contract_name"], data_bikes[elem]["name"], data_bikes[elem]["number"], data_bikes[elem]["status"], data_bikes[elem]['position']['lat'], data_bikes[elem]['position']['lng'] )

        mycursor.execute(sql_bikes, val)



    mydb.commit()

    # Close the connection
    mydb.close()

except mysql.connector.Error as err:
    print("Unable to connect to database: {}".format(err))
    sys.exit(1)