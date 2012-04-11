#AutoURL-Related Documents
#By Nader Heidari
#This script pulls URLS from a list file, pulls their title using BeautifulSoup, and outputs them into an output file all ready for additional editing
#
import urllib2
import sys
import urlparse
import re
import htmlentitydefs
from sys import argv
from BeautifulSoup import BeautifulSoup
#from BeautifulSoup import BeautifulStoneSoup #Need that soup.
url=""
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
txt=open("RDURL") # Open the URL file.
output=open("output.txt",'w') #Open the output file, make it writable
output.truncate() #...but clear it first.
while True:
	url=txt.readline()#Pull a line
	if not url: break #If it's empty, end the program
	if not urlparse.urlparse(url).scheme: #If the line isn't a good URL, maybe it just needs an http:// added. Add that.
		url = "http://"+url
	page = urllib2.urlopen(url) # Generate source from page
	soup = BeautifulSoup(page) #Start parsing source using BS
	string=""
	if not soup.head.findAll(attrs={"name" : "article_title"}):
		for line in soup.findAll('ti'):
			if not line:break
			text=str(line).replace("</ti>","")
			text=text.replace("<ti>","")
			totalstring="|"+text+"|"+url+'||'
			finalstring=unescape(totalstring)
			output.write(finalstring)
			output.write("\n")
	for line in soup.head.findAll(attrs={"name" : "article_title"}):
		text=re.search('(?<=name="article_title" content=").*?(?=")', str(line))
		totalstring="|"+text.group(0).replace("\t","")+"|"+url.replace("\n","")+'||'
		print totalstring.replace(" | ","|")
		finalstring=unescape(totalstring)
		output.write(finalstring)
		output.write("\n")
print "Final processing stage..."
output=open("output.txt",'r')
initialrd=output.readline()
totalrd=initialrd
while True:
	rd=output.readline()
	if not rd: break
	totalrd=totalrd+"~"+rd
print totalrd.replace("\n","")
rdfile=open("rd.txt",'w')
rdfile.write(totalrd.replace("\n",""))
output.close()
rdfile.close()