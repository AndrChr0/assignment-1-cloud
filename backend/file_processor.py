# Required imports
import tarfile
import os

# Define variables (change to env vars in the future)
UPLOAD_FOLDER = './uploads'
PROCESSED_MD_FOLDER = './files/MD'


def process_file(file_path):
    # Extract the tarfile
    with tarfile.open(file_path, "r:gz") as file:
        file.extractall(UPLOAD_FOLDER, filter="data")
    # Assign the markdown template to a variable
    with open(os.path.join(UPLOAD_FOLDER, "names.md")) as f:
        template = f.read()
    # Assign the csv file contents to a variable
    with open(os.path.join(UPLOAD_FOLDER, "names.csv")) as f:
        names = f.read()
    # Split csv file on newline characters, creating a list of people
    csv_lines = names.split("\n")
    # For each person...
    for line in csv_lines:
        # create a list of values, and trim leading and trailing whitespace from each item
        items = [x.strip() for x in line.split(",")]
        # Skip the iteration if the first item is "FirstName" – we don't need a certificate for the legend
        if items[0] == "FirstName":
            continue
        # Take the template, and replace the palceholder values with the items from the current person
        md_output = template.replace("{{FirstName}}", items[0]).replace("{{LastName}}", items[1])
        # Creates an output path with a file names based on the current person
        output_path = os.path.join(PROCESSED_MD_FOLDER, f"{items[0].lower()}_{items[1].lower()}.md")
        # Writes the finished certificate to the new file
        with open(output_path, "w") as f:
            f.write(md_output)
    # Once all the new files have been creates, the output file is compressed
    with tarfile.open(os.path.join(UPLOAD_FOLDER, 'processed_files.tar.gz'), "w:gz") as tar:
        tar.add(PROCESSED_MD_FOLDER, arcname=os.path.basename(PROCESSED_MD_FOLDER))
