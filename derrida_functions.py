import re
import htmlentitydefs
import urlparse
import urllib2
from BeautifulSoup import BeautifulSoup
def unescape(text):#Lifted this off effbot.org, it cleans up all those nasty unicode characters. Don't ask me how it works, honestly.
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def checkURL(url):
    if not url: return 0 # If it's empty, why bother?
    if not urlparse.urlparse(url).scheme: # If it doesn't parse, maybe it's just missing a "http://"
        url="http://"+url # so lets add that and try again.
    if not urlparse.urlparse(url).scheme: return 0 # Womp womp
    else: return url

def makeSoup(url):
    page = urllib2.urlopen(url) # Generate source from page
    soup = BeautifulSoup(page) #Start parsing source using BS
    return soup