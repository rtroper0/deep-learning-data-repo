
# Library imports
from bs4 import BeautifulSoup
import requests

# Generic web parser providing basic functionality to load a webpage
# Use this as a base class for more specific webpage parsers
class WebpageParser:
    # WebpageParser version
    version = '0.1'
    
    # Used to request web page
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    
    def __init__(self, url = None):
        # Store current URL
        self.current_url = url
        # Store full page content
        self.pageContent = None
        self.pageLoaded = False
        # Load page if URL provided
        if not (url == None):
            # setUrl also calls loadCurrentPage
            self.setUrl(url)
    
    def getVersion(self):
        return self.version
    
    # Set URL and attempt to load page
    # Return the return value of 'loadCurrentPage()
    def setUrl(self, url):
        self.current_url = url
        self.pageContent = None
        self.pageLoaded = False
        return self.loadCurrentPage()
    
    def getUrl(self):
        # Check if URL has not been specified yet
        if self.current_url == None:
            print("Note: A valid URL has not been specified!")
            return ""
        # Return URL
        else:
            return self.current_url
    
    # Attempt to load current page; Return True if successful
    def loadCurrentPage(self):
        # Check if a URL has been specified
        if self.current_url == None:
            print("Error: Cannot retrieve current page! A URL has not been specified!")
            self.pageLoaded = False
            return self.pageLoaded
        # Check if page for current URL has already been loaded
        elif self.pageLoaded:
            print("Note: Page has already been loaded for current URL.")
        # Assume that page for current URL has not been loaded
        else:
            # Try to load page
            try:
                req = requests.get(self.current_url, headers=self.headers)
                self.pageContent = BeautifulSoup(req.content, "lxml")
                self.pageLoaded = True
            except:
                print("Warning: Could not load page: %s" % self.current_url)
                self.pageContent = None
                self.pageLoaded = False
        # Return Boolean indicating success or failuer
        return self.pageLoaded
    
    # Get text from the html section specified by tag and attributes
    # tag is a string and attributes is a dictionary of attribute/value pairs
    def getTextFromSection(self, tag, attributes):
        text = ""
        # Return if URL has not been specified
        if self.current_url == None:
            print("Warning: Cannot get text from specified html, because URL has not been specified!")
            return text
        # If this point is reached, URL has been specified
        html = self.pageContent.find(tag, attributes)
        if not (html == None):
            text = html.text
        else:
            print("Warning: Cannot get text from specified html! Returning empty string.")
            text = ""
        return text
        
        

