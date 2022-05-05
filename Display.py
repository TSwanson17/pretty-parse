# The graphics

import turtle

class Branch:
	def __init__(self, text, pos, height, width, color, style):
		self.text = text
		self.pos = pos
		self.height = height
		self.width = width
		self.color = color
		self.style = style

	def drawBox(self):
		self.t.setpos(self.pos)
		self.t.fillcolor(self.color)
		self.t.begin_fill()
		for i in range(4):
			if i % 2 == 1:
				self.t.pendown()
				self.t.forward(self.height)
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
		return x - self.t.pos()[0]

	def draw(self):
		self.t = turtle.Turtle()
		self.t.penup()
		self.drawBox()
		self.drawText()

class Leaf(Branch):
	def __init__(self, text, pos, height, width, style):
		Branch.__init__(self, text, pos, height, width, None, style)

	def draw(self):
		self.t = turtle.Turtle()
		self.size = self.drawText()
		self.size *= 2
		return self.size


# This will be the master class for displaying content
class visTree:
	def __init__(self, block_grid):
		self.bGrid = block_grid
		self.color_list = ['#33cc8c', '#804f5f', '#2f4b7c', '#665191', '#a05195', '#d45087', '#f95d6a', '#ff7c43', '#ffa600']
		self.colorscheme = self.colorgen(color_list)

	def colorgen(colors):
		for color in colors:
			yield color

	def draw(self):
		tDepth = len(self.bGrid)
		# each level botom up
		for i in range(tDepth, -1, -1):
			pass


turtle.tracer(0, 0) # stops the drawing animation
style = ("Arial", 20)

b = Branch("Hi", (0, 0), 30, 300, next(colorscheme), style)
b.draw()

b = Branch("Oh", (-200, 0), 30, 200, next(colorscheme), style)
b.draw()

l = Leaf(" leafy ", (0, -30), 30, 200, style)
l.draw()



input("")

