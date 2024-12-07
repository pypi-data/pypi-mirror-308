class Link:
	empty = ()
	def __init__(self, first, rest=empty):
		assert rest is Link.empty or isinstance(rest, Link)
		self.first = first
		self.rest = rest

	def __repr__(self):
		if self.rest:
			rest_repr = ', ' + repr(self.rest)
		else:
			rest_repr = ''
		return 'Link(' + repr(self.first) + rest_repr + ')'

	def __str__(self):
		string = '<'
		while self.rest is not Link.empty:
			string += str(self.first) + ' '
			self = self.rest
		return string + str(self.first) + '>'

class Tree:
	def __init__(self, label, branches=[]):
		for b in branches:
			assert isinstance(b, Tree)

		self.label = label
		self.branches = list(branches)

	def is_leaf(self):
		return not self.branches
