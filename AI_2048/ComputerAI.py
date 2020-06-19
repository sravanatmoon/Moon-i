import sys
from random import randint

from BaseAI import BaseAI

sys.path.append(".")


class ComputerAI(BaseAI):
    def getMove(self, grid):
        cells = grid.getAvailableCells()

        return cells[randint(0, len(cells) - 1)] if cells else None
