import requests
import sys

def getTitle(url):	# Uniform Resource Locator
	try:
		response = requests.get(url)	# Calls http get method
		# print(dir(response))
		if response.status_code == 200:
			# print(str(response))
			data = response.text
			# print(data)
			start = data.find("<title")
			end = data.find("</title>")
			current = start + 7
			value = []
			while (current < end):
				if data[current] == '#':
					while data[current] != ';':
						current += 1
					current += 1
				value.append(data[current])
				current += 1
			return ''.join(value)

		else:
			print(response.status_code)

	except Exception as e:
		print("Got error😑")
		print(e)

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
			print(response.status_code)

	except Exception as e:
		print("Got error😑")
		return e

def getURL(url):
	try:
		response = requests.get(url)	# Calls http get method
		# print(dir(response))
		if response.status_code == 200:
			# print(str(response))
			data = response.text
			# print(data)
			# start1 = "http://"
			start = "https://"
			# value = []
			index = data.find(start)
			while index != -1:
				# Assuming that every link is defined under double quote
				nextSpace = data.find('"', index)
				link = data[index:nextSpace]
				print(link)
				# value.append(link)
				# value.append("\n")
				index = data.find(start, nextSpace)
			# return value

		else:
			print(response.status_code)

	except Exception as e:
		print("Got error😑")
		print(e)


if __name__ == '__main__':
	URL = sys.argv[1]
	# a = getTitle(URL)
	# print("Title: ", a, "\n")
	b = getBody(URL)
	print(b)
	# print("Body", b, "\n")
	# print("Extracted links are:")
	# c = getURL(URL)