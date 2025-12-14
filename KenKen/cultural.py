import random
import time
import copy
from typing import List, Tuple, Dict, Any
from grid import KenKenGrid
from constraints import cage_satisfied

class CulturalAlgorithm:
    def __init__(self, grid_obj: KenKenGrid, pop_size: int = 200, elite_fraction: float = 0.1, max_gen: int = 1000):
        self.grid_obj = grid_obj
        self.n = grid_obj.n
        self.cages = grid_obj.get_cages()
        self.pop_size = max(20, pop_size)
        self.elite_fraction = max(0.05, min(0.4, elite_fraction))
        self.max_gen = max(10, max_gen)
        # belief: probability matrix per cell for values 1..n, initially uniform
        self.belief = [[[1.0/self.n for _ in range(self.n)] for _ in range(self.n)] for _ in range(self.n)]
        self.population: List[List[List[int]]] = []

    def random_individual(self):
        # Each row is a permutation to satisfy row uniqueness
        nums = list(range(1, self.n+1))
        grid = []
        for _ in range(self.n):
            row = nums[:]
            random.shuffle(row)
            grid.append(row)
        return grid

    def fitness(self, grid: List[List[int]]) -> int:
        # count violations: column duplicates + cage violations
        violations = 0
        # column duplicates
        for c in range(self.n):
            col = [grid[r][c] for r in range(self.n)]
            violations += (self.n - len(set(col)))
        # cage checks
        for cage in self.cages:
            vals = [grid[r][c] for (r,c) in cage['cells']]
            # if any zero (shouldn't happen with our representation), skip
            if any(v == 0 for v in vals):
                violations += 1
            else:
                if not cage_satisfied(vals, cage['target'], cage['op']):
                    violations += 1
        return violations

    def update_belief(self, elites: List[List[List[int]]], alpha: float = 0.3):
        # Decay old belief slightly
        for r in range(self.n):
            for c in range(self.n):
                for v in range(self.n):
                    self.belief[r][c][v] *= (1 - alpha)
        # reinforce seen values in elites
        if len(elites) == 0:
            return
        for g in elites:
            for r in range(self.n):
                for c in range(self.n):
                    val = g[r][c]
                    self.belief[r][c][val-1] += alpha / len(elites)
        # normalize
        for r in range(self.n):
            for c in range(self.n):
                s = sum(self.belief[r][c])
                if s <= 0:
                    self.belief[r][c] = [1.0/self.n]*self.n
                else:
                    self.belief[r][c] = [x/s for x in self.belief[r][c]]

   )
              

    def crossover(self, a: List[List[int]], b: List[List[int]]):
        # row-wise crossover (swap rows with probability 0.5)
        child = [row[:] for row in a]
        for r in range(self.n):
            if random.random() < 0.5:
                child[r] = b[r][:]
        return child

    def mutate(self, g: List[List[int]], mutation_rate: float = 0.15):
        # swap two positions in a row sometimes
        grid = [row[:] for row in g]
        for r in range(self.n):
            if random.random() < mutation_rate:
                i,j = random.sample(range(self.n), 2)
                grid[r][i], grid[r][j] = grid[r][j], grid[r][i]
        # guided resampling from belief with small prob
        for r in range(self.n):
            for c in range(self.n):
                if random.random() < 0.02:
                    probs = self.belief[r][c]
                    grid[r][c] = random.choices(range(1, self.n+1), weights=probs, k=1)[0]
            # repair row
            missing = [v for v in range(1, self.n+1) if v not in grid[r]]
            seen = set()
            for i,v in enumerate(grid[r]):
                if v in seen:
                    grid[r][i] = missing.pop()
                else:
                    seen.add(v)
        return grid

    def solve(self, timeout_seconds: float = 5.0):
        start = time.time()
        # init population
        self.population = [self.random_individual() for _ in range(self.pop_size)]
        best = None
        best_fit = float('inf')
        history = []
        iterations = 0

        for gen in range(self.max_gen):
            scored = [(self.fitness(g), g) for g in self.population]
            scored.sort(key=lambda x: x[0])
            iterations += 1
            if scored[0][0] < best_fit:
                best_fit = scored[0][0]
                best = copy.deepcopy(scored[0][1])
            history.append(best_fit)
            # success condition
            if best_fit == 0:
                # return as KenKenGrid
                out_grid = KenKenGrid(self.n)
                out_grid.from_matrix(best)
                end = time.time()
                return True, out_grid, end - start, iterations

            # elites
            k = max(1, int(self.elite_fraction * self.pop_size))
            elites = [g for _,g in scored[:k]]
            # update belief
            self.update_belief(elites)
            # new population: carry elites
            newpop = elites[:]
            while len(newpop) < self.pop_size:
                # selection tournament
                a = min(random.sample(scored, 3), key=lambda x: x[0])[1]
                b = min(random.sample(scored, 3), key=lambda x: x[0])[1]
                child = self.crossover(a,b)
                child = self.mutate(child)
                newpop.append(child)
            self.population = newpop

            if time.time() - start > timeout_seconds:
                break

        # finished without perfect solution: return best found
        if best is not None:
            out_grid = KenKenGrid(self.n)
            out_grid.from_matrix(best)
            end = time.time()
            return False, out_grid, end - start, iterations
        end = time.time()
        return False, None, end - start, iterations

