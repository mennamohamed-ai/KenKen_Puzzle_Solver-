# backtracking.py
# Backtracking KenKen solver with basic heuristics (no heavy MRV but can be extended)
# Exports: solve_backtracking(grid_obj) -> (solved_bool, time_taken_seconds, iterations)

import time
from typing import Tuple, List
from grid import KenKenGrid
from constraints import check_all_constraints_for_cell, cage_satisfied

def find_empty_cell(grid_mat):
    n = len(grid_mat)
    for r in range(n):
        for c in range(n):
            if grid_mat[r][c] == 0:
                return (r,c)
    return None

def solve_backtracking(grid_obj: KenKenGrid, max_solutions: int = 1) -> Tuple[bool, float, int]:
    """
    Attempt to solve KenKen using backtracking.
    Returns (solved_bool, time_seconds, iterations_count).
    Grid_object is modified in-place on success.
    """
    start = time.time()
    grid = grid_obj.grid
    cages = grid_obj.get_cages()
    n = grid_obj.n
    iterations = 0
    solved_flag = False
    solutions_found = 0

    # Optional improvement: we can precompute cage map for fast lookup
    cell_to_cage = {}
    for cage in cages:
        for cell in cage['cells']:
            cell_to_cage[cell] = cage

    def backtrack():
        nonlocal iterations, solved_flag, solutions_found
        pos = find_empty_cell(grid)
        if pos is None:
            # full grid — verify all cages satisfied (safety)
            ok = True
            for cage in cages:
                vals = [grid[r][c] for (r,c) in cage['cells']]
                if not cage_satisfied(vals, cage['target'], cage['op']):
                    ok = False
                    break
            if ok:
                solved_flag = True
                solutions_found += 1
                return True
            return False

        r,c = pos
        iterations += 1
        for val in range(1, n+1):
            if check_all_constraints_for_cell(grid, cages, r, c, val):
                grid[r][c] = val
                cont = backtrack()
                if cont and solutions_found >= max_solutions:
                    return True
                # backtrack
                grid[r][c] = 0
        return False

    backtrack()
    end = time.time()
    return (solved_flag, end-start, iterations)
