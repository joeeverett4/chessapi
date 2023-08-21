import urllib.parse
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

username = "joe.everett34@gmail.com"
password = "plantbasedpassword!"

encoded_username = urllib.parse.quote_plus(username)
encoded_password = urllib.parse.quote_plus(password)

uri = f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.2sqehkd.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
