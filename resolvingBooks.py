import wikipedia
from bs4 import BeautifulSoup
import urllib2
from goodreads import client
import csv
import os


def getWikiGenre(title):
	genre = ''

	try:
		book = wikipedia.page(title)
	except wikipedia.DisambiguationError, e:

		allResults = e.options

		found = False
		for result in allResults:
			if '(novel)' in result:
				book = wikipedia.page(result)
				found = True

		if found == False:
			return 'Wiki not found'



	url = book.url

	print url

	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page, "lxml")

	vcard = soup.find_all("table", class_="infobox vcard")[0]
	rows = vcard.find_all("tr")

	for row in rows:
		try:
			th = row.find_all("th")[0]
			td = row.find_all("td")[0]
			if th.text.lower() == 'genre':
				genre = td.text
				genre = genre.encode(('utf8'))
				genre = genre.rstrip().split('\n')
				genre = "; ".join(genre)
				return genre
		
		except:
			continue

	return 'No Genre found'

def getGoodReadsGenres(link):
	page = urllib2.urlopen(link)
	soup = BeautifulSoup(page, "lxml")

	main = soup.find_all("div", class_="mainContent")[0]
	content = main.find_all("div", class_="mainContentFloat")[0]
	right = content.find_all("div", class_="rightContainer")[0]
	left = right.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['stacked'])[0]
	bigBox = left.find_all("div", class_="bigBox")[0]
	genreBox = bigBox.find_all("div", class_="bigBoxBody")[0]
	genres = genreBox.find_all("div", class_="elementList")

	listGenres = []
	for genre in genres:
		thisGenreContainer = genre.find_all("div", class_="left")[0]
		thisGenre = thisGenreContainer.find_all("a", "actionLinkLite bookPageGenreLink")[0].text
		listGenres.append(thisGenre)


	return list(set(listGenres))

def getAllGenres(title, gc):
	print 'finding Goodreads URL'
	book = gc.search_books(title)[0]


	isbn =  book.isbn
	link = book.link
	print link
	wikiGenre = ""
	GRgenre = []


	try:
		wikiGenre = getWikiGenre(title)
	except Exception, e:
		print "Unable to get wiki"
		print e

	try:
		GRgenre = getGoodReadsGenres(link)
	except Exception, e:
		print "Unable to get goodreads"
		print e

	print title
	print "Wikipedia finds: " + wikiGenre
	print "Goodreads finds: " + "; ".join(GRgenre)

	return title, wikiGenre, "; ".join(GRgenre)


def main():
	print 'authenticating goodreads'
	gc = client.GoodreadsClient("ENQJ9KubRltIC7lSKZSYA", "trYzd1HBcV4kNCtarG071uFZS1nbKLvo5Rg8CTb0ao")


	lines = list(open('bookTitles.txt', 'r'))[0]
	listBooks = lines.split(', ')

	outputFile = open('bookGenres.csv', 'a')
	for book in listBooks:
		title, wikiGenre, grGenre = getAllGenres(book, gc)
		outputFile.write(title + ',' + wikiGenre + ',' + grGenre + '\n')
		

if __name__ == '__main__':
   main()


