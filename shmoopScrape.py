from lxml import html
import requests
from bs4 import BeautifulSoup
from urllib2 import urlopen, HTTPError
import string


def getThemes(url, bookDetails):
	print url
	html = urlopen(url).read()
	soup = BeautifulSoup(html, "lxml")


	section = soup.find("div", "btn-color-cycle-long")
	allThemes = section.find_all("div", "panel-heading")

	themes = []

	for theme in allThemes:
		text = theme.find("h4").text.encode('utf-8')
		themes.append(text)
	
	themes = ";!".join(themes)
	bookDetails = [bookDetails[0], bookDetails[1], bookDetails[2], themes]

	return bookDetails





def getBookLinks(url):
	html = urlopen(url).read()
	soup = BeautifulSoup(html, "lxml")


	section = soup.find("div", "row", id = "displayBio")
	books = section.find_all("div", "nameBio")
	allAuthors = section.find_all("div", "birthBio")


	links = []
	titles = []
	authors = []


	for book in books:
		link = book.find("a", href=True)['href']
		title = book.find("a", href=True)['title']
		links.append(link)
		titles.append(title.encode('ASCII', 'ignore'))

	for author in allAuthors:
		thisAuthor = author.text.encode('ASCII', 'ignore')
		authors.append(thisAuthor)

	return zip(links, titles, authors)



base_url = "http://www.shmoop.com/literature/"
links = getBookLinks(base_url)
print links
allBooks = []

base_url = "http://www.shmoop.com"

for link in links:
	url = base_url + link[0] + '/themes.html'
	try:
		bookDetails = getThemes(url, link)
	except:
		bookDetails = ()
		pass
	print bookDetails
	allBooks.append(bookDetails)


outputFile = open('shmoopTrainThemes.csv', 'w')
for book in allBooks:
	print book
	try:
		outputFile.write(book[1] + ',' + book[2] + ',' + book[3] + '\n')
	except Exception, e:
		print e
		pass




#for letter in lettersList:
#	url = base_url + letter + '.html'
#	theseLinks = getBookLinks(url)
#	bookLinks = bookLinks + theseLinks






