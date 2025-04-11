from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    firstName = fields.String(required=True, validate=validate.Length(2, 15), allow_none=False)
    lastName = fields.String(required=True, validate=validate.Length(2, 15), allow_none=False)
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8), allow_none=False)
    flashcards = fields.Dict(required=False, keys=fields.Str() , values=fields.Str(), load_default={}) # Key: Set ID, Value: Set Name

# This gets nested in flashcardsSchema. 
class CardSchema(Schema):
    front = fields.String(required=True, allow_none=False)
    back = fields.String(required=True, allow_none=False)

class flashcardsSchema(Schema):
    setName = fields.String(required=True, validate=validate.Length(1, 20), allow_none=False)
    timeStamp = fields.Time(required=False)
    setDescription = fields.String(required=True, validate=validate.Length(min=10), allow_none=False)

    # Updated the actual flashcards to be a nested list within the set schema
    # I feel this allows some more options for dealing with the flashcards later on
    # - Isaac
    terms = fields.List(fields.Nested(CardSchema))



