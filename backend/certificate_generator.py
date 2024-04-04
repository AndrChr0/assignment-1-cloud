from flask import Flask, request, send_from_directory, render_template, redirect, url_for, flash, session
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from backend.file_processor import process_file

# Create Flask app
app = Flask(__name__)

# Set secret key for session management, uses variable from environment in railway
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# Define upload and processed file directories
UPLOAD_FOLDER = './uploads'
PROCESSED_MD_FOLDER = './files/MD'

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_MD_FOLDER, exist_ok=True)


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

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
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

    # Only redirect to download if the above steps complete without issue
    return redirect(url_for('download_file'))


# Define route for file download
@app.route('/download')
def download_file():
    try:
        if os.path.exists(os.path.join(UPLOAD_FOLDER, 'processed_files.tar.gz')):
            # Send the processed file as a download
            return send_from_directory(directory=UPLOAD_FOLDER, filename='processed_files.tar.gz', as_attachment=True)
        else:
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