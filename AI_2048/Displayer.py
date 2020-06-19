import platform

from BaseDisplayer import BaseDisplayer

colorMap = {
    0: 97,
    2: 40,
    4: 100,
    8: 47,
    16: 107,
    32: 46,
    64: 106,
    128: 44,
    256: 104,
    512: 42,
    1024: 102,
    2048: 43,
    4096: 103,
    8192: 45,
    1634: 105,
    3278: 41,
    6556: 101,
}

cTemp = "\x1b[%dm%7s\x1b[0m "


class Displayer(BaseDisplayer):
    def __init__(self):
        super().__init__()
        if "Windows" == platform.system():
            self.display = self.winDisplay
        else:
            self.display = self.unixDisplay

    def display(self, grid):
        pass

    @staticmethod
    def winDisplay(grid):
        for i in range(grid.size):
            for j in range(grid.size):
                print("%6d  " % grid.map[i][j], end="")
            print("")
        print("")

    @staticmethod
    def unixDisplay(grid):
        for i in range(3 * grid.size):
            for j in range(grid.size):
                v = grid.map[int(i / 3)][j]

                if i % 3 == 1:
                    string = str(v).center(7, " ")
                else:
                    string = " "

                print(cTemp % (colorMap[v], string), end="")
            print("")

            if i % 3 == 2:
                print("")
