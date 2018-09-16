import sys
import time

# Add project root folder to sys.path
sys.path.append("..\\..")

from Lib.GenericWebpageParser import WebpageParser

# Output file path
output_file_path = "..\\..\\ldsorg\\data\\scriptures\\"

# Root URL
LDS_SCRIPTURES_ROOT = "https://www.lds.org/scriptures/"

# Scripture book abbreviations (lds.org)
ABBREVIATION = ["ot", "nt", "bofm", "dc-testament", "pgp"]

# Scripture book names
NAME = ["Old Testament", "New Testament", "Book of Mormon", "Doctrine and Covenants", "Pearl of Great Price"]

# Generate a dictionary with index keys
INDEX = dict(list(enumerate(ABBREVIATION)))

# Column names for Volumes table
COLUMNS = ['index', 'abbreviation', 'name', 'title_page', 'introduction']

# Specify html tag and attributes for title page content
title_page_tag = "div"
title_page_attr = {"id":"primary"}

# Specify html tag and attributes for introduction content
introduction_tag = "div"
introduction_attr = {"class":"article"}

# Specify separator for output_list
separator = "\t"

def main(argv):
    # Initialize indexes to None
    i = None
    j = None
    # First check that at least one argument was provided
    if(len(argv) == 0):
        print("You must provide an integer argument!")
        return
    # Try to convert the first command line argument to an int
    try:
        i = int(argv[0])
    except ValueError:
        # Issue message and return if conversion fails
        print("Could not convert first argument to int!")
        return
    # Check if index i is out of range
    if((i < 0) | (i >= len(NAME))):
        # If out of range, print message and return
        print("First index is out of range!")
        return
    # Check if more than one argument was provided
    if(len(argv) > 1):
        # Try to convert second argument to int
        try:
            j = int(argv[1])
        except ValueError:
            # Issue message and return if conversion fails
            print("Could not convert second argument to int!")
            return
        # If second argument is less than first, issue message and return
        if(j < i):
            print("Second argument must be greater than or equal to first!")
            return
        # Check if index j is out of range
        if((j < 0) | (j >= len(NAME))):
            # If out of range, print message and return
            print("Second index is out of range!")
            return
    
    # If a second argument was never set, set j to id
    if( j == None):
        j = i
    # Write headers to output file
    f = open(output_file_path + 'volumes_data.tsv', 'w')
    f.write(separator.join(COLUMNS) + '\n')
    f.close()
    # Create a WebpageParser instance
    parser = WebpageParser()
    for index in range(i, j+1):
        abbr = ABBREVIATION[index]
        name = NAME[index]
        # Set parser URL to retrieve title page content
        parser.setUrl(LDS_SCRIPTURES_ROOT + abbr + "/title-page")
        # Get title page content
        title_page = parser.getTextFromSection(title_page_tag, title_page_attr)
        title_page = title_page.strip().encode('unicode_escape').decode()
        # Set parser URL to retrieve introduction content
        parser.setUrl(LDS_SCRIPTURES_ROOT + abbr + "/introduction")
        # Get introduction content
        introduction = parser.getTextFromSection(introduction_tag, introduction_attr)
        introduction = introduction.strip().encode('unicode_escape').decode()
        # Insert a pause
        time.sleep(2)
        # Write information to output file
        output_list = [str(index), abbr, name, title_page, introduction]
        f = open(output_file_path + 'volumes_data.tsv', 'a')
        f.write(separator.join(output_list) + '\n')
        f.close()

if __name__ == "__main__":
    main(sys.argv[1:])
    