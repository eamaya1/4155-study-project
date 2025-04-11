from bson import json_util
from bson.objectid import ObjectId
from flask import Blueprint, current_app, jsonify
from ..models.schema import flashcardsSchema
from marshmallow import ValidationError
import pymongo

def create_flashcard_set(json):
    db = current_app.config['DB']
    collection = db['flashcards']

    flashcard_schema = flashcardsSchema()
    validated_flashcards = flashcard_schema.load(json)

    return validated_flashcards


def save_set_to_flashcard_collection(flashcards):
    db = current_app.config['DB']
    collection = db['flashcards']
    try:
        set_id = collection.insert_one(flashcards).inserted_id
        set_id = str(set_id)

        return set_id
    except Exception as e:
        print(e)
        return None


# TODO: Make sure to add better error handling for the above 2 methods as well.
def save_set_for_user(user, setID, setName):
    db = current_app.config['DB']
    collection = db['users']
    try:
        result = collection.update_one({"_id": ObjectId(user['_id'])}, 
                                       {"$set": {f"flashcards.{setID}": setName}})
        
        return result.modified_count > 0
    
    except Exception as e:
        print(e)
        return None
        

def save_flashcard(set_id, flashcard):
    db = current_app.config['DB']
    collection = db['users']
    try:
        result = collection.update_one({"_id": ObjectId(set_id)}, {"$push": {"flashcards": flashcard}})
        return result.modified_count > 0
    except Exception as e:
        print(e)
        return None

def get_set(set_id):
    db = current_app.config['DB']
    collection = db['flashcards']
    try:
        study_set = collection.find_one({"_id": ObjectId(set_id)})
        study_set['_id'] = str(study_set['_id'])

        return study_set
    except Exception as e:
        print(e)
        return None

def get_all_sets():
    try:
        cursor = collection.find()
        return list(cursor)
    except Exception as e:
        print(e)
        return None

def get_flashcards(set_id):
    try:
        study_set = collection.find_one({"_id", ObjectId(set_id)}, {"flashcards", 1})
        if study_set and 'flashcards' in study_set:
            return study_set['flashcards'] 
        else:
            return []
    except Exception as e:
        print(e)
        return None

def update_set(set_id, json):
    try:
        new_set = json_util.loads(json)
        result = collection.replace_one({"_id": ObjectId(set_id)}, new_set)
        return result.modified_count > 0
    except Exception as e:
        print(e)
        return False

def update_flashcard(set_id, flashcard_index, new_card):
    try:
        result = collection.update_one({"_id": ObjectId(set_id)}, {"$set": {f"flashcards.{flashcard_index}": new_card}})
        return result.modified_count > 0
    except Exception as e:
        print(e)
        return False

def delete_set_from_flashcard_collection(set_id):
    db = current_app.config['DB']
    collection = db['flashcards']
    
    try:
        result = collection.delete_one({"_id": ObjectId(set_id)})
        return result.deleted_count > 0
    except Exception as e:
        print(e)
        return False

# Technically an update function on a study set. $unset aggregation
def delete_flashcard_for_user(user_id, set_id):
    db = current_app.config['DB']
    collection = db['users']

    try:
        result = collection.update_one({"_id": ObjectId(user_id)}, {"$unset": {f"flashcards.{set_id}": 1}})
        return result.modified_count > 0
    except Exception as e:
        print(e)
        return False