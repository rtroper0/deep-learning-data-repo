# Library imports
import re
from bs4 import BeautifulSoup
import requests

# Used to request web page
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

# Define function to get content from specified url
def get_content_from_url(url):
    # Get content from url
    req = requests.get(url, headers)
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, "lxml")
    else:
        print("Warning: Could not load page! Response code is %s." % str(req.status_code))
    # Return page soup
    return soup

# Define function to parse text from <div id="details">
def parse_div_id_details(div_id_details):
    # Find <span class="active"> in div_id_details
    span_class_active = div_id_details.find('span', {'class':'active'})
    # Get volume name from span_class_active
    volume_name = span_class_active.text
    # Find <h1> in div_id_details
    h1 = div_id_details.find('h1')
    # Get volume title from h1
    volume_title = h1.text.strip()
    volume_title = ' '.join(volume_title.split())
    # Return volume name and title
    return (volume_name, volume_title)

# Define function to parse book information from <a class="tocEntry" ...>
def parse_a_class_tocentry(a_class_tocentry):
    # Get book name from <a class="tocEntry" ...>
    book_name = a_class_tocentry.text
    book_name = ' '.join(book_name.split())
    # Get book url
    book_url = a_class_tocentry.get('href')
    # Return book name and url
    return (book_name, book_url)

# Define function to parse book list from <ul class="books">
def parse_ul_class_books(ul_class_books):
    # Find all <li ...> in ul_class_books
    all_li = ul_class_books.find_all('li')
    # Get all book information from all_li
    book_information = []
    for li in all_li:
        # Get book id from li
        book_id = li.get('id')
        # Find <a class="tocEntry" ...> in li
        a_class_tocentry = li.find('a', {'class':'tocEntry'})
        # Parse book information from <a class="tocEntry" ...>
        book_name, book_url = parse_a_class_tocentry(a_class_tocentry)
        # Add book information to book_information
        book_information.append((book_id, book_name, book_url))
    # Return list of book information
    return book_information

# Define function to parse text from <div class="table-of-contents">
def parse_div_class_table_of_contents(div_class_table_of_contents):
    # Find all <ul class="books"> in div_class_table_of_contents
    all_ul_class_books = div_class_table_of_contents.find_all('ul', {'class':'books'})
    # Parse all <ul class="books"> and store results in list
    book_list = []
    for ul_class_books in all_ul_class_books:
        # Get book lists from each ul_class_books
        book_list = book_list + parse_ul_class_books(ul_class_books)
    # Return the book list
    return book_list

# Define function to parse all text from the page
def parse_all_text_from_page(page):
    parsed_text = {}
    # Find <div id="details"> in page
    div_id_details = page.find('div', {'id':'details'})
    # Parse <div id="details"> to get volume name and title
    name, title = parse_div_id_details(div_id_details)
    # Find <div class="table-of-contents"> in page
    div_class_table_of_contents = page.find('div', {'class': 'table-of-contents'})
    # Parse <div class="table-of-contents"> to get book list
    book_list = parse_div_class_table_of_contents(div_class_table_of_contents)
    # Store parsed text in dictionary
    parsed_text['name'] = name
    parsed_text['title'] = title
    parsed_text['books'] = book_list
    # Return parsed text
    return parsed_text

