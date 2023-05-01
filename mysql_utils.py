import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="test_root",
    database="academicworld"
)

cursor = db.cursor()

