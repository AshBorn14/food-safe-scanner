import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'root@123'
)

cursorObject = dataBase.cursor()

cursorObject.execute('CREATE DATABASE foodsafe')

print("All Done")