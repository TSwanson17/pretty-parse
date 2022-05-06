import os

import NLPserver
import Block
import Display


stext = "The quick brown fox jumped over the lazy dog"


def checkExit(c):
	if c == 'n' or c == 'no' or c == 'q' or c == 'quit' or c == 'exit':
		return True
	else:
		return False


parser = NLPserver.parser()

parser.start()
while True:
	# Input
	text = input("\nInput a sentence to parse: \n").strip()
	if text == None:
		text = stext
	if len(text) < 5:
		if checkExit(text):
			break
		else:
			print("'{}' is too short, using default text".format(text))
			text = stext

	# Parse and visualize
	tree = parser.parse(text)
	p = Block.parseTable(tree, False)
	d = Display.visTree((-400, 400), p.grid)
	d.create()
	d.draw()

	# Continue:
	c = input("\nContinue?  ").lower()
	if checkExit(c):
		break
parser.stop()
