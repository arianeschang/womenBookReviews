import resolvingBooks as resolve
from goodreads import client
import sys, os



def main():

	args = sys.argv

	if len(args) == 2:
		pathToDir = args[1]
	else:
		print 'Please Supply a Path to a Directory'
		return

	if not os.path.isdir(pathToDir):
		print 'Not a valid filepath'
		return


	print 'authenticating goodreads'
	gc = client.GoodreadsClient("ENQJ9KubRltIC7lSKZSYA", "trYzd1HBcV4kNCtarG071uFZS1nbKLvo5Rg8CTb0ao")

	files = os.listdir(pathToDir)
	print files

	listOfFiles = []

	for fileName in files:
		if '-by-' in fileName:
			trimmed = fileName.split('.html.txt')[0]
			seperated = trimmed.split('-')
			final = ' '.join(seperated)
			listOfFiles.append(final)

	outputFile = open('piperData1.csv', 'a')
	missed = 0
	total = 0
	for book in listOfFiles:
		total = total + 1

		try:
			title, wikiGenre, grGenre = resolve.getAllGenres(book, gc)

		except Exception, e:
			print e
			missed = missed + 1
			print book

		outputFile.write(title + ',' + wikiGenre + ',' + grGenre + '\n')
		

if __name__ == '__main__':
   main()