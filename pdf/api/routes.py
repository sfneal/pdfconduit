import os
from uuid import uuid4

from flask import Flask, request, flash, redirect, send_from_directory, abort
from werkzeug.utils import secure_filename

from pdf.api.config import MAX_CONTENT_LENGTH, UPLOAD_FOLDER
from pdf.api.controllers import apply_watermark
from pdf.api.helpers import construct_url, allowed_file

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
def index():
    return 'pdfconduit api is running'


@app.route('/watermark', methods=['POST'])
def watermark():
    """Apply a watermark to a PDF file."""
    if not request.method == 'POST':
        abort(404)

    # Check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    return 'file'

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
