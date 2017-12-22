from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES


# Initializing the app
app = Flask(__name__)
# Configuring the app
app.config.from_object('settings')
# Initialzing flask-sqlalchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Initializing flask-login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Configuring photo uploading using flask-uploads
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# Importing flask modules containing all routes 
from user import views
from timeline import views
