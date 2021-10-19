"""
Routes and views for the flask application. Work in progress.
"""

import logging
import os

from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from web_application import app
from web_application.analysis_utils import parse_csv, verify_file

"Configuring logging to make my life easier"
logging.basicConfig(filename='record.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s '
                           f': %(message)s')


@app.route('/')
@app.route('/upload', methods=('GET', 'POST'))
def upload():
    """Renders the home page."""
    # TODO: Make a proper home page and make it look pretty
    # TODO: Figure out how to display the CSV
    if request.method == 'GET':
        return render_template('upload.html')

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file found')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No file uploaded')
            return redirect(request.url)

        if file and verify_file(file.filename):
            filename = secure_filename(file.filename)
            new_filename = 'upload_' + filename

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

            with open(file=app.config['UPLOAD_FOLDER'] + new_filename,
                      mode='r+', encoding='utf-8') as upload_file:
                data_file = parse_csv(upload_file)

            return render_template('temp.html', columns=data_file)
    return render_template('upload.html')


@app.route('/temp', methods=('GET', 'POST'))
def temp():
    return render_template('temp.html')
