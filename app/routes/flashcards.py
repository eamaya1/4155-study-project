from io import StringIO
from flask import Blueprint, current_app, jsonify, request, render_template, session
from bson.objectid import ObjectId
import pymongo
import pymongo.errors
from ..models.schema import flashcardsSchema
from ..models.user import get_user_by_id
from ..models.flashcards import create_flashcard_set, save_set_to_flashcard_collection, save_set_for_user, get_set, delete_set_from_flashcard_collection, delete_flashcard_for_user
from app.utils.conversions import FileConvert


flashcard_bp = Blueprint("flashcards", __name__)

# GET /user/<user_id>/flashcards 
# Returns the users flashcards as a dictionary with keys = setID and values = setNames
@flashcard_bp.route('/flashcards', methods=["GET"])
def get_all_users_flashcards(user_id):

    # Verify that the user is logged in,
    # Get the user
    try:
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User is none"}, 404)
        
    except pymongo.errors.PyMongoError:
        return jsonify({"error": "No user exists with that ID or Database error"}, 404)
    
    if "flashcards" not in user.keys():
        return {"No flashcards to show": "0"}, 200

    # Get the user's flashcards: This is a dictionary of key: setID, value: setName
    flashcards = user['flashcards']

    print(flashcards.keys())
    print(flashcards.values())
    
    return jsonify(flashcards), 200

# GET /users/<user_id>/flashcards/<setID>
# Returns a users specific flashcard set as requested with the setID in dictionary form
@flashcard_bp.route('/flashcards/<set_id>', methods=["GET"])
def get_specific_user_flashcards(user_id, set_id):
    try:
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User is none"}, 404)
        
    except pymongo.errors.PyMongoError:
        return jsonify({"error": "No user exists with that ID or Database error"}, 404)
    
    if "flashcards" not in user.keys():
        return {"No flashcards to show": "0"}, 200

    # Get the user's flashcards: This is a dictionary of key: setID, value: setName
    flashcards = user['flashcards']

    # If the set ID isn't located in the user's flashcards, show an error
    if set_id not in flashcards.keys():
        return jsonify({"Error": "You are not authorized to view this set or set doesn't exist"}, 404)
    
    # Use the get_set method to locate the set in the flashcard collection in MongoDB, if not found returns None and thus an error
    try:
        requested_cards = get_set(set_id)
        
        if not requested_cards:
            return jsonify({"Error": "Flashcards not found"}, 404)
    except:
        return {"Error": "Exception found "}, 404
    
    # Returns the specific flashcard set in dictionary form
    return jsonify(requested_cards), 200

# POST /users/<user_id>/flashcards
# Creates a new set for the user based on the JSON request body and saves it to the users flashcard collection
@flashcard_bp.route('/flashcards', methods=["POST"])
def create_and_save_flashcards_for_user_route(user_id):
    # Verify that the user is logged in, once thats possible

    # Get the user
    try:
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User is none"}, 404)
        
    except pymongo.errors.PyMongoError:
        return jsonify({"error": "No user exists with that ID or Database error"}, 404)
    
    # Create the set for the user
    flashcards = create_flashcard_set(request.json)
    setName = flashcards['setName']

    # Returns set id to save into users study set 
    set_id = save_set_to_flashcard_collection(flashcards)

    # Save the set for the user
    isSaved = save_set_for_user(user, set_id, setName)

    if not isSaved:
        return jsonify({"Error": "Error: Couldn't save flashcards for user"}, 400)

    return {"Message": "Successfully saved flashcards for user"}, 200


# DELETE /users/<user_id>/flashcards/<set_id>
# Deletes a flashcard set from the flashcards collection in the database and the user's reference to that
# set from their flashcards field 
@flashcard_bp.route('/flashcards/<set_id>', methods=['DELETE'])
def delete_user_flashcard(user_id, set_id):
    try:
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User is none"}, 404)
        
    except pymongo.errors.PyMongoError:
        return jsonify({"error": "No user exists with that ID or Database error"}, 404)
    
    deleted_from_collection = delete_set_from_flashcard_collection(set_id)
    if not deleted_from_collection:
        return jsonify({"error": "Flashcards couldn't be deleted from flashcards collection or don't exist"}, 404)
    
    deleted_for_user = delete_flashcard_for_user(user_id, set_id)
    if not deleted_for_user:
        return jsonify({"error": "Flashcards couldn't be deleted from user's flashcards field or don't exist"}, 404)

    return jsonify({"Message": "Successfully deleted flashcards from flashcard collection and user field"}), 200



@flashcard_bp.route('/flashcards/upload', methods=['GET', 'POST'])
def upload_flashcards():
    """ Route for user to upload their file to be converted into a study set.
    
    GET: renders the upload page.
    POST: converts a given file to flashcards and inserts a set to the users database.

    The template form should send:
    setName: name of the set
    setDescription: description of the set
    file: the file to be converted into flashcards

    see templates/test/test_upload.html for an example

    currently accepted file types: md
    """

    # A get request to the same url should render the page to upload the set
    if request.method == "GET":
        return render_template('test/test_upload.html')

    #TODO: set up sessions so that the set can be saved for a user

    flashcards = []

    file = request.files['file']
    if file == '':
        return jsonify({"error": "No file Selected"}), 400
    
    # Setting mimetype this way because file.mimetype does not like md files
    filename = file.filename
    if filename.endswith('.md'):
        mimetype = 'text/markdown'
    else:
        return jsonify({"error": "Unsupported file type, expected .md file!"}), 415
    
    read_file = file.read().decode('UTF-8') # Decode to a string
    file_like_object = StringIO(read_file)

    try:
        flashcards = FileConvert.handle_file(file_like_object, mimetype)
    except ValueError as ve:
        print(ve)
        return jsonify({"error": "Unsupported file type"}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": f"Server error while handling file, {str(e)}"}), 500
        
    # Construct the set to be uploaded
    set_name = request.form['setName']
    set_description = request.form['setDescription']
    flash_set = {
        "setName": set_name,
        "setDescription": set_description,
        "terms": flashcards,
    }

    # Only saving to test db while user auth is not included
    if current_app.config['TESTING']:
        set_id = save_set_to_flashcard_collection(flash_set)
        if set_id is None:
            return jsonify({"error": "Error saving the flashcard set to db"}), 500
        return jsonify({"id": set_id}), 201

    #TODO: Once user auth is figured for session, set up set save funcionality 
    # isSaved = save_set_for_user(user, set_id, set_name)

    # if not isSaved:
    #     return jsonify({"Error": "Error: Couldn't save flashcards for user"}, 400)

    # return {"Message": "Successfully saved flashcards for user"}, 200
    
    # Change to code 201 when the set actually gets pushed to db
    return jsonify(flash_set), 200
    
