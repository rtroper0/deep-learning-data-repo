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

# Define function to parse text from <p class="verse" ...>
def parse_p_class_verse(p_class_verse):
    # Find <span class="verse-number verse"> in p_class_verse
    span_class_verse_number_verse = p_class_verse.find('span', {'class':'verse-number verse'})
    # Get verse number from span_class_verse_number_verse
    verse_number = span_class_verse_number_verse.text.strip()
    # Remove span_class_verse_number_verse (to get only the paragraph text)
    span_class_verse_number_verse.decompose()
    # Remove all <sup class="studyNoteMarker dontHighlight"> in p_class_verse
    for sup in p_class_verse.find_all('sup', {'class': 'studyNoteMarker dontHighlight'}):
        sup.decompose()
    # Get verse text from p_class_verse
    verse_text = p_class_verse.text
    # Return parsed text
    return (verse_number, verse_text)

# Define function to parse text from <div class="article">
def parse_div_class_article(div_class_article):
    # Find all <p class="verse" ...> in div_class_article
    all_p_class_verse = div_class_article.find_all('p', {'class':'verse'})
    # Parse all <p class="verse" ...>
    all_verses = []
    for p_class_verse in all_p_class_verse:
        all_verses.append(parse_p_class_verse(p_class_verse))
    # Return all parsed verses
    return all_verses

# Define function to parse text from <div id="primary">
def parse_div_id_primary(div_id_primary):
    # Get chapter title from <h2 class="title-number" ...>
    chapter_title = div_id_primary.find('h2', {'class':'title-number'}).text
    # Get chapter number from chapter_title
    chapter_number = chapter_title.split()[-1]
    # Get chapter summary from <p class="study-summary" ...>
    chapter_summary = div_id_primary.find('p', {'class':'study-summary'}).text
    # Find <div class="article"> in div_id_primary
    div_class_article = div_id_primary.find('div', {'class':'article'})
    # Parse <div class="article"> (to get text of all verses)
    verses = parse_div_class_article(div_class_article)
    # Return all parsed text
    return (chapter_title, chapter_number, chapter_summary, verses)

# Define function to parse all text from the page
def parse_all_text_from_page(page):
    parsed_text = {}
    # Find <div id="primary"> in page
    div_id_primary = page.find('div', {'id': 'primary'})
    # Parse <div id="primary"> to get chapter title/number, summary, and verses
    chapter_title, chapter_number, chapter_summary, chapter_verses = parse_div_id_primary(div_id_primary)
    # Store parsed text in dictionary
    parsed_text['title'] = chapter_title
    parsed_text['number'] = chapter_number
    parsed_text['summary'] = chapter_summary
    parsed_text['verses'] = chapter_verses
    # Return parsed text
    return parsed_text

