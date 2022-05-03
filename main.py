import os
from nltk.parse.corenlp import CoreNLPServer
from nltk.parse.corenlp import CoreNLPParser

stext = "The quick brown fox jumped over the lazy dog"


# Stanford NLP Server
stanford_core = "stanford-corenlp-4.4.0"

server = CoreNLPServer(
   os.path.join(stanford_core, "stanford-corenlp-4.4.0.jar"),
   os.path.join(stanford_core, "stanford-corenlp-4.4.0-models.jar"),    
)

print("Starting Stanford NLP Server")
server.start()
print("Server Started")

# The parser

parser = CoreNLPParser()

tree = next(parser.raw_parse(stext))

# Stop the Stanford NLP Server
print("Stopping server")
server.stop()

# Tree work

class Block:
	def __init__(self, _label, _top, _width, _text=None, _bottom=None):
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
		if self.text is None:
			read = self.label
		else:
			read = self.text
		padding = (self.width - len(read)) - 2
		lPad = padding // 2
		rPad = padding // 2
		#add extra to right pad
		rPad += self.width % (rPad + lPad + len(read))
		return "|{} {} {}|".format(padChar * lPad, read, padChar * rPad)


class Spacer(Block):
	def init(self, _width, _label=None):
		self.width = _width
		if _label is None:
			self.label = None
		else:
			self.label = _label
		self.text = "[spacer]"
		self.leaf = False
		self.top = None




class pTree:
	def __init__(self, tree):
		self.block_table = self.build(tree)

	def build(self, tree, depth=0):# Recursive
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
				b = Block(tree.label(), depth, len(tree[i]), _text=tree[i])
				# append to this level - this is the current tree
				levels[0][0] = b
				return levels
			# has children
			b = self.build(tree[i], depth+1) # recursive call
			ptables.append(b)
			# update width counter
			width += b[0][0].width + 2
		# Stitch ptables with levels
		d = 0
		while True:
			stopcount = 0
			for ptable in ptables:
				# does this ptable go this deep?
				if len(ptable) <= d: # if it does not
					# copy phrase type down

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

		return levels


def printT(tree, d=0):
	if d == 5: return

	print("|{}>".format(d), end='')
	#print("  " * d, end='')
	print("[{}]  ".format(tree if isinstance(tree, str) else tree.label()), end='')
	print("{}".format(tree))
	print("|{}|".format(len(tree)))
	for i in range(len(tree)):
		printT(tree[i], d+1)



#printT(tree)
p = pTree(tree)

for b in p.block_table:
	for d in b:
		print(d, end='')
	print()
