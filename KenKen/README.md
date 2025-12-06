# 🧩 KenKen Puzzle Solver

An intelligent KenKen (KenDoku) puzzle solver implemented using **Backtracking Search Algorithm** and **Cultural Algorithm**. This project demonstrates the application of constraint satisfaction and evolutionary computation techniques to solve mathematical grid-based puzzles.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [KenKen Puzzle Rules](#kenken-puzzle-rules)
- [Algorithms](#algorithms)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Performance Metrics](#performance-metrics)
- [Examples](#examples)
- [Technical Details](#technical-details)
- [Future Improvements](#future-improvements)
- [License](#license)

## 🎯 Overview

KenKen is a mathematical and logical grid-based puzzle that combines aspects of Sudoku and arithmetic operations. The goal is to fill an N×N grid with digits (1 to N) such that:
- Each row and column contains unique numbers
- Each outlined region (cage) satisfies a specified arithmetic operation with a target number

This solver implements two distinct algorithmic approaches:
1. **Backtracking Search Algorithm** - A systematic constraint satisfaction approach
2. **Cultural Algorithm** - An evolutionary computation approach with belief space

## ✨ Features

- 🎨 **User-Friendly GUI** - Intuitive Tkinter-based interface
- 🔄 **Dual Algorithm Support** - Choose between Backtracking or Cultural Algorithm
- 📊 **Performance Metrics** - Real-time display of solving time and iterations/generations
- 🎯 **Flexible Grid Sizes** - Support for any N×N grid size
- 🧮 **Complete Operation Support** - Addition (+), Subtraction (-), Multiplication (*), Division (/), and Single-cell (=)
- 🔍 **Constraint Validation** - Comprehensive constraint checking for row/column uniqueness and cage operations
- 📈 **Visual Feedback** - Display solved puzzles with metrics

## 📖 KenKen Puzzle Rules

1. **Digit Placement**: Fill the grid with digits from 1 to N
2. **Row/Column Uniqueness**: Each row and column must contain unique digits
3. **Cage Operations**: Digits within each cage must satisfy the specified arithmetic operation to achieve the target number
   - **Addition (+)**: Sum of all digits in the cage equals the target
   - **Subtraction (-)**: Absolute difference between two digits equals the target
   - **Multiplication (*)**: Product of all digits in the cage equals the target
   - **Division (/)**: Quotient of two digits (either direction) equals the target
   - **Single-cell (=)**: The cell value equals the target

## 🤖 Algorithms

### 1. Backtracking Search Algorithm

A systematic depth-first search algorithm that:
- Explores the solution space by assigning values to cells
- Backtracks when constraints are violated
- Uses constraint propagation to prune invalid branches
- Guarantees finding a solution if one exists

**Key Features:**
- Constraint checking before assignment
- Efficient backtracking mechanism
- Iteration counting for performance analysis

### 2. Cultural Algorithm

An evolutionary computation approach inspired by cultural evolution:
- **Population-based**: Maintains a population of candidate solutions
- **Belief Space**: Tracks probability distributions for each cell value based on elite solutions
- **Genetic Operators**: 
  - Crossover: Row-wise recombination
  - Mutation: Guided by belief space and random swaps
- **Selection**: Tournament selection for parent selection
- **Elite Preservation**: Maintains best solutions across generations

**Key Features:**
- Belief space updates from elite solutions
- Row permutation representation (ensures row uniqueness)
- Fitness function based on column uniqueness and cage satisfaction
- Timeout mechanism for practical usage

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- tkinter (usually included with Python)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/kenken-solver.git
cd kenken-solver
```

2. No additional dependencies required! The project uses only Python standard library.

## 💻 Usage

### Running the Application

```bash
python main.py
```

### Using the GUI

1. **Set Grid Size**: Enter the desired grid size (N) and click "Apply Size"
2. **Add Cages**: 
   - Format: `row1,col1,row2,col2,...;operation;target`
   - Example: `0,0,0,1;+;5` (cells at (0,0) and (0,1) with addition targeting 5)
   - Click "Add Cage" to add the cage
3. **Select Algorithm**: Choose between "Backtracking" or "Cultural" from the dropdown
4. **Solve**: Click "Solve" to find the solution
5. **View Results**: The solved grid and performance metrics will be displayed

### Cage Input Format

```
row1,col1,row2,col2,...;operation;target
```

**Operations:**
- `+` for addition
- `-` for subtraction
- `*` for multiplication
- `/` for division
- `=` for single-cell (target value)

**Examples:**
- `0,0,0,1;+;5` - Two cells in row 0, columns 0 and 1, sum to 5
- `1,0,1,1,1,2;*;12` - Three cells in row 1, product equals 12
- `2,0,2,1;-;2` - Two cells in row 2, absolute difference is 2
- `3,0;=;4` - Single cell at (3,0) equals 4

## 📁 Project Structure

```
kenken-solver/
│
├── main.py              # Entry point - launches GUI
├── gui.py               # Tkinter GUI implementation
├── grid.py              # KenKenGrid class - grid and cage representation
├── backtracking.py      # Backtracking solver implementation
├── cultural.py          # Cultural Algorithm implementation
├── constraints.py       # Constraint checking utilities
└── README.md            # This file
```

### File Descriptions

- **`main.py`**: Application entry point that initializes and runs the GUI
- **`gui.py`**: Complete GUI implementation with grid display, cage input, and algorithm selection
- **`grid.py`**: Core data structure for representing KenKen puzzles (grid and cages)
- **`backtracking.py`**: Backtracking search algorithm with constraint checking
- **`cultural.py`**: Cultural Algorithm with belief space, genetic operators, and evolution
- **`constraints.py`**: Utility functions for validating row/column uniqueness and cage operations

## 📊 Performance Metrics

The solver displays the following metrics:

### Backtracking Algorithm
- **Time**: Execution time in seconds
- **Iterations**: Number of backtracking steps

### Cultural Algorithm
- **Time**: Execution time in seconds
- **Generations**: Number of evolutionary generations
- **Status**: Whether a perfect solution was found or best-found solution

## 🎮 Examples

### Example 1: 4×4 Grid

**Cages:**
```
0,0,0,1;+;5
0,2,0,3;*;6
1,0,1,1;-;1
1,2,1,3;/;2
2,0,2,1;+;6
2,2,2,3;*;4
3,0,3,1;-;1
3,2,3,3;+;5
```

### Example 2: Simple 3×3 Grid

**Cages:**
```
0,0,0,1;+;5
0,2;=;3
1,0,1,1;*;2
1,2;=;1
2,0,2,1;+;4
2,2;=;2
```

## 🔧 Technical Details

### Constraint Checking

The solver implements comprehensive constraint validation:

1. **Row/Column Uniqueness**: Ensures no duplicate values in rows or columns
2. **Cage Partial Validation**: Checks if partial cage assignments can lead to valid solutions
3. **Cage Complete Validation**: Verifies fully-filled cages satisfy their operations

### Cultural Algorithm Parameters

- **Population Size**: 200 (default)
- **Elite Fraction**: 0.12 (12% of population)
- **Max Generations**: 1000
- **Timeout**: 8 seconds (default)
- **Mutation Rate**: 0.15
- **Belief Update Alpha**: 0.3

### Data Structures

- **Grid**: 2D list of integers (0 = empty, 1-N = filled)
- **Cages**: List of dictionaries with `cells`, `op`, and `target` keys
- **Belief Space**: 3D probability matrix [row][col][value]

## 🚧 Future Improvements

- [ ] Add MRV (Minimum Remaining Values) heuristic for Backtracking
- [ ] Implement LCV (Least Constraining Value) heuristic
- [ ] Add visualization of solving process
- [ ] Support for puzzle import/export (JSON format)
- [ ] Performance comparison plots between algorithms
- [ ] Support for larger grid sizes with optimizations
- [ ] Add puzzle generator
- [ ] Implement constraint propagation improvements
- [ ] Add unit tests
- [ ] Create web-based interface


