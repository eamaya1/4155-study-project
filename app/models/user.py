from bson import json_util
from bson.objectid import ObjectId
from flask import Blueprint, current_app, jsonify, request, session
from ..models.schema import UserSchema
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash


def get_id_from_username(username):
    db = current_app.config['DB']
    collection = db['users']

    try:
        result = db.collection.find_one({"username": username})
        if result is not None:
            return result['_id']
        else:
            return None
    except Exception as e:
        print(e)
        return None

# Function connects to database and tries to get all users in the users collection. Returns an array of dictionaries of users.
# feeds into routes/users.py and is used by get_users_route()
def get_users():
    db = current_app.config['DB']
    collection = db['users']

    try:
        # cursor = collection.find()
        users = list(collection.find({}, {'_id': 0}))
        return users

    except Exception as e:
        print(e)
        return None

# Function connects to the database and tries to find a user matching the user_id provided in route. Return either a user or none
# feeds into routes/users.py where it is used by get_user_by_id_route
def get_user_by_id(user_id):
    db = current_app.config['DB']
    collection = db['users']
    try:
        user = collection.find_one({"_id": ObjectId(user_id)})
        user['_id'] = str(user['_id'])
        if not user:
            return None
        
        return user
    except Exception as e:
        print(e)
        return None

def update_user(user_id, json):
    db = current_app.config['DB']
    collection = db['users']
    try:
        new_user = json_util.loads(json)
        user = collection.replace_one({"_id": ObjectId(user_id)}, new_user)
        if user is None:
            raise
        else:
            return user.modified_count > 0
    except Exception as e:
        print(e)
        return False

# Function attempts to grab and delete the user by their user_id. This will return true if deleted or false otherwise
# feeds into routes/users.py where it is used in delete_user_by_id_route() 
def delete_user_by_id(user_id):
    db = current_app.config['DB']
    collection = db['users']
     
    try:
        deleted_user = collection.delete_one({"_id": ObjectId(user_id)})
        if deleted_user.deleted_count == 0:
            return False
         
        return True
    except Exception as e:
        print(e)
        return False

# Function creates an object of UserSchema, which is a validator that makes sure all that is going into the database is correct per the schema
# made in models/schema returns that as a Python Dictionary. Used in /routes/users.py to /users POST request
def create_user(user_data):
    user_schema = UserSchema()
    validated_user = user_schema.load(user_data)
    
    validated_user['password'] = generate_password_hash(validated_user['password'])

    return validated_user

# Function saves an already validated user into the database. 
# Used in /routes/users.py by /users POST to save a validated user into the db. Returns None if unsuccessful.
def save_user(validated_user):
    db = current_app.config['DB']
    collection = db['users']
    try:
        user_id = collection.insert_one(validated_user)
        return user_id
    except Exception as e:
        print(e)
        return None
    

def login_and_validate_user(request):
    db = current_app.config['DB']
    collection = db['users']

    # The data should be the email and password in JSON
    data = request.json

    user = collection.find_one({"email": data.get("email")})

    if user and check_password_hash(user['password'], data.get("password")):
        session['user_id'] = str(user['_id'])
        session['email'] = user['email']

        return True
    else:
        return False
