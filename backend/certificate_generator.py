# Required imports
from flask import Flask, request, send_from_directory, render_template, redirect, url_for, flash, session
import os

# Required for local execution
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
# end of local requirement

from backend.file_processor import process_file

# Create Flask app
app = Flask(__name__)

# Set secret key for session management, uses variable from environment in railway
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# Define upload and processed file directories
UPLOAD_FOLDER = 'uploads'
PROCESSED_MD_FOLDER = 'MD_files'

# Define full filepaths based on OS working directory - more robust code
FULL_UPLOAD_PATH = os.path.join(os.getcwd(), UPLOAD_FOLDER)
FULL_MD_PATH = os.path.join(os.getcwd(), PROCESSED_MD_FOLDER)

# Create directories if they don't exist
os.makedirs(FULL_UPLOAD_PATH, exist_ok=True)
os.makedirs(FULL_MD_PATH, exist_ok=True)


# Define route for the home page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Define route for file upload
@app.route('/', methods=['POST'])
def upload_file():
    # Check if file is present in the request
    if 'uploadedFile' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['uploadedFile']

    # Check if a file is selected
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    # Check if the file has a valid extension
    if not file or not file.filename.endswith('.tar.gz'):
        flash('Invalid file type')
        return redirect(request.url)

    # Iterates on MD_files and uploads, and removes every file they contain
    # This clears the relevant processing-folders each time a new file is uploaded
    for filename in os.listdir(FULL_UPLOAD_PATH):
        if os.path.isfile(os.path.join(FULL_UPLOAD_PATH, filename)):
            os.remove(os.path.join(FULL_UPLOAD_PATH, filename))
    for filename in os.listdir(FULL_MD_PATH):
        if os.path.isfile(os.path.join(FULL_MD_PATH, filename)):
            os.remove(os.path.join(FULL_MD_PATH, filename))

    # Saves the uploaded file to the uploads folder
    file_path = os.path.join(FULL_UPLOAD_PATH, file.filename)
    file.save(file_path)

    try:
        # Process the uploaded file
        process_file(file_path)
        flash('File successfully uploaded and processed')
        session['file_processed'] = True  # Indicate that file has been processed
    except Exception as e:
        flash(str(e))
        session['file_processed'] = False  # Indicate failure
        return redirect(request.url)

    # Rerenders the page if the above steps complete without issue
    # This will cause the download button to appear
    return redirect(url_for('index'))


# Define route for file download
@app.route('/download')
def download_file():
    try:
        # If the processed file exists...
        if os.path.exists(os.path.join(FULL_UPLOAD_PATH, 'processed_files.tar.gz')):
            # send the processed file as a download
            return send_from_directory(directory=FULL_UPLOAD_PATH, path='processed_files.tar.gz', as_attachment=True)
        else:
            # If it does not, provide an error message and redirect to index
            flash("Processed file not found.")
            return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 for local development
    print("This should not appear when run with Gunicorn")
    print(port)
    print(app.secret_key)
