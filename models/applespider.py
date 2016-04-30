from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse
from bs4 import BeautifulSoup

# We are going to create a class called LinkParser that inherits some
# methods from HTMLParser which is why it is passed into the definition
class LinkParser(HTMLParser):

    # This is a function that HTMLParser normally has
    # but we are adding some functionality to it
    def handle_starttag(self, tag, attrs):
        # We are looking for the begining of a link. Links normally look
        # like <a href="www.someurl.com"></a>
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    # We are grabbing the new URL. We are also adding the
                    # base URL to it. For example:
                    # www.netinstructions.com is the base and
                    # somepage.html is the new URL (a relative URL)
                    #
                    # We combine a relative URL with the base URL to create
                    # an absolute URL like:
                    # www.netinstructions.com/somepage.html
                    newUrl = parse.urljoin(self.baseUrl, value)
                    # And add it to our colection of links:
                    if self.rules is not None and self.rules.get('link_prefix') is not None:
                        found = False
                        for rule in self.rules.get('link_prefix'):
                            found = found or newUrl.startswith( parse.urljoin(self.baseUrl, rule ) )
                        if not found:
                            break
                    self.links = self.links + [newUrl]

    # This is a new function that we are creating to get links
    # that our spider() function will call
    def getLinks(self, url, rules=None):
        self.links = []
        self.rules = rules
        # Remember the base URL which will be important when creating
        # absolute URLs
        self.baseUrl = url
        # Use the urlopen function from the standard Python 3 library
        response = urlopen(url)
        # Make sure that we are looking at HTML and not other things that
        # are floating around on the internet (such as
        # JavaScript files, CSS, or .PDFs for example)
        if response.getheader('Content-Type')=='text/html':
            htmlBytes = response.read()
            # Note that feed() handles Strings well, but not bytes
            # (A change from Python 2.x to Python 3.x)
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return htmlString, self.links
        else:
            return "",[]

class AppleSpider:
    
    def __init__(self, baseUrl=None, rules=None, callback=None):
        self.baseUrl = baseUrl or [('http://hkm.appledaily.com/list.php?category_guid=10829391&category=instant', 0)]
        self.rules = rules or {'link_prefix': ['http://hkm.appledaily.com/detail.php']}
        self.callback = callback

    def setCallback(self,callback):
        self.callback = callback
        
    def extractContent(self, html, url):
        soup = BeautifulSoup(html, 'html.parser')
        content = ''
        lastUpdateTime = None
        title = ''
        if soup.select('.lastupdate'):
            lastUpdateTime = soup.select('.lastupdate')[0].text
        if soup.select('#content-article h1'):
            title = soup.select('#content-article h1')[0].text
        paragraphs = soup.select('#content-article p')
        for paragraph in paragraphs:
            if paragraph.get('class') is None or ( paragraph.get('class') not in [ ['video-caption'], ['next'] ] ):
                content += paragraph.text
        if self.callback is not None and lastUpdateTime is not None:
            self.callback(title, content, url, lastUpdateTime)

    # And finally here is our spider. It takes in an URL, a word to find,
    # and the number of pages to search through before giving up
    def crawl(self, maxLevel):  
        pagesToVisit = self.baseUrl
        levelVisited = 0
        # The main loop. Create a LinkParser and get all the links on the page.
        # Also search the page for the word or string
        # In our getLinks function we return the web page
        # (this is useful for searching for the word)
        # and we return a set of links from that web page
        # (this is useful for where to go next)
        while pagesToVisit != []:
            # Start from the beginning of our collection of pages to visit:
            url, levelVisited = pagesToVisit[0]
            if levelVisited > maxLevel:
                break
            pagesToVisit = pagesToVisit[1:]
            print(levelVisited, "Visiting:", url)
            parser = LinkParser()
            data, links = parser.getLinks(url, self.rules)
            self.extractContent(data,url)
            # Add the pages that we visited to the end of our collection
            # of pages to visit:
            links = [(link, levelVisited+1) for link in links ]
            pagesToVisit = pagesToVisit + links

