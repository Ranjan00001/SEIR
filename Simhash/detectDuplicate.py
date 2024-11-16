import requests
import sys


def wordList(content):
	lst = []
	word = ''
	for character in content:
		character = character.lower()
		if character.isalnum():
			word += character
		else:
			if word.isalnum():
				lst.append(word)
			word = ''
	return lst

# def wordFrequency(content):
# 	frequency = {}
# 	word = ''
# 	for character in content:
# 		character = character.lower()
# 		if character.isalnum():
# 			word += character
# 		else:
# 			if word not in frequency:
# 				if word.isalnum():
# 					frequency[word] = 1
# 			else:
# 				frequency[word] += 1
# 			word = ''
# 	return frequency

def wordFreq(lst, n = 5, overlap = 2):
	frequency = {}
	for i in range(0, len(lst), overlap):
		nGram = ' '.join(lst[i:i+n])
		# print(nGram)
		if nGram in frequency:
			frequency[nGram] += 1
		else:
			frequency[nGram] = 1
	return frequency

def polyHash(word, p, m):
	value = 0
	for i in range(len(word)):
		# print(word[i])
		value += ord(word[i]) * p**i
	return value % m

def simhash(document):
	vector = {}
	for word in document:
		binary = str(bin(polyHash(word, 53, 2**64)))[2:].rjust(64, '0')	# 64 bit binary
		vector[binary] = document[word]

	simhash = []
	for i in range(64):
		weight = 0
		for binry in vector:
			one = binry[i] == '1'
			weight += vector[binry] if one else -vector[binry]
		if weight > 0:
			simhash.append(1)
		else:
			simhash.append(0)

	return simhash

def percentageDuplicate(document1, document2):
	# Document1 and 2 are dictionry of unique words
	s1 = simhash(document1)
	s2 = simhash(document2)
	assert len(s1) == len(s2)
	match = 0
	for i in range(len(s1)):
		if s1[i] == s2[i]:
			match += 1
	return match*100/len(s1)




def clean(data):		# Helper function
	start = data.find("<body")
	end = data.find("</body>")
	value = []
	current = start - 1
	last = False		# Tells whether last string encountered was a white-space or not
	while current < end:
		if data[current] == '<':
			current += 1
			# Identify the current tag going on and acc to that deal with the tag part
			currentTag = []
			tagCollected = False
			while data[current] != '>':
				if not tagCollected and not data[current].isspace():
					currentTag.append(data[current])
				else:
					tagCollected = True

				currTag = ''.join(currentTag)
				if currTag in ["style", "script"]:
					skip = data.find('</'+currTag, current)
					current = skip

				if value[-1] != "\n" and currTag == 'a':
					value.append('\n')
				current += 1
		elif data[current] == '#':
			while data[current] != ';':
				current += 1
		elif data[current:current + 8] == 'https://':
			current += 8
			while data[current] != '"':
				current += 1
		else:
			if data[current].isspace() and not last:
				# If the current character is a whitespace and not the last one, append a single space
				value.append(' ')
				last = True
			elif not data[current].isspace():
				# If the current character is not a whitespace, append it to the result
				value.append(data[current])
				last = False
		current += 1
	return ''.join(value)

def getBody(url):
	try:
		response = requests.get(url)	# Calls http get method
		# print(dir(response))
		if response.status_code == 200:
			# print(str(response))
			data = response.text
			return clean(data)

		else:
			return (response.status_code)

	except Exception as e:
		print("Got error😑")
		return e

if __name__ == '__main__':
	url1 = sys.argv[1]
	url2 = sys.argv[2]
	content1 = getBody(url1)
	content2 = getBody(url2)
	lst1 = (wordList(content1))
	lst2 = wordList(content2)
	document1 = wordFreq(lst1)
	document2 = wordFreq(lst2)
	print(document1)
	print("")
	print(document2)
	print(percentageDuplicate(document1, document2))