"""
The flask application package.
"""

from flask import Flask, request
import git
from werkzeug.utils import secure_filename

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(SECRET_KEY='dev')
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024

UPLOAD_FOLDER = 'web_application/uploads/'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app = Flask(__name__)


@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('https://github.com/FigoFeras1/HonorsProject')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

from web_application import routes
