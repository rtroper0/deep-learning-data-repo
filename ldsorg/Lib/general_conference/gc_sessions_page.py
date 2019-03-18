# Library imports
import re
from bs4 import BeautifulSoup
import requests

# Used to request web page
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
# Define domain-level url
domain_url = 'https://www.lds.org'

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

# Define function to parse text from <div class="title-block">
def parse_div_class_title_block(div_class_title_block):
    # Get conference title text from <h1 class="title">
    conference = div_class_title_block.find('h1', {'class': 'title'}).text
    # Return parsed text
    return conference

# Define function to parse text from <div class="section__header">
def parse_div_class_section_header(div_class_section_header):
    # Get session title from <span class="section__header__title">
    session = div_class_section_header.find('span', {'class': 'section__header__title'}).text
    # Return parsed text
    return session

# Define function to parse text from <div class="lumen-tile__text-wrapper">
def parse_div_class_lumen_tile_text_wrapper(div_class_lumen_tile_text_wrapper):
    # Get talk title from <div class="lumen-tile__title">
    title = div_class_lumen_tile_text_wrapper.find('div', {'class': 'lumen-tile__title'}).text.strip()
    # Get talk author from <div class="lumen-tile__content">
    author = div_class_lumen_tile_text_wrapper.find('div', {'class': 'lumen-tile__content'}).text
    # Return parsed text
    return (title, author)

# Define function to parse text from <div class="lumen-tile lumen-tile--horizontal lumen-tile--list">
def parse_div_class_lumen_tile_lumen_tile_horizontal_lumen_tile_list(div_class_lumen_tile_lumen_tile_horizontal_lumen_tile_list):
    # Get talk url from <a href=... class="lumen-tile__link">
    talk_url = div_class_lumen_tile_lumen_tile_horizontal_lumen_tile_list.find('a', {'class': 'lumen-tile__link'})
    talk_url = domain_url + talk_url.get('href')
    # Find <div class="lumen-tile__text-wrapper"> in div_class_lumen_tile_lumen_tile_horizontal_lumen_tile_list
    div_class_lumen_tile_text_wrapper = div_class_lumen_tile_lumen_tile_horizontal_lumen_tile_list.find('div', {'class': 'lumen-tile__text-wrapper'})
    # Parse <div class="lumen-tile__text-wrapper">
    talk_info = parse_div_class_lumen_tile_text_wrapper(div_class_lumen_tile_text_wrapper)
    # Return parsed text as a tuple
    return (talk_url, talk_info)

# Define function to parse text from <div class="section tile-wrapper layout--3 lumen-layout__item">
def parse_div_class_section_tile_wrapper_layout_3_lumen_layout_item(div_class_section_tile_wrapper_layout_3_lumen_layout_item):
    # Find <div class="section__header"> in div_class_section_tile_wrapper_layout_3_lumen_layout_item
    div_class_section_header = div_class_section_tile_wrapper_layout_3_lumen_layout_item.find('div', {'class': 'section__header'})
    # Parse <div class="section__header">
    session = parse_div_class_section_header(div_class_section_header)
    # Find all <div class="lumen-tile lumen-tile--horizontal lumen-tile--list"> in div_class_section_tile_wrapper_layout_3_lumen_layout_item
    all_div_class_lumen_tile_lumen_tile_horizontal_lumen_tile_list =         div_class_section_tile_wrapper_layout_3_lumen_layout_item.find_all('div', {'class': 'lumen-tile lumen-tile--horizontal lumen-tile--list'})
    # Parse all <div class="lumen-tile lumen-tile--horizontal lumen-tile--list">
    all_talk_info = []
    for div_class_lumen_tile_lumen_tile_horizontal_lumen_tile_list in all_div_class_lumen_tile_lumen_tile_horizontal_lumen_tile_list:
        all_talk_info.append(parse_div_class_lumen_tile_lumen_tile_horizontal_lumen_tile_list(div_class_lumen_tile_lumen_tile_horizontal_lumen_tile_list))
    # Return parsed text as a tuple
    return (session, all_talk_info)

# Define function to parse text from <div class="section-wrapper lumen-layout lumen-layout--landing-3">
def parse_div_class_section_wrapper_lumen_layout_lumen_layout_landing_3(div_class_section_wrapper_lumen_layout_lumen_layout_landing_3):
    # Find all <div class="section tile-wrapper layout--3 lumen-layout__item"> in div_class_section_wrapper_lumen_layout_lumen_layout_landing_3
    all_div_class_section_tile_wrapper_layout_3_lumen_layout_item =         div_class_section_wrapper_lumen_layout_lumen_layout_landing_3.find_all('div', {'class': 'section tile-wrapper layout--3 lumen-layout__item'})
    # Parse all <div class="section tile-wrapper layout--3 lumen-layout__item">
    all_session_info = []
    for div_class_section_tile_wrapper_layout_3_lumen_layout_item in all_div_class_section_tile_wrapper_layout_3_lumen_layout_item:
        all_session_info.append(parse_div_class_section_tile_wrapper_layout_3_lumen_layout_item(div_class_section_tile_wrapper_layout_3_lumen_layout_item))
    # Return parsed text
    return all_session_info

# Define function to parse all text from the page
def parse_all_text_from_page(page):
    parsed_text = {}
    # Find <div class="title-block"> in page
    div_class_title_block = page.find('div', {'class': 'title-block'})
    # Parse <div class="title-block">
    conference_title = parse_div_class_title_block(div_class_title_block)
    # Find <div class="section-wrapper lumen-layout lumen-layout--landing-3"> in page
    div_class_section_wrapper_lumen_layout_lumen_layout_landing_3 = page.find('div', {'class': 'section-wrapper lumen-layout lumen-layout--landing-3'})
    # Parse <div class="section-wrapper lumen-layout lumen-layout--landing-3">
    sessions_info = parse_div_class_section_wrapper_lumen_layout_lumen_layout_landing_3(div_class_section_wrapper_lumen_layout_lumen_layout_landing_3)
    # Add all parsed text to dictionary
    parsed_text['conference_title'] = conference_title
    parsed_text['sessions_info'] = sessions_info
    # Return parsed text
    return parsed_text

