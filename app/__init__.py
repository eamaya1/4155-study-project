from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from .routes import main_bp
from .routes.users import user_bp
from .routes.flashcards import flashcard_bp


# Add URI=mongodb+srv://<username>:<password>@fsb-cluster.7u2uh.mongodb.net/?retryWrites=true&w=majority&appName=fsb-cluster
# to the .env file
# update <username> and <password> with your credentials from mongo

def create_app(config_name="default"):
    load_dotenv()
    app = Flask(__name__, static_folder='static', template_folder='templates')

    uri = os.getenv('URI')
    if not uri:
        raise ValueError("MongoDB URI wasn't found in environment variables")
    
    mongo_client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        mongo_client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    # Choose DB based on config
    db_name = 'study-guide-test' if config_name == 'testing' else 'study-guide'

    # Flask app config variables
    app.config['MONGO_CLIENT'] = mongo_client
    app.config['DB'] = mongo_client[db_name]
    # app.config['EXPLAIN_TEMPLATE_LOADING'] = True

    # set TESTING based on the config_name
    if config_name == 'testing':
        app.config['TESTING'] = True
    else:
        app.config['TESTING'] = False

    # Session secret key
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(flashcard_bp)

    return app