import math
import sys
import time

import numpy as np
from BaseAI import BaseAI


class PlayerAI(BaseAI):
    max_ctr, min_ctr = 0, 0
    # Time Limit Before Losing
    time_limit, allowance, in_time = 0.2, 0.005, None
    # increasing limit to not fail execution
    sys.setrecursionlimit(0x100000)

    def getMove(self, grid):  # minimax
        self.max_ctr, self.min_ctr = 0, 0
        best_move, best_utility = None, -math.inf
        for move in grid.getAvailableMoves():
            self.in_time = time.perf_counter()
            new_grid = grid.clone()
            new_grid.move(move)
            for child in self.get_children_min(new_grid):
                max_util, α, β = self.maximize(child, -math.inf, math.inf)
                if max_util > best_utility:
                    best_move, best_utility = move, max_util
        print('Max_util :', max_util)
        return best_move

    def maximize(self, grid, α, β):
        self.max_ctr += 1
        if self.too_late(grid) or not grid.canMove():  # or self.max_ctr==7
            return self.eval_util(grid), α, β

        max_child, max_util, child_ctr = None, -math.inf, 0
        for (move, child) in self.get_children_max(grid):
            util, α, β = self.minimize(child, α, β)
            # util += self.movement(child)
            if util > max_util:
                max_child, max_util = child, util
            α = max(max_util, α)  # child_ctr += 1
            if max_util >= β:  # print("prune", len(self.get_children_max(grid)) - child_ctr, "from max ", self.max_ctr)
                break
        # print('max_ctr: ',self.max_ctr,' max util: ', max_util, ' α = ', α, ' β = ', β)
        return max_util, α, β

    def minimize(self, grid, α, β):
        self.min_ctr += 1
        if self.too_late(grid) or not grid.canMove():  # or self.max_ctr == 7
            return self.eval_util(grid), α, β

        min_child, min_util, child_ctr = None, math.inf, 0
        for child in self.get_children_min(grid):
            util, α, β = self.maximize(child, α, β)
            if util < min_util:
                min_child, min_util = child, util
            β = min(min_util, β)  # child_ctr += 1
            if min_util <= α:  # print("prune", len(self.get_children_min(grid)) - child_ctr, "from min", self.min_ctr)
                break
        # print('min_ctr: ',self.min_ctr,' min_util: ',min_util, ' α = ',α, ' β = ',β)
        return min_util, α, β

    @staticmethod
    def get_children_max(grid):
        children, moves = [], []
        for move in grid.getAvailableMoves():
            new_grid = grid.clone()
            new_grid.move(move)
            children.append((move, new_grid))
        return children

    @staticmethod
    def get_children_min(grid):
        children = []
        for cell in grid.getAvailableCells():
            new_grid = grid.clone()
            new_grid.insertTile(cell, 2)
            children.append(new_grid)
            new_grid = grid.clone()
            new_grid.insertTile(cell, 4)
            children.append(new_grid)

        return children

    def nbd(self, pos, grid):
        nbd = []
        points = [(pos[0], pos[1] - 1), (pos[0], pos[1] + 1), (pos[0] - 1, pos[1]), (pos[0] + 1, pos[1])]
        for (x, y) in points:
            if x in range(4) and y in range(4):
                nbd.append(grid.map[x][y])
        return nbd

    def log_score(self, grid):
        score = 0
        for row in grid.map:
            for ele in row:
                if ele != 0:
                    n = math.log(ele, 2)
                    score += (n - 1) * (2 ** n)
        return (math.log(max(score, 1))/2)

    def movement(self, grid):
        util = 0
        for (move, child) in self.get_children_max(grid):
            for x in range(grid.size):
                for y in range(grid.size):
                    if child.getMaxTile() >= 64:
                        if grid.map[x][y] == child.map[x][y]:
                            util += 1
        return util

    def eval_util(self, grid):
        util, All_Tiles = 0, []
        [[All_Tiles.append(grid.map[x][y]) for y in range(grid.size)] for x in range(grid.size)]
        All_Tiles.sort(reverse=True)  # Maxtile is first

        util += len(grid.getAvailableCells()) * self.log_score(grid)  # 20-50
        for x in range(grid.size):
            for y in range(grid.size):
                cell = grid.map[x][y]
                if cell == All_Tiles[0]:
                    # corners (-10 t0 10)
                    if (x, y) in [(0, 0), (0, 3), (3, 0), (3, 3)]:  # corners
                        util += 2*math.log(cell, 2)
                    # Centers
                    elif (x, y) in [(1, 1), (1, 2), (2, 1), (2, 2)]:  # Centers
                        util += -1000*math.log(cell, 2)
                # similar cells to merge
                # if cell in self.nbd((x, y), grid):
                # util += 0#10*math.log(max(1,cell),2)
                # monotonicity
                for i in range(5):
                    if All_Tiles[i] == cell:
                        if All_Tiles[i] in self.nbd((x, y), grid):
                            util += math.log(max(1,cell),2)
        for i in range(5):
            if All_Tiles[i] != 0:
                util += -self.manh_dist(grid, All_Tiles[i], All_Tiles[1 + i])
        return util

    def manh_dist(self, grid, val1, val2):
        pos1, pos2 = np.where(grid.map == val1), np.where(grid.map == val2)
        (x1, y1), (x2, y2) = (pos1[0][0], pos1[1][0]), (pos2[0][0], pos2[1][0])
        dist = (abs(x2 - x1) + abs(y2 - y1))*math.log(grid.map[x1][y1])/10
        return dist

    def manh_util(self, grid):
        util, All_Tiles = 0, []
        [[All_Tiles.append(grid.map[x][y]) for y in range(grid.size)] for x in range(grid.size)]
        All_Tiles.sort(reverse=True)

        return util

    def too_late(self, grid):
        curr_time = time.perf_counter()
        divider = max(1, len(self.get_children_max(grid)), len(self.get_children_min(grid)))
        valid_time = self.time_limit / divider - self.allowance
        # print("time", curr_time - self.in_time, "valid time", valid_time)
        # give every move equal time to evaluate further states
        if curr_time - self.in_time > valid_time:
            # print("time exceeded")
            return True
        else:
            # print("Succeeded")
            return False
