import mysql.connector
from mysql.connector import Error

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="test_root",
    database="academicworld"
)

cursor = db.cursor()

# faculty = { 1, 'Syed Hassan', 'SE', 'ASD'...}
def add_faculty(faculty):
    field_names = [
        "name", "position", "researchInterest", "email", "phone",
        "photoUrl", "keywords", "publications", "`affiliation.id`",
        "`affiliation.name`", "`affiliation.photoUrl`"
    ]

    query_fields = []
    query_values = []
    query_placeholders = []

    for field, value in zip(field_names, faculty):
        if value is not None:
            query_fields.append(field)
            query_values.append(value)
            query_placeholders.append("%s")

    if not query_fields:
        print("No values provided to add faculty member.")
        return

    query = f"""
    INSERT INTO faculty_all_attributes ({', '.join(query_fields)})
    VALUES ({', '.join(query_placeholders)})
    """

    try:
        cursor.execute(query, tuple(query_values))
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