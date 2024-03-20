from flask import Flask, request, send_from_directory, render_template, redirect, url_for, flash
import os
# import tarfile
import sys
from backend.file_processor import process_file


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))
UPLOAD_FOLDER = './uploads'
PROCESSED_MD_FOLDER = './files/MD'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_MD_FOLDER, exist_ok=True)

# def process_file(file_path):
#     # Extract the tarfile
#     with tarfile.open(file_path, "r:gz") as file:
#         file.extractall(UPLOAD_FOLDER, filter="data")
#     # Assign the markdown template to a variable
#     with open(os.path.join(UPLOAD_FOLDER, "names.md")) as f:
#         template = f.read()
#     # Assign the csv file contents to a variable
#     with open(os.path.join(UPLOAD_FOLDER, "names.csv")) as f:
#         names = f.read()
#     # Split csv file on newline characters, creating a list of people
#     csv_lines = names.split("\n")
#     # For each person...
#     for line in csv_lines:
#         # create a list of values, and trim leading and trailing whitespace from each item
#         items = [x.strip() for x in line.split(",")]
#         # Skip the iteration if the first item is "FirstName" – we don't need a certificate for the legend
#         if items[0] == "FirstName":
#             continue
#         # Take the template, and replace the palceholder values with the items from the current person
#         md_output = template.replace("{{FirstName}}", items[0]).replace("{{LastName}}", items[1])
#         # Creates an output path with a file names based on the current person
#         output_path = os.path.join(PROCESSED_MD_FOLDER, f"{items[0].lower()}_{items[1].lower()}.md")
#         # Writes the finished certificate to the new file
#         with open(output_path, "w") as f:
#             f.write(md_output)
#     # Once all the new files have been creates, the output file is compressed
#     with tarfile.open(os.path.join(UPLOAD_FOLDER, 'processed_files.tar.gz'), "w:gz") as tar:
#         tar.add(PROCESSED_MD_FOLDER, arcname=os.path.basename(PROCESSED_MD_FOLDER))


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
    print("This should not appear when run with Gunicorn")
    print(port)
    print(app.secret_key)
    # app.run(debug=True)
    # app.run(host='0.0.0.0', port=port)
