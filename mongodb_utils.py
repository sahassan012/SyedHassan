from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["academicworld"]

faculty_collection = db["faculty"]
publications_collection = db["publications"]

faculty_columns = {"name":1, "position":1, "researchInterest":1, "email":1, "phone":1, "photoUrl":1, "affiliation.name":1, "_id":0}

def get_professor_by_name(name):
    name = {"name" : "{}".format(name)}
    result = faculty_collection.find(name, faculty_columns)
    return list(result) if result else {}

def get_all_professors():
    return list(faculty_collection.find({}))

def get_top_3_most_cited_publications_overall():
    return list(publications_collection.aggregate([ {'$sort': { 'numCitations' : -1 }}, {'$limit': 3}]))

def get_num_cited_publications_by_year():
    result = publications_collection.aggregate([
        {
            '$group': {
            '_id': "$year",
            'totalCitations': { '$sum': "$numCitations" }
            }
        },
        { '$sort': { '_id': 1 } }
        ])
    return list(result)