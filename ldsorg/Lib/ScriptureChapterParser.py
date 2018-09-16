
# Library imports
from bs4 import BeautifulSoup
import requests
import ../../Lib/GenericWebpageParser as gwp


# Constants for retrieving content from lds.org
# Root URLs
LDS_ORG_ROOT = "https://www.lds.org/"
LDS_SCRIPTURES_ROOT = "https://www.lds.org/scriptures/"

# Scripture book names
SCRIPTURES = ["Old Testament", "New Testament", "Book of Mormon", "Doctrine and Covenants", "Pearl of Great Price"]

OT_IDX = 0; NT_IDX = 1; BM_IDX = 2; DC_IDX = 3; PGP_IDX = 4
# Scripture book abbreviations (lds.org)
SCRIPTURE_ABBV = ["ot", "nt", "bofm", "dc-testament", "pgp"]

# Old Testament book names
OT_BOOKS = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth",
            "First Samuel", "Second Samuel", "First Kings", "Second Kings", "First Chronicles",
            "Second Chronicles", "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
            "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel",
            "Daniel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
            "Zephaniah", "Haggai", "Zechariah", "Malachi"]

# Old Testament book abbreviations (lds.org)
OT_LDS_ABBV = ["gen", "ex", "lev", "num", "deut", "josh", "judg", "ruth",
            "1-sam", "2-sam", "1-kgs", "2-kgs", "1-chr",
            "2-chr", "ezra", "neh", "esth", "job", "ps", "prov",
            "eccl", "song", "isa", "jer", "lam", "ezek",
            "dan", "hosea", "joel", "amos", "obad", "jonah", "micah", "nahum", "hab",
            "zeph", "hag", "zech", "mal"]

# Old Testament book chapter counts (lds.org)
OT_CHAP_COUNTS = [50, 40, 27, 36, 34, 24, 21, 4,
            31, 24, 22, 25, 29,
            36, 10, 13, 10, 42, 150, 31,
            12, 8, 66, 52, 5, 48,
            12, 14, 3, 9, 1, 4, 7, 3, 3,
            3, 2, 14, 4]

# New Testament book names
NT_BOOKS = ["Matthew", "Mark", "Luke", "John", "Acts", "Romans", "First Corinthians", "Second Corinthians",
            "Galatians", "Ephesians", "Philippians", "Colossians", "First Thessalonians",
            "Second Thessalonians", "First Timothy", "Second Timothy", "Titus", "Philemon", "Hebrews", "James",
            "First Peter", "Second Peter", "First John", "Second John", "Third John", "Jude",
            "Revelation"]

# New Testament book abbreviations (lds.org)
NT_LDS_ABBV = ["matt", "mark", "luke", "john", "acts", "rom", "1-cor", "2-cor",
            "gal", "eph", "philip", "col", "1-thes",
            "2-thes", "1-tim", "2-tim", "titus", "philem", "heb", "james",
            "1-pet", "2-pet", "1-jn", "2-jn", "3-jn", "jude",
            "rev"]

# New Testament book chapter counts (lds.org)
NT_CHAP_COUNTS = [28, 16, 24, 21, 28, 16, 16, 13,
            6, 6, 4, 4, 5,
            3, 6, 4, 3, 1, 13, 5,
            5, 3, 5, 1, 1, 1,
            22]

# Book of Mormon book names
BM_BOOKS = ["First Nephi", "Second Nephi", "Jacob", "Enos", "Jarom", "Omni", "Words of Mormon", "Mosiah",
            "Alma", "Helaman", "Third Nephi", "Fourth Nephi", "Mormon",
            "Ether", "Moroni"]

# Book of Mormon book abbreviations (lds.org)
BM_LDS_ABBV = ["1-ne", "2-ne", "jacob", "enos", "jarom", "omni", "w-of-m", "mosiah",
            "alma", "hel", "3-ne", "4-ne", "morm",
            "ether", "moro"]

# Book of Mormon book chapter counts (lds.org)
BM_CHAP_COUNTS = [22, 33, 7, 1, 1, 1, 1, 29,
            63, 16, 30, 1, 9,
            15, 10]

# Doctrine and Covenant book names
DC_BOOKS = ["Sections"]

# Doctrine and Covenant book abbreviations (lds.org)
DC_LDS_ABBV = ["dc"]

# Doctrine and Covenant book chapter counts (lds.org)
DC_CHAP_COUNTS = [138]

# Pearl of Great Price book names
PGP_BOOKS = ["Moses", "Abraham", "Joseph Smith Matthew", "Joseph Smith History", "Articles of Faith"]

# Pearl of Great Price book abbreviations (lds.org)
PGP_LDS_ABBV = ["moses", "abr", "js-m", "js-h", "a-of-f"]

