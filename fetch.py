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
			# print(start)
			value = []
			for i in range(start+7, end):
				value.append(data[i])
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
	current = start + 5
	last = False		# Tells whether last string encountered was a white-space or not
	while current < end:
		if data[current] == '<':
			# Skip the tag part
			while data[current] != '>':
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
			value = []
			index = data.find(start)
			while index != -1:
				# Assuming that every link is defined under double quote
				nextSpace = data.find('"', index)
				link = data[index:nextSpace]
				# print(link)
				value.append(link)
				index = data.find(start, nextSpace)
			return value

		else:
			print(response.status_code)

	except Exception as e:
		print("Got error😑")
		return e


if __name__ == '__main__':
	URL = sys.argv[1]
	a = getTitle(URL) 
	b = getBody(URL)
	c = getURL(URL)
	print("Title: ", a, "\n")
	print("Extracted links are: ", c, "\n")
	print("Body: ", b)