from flask import Flask, request  # importing Flask and request module                      # importing datetime module
from dotenv import load_dotenv     # importing load_dotenv to load environment variables
import os                                           # importing os module to access environment variables
import pymongo                                      # importing pymongo to interact with MongoDB

load_dotenv()                                       # Load environment variables from .env file

mongo_url = os.getenv("mongo_url")                  # Get the MongoDB URL from environment variables
client = pymongo.MongoClient(mongo_url)             # Create a MongoDB client
db = client.test                                    # Access the test_database
collection = db['users']                            # Access the users collection

app = Flask(__name__)                               # creating a Flask app instance

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if password != confirm_password:
        return {"status": "error", "message": "Passwords do not match"}, 400

    collection.insert_one({
        "name": name,
        "email": email,
        "password": password
    })

    return {
        "DATA SUBMITTED SUCCESSFULLY!": "SUCCESS",
        "status": "success",
        "message": f"Signup successful for {name}"
    }, 201


@app.route('/view')
def view():
    users = list(collection.find())

    clean_users = []  # List to hold cleaned user data

    for user in users:
        user_dict = dict(user)        # Convert BSON to Python dict
        user_dict.pop("_id", None)    # Remove MongoDB _id field
        clean_users.append(user_dict) # Append cleaned user dict to list

    return {"users in DB are": clean_users}

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=9000)