# Pearl of Great Price book chapter counts (lds.org)
PGP_CHAP_COUNTS = [8, 5, 1, 1, 1]

ALL_BOOKS = [OT_BOOKS, NT_BOOKS, BM_BOOKS, DC_BOOKS, PGP_BOOKS]
ALL_LDS_ABBV = [OT_LDS_ABBV, NT_LDS_ABBV, BM_LDS_ABBV, DC_LDS_ABBV, PGP_LDS_ABBV]
ALL_CHAP_COUNTS = [OT_CHAP_COUNTS, NT_CHAP_COUNTS, BM_CHAP_COUNTS, DC_CHAP_COUNTS, PGP_CHAP_COUNTS]


# Class used to parse scripture chapters from lds.org
# A scripture chapter page should have the following form:
#   'https://www.lds.org/scriptures/nt/john/1'
# In other words, it should consist of the scripture site root url
#   ('https://www.lds.org/scriptures/'), a scripture abbreviation (in this
#   case, 'nt'), a scripture book or book abbreviation (in this case, 'john')
#   and a chapter number (in this case, '1')  
class ScriptureChapterParser(gwp.WebpageParser):
    # Title block tag and attributes
    title_tag = "span"
    title_attrs = {"class":"dominant"}
    
    intro_tag = "p"
    intro_attrs = {"class":"intro"}
    
    chapter_tag = "h2"
    chapter_attrs = {"class":"title-number"}
    
    # Article tag and attributes
    article_tag = "div"
    article_attrs = {"class":"article"}
    
    # Verse number tag and attributes (for deleting)
    verseNum_tag = "span"
    verseNum_attrs = {"class":"verse-number verse"}
    
    # Study note marker tag and attributes (for deleting)
    noteMarker_tag = "sup"
    noteMarker_attrs = {"class":"studyNoteMarker dontHighlight"}
    
    def __init__(self, url = None):
        # Stores article block
        self.articleBlock = None
        # Call the parent class constructor
        if(url == None):
            gwp.WebpageParser.__init__(self)
        else:
            gwp.WebpageParser.__init__(self, url)
    
    def setUrl(self, url):
        successful = gwp.WebpageParser.setUrl(self, url)
        if successful:
            self.articleBlock = self.pageContent.find(self.article_tag, self.article_attrs)
        else:
            print("Error in 'setUrl'! New page may not have been loaded successfully!")
            self.articleBlock = None
    
    def getTitle(self):
        title = ""
        # Return if URL has not been specified
        if self.current_url == None:
            print("Warning: Cannot get title, because URL has not been specified!")
            return title
        # If this point is reached, URL has been specified
        title = self.pageContent.find(self.title_tag, self.title_attrs)
        if not (title == None):
            title = title.text
        else:
            print("Warning: Cannot get \'title\'! Returning empty string.")
            title = ""
        return title
    
    def getIntro(self):
        intro = ""
        # Return if URL has not been specified
        if self.current_url == None:
            print("Warning: Cannot get \'intro\' block, because URL has not been specified!")
            return intro
        # If this point is reached, URL has been specified
        intro = self.pageContent.find(self.intro_tag, self.intro_attrs)
        if not (intro == None):
            intro = intro.text
        else:
            #print("Warning: Cannot get \'intro\'! Returning empty string.")
            intro = ""
        return intro
    
    def getChapter(self):
        chapter = ""
        # Return if URL has not been specified
        if self.current_url == None:
            print("Warning: Cannot get chapter number, because URL has not been specified!")
            return chapter
        # If this point is reached, URL has been specified
        chapter = self.pageContent.find(self.chapter_tag, self.chapter_attrs)
        if not (chapter == None):
            chapter = chapter.text
        else:
            print("Warning: Cannot get chapter number! Returning empty string.")
            chapter = ""
        return chapter
    
    def getContent(self):
        chapContent = ""
        # Return if URL has not been specified
        if self.current_url == None:
            print("Warning: Cannot get scripture chapter content, because URL has not been specified!")
            return chapContent
        # If this point is reached, URL has been specified
        # Assume page has already been loaded; Check if articleBlock has been retrieved
        if not (self.articleBlock == None):
            # Remove verse numbers from article block
            verseNumbers = self.articleBlock.find_all(self.verseNum_tag, self.verseNum_attrs)
            for num in verseNumbers:
                num.decompose()
            # Remove reference footnotes from article block
            noteMarkers = self.articleBlock.find_all(self.noteMarker_tag, self.noteMarker_attrs)
            for marker in noteMarkers:
                marker.decompose()
            # Retrieve scripture chapter text
            chapContent = self.articleBlock.text
        else:
            print("Warning: Cannot get scripture chapter content, because articleBlock is None!")
        return chapContent

