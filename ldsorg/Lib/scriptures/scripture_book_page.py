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

# Define function to parse book title from <h1 ... id="title1">
def parse_h1_id_title1(h1_id_title1):
    # Get title from h1_id_title1
    title = h1_id_title1.text.strip()
    title = ' '.join(title.split())
    # Return the title
    return title

# Define function to parse URLs from <ul class="jump-to-chapter">
def parse_ul_class_jump_to_chapter(ul_class_jump_to_chapter):
    # Find all <a ...> in ul_class_jump_to_chapter
    all_a = ul_class_jump_to_chapter.find_all('a')
    # Get all chapter numbers and URLs from all_a
    chapters = []
    for a in all_a:
        # Get the chapter number
        chapter_number = a.text
        # Get the chapter URL
        chapter_url = a.get('href')
        # Append to the chapters list
        chapters.append((chapter_number, chapter_url))
    # Return the list of chapter numbers and urls
    return chapters

# Define function to parse text from <div id="primary">
def parse_div_id_primary(div_id_primary):
    # Get scripture book name from <h2>
    scripture_book = div_id_primary.find('h2').text.strip()
    scripture_book = ' '.join(scripture_book.split())
    # Find <ul class="jump-to-chapter"> in div_id_primary
    ul_class_jump_to_chapter = div_id_primary.find('ul', {'class':'jump-to-chapter'})
    # Parse <ul class="jump-to-chapter"> (to get chapter numbers and urls)
    chapters = parse_ul_class_jump_to_chapter(ul_class_jump_to_chapter)
    # Return all parsed text
    return (scripture_book, chapters)

# Define function to parse all text from the page
def parse_all_text_from_page(page):
    parsed_text = {}
    # Find <h1 ... id="title1"> in page
    h1_id_title1 = page.find('h1', {'id':'title1'})
    # Only parse <h1 ... id="title1"> if it was found
    if(not(h1_id_title1 == None)):
        # Get book title from <h1 ... id="title1">
        title = parse_h1_id_title1(h1_id_title1)
    # Otherwise, search directly for <span class="dominant">
    else:
        # Find <span class="dominant"> in page
        span_class_dominant = page.find('span', {'class':'dominant'})
        # Get title from <span class="dominant">
        title = ' '.join(span_class_dominant.text.split())
    # Find <div id="primary"> in page
    div_id_primary = page.find('div', {'id': 'primary'})
    # Parse <div id="primary"> to get scripture book name and chapter numbers and urls
    book_name, chapters = parse_div_id_primary(div_id_primary)
    # Store parsed text in dictionary
    parsed_text['title'] = title
    parsed_text['name'] = book_name
    parsed_text['chapters'] = chapters
    # Return parsed text
    return parsed_text

