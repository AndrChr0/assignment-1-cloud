from flask import Flask, request, send_from_directory, render_template, redirect, url_for, flash
import os
from file_processor import process_file

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))
UPLOAD_FOLDER = './uploads'
PROCESSED_MD_FOLDER = './files/MD'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_MD_FOLDER, exist_ok=True)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file():
    if 'uploadedFile' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['uploadedFile']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and file.filename.endswith('.tar.gz'):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        try:
            process_file(file_path)
            flash('File successfully uploaded and processed')
            return redirect(url_for('download_file'))
        except Exception as e:
            flash(str(e))
            return redirect(request.url)
    else:
        flash('Invalid file type')
        return redirect(request.url)


@app.route('/download')
def download_file():
    try:
        if os.path.exists(os.path.join(UPLOAD_FOLDER, 'processed_files.tar.gz')):
            return send_from_directory(directory=UPLOAD_FOLDER, filename='processed_files.tar.gz', as_attachment=True)
        else:
            flash("Processed file not found.")
            return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 for local development
    # app.run(host='0.0.0.0', port=port)
