"""
The flask application package.
"""

from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(SECRET_KEY='dev')
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024

UPLOAD_FOLDER = 'web_application/uploads/'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


from web_application import routes
