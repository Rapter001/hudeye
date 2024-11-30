import os
import smtplib
import requests
from flask import jsonify
from email.mime.text import MIMEText
from werkzeug.utils import secure_filename
from email.mime.multipart import MIMEMultipart
from werkzeug.exceptions import RequestEntityTooLarge
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'svg', 'gif', 'mp4', 'webp', 'ogg', 'webm', 'bmp'}
app.secret_key = "#U*P5g@x1SwvqP"

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    """
    Check if the file extension is allowed.
    :param filename: Name of the file to check.
    :return: True if the file extension is allowed, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.errorhandler(RequestEntityTooLarge)
def handle_file_size_error(error):
    """
    Handle the error when the uploaded file is too large.
    :param error: The error object.
    :return: Redirect to the upload page with an error message.
    """
    flash('File is too large. Maximum size allowed is 10 MB.', 'error')
    return redirect(url_for('upload'))

@app.route('/')
def home():
    """
    Render the home page and list uploaded files.
    :return: The home.html template with the list of files.
    """
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('home.html', files=files)

@app.route('/get_files')
def get_files():
    try:
        files = []
        for filename in os.listdir("uploads"):
            file_path = os.path.join("uploads", filename)
            # Ensure that only files (not directories) are included
            if os.path.isfile(file_path):
                files.append(filename)  # Add the file name to the list
        return jsonify({'files': files})
    except Exception as e:
        # Handle any errors (e.g., folder doesn't exist)
        return jsonify({'error': str(e)}), 500


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    Handle file upload.
    If the request method is POST, save the uploaded file if it is allowed.
    :return: The upload.html template.
    """
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                try:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash('File uploaded successfully!', 'success')
                except Exception as e:
                    flash('Error uploading file. Please try again.', 'error')
            else:
                flash('File type not allowed. Please upload a file of allowed type.', 'error')
        else:
            flash('No file selected. Please choose a file to upload.', 'error')
    return render_template('upload.html')

@app.route('/view')
def view_files():
    """
    View the list of uploaded files.
    :return: The view.html template with the list of files.
    """
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('view.html', files=files, upload_folder='uploads')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Serve an uploaded file.
    :param filename: Name of the file to serve.
    :return: The file from the upload directory.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/view/<filename>')
def view_file(filename):
    """
    Serve a file for viewing.
    :param filename: Name of the file to view.
    :return: The file from the upload directory.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/sent')
def sent():
    """
    Render the sent confirmation page.
    :return: The sent.html template.
    """
    return render_template('sent.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=False, threaded=True)