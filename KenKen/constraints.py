# constraints.py
# Constraint checking utilities for KenKen puzzle
# Functions:
# - valid_in_row_col: uniqueness in row/col
# - cage_valid_partial: prune partial assignments per cage
# - cage_satisfied: check fully-filled cage
# - check_all_constraints_for_cell: wrapper used by solvers

from typing import List, Tuple, Dict, Any
from math import prod

Cell = Tuple[int,int]
Cage = Dict[str,Any]

def valid_in_row_col(grid: List[List[int]], r: int, c: int, value: int) -> bool:
    n = len(grid)
    # row
    for j in range(n):
        if grid[r][j] == value:
            return False
    # column
    for i in range(n):
        if grid[i][c] == value:
            return False
    return True

def cage_valid_partial(values: List[int], target: int, op: str, N:int) -> bool:
    """
    Given a list of values for cells in the cage (zeros allowed for empty),
    decide if the partial assignment can still lead to a valid solution.
    Conservative pruning only: we avoid false negatives.
    """
    filled = [v for v in values if v != 0]
    if not filled:
        return True
    if op == '+':
        s = sum(filled)
        if s > target:
            return False
        # even if equals target and not all filled -> still invalid
        if s == target and len(filled) < len(values):
            return False
        return True
    if op == '*':
        p = 1
        for v in filled:
            p *= v
        if p > target:
            return False
        if p == target and len(filled) < len(values):
            return False
        return True
    if op == '-':
        # subtraction or difference usually for 2 cells: only check when both present
        if len(filled) == len(values):
            a,b = filled[0], filled[1]
            return abs(a-b) == target
        return True
    if op == '/':
        # division usually for 2 cells: check when both present
        if len(filled) == len(values):
            a,b = filled[0], filled[1]
            if b != 0 and a / b == target:
                return True
            if a != 0 and b / a == target:
                return True
            return False
        return True
    if op == '=':
        # single-cell cage
        if len(filled) == 0:
            return True
        return filled[0] == target
    return True

def cage_satisfied(values: List[int], target: int, op: str) -> bool:
    """Assumes values list has no zeros (fully filled)"""
    if op == '+':
        return sum(values) == target
    if op == '*':
        p = 1
        for v in values:
            p *= v
        return p == target
    if op == '-':
        if len(values) != 2:
            return False
        a,b = values
        return abs(a-b) == target
    if op == '/':
        if len(values) != 2:
            return False
        a,b = values
        # check integer division target (but allow floats)
        if b != 0 and a / b == target:
            return True
        if a != 0 and b / a == target:
            return True
        return False
    if op == '=':
        return values[0] == target
    return False

def check_all_constraints_for_cell(grid: List[List[int]], cages: List[Cage], r: int, c: int, value: int) -> bool:
    """
    Check if putting 'value' at (r,c) is consistent with:
    - row uniqueness
    - column uniqueness
    - cage partial validity
    """
    n = len(grid)
    # row and col
    for j in range(n):
        if grid[r][j] == value:
            return False
    for i in range(n):
        if grid[i][c] == value:
            return False
    # cage checks
    # find cage containing (r,c)
    for cage in cages:
        if (r,c) in cage['cells']:
            # build values for cage after hypothetical placement
            vals = []
            for (rr,cc) in cage['cells']:
                if rr == r and cc == c:
                    vals.append(value)
                else:
                    vals.append(grid[rr][cc])
            if not cage_valid_partial(vals, cage['target'], cage['op'], n):
                return False
            # if fully filled, ensure exact satisfaction
            if all(v != 0 for v in vals):
                if not cage_satisfied(vals, cage['target'], cage['op']):
                    return False
            break
    return True
