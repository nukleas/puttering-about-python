#Derrida
import urllib2
import sys
import urlparse
import re
import htmlentitydefs
from sys import argv
from BeautifulSoup import BeautifulSoup
print "Derrida: a Deconstructionist Program"
print "Originally in bash, now in Python!"
scriptname, filename = argv
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

rawdata=open(filename) # Open the URL file.
rawtext=rawdata.read() # Well, read the URL file.
print re.sub('“|”','\"',rawtext) # Damn those weird quotes!
URL_results=[] # And lets set up the URL results list.
for found_URL in re.finditer("(((ht|f)tp(s?))\://)?(www.|[a-zA-Z].)[a-zA-Z0-9\-\.]+\.(com|edu|gov|mil|net|org|biz|info|name|museum|us|ca|uk)(\:[0-9]+)*(/($|[a-zA-Z0-9\.\,\;\?\'\\\+&amp;%\$#\=~_\-]+))*",str(rawtext)):
	URL_results.append(found_URL.group())
print URL_results
URL_file=open("URL",'w')
for url in URL_results:
	urltext=url+"\n"
	URL_file.write(urltext)
URL_file.close()
txt=open("URL") # Open the URL file.
output=open("output.txt",'w') #Open the output file, make it writable
rdurl_list=open("RDURL",'w')
output.truncate() #...but clear it first.
while True:
	url=txt.readline()#Pull a line
	if not url: break #If it's empty, end the program
	if not urlparse.urlparse(url).scheme: #If the line isn't a good URL, maybe it just needs an http:// added. Add that.
		url = "http://"+url
	m = re.match('insertspecialcasesitetypehere', url) #Hey! is this a special type fodder?! Then we better sort it out somewhere else.
	if m:
		rdurl_list.write(url)
	else:
		soup=""
		try:
			page = urllib2.urlopen(url) # Generate source from page
			soup = BeautifulSoup(page) #Start parsing source using BS
		except:
			print url+"is not proper. One ought to fix that in the URL file." # Y U NO GOOD INPUT
		string=""
		try:
			for line in soup.head.title:
				string+=line.replace("\n","")
				totalstring=url.replace("\n","")+'|'+string.replace("\t","")
				print totalstring.replace(" | ","|")
				finalstring=unescape(totalstring)
				output.write(re.sub('[^A-Za-z0-9:\\/.,| &]+', '', finalstring))
				output.write("\n")
		except: print url+" is invalid. Please check URL file"
output.close()