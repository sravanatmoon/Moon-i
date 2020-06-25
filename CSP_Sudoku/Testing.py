from CSP_Sudoku.Sudoku_Solver import sudoku, Display_Board, GetFreecells
import numpy as np


def Constraints():
    constraints = [
        # Row Constraints (9 in total)
        ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9"],
        ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9"],
        ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"],
        ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9"],
        ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9"],
        ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9"],
        ["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"],
        ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9"],
        ["I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9"],
        # Col Constraints (9 in total)
        ["A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1", "I1"],
        ["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2", "I2"],
        ["A3", "B3", "C3", "D3", "E3", "F3", "G3", "H3", "I3"],
        ["A4", "B4", "C4", "D4", "E4", "F4", "G4", "H4", "I4"],
        ["A5", "B5", "C5", "D5", "E5", "F5", "G5", "H5", "I5"],
        ["A6", "B6", "C6", "D6", "E6", "F6", "G6", "H6", "I6"],
        ["A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7", "I7"],
        ["A8", "B8", "C8", "D8", "E8", "F8", "G8", "H8", "I8"],
        ["A9", "B9", "C9", "D9", "E9", "F9", "G9", "H9", "I9"],
        # Squares constraints (9 in total)
        ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"],
        ["D1", "D2", "D3", "E1", "E2", "E3", "F1", "F2", "F3"],
        ["G1", "G2", "G3", "H1", "H2", "H3", "I1", "I2", "I3"],
        ["A4", "A5", "A6", "B4", "B5", "B6", "C4", "C5", "C6"],
        ["D4", "D5", "D6", "E4", "E5", "E6", "F4", "F5", "F6"],
        ["G4", "G5", "G6", "H4", "H5", "H6", "I4", "I5", "I6"],
        ["A7", "A8", "A9", "B7", "B8", "B9", "C7", "C8", "C9"],
        ["D7", "D8", "D9", "E7", "E8", "E9", "F7", "F8", "F9"],
        ["G7", "G8", "G9", "H7", "H8", "H9", "I7", "I8", "I9"]]
    return constraints


board, i, puzzle = {}, 0, "003020600900305001001806400008102900700000008006708200002609500800203009005010300"
print(len(puzzle))
for row in "ABCDEFGHI":
    for col in "123456789":
        board[row + col] = int(puzzle[i])
        i += 1

variables = board.keys()
domain = \
    {var: [board[var]] if board[var] != 0 else [1, 2, 3, 4, 5, 6, 7, 8, 9] for var in variables}

NBD = {}
for cell in variables:
    NBD[cell] = []
    for constraint in Constraints():
        if cell in constraint:
            for otherCell in constraint:
                if otherCell != cell and otherCell not in NBD[cell]:
                    NBD[cell].append(otherCell)

# print(NBD)
i = 0
'''print('Initial Board')
Display_Board(board)
print(domain)
while len(GetFreecells(board)) > 0:
    print(f'Iteration : {i}')
    for cell in variables:
        for nbr in NBD[cell]:
            if board[nbr] != 0 and board[nbr] in domain[cell]:
                domain[cell].remove(board[nbr])
    Rem_Dom = {}
    for cell in GetFreecells(board):
        if len(domain[cell]) == 1:
            print(f'{cell}', end=',')
            board[cell] = domain[cell][0]
        else:
            Rem_Dom[cell] = domain[cell]
    print('\n')
    Display_Board(board)
    print('Domain', domain)
    """for cell in GetFreecells(board):
        if len(Rem_Dom[cell]) == 1:
            print(f"{cell}")"""
    print(f'Domain left after {i}th Iteration', Rem_Dom)
    i += 1'''


def forward_check(self, var, val, assignment):
    "Do forward checking (current domain reduction) for this assignment."
    if self.curr_domains:
        # Restore prunings from previous value of var
        for (B, b) in self.pruned[var]:
            self.curr_domains[B].append(b)
        self.pruned[var] = []
        # Prune any other B=b assignement that conflict with var=val
        for B in self.neighbors[var]:
            if B not in assignment:
                for b in self.curr_domains[B][:]:
                    if not self.constraints(var, val, B, b):
                        self.curr_domains[B].remove(b)
                        self.pruned[var].append((B, b))


with open('Sudoku_start.txt', mode='r') as f:  # The file will be f from now on.
    lines = np.array(f.read().split('\n'))
    y = 0
    for line in lines:
        x = str(line)
        ctr = 0
        for i in x:
            if i == '0':
                ctr += 1
        print(y, ctr)
        y += 1


def AC3(csp):  # Returns False if an inconsistency is found, True otherwise
    queue = csp.binary_constraints
    while len(queue) > 0:
        (Xi, Xj) = queue.pop(0)
        if Revise(csp, Xi, Xj):
            if len(csp.domain[Xi]) == 1:
                csp.board[Xi] = csp.domain[Xi][0]
                print(f'Assigned {csp.domain[Xi][0]} to {Xi}')
            elif len(csp.domain[Xi]) == 0:
                print(f'False {Xi}')
                return False
            print("Appening")
            for Xk in nbd(csp, Xi):
                if Xk != Xj and Xk != Xi:
                    queue.append((Xk, Xi))
                    print(f'appened {Xk} to {Xi}')
    return True


def Revise(csp, X, Y):  # returns true iff we revise the domain of Xi
    revised = False
    print(X, Y, ':', csp.domain[X], csp.domain[Y])
    for x in csp.domain[X]:
        if csp.domain[Y] == [x]:
            csp.board[Y] = x
            csp.domain[X].remove(x)
            revised = True
    for y in csp.domain[Y]:
        if csp.domain[X] == [y]:
            csp.board[X] = y
            csp.domain[Y].remove(y)
            revised = True
    return revised