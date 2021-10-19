"""
The flask application package.
"""

from flask import Flask
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'web_application\\uploads\\'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from web_application import routes
