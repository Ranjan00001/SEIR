import os
import math

root = 'C:\\Documents\\Sem4\\SEIR\\Projects\\p3\\25'
filepaths = [os.path.join(root,i) for i in os.listdir(root)]

def get_docno(text):
	start = text.find('<DOCNO>')
	end = text.find('</DOCNO>')
	return text[start+7:end]

collection = {}
def extract(filepaths):
	docnoDict = {}
	docId = 1
	for path in filepaths:
		fp = open(path, 'r')
		text = fp.read()
		docnoDict[get_docno(text)] = docId
		collection[docId] = tokenise(text)
		docId += 1
		fp.close()
	return docnoDict

dfDict = {}
def tokenise(doc):
	result = {}
	N = 0
	start = doc.find('TEXT')
	end = doc.find('/TEXT')
	current = start + 5
	word = ''
	while current < end:
		char = doc[current]
		if char.isalnum() or char == '_':
			word += char.lower()
		elif word != '':
			if word in result:
				result[word] += 1	# adding to tf (if observed again!)
			else:
				result[word] = 1	# Currently tf (observed till now) only as score, will multiply with idf later
				if word in dfDict:
					dfDict[word] += 1
				else:
					dfDict[word] = 1
			word = ''
			N += 1
		current += 1

	start = doc.find('TITLE')
	end = doc.find('/TITLE')
	current = start + 6
	word = ''
	while current < end:
		char = doc[current]
		if char.isalnum() or char == '_':
			word += char.lower()
		elif word != '':
			if word in result:
				result[word] += 1
			else:
				result[word] = 1
				if word in dfDict:
					dfDict[word] += 1
				else:
					dfDict[word] = 1
			word = ''
			N += 1
		current += 1

	# score updation as dividing tf by N
	# for term in result:
	# 	result[term] = result[term]/N
	return result

def similarity(d1, d2):
	score = 0
	m1 = 0
	m2 = 0
	for i, s1 in d1.items():
		m1 += s1 ** 2
		if i in d2:
			s2 = d2[i]
			score += s1 * s2

	for j, s2 in d2.items():
		m2 += s2 ** 2
	return score/((m1 ** 0.5) * (m2 ** 0.5))


docnoDict = extract(filepaths)
# print(docnoDict)
# Score updation as multiplying idf
for d in collection:
	for term in collection[d]:
		collection[d][term] = collection[d][term] * math.log(132/dfDict[term])

# print(collection)

similarityScore = []
# for d1 in collection:
# 	for d2 in collection:
for i in range(131, -1, -1):
	for j in range(i):
		p1 = filepaths[i]
		p2 = filepaths[j]
		d1 = get_docno(open(p1).read())
		d2 = get_docno(open(p2).read())
		if d1 != d2:
			a = similarity(collection[docnoDict[d1]], collection[docnoDict[d2]])
			similarityScore.append((d1, d2, a))

sort = sorted(similarityScore, key = lambda x : -x[2])
print(sort)
# print(sorted(similarityScore, key = lambda x : x[2]))
# print(similarityScore)