from CSP_Sudoku.Sudoku_Solver import AC3, sudoku, BTS
import numpy as np


# ----------------------------------------------------------------------------------#
#        Solves a sudoku passed as a string from command line.                      #
#        This is the Driver file for Project CSP in the course of                   #
#        Artificial Intelligence offered by Columbia University  through edX        #
# __________________________________________________________________________________#

def Lines():  # Give the lines as array(1,81)
    with open('Sudoku_start.txt', mode='r') as f:  # The file will be f from now on.
        lines = np.array(f.read().split('\n'))
        line = lines[5]
    return line


def solve(csp):
    for key in csp.variables:
        if len(csp.domain[key]) == 1:
            csp.board[key] = csp.domain[key][0]
        if csp.board[key] == 0:
            return BTS(csp)
    return csp.board, ': AC3'


def String(Solution):
    if Solution != "Failure":
        sol = ""
        for row in "ABCDEFGHI":
            for col in "123456789":
                sol += str(Solution[0][row + col])
        sol += Solution[1]
    else:

        sol = "Failed"
    return sol


def start():
    with open("output.txt", "w") as output:
        for line in Lines():
            Sudoku = sudoku(line)
            if AC3(Sudoku):
                Solution = solve(Sudoku)
            else:
                Solution = BTS(Sudoku)
            output.write(String(Solution) + '\n')


if __name__ == "__main__":
    start()
