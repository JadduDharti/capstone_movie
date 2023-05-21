import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

# give access to the project in ANY OS were find outselves in
#allow outside file/folder to be added to the project
#from the base directory
load_dotenv(os.path.join(basedir, '.env'))

class Config():
    """
    set configuration variable for the flask app.
    Using enviroment variable where availabe
    Otherwise create the config variable if not done
    already
    """
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
   
    SECRET_KEY = os.environ.get("SECRET_KEY") or "Nana nana boo noo yell neb=ver guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite://" + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFIACTIONS = False # turns of message from sqlalchemy regards update to our db
    