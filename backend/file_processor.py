import tarfile
import os

UPLOAD_FOLDER = './uploads'
PROCESSED_MD_FOLDER = './files/MD'


def process_file(file_path):
    with tarfile.open(file_path, "r:gz") as file:
        file.extractall(UPLOAD_FOLDER)
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
    with tarfile.open(os.path.join(UPLOAD_FOLDER, 'processed_files.tar.gz'), "w:gz") as tar:
        tar.add(PROCESSED_MD_FOLDER, arcname=os.path.basename(PROCESSED_MD_FOLDER))
