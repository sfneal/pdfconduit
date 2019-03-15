import os
from uuid import uuid4

from flask import Flask, request, flash, redirect, send_from_directory, abort
from werkzeug.utils import secure_filename
from dirutility import DirPaths

from pdf.api.config import MAX_CONTENT_LENGTH, UPLOAD_FOLDER
from pdf.api.controllers import apply_watermark
from pdf.api.helpers import construct_url, allowed_file

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
def index():
    return 'pdfconduit api is running'


@app.route('/watermark', methods=['GET'])
def watermark():
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''


@app.route('/watermark/process', methods=['POST'])
def watermark_process():
    """Apply a watermark to a PDF file."""
    # Redirect to watermark page that contains form
    if not request.method == 'POST':
        redirect('/watermark')

    # Check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    # If user does not select file, browser also submit an empty part without filename
    if request.files['file'].filename == '':
        flash('No selected file')
        return redirect(request.url)

    # Check if the file is an allowed file type
    if not allowed_file(request.files['file'].filename.filename):
        flash('Invalid file type.  Only .pdf files are permitted')
        return redirect(request.url)

    # Retrieve PDF file and parameters
    file = request.files['file']
    params = {
        'address': request.form['address'],
        'town': request.form['town'],
        'state': request.form['state'],
    }

    # File has been added and validated
    if file:
        # Save file to uploads folder
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Make uploads directory if it does not exist
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.mkdir(app.config['UPLOAD_FOLDER'])

        file.save(file_path)

        # Create new watermarked file and return file path
        watermarked = apply_watermark(file_path, params)
        return send_from_directory(app.config['UPLOAD_FOLDER'], os.path.basename(watermarked))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/uploads', methods=['GET'])
def all_uploads():
    uploads = DirPaths(UPLOAD_FOLDER, full_paths=True).walk()
    if len(uploads) > 0:
        response = '<h2>Files on mounted drive</h2>'
        response += '<ul>'
        for upload in uploads:
            response += '''
            <li>
                <a href="/uploads/{0}">{1}</a>
            </li>
            '''.format(os.path.basename(upload), upload)
        response += '</ul>'
        return response
    else:
        return 'No files exist in directory {0}'.format(UPLOAD_FOLDER)
