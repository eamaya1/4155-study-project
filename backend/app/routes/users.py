from flask import Blueprint, current_app, jsonify, request
from bson.objectid import ObjectId
import pymongo
import pymongo.errors
from .flashcards import flashcard_bp
from ..models.user import get_user_by_id, delete_user_by_id, get_users, create_user, save_user
from ..models.schema import UserSchema
from marshmallow import ValidationError


user_bp = Blueprint('users', __name__, url_prefix='/users')
user_bp.register_blueprint(flashcard_bp, url_prefix='/<user_id>')

# You can test this out by doing curl http://127.0.0.1:5000/users, might not be the path we used in the end but it works for now
# GET /users
# Returns all users in the database
@user_bp.route('/', methods=['GET'])
def get_users_route():  
    # db = current_app.config['DB']
    # users_collection = db['users']

    try:
        #users = list(users_collection.find({}, {'_id': 0}))
        users = get_users()
        if not users:
            return ({"error": "Error: Collection found to have no users"}, 404)
        
    except pymongo.error.PyMongoError:
        return jsonify({"error": "Error: Unable to retrieve all users from database"}, 404)
    
    return jsonify(users), 200

# POST /users
# Creates a new user
# Returns a success message if a new user was created

@user_bp.route("/", methods=['POST'])
def create_user_route():
    try:
        validated_user = create_user(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}, 404)
    
    try:
        saved_user_id = save_user(validated_user)
        if not saved_user_id:
            return jsonify({"error": "Error: Saving was unsuccessful"}, 400)
    except:
        return jsonify({"error": "Error: Unable to save user"}, 404)

    return jsonify({"Message":"Successfully created and saved user"}), 200

# GET /users/<user_id>
# Returns a user based on their user_id in the form of a dictionary
@user_bp.route('/<user_id>')
def get_user_by_id_route(user_id):
    #db = current_app.config['DB']
    #users_collection = db['users']

    try:
        #user = users_collection.find_one({"_id": ObjectId(user_id) })
        user = get_user_by_id(user_id)

        if not user:
            return jsonify({"error": "User is none"}, 404)
    except pymongo.errors.PyMongoError:
        return jsonify({"error": "No user exists with that ID or Database error"}, 404)

    #user['_id'] = str(user['_id'])
    # if not user:
    #     return jsonify({"error": "User was not properly populated and is null"}, 404)
    
    return jsonify(user), 200


# DELETE /users/<user_id>
# This would need to be modified to include some sort of credential tracking first, can't have any old user deleting people after all...
@user_bp.route('/<user_id>', methods=["DELETE"])
def del_user_by_id_route(user_id):
    # db = current_app.config['DB']
    # users_collection = db['users']
    
    try:
        is_deleted = delete_user_by_id(user_id)
        # deleted = users_collection.delete_one({"_id": ObjectId(user_id)})
        if not is_deleted:
            return jsonify({"error": "Error: User not found"}, 404)
        
    except pymongo.errors.PyMongoError:
        return jsonify({"error": "Database connection error"}, 400)

    return {"Message": "Successful deletion"}, 200



# PUT /users/<user_id>
# Could be used for updating passwords, not sure yet..
# @user_bp.route('/<user_id>', methods=["PUT"])
# def update_user_by_id(user_id, updated_value):
