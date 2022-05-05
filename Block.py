# Tree work
from uuid import uuid1


class Gridblock:
	def __init__(self):
		self.id = None
		self.label = None
		self.text = None
		self.content = True
	def __str__(self):
		return "[{}]".format(b)
class GridPOS(Gridblock):
	def __init__(self, id, label):
		Gridblock.__init__(self)
		self.id = id
		self.label = label
		self.content = True
	def __str__(self):
		return "[{}]".format(self.label)
class GridWord(Gridblock):
	def __init__(self, label, text):
		Gridblock.__init__(self)
		self.label = label
		self.text = text
		self.content = True
	def __str__(self):
		return "[{}]".format(self.text)
class GridSpace(Gridblock):
	def __init__(self):
		Gridblock.__init__(self)
		self.content = False
	def __str__(self):
		return "[{}]".format('--')



class parseTable:
	def __init__(self, tree, verbose=False):
		#self.block_table = self.build(tree, 0, verbose)
		#self.gridify(verbose)

		self.grid = self.assemble(tree[0], verbose)


	def containsPOS(self, group):
		for elem in group:
			if isinstance(elem, GridPOS):
				return False
		return True

	def gridStitch(self, gridA, gridB):
		# B should always follow A
		print("\nA")
		printT(gridA)
		print("\nB")
		printT(gridB)


		dif = len(gridA) - len(gridB)
		if dif == 0:
			# they match
			for i in range(len(gridA)):
				gridA[i].extend(gridB[i])
				print("\n| AB")
				printT(gridA)
			return gridA
		else:
			newgrid = []
			for i in range((len(gridA) if dif < 0 else len(gridB)) - 1):
				# range of shorter list - 1; all matching
				newgrid.append(gridA[i])
				newgrid[-1].extend(gridB[i])
			# Last x levels, don't match
			i = len(newgrid)
			if dif > 0:
				# gridA is longer
				for j in range(dif):
					newgrid.append(gridA[i + j]) # second to last row
					spacers = [GridSpace() for _ in range(len(gridB[-1]))]
					newgrid[-1].extend(spacers)
				newgrid.append(gridA[-1]) # last row
				newgrid[-1].extend(gridB[-1])
			else:
				# gridB is longer
				for j in range(dif * -1):
					spacers = [GridSpace() for _ in range(len(gridA[-1]))]
					newgrid.append(spacers)
					newgrid[-1].extend(gridB[i + j])
				newgrid.append(gridA[-1])
				newgrid[-1].extend(gridB[-1])


		print("\n| AB")
		printT(newgrid)
		return newgrid


	def assemble(self, tree, verbose=False):
		# is tree a word?
		if isinstance(tree[0], str):
			return [[GridWord(tree.label(), tree[0])]]

		# for each child
		grid = None
		for subtree in tree:
			if grid is None:
				grid = self.assemble(subtree, verbose)
			else:
				grid = self.gridStitch(grid, self.assemble(subtree, verbose))
		# top level of grid
		treeID = uuid1().int
		top = [GridPOS(treeID, tree.label()) for _ in range(len(grid[0]))]

		grid.insert(0, top)

		if verbose:
			print('\nG')
			printT(grid)
			print('')

		return grid




def printT(block_table):
	for b in block_table:
		for d in b:
			print(d, end='')
		print()