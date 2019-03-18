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

# A clean-up function to insert a single space after punctuation that is followed immediately by the first letter
# of the next sentence. By default, it does this after periods, question marks, colons, and closing quotes
def insert_space_between_sentences(input_string, regex=r'[.”:?…][“A-Z]'):
    pattern = re.compile(regex)
    return pattern.sub(insert_space, input_string)

# Supporting function that replaces the regex matches
def insert_space(match):
    s = match.group()
    return '{0} {1}'.format(s[:-1], s[-1:])

# Define function to parse text from <div class='sticky-banner fademe'>
def parse_div_class_sticky_banner_fademe(div_class_sticky_banner_fademe):
    # Get session text
    session = div_class_sticky_banner_fademe.find('a', {'class': 'sticky-banner__link'}).text
    # Get title text
    title = div_class_sticky_banner_fademe.find('span', {'class': 'sticky-banner__current'}).text
    # Return parsed text as a tuple
    return (session, title)

# Define function to parse text from <div class="article-author">
def parse_div_class_article_author(div_class_article_author):
    # Get author title text
    title = div_class_article_author.find('p', {'class': 'article-author__title'})
    title_text = '' if title == None else title.text.strip()
    # Remove <p class=article-author__title>
    title.decompose()
    # Get author name text
    author = div_class_article_author.find('a', {'class': 'article-author__name'})
    author_text = div_class_article_author.text.strip() if author == None else author.text
    # Return parsed text as a tuple
    return (author_text, title_text)

# Define function to parse text from <div class="title-block">
def parse_div_class_title_block(div_class_title_block):
    # Get title text
    title = div_class_title_block.find('h1', {'class': 'title'}).text
    # Get session text
    session = div_class_title_block.find('h2', {'class': 'title printTitle'}).text
    # Find <div class="article-author"> in div_class_title_block
    div_class_article_author = div_class_title_block.find('div', {'class': 'article-author'})
    # Parse <div class="article-author">
    author_info = parse_div_class_article_author(div_class_article_author)
    # Return parsed text as a tuple
    return (session, title, author_info)

# Define function to parse text from <div class="article-content">
def parse_div_class_article_content(div_class_article_content, search_tags=['p', 'h1', 'h2']):
    parsed_text = []
    # Find all <p ...> in div_class_article_content
    all_p = div_class_article_content.find_all(search_tags)
    # Get text for each paragraph
    for p in all_p:
        # Remove all <sup class="marker"> in p
        for sup in p.find_all('sup', {'class': 'marker'}):
            sup.decompose()
        parsed_text.append(p.text)
    # Also get text from div_class_article_content (in case sections were missed by getting just p tags)
    full_text = ' '.join(div_class_article_content.text.split())
    # Insert a single space after every period that has no white space after it
    full_text = insert_space_between_sentences(full_text)
    # Return parsed text
    return (parsed_text, full_text)

# Define function to parse text from <section class="article-page lumen-template-read">
def parse_section_class_article_page_lumen_template_read(section_class_article_page_lumen_template_read):
    parsed_text = {}
    # Find <div class="title-block"> in section_class_article_page_lumen_template_read
    div_class_title_block = section_class_article_page_lumen_template_read.find('div', {'class': 'title-block'})
    # Parse <div class="title-block">
    title_block = parse_div_class_title_block(div_class_title_block)
    # Get text from <p class='kicker' ...>
    kicker = section_class_article_page_lumen_template_read.find('p', {'class': 'kicker'})
    kicker_text = '' if kicker == None else kicker.text
    # Find <div class="article-content"> in section_class_article_page_lumen_template_read
    div_class_article_content = section_class_article_page_lumen_template_read.find('div', {'class': 'article-content'})
    # Parse <div class="article-content">
    content = parse_div_class_article_content(div_class_article_content)
    # Add all parsed text to dictionary
    parsed_text['title_block'] = title_block
    parsed_text['kicker'] = kicker_text
    parsed_text['content'] = content
    # Return parsed text
    return parsed_text

# Define function to parse all text from the page
def parse_all_text_from_page(page):
    parsed_text = {}
    # Find <div class='sticky-banner fademe'> in page
    div_class_sticky_banner_fademe = page.find('div', {'class': 'sticky-banner fademe'})
    # Parse <div class='sticky-banner fademe'>
    sticky_banner = parse_div_class_sticky_banner_fademe(div_class_sticky_banner_fademe)
    # Find <section class="article-page lumen-template-read"> in page
    section_class_article_page_lumen_template_read = page.find('section', {'class': 'article-page lumen-template-read'})
    # Parse <section class="article-page lumen-template-read">
    article_content = parse_section_class_article_page_lumen_template_read(section_class_article_page_lumen_template_read)
    # Add all parsed text to dictionary
    parsed_text['sticky_banner'] = sticky_banner
    parsed_text['article_content'] = article_content
    # Return parsed text
    return parsed_text

