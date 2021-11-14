"""
The flask application package.
"""

from flask import Flask
from werkzeug.utils import secure_filename

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(SECRET_KEY='dev')

UPLOAD_FOLDER = 'web_application\\uploads\\'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from web_application import routes
