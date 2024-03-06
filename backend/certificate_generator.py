from flask import Flask, request, send_from_directory, render_template, redirect, url_for, flash
import tarfile
import os
import pypandoc

app = Flask(__name__)
app.secret_key = os.urandom(24)
UPLOAD_FOLDER = './uploads'
PROCESSED_MD_FOLDER = './files/MD'
PDF_FOLDER = './files/PDF'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_MD_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    # Serve the HTML form from the templates folder
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
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

def process_file(file_path):
    with tarfile.open(file_path, "r:gz") as file:
        file.extractall(UPLOAD_FOLDER)
    
    # Assuming the CSV and MD files are located directly inside the extracted folder
    # Adjust the paths as needed based on your actual file structure
    with open(os.path.join(UPLOAD_FOLDER, "names.md")) as f:
        template = f.read()
    with open(os.path.join(UPLOAD_FOLDER, "names.csv")) as f:
        names = f.read()

    csv_lines = names.split("\n")
    for line in csv_lines:
        items = [x.strip() for x in line.split(",")]
        if items[0] == "FirstName":
            continue
        md_output = template.replace("{{FirstName}}", items[0]).replace("{{LastName}}", items[1])
        output_path = os.path.join(PROCESSED_MD_FOLDER, f"{items[0].lower()}_{items[1].lower()}.md")
        with open(output_path, "w") as f:
            f.write(md_output)

    for md_file in os.listdir(PROCESSED_MD_FOLDER):
        if md_file.endswith('.md'):
            input_path = os.path.join(PROCESSED_MD_FOLDER, md_file)
            output_path = os.path.join(PDF_FOLDER, md_file.replace('.md', '.pdf'))
            pypandoc.convert_file(input_path, 'pdf', outputfile=output_path)

    with tarfile.open(os.path.join(UPLOAD_FOLDER, 'processed_files.tar.gz'), "w:gz") as tar:
        tar.add(PDF_FOLDER, arcname=os.path.basename(PDF_FOLDER))

@app.route('/download')
def download_file():
    return send_from_directory(directory=UPLOAD_FOLDER, filename='processed_files.tar.gz', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)