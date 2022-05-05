import os

import NLPserver
import Block
import Display


stext = "The quick brown fox jumped over the lazy dog and we ran"

parser = NLPserver.parser()
tree = parser.parse(stext)


p = Block.parseTable(tree, True)
#Block.printT(p.block_table)
#Block.printT(p.grid)




d = Display.visTree((-400, 400), p.grid)
d.create()
d.draw()

input('')