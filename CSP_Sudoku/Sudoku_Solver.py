import math
from copy import deepcopy


class sudoku:
    def __init__(self, puzzle):
        self.board = self.string_to_board_dict(puzzle)
        self.variables = self.board.keys()  # X
        self.Constraints = [
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
            # Squares Constraints (9 in total)
            ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"],
            ["D1", "D2", "D3", "E1", "E2", "E3", "F1", "F2", "F3"],
            ["G1", "G2", "G3", "H1", "H2", "H3", "I1", "I2", "I3"],
            ["A4", "A5", "A6", "B4", "B5", "B6", "C4", "C5", "C6"],
            ["D4", "D5", "D6", "E4", "E5", "E6", "F4", "F5", "F6"],
            ["G4", "G5", "G6", "H4", "H5", "H6", "I4", "I5", "I6"],
            ["A7", "A8", "A9", "B7", "B8", "B9", "C7", "C8", "C9"],
            ["D7", "D8", "D9", "E7", "E8", "E9", "F7", "F8", "F9"],
            ["G7", "G8", "G9", "H7", "H8", "H9", "I7", "I8", "I9"]]  # C
        self.raw_domain = self.raw_Domain()  # D
        self.domain = self.initial_domain()
        self.binary_constraints = self.binary_constraints()

    @staticmethod
    def string_to_board_dict(puzzle):
        board, i = {}, 0
        for row in "ABCDEFGHI":
            for col in "123456789":
                board[row + col] = int(puzzle[i])
                i += 1
        return board

    def binary_constraints(self):
        binary_constraints = []
        for cell in self.variables:
            for constraint in self.Constraints:
                if cell in constraint:
                    for otherCell in constraint:
                        if otherCell != cell and (cell, otherCell) not in binary_constraints and (
                                otherCell, cell) not in binary_constraints:
                            binary_constraints.append((cell, otherCell))
        return binary_constraints

    def raw_Domain(self):
        Domain = {}
        for var in self.variables:
            if self.board[var] != 0:
                Domain[var] = [self.board[var]]
            else:
                Domain[var] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        return Domain

    def initial_domain(self):
        domain = self.raw_domain
        for arc in self.binary_constraints():
            x, y = self.board[arc[0]], self.board[arc[1]]
            if x != 0 and x in domain[arc[1]]:
                domain[arc[1]].remove(x)
            if y != 0 and y in domain[arc[0]]:
                domain[arc[0]].remove(y)
        return domain


def Display_Board(board):
    Board = ""
    line = "----------------------------------------------\n"
    Board += line
    for row in "ABCDEFGHI":
        Board += "|"
        for col in "123456789":
            if board[row + col] != 0:
                Board += ("%3d" % board[row + col]) + " |"
            else:
                Board += ("%3c" % ' ') + " |"
        Board += "\n" + line
    print(Board)


def AC3(csp):  # Returns False if an inconsistency is found, True otherwise
    queue = csp.binary_constraints

    while len(queue) > 0:
        (Xi, Xj) = queue.pop(0)
        if Revise(csp, Xi, Xj):
            if len(csp.domain[Xi]) == 0:
                return False

            for Xk in nbd(csp, Xi):
                if Xk != Xj and Xk != Xi:
                    queue.append((Xk, Xi))
    return True


def Revise(csp, X, Y):  # returns true iff we revise the domain of Xi
    revised = False

    for x in csp.domain[X]:
        if csp.domain[Y] == [x]:
            csp.domain[X].remove(x)
            revised = True

    for y in csp.domain[Y]:
        if csp.domain[X] == [y]:
            csp.domain[Y].remove(y)
            revised = True
    return revised


def nbd(csp, cell):  # Returns Neighbourhood of the Cell with The exception
    NBD = []
    for constraint in csp.Constraints:
        if cell in constraint:
            for nbr in constraint:
                if nbr != cell and nbr not in NBD:
                    NBD.append(nbr)
    return NBD


def Alldiff(board, variables):
    n = len(variables)
    for i in range(n):
        if board[variables[i]] != 0:
            for j in range(i + 1, n):
                if board[variables[j]] != 0:
                    if board[variables[i]] == board[variables[j]]:
                        return False
    return True


def consistent(csp, board):
    Consistent = True
    for constraint in csp.Constraints:
        Consistent = Consistent and Alldiff(board, constraint)
    return Consistent


def GetFreecells(board):
    FreeCells = []
    for row in "ABCDEFGHI":
        for col in "123456789":
            if board[row + col] == 0:
                FreeCells.append(row + col)
    return FreeCells


def forwardChecking(csp, Xi, value):
    # Keeps track of remaining legal values for the unassigned variables
    # Terminate when any variable has no legal values
    Freecells, Consistent = GetFreecells(csp.board), consistent(csp, csp.board)
    if Xi in Freecells:
        csp.board[Xi] = value
        Freecells.remove(Xi)

    for x in Freecells:
        for d in csp.domain[x]:
            csp.board[x] = d
            if not consistent(csp, csp.board):
                csp.domain[x].remove(d)
            if len(csp.domain[x]) == 0:
                return False

        if len(csp.domain[x]) == 1:
            csp.board[x] = csp.domain[x][0]
        else:
            csp.board[x] = 0
    return True


def Order_Domain_values(csp, Xi):
    # TODO
    Order, list = {}, []
    for val in csp.domain[Xi]:
        Order[val] = 0
        for cell in nbd(csp, Xi):
            if val in csp.domain[cell]:
                Order[val] += 1
    for x in Order:
        list.append(Order[x])


def BTS(csp):  # BackTrackingSreach
    # Returns a solution or failure
    return Backtrack(csp)


def Backtrack(csp):
    FreeCells = GetFreecells(csp.board)

    if len(FreeCells) == 0:  # => Assignment Complete
        return csp.board, ': BTS'

    # Minimum Domain Variable (MRV Heuristic)
    maxDomain, Xi = math.inf, None
    for FreeCell in FreeCells:
        if len(csp.domain[FreeCell]) < maxDomain:
            maxDomain, Xi = len(csp.domain[FreeCell]), FreeCell

    # TODO Order Domain Values
    for value in csp.domain[Xi]:  # Storing board for retoring if fail
        Board, Domain = deepcopy(csp.board), deepcopy(csp.domain)
        csp.board[Xi] = value
        if consistent(csp, csp.board):
            inference = forwardChecking(csp, Xi, value)
            if inference:
                for v in GetFreecells(csp.board):
                    if len(csp.domain[v]) == 1:
                        csp.board[v] = csp.domain[v][0]

                result = Backtrack(csp)
                if result != "Failure":
                    return result

            csp.board, csp.domain = Board, Domain  # Restoring and trying New value

    return "Failure"
