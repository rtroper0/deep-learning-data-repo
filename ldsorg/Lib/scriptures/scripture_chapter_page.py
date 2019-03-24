# Library imports
import os
import re
import time
from tqdm import tqdm
from bs4 import BeautifulSoup
import pandas as pd
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
    chapter_summary = div_id_primary.find('p', {'class':'study-summary'})
    chapter_summary = '' if (chapter_summary == None) else chapter_summary.text
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

# Utility function to generate file name
def generate_file_name_root(all_book_info, book_id):
    # Get information for specified book_id
    selection = all_book_info.book_id == book_id
    book_info = all_book_info.loc[selection]
    # Get volume id
    volume_id = book_info.volume_id.values[0]
    # Get list of book_ids
    book_ids = list(all_book_info.book_id[all_book_info.volume_id == volume_id])
    # Get list of unique volume ids
    unique_volume_ids = list(all_book_info.volume_id.unique())
    # Get 1-based index of volume id
    volume_index = str(unique_volume_ids.index(volume_id)+1)
    # Get 1-based index of book id
    book_index = str(book_ids.index(book_id)+1)
    # Generate file name root
    file_name_root = '_'.join([volume_index, volume_id, zero_pad(book_index, 2), book_id])
    # Return file name root
    return file_name_root

# Utility function to convert integer to zero-padded string
def zero_pad(number, size):
    padded_number = size*'0' + str(number)
    padded_number = padded_number[-size:]
    return padded_number

# Function to loop over all chapters and get verse texts
def scrape_verses_for_book(all_book_info, book_id):
    # Get information for specified book_id
    selection = all_book_info.book_id == book_id
    book_info = all_book_info.loc[selection]
    # Get the volume id
    volume_id = book_info.volume_id.values[0]
    # Get the root url
    root_url = book_info.book_url.values[0]
    # Get number of chapters
    num_chapters = book_info.chapter_count.values[0]
    # Loop over all chapters, scrape verse texts and store in list
    all_verses = []
    for chapter_num in tqdm(range(1, num_chapters+1)):
        # Break after specified number of loops
        #if(chapter_num > 2): break
        # Generate url
        url = '/'.join([root_url, str(chapter_num)])
        # Print url for diagnostic purposes
        #print(url)
        # Get content from url
        page_soup = get_content_from_url(url)
        # Parse all text from page
        all_text_from_page = parse_all_text_from_page(page_soup)
        # Loop over verses and store in list
        for verse_num, verse_text in all_text_from_page['verses']:
            # Information to append
            info = (volume_id, book_id, chapter_num, verse_num, verse_text)
            all_verses.append(info)
        # Add pause
        time.sleep(2)
    # Create a dataframe
    column_labels = ['volume_id', 'book_id', 'chapter_number', 'verse_number',  'verse_text']
    verses_df = pd.DataFrame(all_verses, columns = column_labels)
    # Return the dataframe
    return verses_df

# Function to scrape all verses for a specified list of book ids
def scrape_verses_for_book_list(all_book_info, book_ids, output_path = 'data/scriptures'):
    # Loop over book ids, scrape verses and write to output file
    for book_id in book_ids:
        # Specify file name with path
        file_name_root = generate_file_name_root(all_book_info, book_id)
        file_and_path = '{0}/{1}.csv'.format(output_path, file_name_root)
        # Only scrape book verses if an output file does not exist for the book
        if(not(os.path.isfile(file_and_path))):
            # Scrape book verses and store as dataframe
            book_verses_df = scrape_verses_for_book(all_book_info, book_id)
            # Write book verses to output file
            book_verses_df.to_csv(file_and_path, index=False, encoding = "utf-8")
            print('Wrote data to \'{0}\''.format(file_and_path))
        else:
            print('File \'{0}\' already exists!'.format(file_and_path))

