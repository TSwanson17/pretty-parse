# The graphics

import turtle

def colorgen(colors):
		for color in colors:
			yield color

def abs(n):
	if n < 0:
		return n * -1
	else:
		return n



class Branch:
	def __init__(self, text, pos, height, width, color, style, layers):
		self.text = text
		self.pos = pos
		self.height = height
		self.width = width
		self.color = color
		self.style = style
		self.layers = layers

		#print("Box: {}  |  {}  [{}]".format(self.pos, self.text, layers))

	def drawBox(self):
		self.t.setpos(self.pos)
		self.t.fillcolor(self.color)
		self.t.begin_fill()
		for i in range(4):
			if i % 2 == 1:
				self.t.pendown()
				self.t.forward(self.height * self.layers)
				self.t.penup()
			else:
				self.t.penup()
				self.t.forward(self.width)
			self.t.right(90)
		self.t.end_fill()

	def drawText(self):
		x = self.pos[0] + (self.width / 2)
		y = self.pos[1] - self.height 
		self.t.penup()
		self.t.setpos(x, y)
		self.t.write(self.text, font=self.style, align='center', move=True)
		return abs(x - self.t.pos()[0])

	def draw(self):
		self.t = turtle.Turtle()
		self.t.penup()
		self.drawBox()
		self.drawText()

class Leaf(Branch):
	def __init__(self, text, pos, height, style, width=0):
		Branch.__init__(self, text, pos, height, width, None, style, 1)

	def draw(self):
		self.t = turtle.Turtle()
		self.size = self.drawText()
		self.size *= 2
		if self.size < self.height * 1.5:
			self.size *= 2
		return self.size


# This will be the master class for displaying content
class visTree:
	def __init__(self, pos, block_grid):
		turtle.setup(width=.75, height=0.5, startx=5, starty=5)

		self.pos = (pos[0] - (turtle.window_width() / 2), (turtle.window_height() / 2) - pos[1]) # this is the upper right corner of the drawn tree
		self.bGrid = block_grid # grid of gridBlock objects

		self.color_list = ['#33cc8c', '#b38d99', '#2f4b7c', '#665191', '#a05195', '#d45087', '#f95d6a', '#ff7c43', '#ffa600', '#ff8c8c', '#eaa3fe', '#bea3fe', '#ac57ac', '#c267fe', '#7784da', '#73b0c2', '#67eafd', '#59f8dd', '#64f88a', '#ed6c74']
		self.colorscheme = colorgen(self.color_list)
		self.style = ("Arial", 14)
		self.layerHeight = 20

	def create(self):
		turtle.tracer(0, 0)
		turtle.hideturtle()
		tDepth = len(self.bGrid) # total depth
		#self.treeTable = [[None for _ in range(len(self.bGrid[0]))] for _ in range(tDepth)]
		self.treeTable = []

		
		# The bottom level, get widths, don't actually draw this, we cant yet
		self.widths = []
		#self.treeTable.append([])
		for word in self.bGrid[tDepth-1]:
			text = '  ' + word.text + ' '
			#text = word.text
			newleaf = Leaf(text, self.pos, self.layerHeight, self.style)
			self.widths.append(newleaf.draw())
			#print("w: {} ".format(self.widths[-1]))
		turtle.clearscreen()

		# now that we have widths, build the tree but don't draw
		# top down
		
		drawPos = list(self.pos)
		for d in range(tDepth):
			self.treeTable.append([])
			# d : depth
			currentBranch = {'id':None, 'width':0, 'text':None}
			for b in range(len(self.widths)):
				#print("{}, {} | {} | {}".format(d, b, drawPos, currentBranch))
				# b : block index
				block = self.bGrid[d][b]
				# don't do spacers
				if not block.content:
					drawPos[0] += self.widths[b]
					continue

				if d + 1 == tDepth:
					# at the bottom, leaves
					text = block.text
					self.treeTable[d].append(Leaf(text, (drawPos[0], self.pos[1] - ((tDepth-1) * self.layerHeight)), self.layerHeight, self.style, width=self.widths[b]))
					drawPos[0] += self.widths[b]
				else:
					# branch
					if block.id == currentBranch['id']:
						# continue creating block
						currentBranch['width'] += self.widths[b]

					
					# finish old branch?
					if not currentBranch['id'] is None:
						if b+1 == len(self.widths) or block.id != currentBranch['id']:
							l = tDepth - (d + 1)
							self.treeTable[d].append(Branch(currentBranch['text'], tuple(drawPos), self.layerHeight, currentBranch['width'], next(self.colorscheme), self.style, l))
							drawPos[0] += currentBranch['width']
					
					if block.id != currentBranch['id']:
						# new branch
						currentBranch['id'] = block.id
						currentBranch['text'] = block.label
						currentBranch['width'] = self.widths[b]
			drawPos[0] = self.pos[0]
			drawPos[1] -= self.layerHeight


	def draw(self):
		turtle.tracer(0, 0)
		turtle.hideturtle()
		for layer in self.treeTable:
			for branch in layer:
				# b : block index
				branch.draw()




