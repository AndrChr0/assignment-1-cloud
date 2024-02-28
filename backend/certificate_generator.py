# Step 1. unpack compressed file to new folder
# import modules
import tarfile
import os

# open the file to be extracted
with tarfile.open("./archive.tar.gz", "r:gz") as file:
    # Extract the contents to a new folder
    file.extractall("./files/raw")

# 2. load CSV and MD file
with open("./files/raw/names.md") as f:
    template = f.read()
with open("./files/raw/names.csv") as f:
    names = f.read()

# split CSV file into lines
csv_lines = names.split("\n")

# create the processed folder if it doesn't exist
processed_folder = "./files/MD"
os.makedirs(processed_folder, exist_ok=True)

# 3. perform replaces and store MD files for each person (folder named "MD")
for line in csv_lines:
    # removes leading and trailing whitespace on CSV items
    items = [x.strip() for x in line.split(",")]
    # skips the CSV header
    if items[0] == "FirstName":
        continue
    # combines CSV values and markdown template to create the output for the MD files
    md_output = template.replace("{{FirstName}}", items[0]).replace("{{LastName}}", items[1])
    # creates filenames based on CSV information
    output_path = f"./files/MD/{items[0].lower()}_{items[1].lower()}.md"
    # write output string to given filepath, "w" mode creates files if they don't exist
    with open(output_path, "w") as f:
        f.write(md_output)


#
# receive tar.gz
# 4. convert MD --> PDF for all files (in "PDF" folder)
# 5. compress PDF folder to tar.gz
# 6. make available for GET at its URI
