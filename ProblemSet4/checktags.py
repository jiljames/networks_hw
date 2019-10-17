# File: CheckTags.py

"""
This program checks that tags are properly matched in an HTML file.
This version of the program runs in Python; the checktags version runs
directly from the command line.
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
    print(type(response))
    parser = HTMLTagParser()
    parser.checkTags(response.read().decode("UTF-8"))

class HTMLTagParser(html.parser.HTMLParser):

    """
    This class extends the standard HTML parser and overrides the
    callback methods used for start and end tags.
    """

    def __init__(self):
        """Creates a new HTMLTagParser object."""
        html.parser.HTMLParser.__init__(self)

    def checkTags(self, text):
        """Checks that the tags are balanced in the supplied text."""
        self._stack = [ ]
        self.feed(text)
        while len(self._stack) > 0:
            startTag,startLine = self._stack.pop()
            print("Missing </" + startTag + "> for <" + startTag +
                  "> at line " + str(startLine))

    def handle_starttag(self, startTag, attributes):
        """Overrides the callback function for start tags."""
        startLine,_ = self.getpos()
        self._stack.append((startTag, startLine))

    def handle_endtag(self, endTag):
        """Overrides the callback function for end tags."""
        endLine,_ = self.getpos()
        if len(self._stack) == 0:
            print("No <" + endTag + "> for </" + endTag +
                  "> at line " + str(endLine))
        else:
            while len(self._stack) > 0:
                startTag,startLine = self._stack.pop()
                if startTag == endTag:
                    break;
                print("Missing </" + startTag + "> for <" + startTag +
                      "> at line " + str(startLine))

# Startup code

if __name__ == "__main__":
    CheckTags()
