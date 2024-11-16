import os
import math

class Posting:
	def __init__(self, docId, position):
		self.docId = docId
		self.positions = [position]
		self.score = 0

	def __eq__(self, otherId):
		return self.docId == otherId
		
	def __repr__(self):
		return str(self.docId) + " " + str(self.positions) + " " + str(self.score)

class InvIndex:
	"""docstring for invIndex"""
	def __init__(self):
		self.data = {}
		self.df = {}

	def add(self, term, docId, position):
		if term in self.df:
			self.df[term].add(docId)
		else:
			self.df[term] = set()
			self.df[term].add(docId)

		if term in self.data:
			ind = self.data[term]
			try:
				ind[ind.index(docId)].positions.append(position)
			except ValueError as e:
				# print(e)
				ind.append(Posting(docId, position))
		else:
			self.data[term] = [Posting(docId, position)]

	def __repr__(self):
		return str(self.data) + '\n\n\n' + str(self.df)

root = 'C:\\Documents\\Sem4\\SEIR\\Projects\\p3\\25'
filepaths = [os.path.join(root,i) for i in os.listdir(root)]

def get_docno(text):
	start = text.find('<DOCNO>')
	end = text.find('</DOCNO>')
	return text[start+7:end]

docnoDict = {}
def docnoDictCreate(filepaths):
	docId = 0
	for path in filepaths:
		# print('hi')
		fp = open(path, 'r')
		text = fp.read()
		docId += 1
		docnoDict[get_docno(text)] = docId
		fp.close()
		# print('hey')
	return docnoDict

tokens = {}
def createIndex(indFile, document, docId, field):
	global tokens
	start = document.find(field)
	end = document.find('/' + field)
	current = start + 5
	word = ''
	while current < end:
		char = document[current]
		if char.isalnum() or char == '_':
			word += char.lower()
		elif word != '':
			indFile.add(word, docId, current-len(word))
			tokens[word] = len(tokens) + 1
			word = ''
		current += 1

def extract(filepaths):
	indices = InvIndex()
	for path in filepaths:
		file = open(path, 'r')
		document = file.read()
		docId = docnoDict[get_docno(document)]
		createIndex(indices, document, docId, 'TITLE')
		createIndex(indices, document, docId, 'TEXT')
	return indices

def addScore(indFile):
	for term, invIndex in indFile.data.items():
		# magnitude = 0
		for posting in invIndex:
			tf = len(posting.positions)
			df = len(indFile.df[term])
			idf = math.log(132/df)
			posting.score = tf*idf
			# magnitude += posting.score ** 2

		# Normalisation
		# for posting in invIndex:
		# 	try:
		# 		posting.score = posting.score / (magnitude ** 0.5)
		# 	except:
		# 		None

def tokenise(doc, field):
	start = doc.find(field)
	end = doc.find('/' + field)
	current = start + 5
	word = ''
	lst = []
	while current < end:
		char = doc[current]
		if char.isalnum() or char == '_':
			word += char.lower()
		elif word != '':
			lst.append(word)
			word = ''
		current += 1
	return lst

def documentise(indFile, lst, docId):
	d = {}
	for tok in lst:
		d[tok] = indFile.data[tok][indFile.data[tok].index(docId)].score
	return d

# Now pairwise document have to be calculated
def similarity(indFile, d1, d2):
	id1 = docnoDict[get_docno(d1)]
	id2 = docnoDict[get_docno(d2)]
	l1 = tokenise(d1, 'TITLE') + tokenise(d1, 'TEXT')
	l2 = tokenise(d2, 'TITLE') + tokenise(d2, 'TEXT')
	token1 = documentise(indFile, l1, id1)
	token2 = documentise(indFile, l2, id2)
	score = 0
	m1 = 0
	m2 = 0
	for i, s1 in token1.items():
		if i in token2:
			s2 = token2[i]
			m1 += s1 ** 2
			m2 += s2 ** 2
			score += s1 * s2
	return score/((m1 ** 0.5) * (m2 ** 0.5) * len(l1) * len(l2))

docnoDict = docnoDictCreate(filepaths)
# print(docnoDict)
ind = extract(filepaths)
# print(tokens)
addScore(ind)
# print(ind)
similarityScore = []
for p in filepaths:
	for q in filepaths:
		d1 = open(p).read()
		d2 = open(q).read()
		a = (docnoDict[get_docno(d1)], docnoDict[get_docno(d2)], similarity(ind, d1, d2))
		similarityScore.append(a)
sorted(similarityScore, key = lambda x : x[2])
print(similarityScore)