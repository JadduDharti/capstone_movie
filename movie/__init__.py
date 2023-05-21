from flask import Flask
from config import Config
from .site.routes import site
from .authentication.routes import auth
from .models import db as root_db,  login_manager, ma
from .api.routes import api
from movie.helpers import JSONEncoder

from flask_migrate import Migrate


#flask CRUS import - CROSS ORIGIN RESOURCE SHARING - future proofing
#our react app so it can make api call to this flask app

from flask_cors import CORS

app = Flask(__name__)


app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)


app.config.from_object(Config)

root_db.init_app(app)

migrate = Migrate(app, root_db)


login_manager.init_app(app)
login_manager.login_view = 'auth.signin' # Specify what page to load for NON-AUTHED users

app.json_encoder = JSONEncoder

ma.init_app(app)


CORS(app)