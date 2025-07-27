from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["stocksage_db"]
collection = db["webpage_static_data"]




# Insert the document
collection.insert_one()

print("Document inserted successfully.")
