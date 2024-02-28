n = 4


def very_useful(input):
    print(input)


very_useful(n)

#
# receive tar.gz
# 1. unpack compressed file to new folder
# 2. load CSV and MD file
# 3. perform replaces and store MD files for each person (folder named "MD")
# 4. convert MD --> PDF for all files (in "PDF" folder)
# 5. compress PDF folder to tar.gz
# 6. make available for GET at its URI
