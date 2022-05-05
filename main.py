import os

import NLPserver
import Block


stext = "The quick brown fox jumped over the lazy dog"

parser = NLPserver.parser()
tree = parser.parse(stext)


p = Block.parseTable(tree)
Block.printT(p.block_table)
Block.printT(p.grid)

