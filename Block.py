# Tree work
import uuid

class Block:
	def __init__(self, _label, _top, _width, _text=None, _bottom=None):
		self.id = uuid.uuid1().int
		self.content = True
		self.label = _label
		self.width = _width
		if _text is None:
			self.text = None
			self.leaf = False
		else:
			self.text = _text
			self.leaf = True
		self.top = _top
		if _bottom is None:
			self.bottom = _top
		else:
			self.bottom = _bottom
		#print(self.__repr__())

	def __repr__(self):
		return "Block({}, {}, {}, {})".format(self.label, self.width, self.text, self.top)

	def __str__(self):
		padChar = '-'
		if self.content:
			if self.text is None:
				read = self.label
			else:
				read = "{}:{}".format(self.label, self.text)
		else:
			read = "[?]"
		padding = ((self.width * 6) - len(read)) - 2
		if padding < 0: padding = 0
		lPad = padding // 2
		rPad = padding // 2
		#add extra to right pad
		rPad += self.width % (rPad + lPad + len(read))
		return "|{} {} {}|".format(padChar * lPad, read, padChar * rPad)


class Gridblock:
	def __init__(self, b):
		if not b == None:
			self.id = b.id
		else:
			self.id = None
		self.block = b
		self.label = None
		self.text = None
	def __str__(self):
		return "[{}]".format(b)
class GridPOS(Gridblock):
	def __init__(self, b):
		Gridblock.__init__(self, b)
		self.label = b.label
		self.content = True
	def __str__(self):
		return "[{}]".format(self.label)
class GridWord(Gridblock):
	def __init__(self, b):
		Gridblock.__init__(self, b)
		self.label = b.label
		self.text = b.text
		self.content = True
	def __str__(self):
		return "[{}]".format(self.text)
class GridSpace(Gridblock):
	def __init__(self):
		Gridblock.__init__(self, None)
		self.content = False
	def __str__(self):
		return "[{}]".format('--')



class parseTable:
	def __init__(self, tree, verbose=False):
		self.block_table = self.build(tree, 0, verbose)
		self.gridify(verbose)

	def build(self, tree, depth=0, verbose=False):# Recursive
		# Skip root
		if tree.label() == "ROOT": return self.build(tree[0])

		levels = [[None]] # what we know about this level and all bellow; our return
		ptables = []

		width = 0
		# For each child
		for i in range(len(tree)):
			# Has children? (grandchildren)
			if isinstance(tree[i], str):
				# no children; tree is a pos; tree[i] is a word - no extra block for word
				b = Block(tree.label(), depth, 1, _text=tree[i])
				# append to this level - this is the current tree
				levels[0][0] = b
				return levels
			# has children
			b = self.build(tree[i], depth+1, verbose) # recursive call
			ptables.append(b)
			# update width counter
			width += b[0][0].width


		# Stitch ptables with levels
		d = 0
		while True:
			stopcount = 0
			for ptable in ptables:
				# does this ptable go this deep?
				if len(ptable) <= d: # if it does not
					stopcount += 1
					continue
				# is the levels table big enough?
				if len(levels) == d+1:
					# make it bigger
					levels.append(ptable[d]) # add ptable at d
				else:
					# extend the list
					levels[d+1].extend(ptable[d])
			d += 1
			#stop condition
			if stopcount == len(ptables):
				# all ptables have been fully explored
				break
		#make own block
		levels[0][0] = Block(tree.label(), depth, width)

		if verbose:
			printT(levels)
			print('')

		return levels

	def gridify(self, verbose=False):
		# move words to the bottom and replace with appropriate spacers
		depth = len(self.block_table)
		width = self.block_table[0][0].width
		if verbose: print("Grid:  {} x {}".format(width, depth))
		self.grid = [[None for _ in range(width)] for _ in range(depth)]

		trueInsert = 0
		for d in range(depth):
			insert = 0
			for i in range(len(self.block_table[d])):
				elem = self.block_table[d][i]
				if elem.text == None:
					#POS
					for j in range(elem.width):
						self.grid[d][insert + j] = GridPOS(elem)
					insert += elem.width
				else:
					#Word
					
					#place it properly
					if verbose: print("[{}] {} -> {}".format(d, elem.text, insert))
					self.grid[depth-1][insert] = GridWord(elem)
					# Cascade
					if d < depth-1:
						self.block_table[d+1].insert(insert, elem)
						# place spacer
						self.grid[d][insert] = GridSpace()
					insert += 1
					
					





def printT(block_table):
	for b in block_table:
		for d in b:
			print(d, end='')
		print()