import mysql.connector
from mysql.connector import Error

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="test_root",
    database="academicworld"
)

cursor = db.cursor()

def add_faculty(faculty):
    query = """
    INSERT INTO faculty_all_attributes
    (id, name, position, researchInterest, email, phone, photoUrl, keywords, publications, `affiliation.id`, `affiliation.name`, `affiliation.photoUrl`)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, faculty)
        db.commit()
        print(f"Faculty member added successfully.")
    except Error as e:
        print(f"There was an error adding faculty member: {e}")

def remove_faculty(name):
    query = "DELETE FROM faculty_all_attributes WHERE name = %s"

    try:
        cursor.execute(query, (name,))
        db.commit()
        print(f"Faculty member deleted successfully.")
    except Error as e:
        print(f"There was an error deleting faculty member: {e}")