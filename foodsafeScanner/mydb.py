import mysql.connector

dataBase = mysql.connector.connect(
    host = 'mysql.railway.internal',
    user = 'root',
    passwd = 'jaresFSVjmPQKwetnFswZCeTQUEkWIKn'
)

cursorObject = dataBase.cursor()

cursorObject.execute('CREATE DATABASE foodsafe')

print("All Done")