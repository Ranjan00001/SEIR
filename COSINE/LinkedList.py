
class Posting(object):
	"""docstring for Posting"""

	__slots__ = ('_element', '_next')

	def __init__(self, e = None):
		self._element = e
		self._next = None

	@property
	def next(self):
		return self._next

	@property
	def element(self):
		return self._element
	
	@next.setter
	def next(self, value):
		self._next = value

	@element.setter
	def element(self, value):
		self._element = value

	def __repr__(self):
		return str([self._element, self._next])


class SingleLinkedList:

	def __init__(self, *args):				# if passed more than one element
		length = len(args)
		self._size = length
		try:
			value = args[0]
		except:
			value = None
		self._head = Posting(value)
		current = self._head
		for i in range(1, length):
			# print(current)
			current._next = Posting(args[i])
			current = current._next

	@property
	def term(self):
		return self._term
	
	@property
	def size(self):
		return self._size
	
	@term.setter
	def term(self, value):
		self._term = value

	# def __init__(self):
	# 	self._head = Posting(None)
	# 	self._size = 0

	def addLast(self, new):
		'''
		new is an element, need not to be a Posting
		'''
		current = self._head
		while current._next is not None:
			# print(current._next)
			current = current._next
			# print(current._next, 'hi')
		a = Posting(new)
		current._next = a
		# print(current._next)
		self._size += 1
		return a
	# if we also keep tail of this LinkedList then we can skip this loop

	def addStart(self, new):
		current = self._head
		a = Posting(new)
		self._head = a
		self._head._next = current
		self._size += 1
		return a

	def delLast(self):
		if self._size == 0:
			raise Error_raise.EmptyLinkedListError('Linked List is empty')
		current = self._head
		while current._next._next is not None:
			current = current._next
		current._next = None
		self._size -= 1
		return current._element

	def delStart(self):
		if self._size == 0:
			raise Error_raise.EmptyLinkedListError('Linked List is empty')
		current = self._head
		self._head = current._next
		self._size -= 1
		return current._element

	def __repr__(self):
		current = self._head
		acc = []
		for i in range(self._size):
			acc.append(current._element)
			current = current._next
		return str(acc)

	def Swap(self, x, y):
		temp1 = x._next._next
		temp2 = y._next._next
		x._next._next = y._next._next
		y._next._next = temp1
		temp3 = x._next
		x._next = temp2
		y._next = temp3