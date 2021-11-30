"""
Routes and views for the flask application. Work in progress.
"""

import logging
import os
import git

import numpy
import pandas
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename

from web_application import app
from web_application.analysis_utils import parse_csv, verify_file, get_numpy_array
from web_application.errors import ColumnTypeOperationMismatch
from web_application.statistic_controller import operations, init_array

"Configuring logging to make my life easier"
logging.basicConfig(filename='record.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s '
                           f': %(message)s')

g = {}


@app.route('/', methods=('GET', 'POST'))
def webhook():
    if request.method == 'POST':
        repo = git.Repo('https://github.com/FigoFeras1/HonorsProject')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return redirect(url_for('upload'))


@app.route('/upload', methods=('GET', 'POST'))
def upload():
    """Renders the home page."""
    # TODO: Make a proper home page and make it look pretty
    # TODO: Figure out how to display the CSV
    global g

    if request.method == 'GET':
        logging.debug("GET")
        return render_template('upload.html')

    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No File Found.")
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            logging.info("No file uploaded")
            flash('No File Uploaded.')
            return redirect(request.url)

        if file and verify_file(file.filename):
            filename = secure_filename(file.filename)
            new_filename = 'upload_' + filename

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

            with open(file=app.config['UPLOAD_FOLDER'] + new_filename,
                      mode='r+', encoding='utf-8') as upload_file:
                data_file = parse_csv(upload_file)
                logging.debug(data_file)
                json_dataframe = data_file.to_json()
            # session['data_file'] = json_dataframe
            g['data_file'] = json_dataframe
            return redirect(url_for('index'))
        else:
            flash("File is not a CSV.")
    return render_template('upload.html')


@app.route('/index', methods=('GET', 'POST'))
def index():
    error = False
    # dataframe = pandas.read_json(session['data_file'])
    dataframe = pandas.read_json(g['data_file'])
    column_names = dataframe.columns
    logging.debug(column_names)
    if request.method == 'GET':
        return render_template('index.html', operations=operations,
                               column_names=column_names,
                               file_html=dataframe.to_html(justify='justify-all',
                                                           classes='table table-striped',
                                                           index=False))
    if request.method == 'POST':
        operation = request.form.get('operation_menu')
        column_name = request.form.get('column_menu')
        init_array(get_numpy_array(dataframe))

        result = operations[operation](column_name)
        if isinstance(result, ColumnTypeOperationMismatch):
            result.get_message(column_name=column_name, operation_name=operation)
            error = True

        if isinstance(result, pandas.DataFrame):
            dataframe = result
            result = ''

        return render_template('index.html', operations=operations, error=error,
                               chosen_operation=operation, chosen_column=column_name,
                               column_names=column_names, result=result,
                               file_html=dataframe.to_html(justify='justify-all',
                                                           classes='table table-striped',
                                                           index=False))
