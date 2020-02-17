import requests
import json
import time
import threading
import mysql.connector


db_connection = mysql.connector.connect(host="bikesdata.cnqobaauuxez.us-east-1.rds.amazonaws.com", user="admin",
                                   passwd="rootadmin", database= "biketest")


db_cursor = db_connection.cursor()



#Here creating database table as student'
db_cursor.execute("CREATE TABLE datatest3 (id INT, name VARCHAR(255))")
#Get database table'
db_cursor.execute("SHOW TABLES")
for table in db_cursor:
	print(table)
