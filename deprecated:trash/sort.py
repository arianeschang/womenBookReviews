from operator import itemgetter

women = [4.8, 1.2, 3.6, 2.5, 14.4, 4.2, 2.6, 9.0, 13.2, 18.9, 9.2, 12.3, 11.0, 5.5, 12.0, 18.4, 3.2, 3.4, 7.3]
men = [10.8, 3.3, 8.0, 5.2, 24.7, 6.7, 3.8, 10.8, 13.3, 16.4, 7.7, 9.0, 7.5, 3.8, 7.6, 11.7, 0.3, 1.3, 3.2]
labels = ['Politics', 'Economics', 'Science', 'Philosophy', 'History', 'War', 'Religion', 'Mystery', \
			'Biography', 'Cultural', 'Fantasy', 'Autobiography', 'Romance', 'Childrens', 'Young Adult', \
			'Historical Fiction', 'Feminism', 'Family', 'Adult Fiction']

tuples = []
difference = []

for i in range(len(women) - 1):
	difference.append(men[i] - women[i])


tuples = zip(women, men, labels, difference)
print tuples
tuples = sorted(tuples, key=itemgetter(3))
print tuples

lists = zip(*tuples)
labels = list(lists[2])
women = list(lists[0])
men = list(lists[1])

print labels
print women
print men
