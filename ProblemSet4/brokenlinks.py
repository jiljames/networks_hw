# File: brokenlinks.py

"""
This program checks an HTML file for broken links
"""
import sys
import html.parser
import urllib.request
import ssl

def CheckLinks():
    """Reads a URL from the user and then checks it for broken links."""
    url = input("URL: ")
    checkURL(url)


def checkURL(url):
    """Checks whether the links are broken in an HTML file."""
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.URLError as e: 
        print("An error occurred while accessing this URL.")
        print("Response status: ", e.code)
        print("Reason for failure given: ", e.reason)
        sys.exit(-1)
    except ValueError:
        print("Consider using http. This URL is of an unknown type: ")
        print(url)
        sys.exit(-1)
    parser = BrokenLinksParser(url)
    parser.checkLinks(response.read().decode("UTF-8"))


class BrokenLinksParser(html.parser.HTMLParser):

    """
    This class extends the standard HTML parser and overrides the
    callback methods used for start and end tags.
    """

    def __init__(self, url):
        """Creates a new BrokenLinksParser object."""
        html.parser.HTMLParser.__init__(self)
        # Prepare our base url
        if url.endswith(".html"):
            url = url[:url.rfind("/")]
        if url[-1] != "/":
            url+= "/"
        self.base = url


    def checkLinks(self, text):
        """Checks that the links aren't broken."""
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
                if "://" not in v and not v.startswith("mailto:"):
                    v = self.base + v
                # Handle security check in case of https
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                try:
                    response = urllib.request.urlopen(v,context=ctx)
                except urllib.error.URLError as e:
                    self._stack.append((startTag, v, startLine))




# Startup code

if __name__ == "__main__":
    CheckLinks()
