# grid.py
# KenKen grid and cage representation
# Author: Generated for project (Helwan University AI310/CS361)
# Contains KenKenGrid class used by solvers and GUI.

from typing import List, Tuple, Optional, Dict, Any
import copy

Cell = Tuple[int, int]
Cage = Dict[str, Any]  # {'cells': [(r,c)...], 'op': '+', 'target': 6}

class KenKenGrid:
    """
    Represent an N x N KenKen puzzle:
    - grid: NxN integers (0 means empty)
    - cages: list of cage dictionaries: {'cells': [...], 'op': '+', 'target': int}
    """

    def __init__(self, n: int):
        if n <= 0:
            raise ValueError("Grid size must be positive")
        self.n = n
        self.grid: List[List[int]] = [[0 for _ in range(n)] for _ in range(n)]
        self.cages: List[Cage] = []

    def reset(self):
        self.grid = [[0 for _ in range(self.n)] for _ in range(self.n)]
        self.cages = []

    def add_cage(self, cells: List[Cell], op: str, target: int):
        # Basic validation
        for (r, c) in cells:
            if not (0 <= r < self.n and 0 <= c < self.n):
                raise ValueError(f"Cell {(r,c)} out of bounds for grid size {self.n}")
        if op not in ['+', '-', '*', '/', '=']:
            raise ValueError("Operation must be one of + - * / =")
        self.cages.append({'cells': cells, 'op': op, 'target': target})

    def get_cages(self) -> List[Cage]:
        return self.cages

    def get_cell(self, r: int, c: int) -> int:
        return self.grid[r][c]

    def set_cell(self, r: int, c: int, value: int):
        if not (0 <= r < self.n and 0 <= c < self.n):
            raise IndexError("Cell out of range")
        self.grid[r][c] = value

    def to_matrix(self) -> List[List[int]]:
        return copy.deepcopy(self.grid)

    def from_matrix(self, mat: List[List[int]]):
        if len(mat) != self.n or any(len(row) != self.n for row in mat):
            raise ValueError("Matrix dimensions do not match grid size")
        self.grid = [row[:] for row in mat]

    def is_complete(self) -> bool:
        for r in range(self.n):
            for c in range(self.n):
                if self.grid[r][c] == 0:
                    return False
        return True
