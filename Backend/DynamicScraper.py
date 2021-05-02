import requests
import json
import time
import threading
import mysql.connector
import sys

# Setting up the database connection
try:
    database = mysql.connector.connect(host="bikesdata.cnqobaauuxez.us-east-1.rds.amazonaws.com", user="admin",
                                       passwd="rootadmin", database="dbikes")

except mysql.connector.Error as error:
    print("Unable to connect to database: {}".format(error))
    sys.exit(1)

# connecting to get the bike data from the jcdecaux API
bikes_url = "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=b0979801c4ff351dc53e4bf7120f76de43e10959"
try:
    bike_request = requests.get(bikes_url)
    bike_response = bike_request.json()

except requests.exceptions.RequestException as e:
    print(e)
    sys.exit(1)

# weather
weather_url = "https://api.openweathermap.org/data/2.5/weather?id=7778677&appid=b0059847f8ec020060d3e56bd7678549"
try:
    weather_request = requests.get(weather_url)
    weather_response = weather_request.json()

except requests.exceptions.RequestException as e:
    print(e)
    sys.exit(1)

# create the table in my mysql
sql_cursor = database.cursor()

# sql_cursor.execute("CREATE TABLE Bike(number VARCHAR(255),contract_name VARCHAR(255), name VARCHAR(255), bike_stands VARCHAR(255), available_bike_stands VARCHAR(255),available_bikes VARCHAR(255), status VARCHAR(255), last_update VARCHAR(255))")
# sql_cursor.execute("CREATE TABLE Weather (coord_lon VARCHAR(255), coord_lat VARCHAR(255), weather_id VARCHAR(255), weather_main VARCHAR(255), weather_description VARCHAR(255),weather_icon VARCHAR(255), weather_base VARCHAR(255) ,main_temp VARCHAR(255),feels_like VARCHAR(255),"\
#                     "main_temp_min VARCHAR(255), main_temp_max VARCHAR(255), main_pressure VARCHAR(255), main_humidity VARCHAR(255), main_visibility VARCHAR(255)," \
#                     "wind_speed VARCHAR(255), wind_deg VARCHAR(255),  clouds_all VARCHAR(255), dt VARCHAR(255), sys_type VARCHAR(255), sys_id VARCHAR(255), sys_country VARCHAR(255),sys_sunrise VARCHAR(255), sys_sunset VARCHAR(255), city_id VARCHAR(255), city_name VARCHAR(255), cod VARCHAR(255))")

# Create the insert statement for the new data
bike_table = "INSERT INTO Bike(number, contract_name, name, bike_stands, available_bike_stands, " \
             "available_bikes, status, last_update) " \
             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

weather_table = "INSERT INTO Weather (coord_lon,coord_lat,weather_id,weather_main,weather_description, " \
                "weather_icon, weather_base , main_temp, feels_like , main_temp_min, main_temp_max, main_pressure, main_humidity, main_visibility, " \
                "wind_speed,clouds_all, dt, sys_type, sys_id, sys_country, " \
                "sys_sunrise, sys_sunset,city_id,city_name,cod) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)"

try:
    sql_cursor = database.cursor()

    # Iterate through the data response object and perform inserts
    for i in range(0, len(bike_response)):
        Bike_data = (bike_response[i]["number"], bike_response[i]["contract_name"], bike_response[i]["name"],
                     bike_response[i]["bike_stands"], bike_response[i]["available_bike_stands"],
                     bike_response[i]["available_bikes"], bike_response[i]["status"],
                     time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(bike_response[i]["last_update"] / 1000)))
        sql_cursor.execute(bike_table, Bike_data)

    Weather_data =(weather_response['coord']['lon'], weather_response['coord']['lat'], weather_response['weather'][0]['id'],
                   weather_response['weather'][0]['main'], weather_response['weather'][0]['description'],
                   weather_response['weather'][0]['icon'],
                   weather_response['base'], weather_response['main']['temp'], weather_response['main']['feels_like'],
                   weather_response['main']['temp_min'], weather_response['main']['temp_max'], weather_response['main']['pressure'],
                   weather_response['main']['humidity'], weather_response['visibility'], weather_response['wind']['speed'],
                   weather_response['clouds']['all'], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(weather_response['dt'])), weather_response['sys']['type'],
                   weather_response['sys']['id'], weather_response['sys']['country'], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(weather_response['sys']['sunrise'])),
                   time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(weather_response['sys']['sunset'])), weather_response['id'], weather_response['name'], weather_response['cod'])

    sql_cursor.execute(weather_table, Weather_data)

    database.commit()

    # Close the connection
    database.close()
except mysql.connector.Error as error:
    print("Connection to the database failed: {}".format(error))
    sys.exit(1)
