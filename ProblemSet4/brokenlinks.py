# File: brokenlinks.py

"""
This program checks an HTML file for broken links
"""
import sys
import html.parser
import urllib.request

def CheckTags():
    """Reads a URL from the user and then checks it for tag matching."""
    url = input("URL: ")
    checkURL(url)

def checkURL(url):
    """Checks whether the tags are balanced in the specified URL."""
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.URLError as e: 
        print("An error occurred while accessing this URL.")
        print("Response status: ", e.code)
        print("Reason for failure given: ", e.reason)
        sys.exit(-1)
    except ValueError:
        print("This URL is of an unknown type: ")
        print(url)
        sys.exit(-1)
    parser = BrokenLinksParser(url)
    parser.checkTags(response.read().decode("UTF-8"))

class BrokenLinksParser(html.parser.HTMLParser):

    """
    This class extends the standard HTML parser and overrides the
    callback methods used for start and end tags.
    """

    def __init__(self, url):
        """Creates a new HTMLTagParser object."""
        html.parser.HTMLParser.__init__(self)
        self.origin = url

    def checkTags(self, text):
        """Checks that the tags are balanced in the supplied text."""
        self._stack = [ ]
        self.feed(text)
        while len(self._stack) > 0:
            startTag,link,startLine = self._stack.pop()
            print("Broken link " + link + " in <" + startTag +
                  "> tag at line " + str(startLine))

    def handle_starttag(self, startTag, attributes):
        """Overrides the callback function for start tags."""
        startLine,_ = self.getpos()
        for (k,v) in attributes:
            if k == "href" or k=="src":
                if "://" not in v:
                    v = self.origin + v
                try:
                    response = urllib.request.urlopen(v)
                except:
                    self._stack.append((startTag, v, startLine))



# Startup code

if __name__ == "__main__":
    CheckTags()
