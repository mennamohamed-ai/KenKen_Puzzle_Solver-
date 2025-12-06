# gui.py
# Tkinter GUI that allows user to:
# - choose grid size
# - add cages
# - choose algorithm (Backtracking/Cultural)
# - solve and display metrics

import tkinter as tk
from tkinter import messagebox, ttk
from grid import KenKenGrid
from backtracking import solve_backtracking
from cultural import CulturalAlgorithm
import time

class KenKenGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("KenKen Solver")
        self.root.geometry("780x820")
        self.root.configure(bg="#f7f7fb")

        self.size = 4
        self.grid_obj = KenKenGrid(self.size)
        self.cells = []
        self.cages_input = []

        # header
        header = tk.Label(root, text="🧩 KenKen Solver", font=("Helvetica", 22, "bold"), bg="#f7f7fb")
        header.pack(pady=12)

        # settings frame
        settings = tk.Frame(root, bg="#f7f7fb")
        settings.pack(pady=6)

        tk.Label(settings, text="Grid size (N):", bg="#f7f7fb").grid(row=0, column=0, padx=6)
        self.size_entry = tk.Entry(settings, width=6)
        self.size_entry.insert(0, "4")
        self.size_entry.grid(row=0, column=1, padx=6)

        tk.Label(settings, text="Algorithm:", bg="#f7f7fb").grid(row=0, column=2, padx=6)
        self.algo_var = tk.StringVar()
        self.algo_menu = ttk.Combobox(settings, textvariable=self.algo_var, values=["Backtracking", "Cultural"], state="readonly", width=16)
        self.algo_menu.current(0)
        self.algo_menu.grid(row=0, column=3, padx=6)

        tk.Button(settings, text="Apply Size", command=self.reset, bg="#1976d2", fg="white").grid(row=0, column=4, padx=6)

        # cage input
        cage_frame = tk.LabelFrame(root, text="Add Cage (cells;op;target)", padx=10, pady=8, bg="#f7f7fb")
        cage_frame.pack(pady=8, fill="x", padx=12)
        tk.Label(cage_frame, text="                                       Example: 0,0,0,1;+;5", bg="#f7f7fb").pack(anchor="w")
        self.cage_entry = tk.Entry(cage_frame, width=60)
        self.cage_entry.pack(side="left", padx=116, pady=6)
        tk.Button(cage_frame, text="Add Cage", command=self.add_cage, bg="#2e7d32", fg="white").pack(side="left", padx=6)

        # cage list
        self.cage_listbox = tk.Listbox(root, height=6, width=80)
        self.cage_listbox.pack(pady=6)

        # grid area
        self.grid_frame = tk.Frame(root, bg="#f7f7fb")
        self.grid_frame.pack(pady=10)

        # buttons
        btn_frame = tk.Frame(root, bg="#f7f7fb")
        btn_frame.pack(pady=6)
        tk.Button(btn_frame, text="Solve", command=self.solve, bg="#0b8457", fg="white", width=12).grid(row=0, column=0, padx=8)
        tk.Button(btn_frame, text="Reset", command=self.reset, bg="#c62828", fg="white", width=12).grid(row=0, column=1, padx=8)
        tk.Button(btn_frame, text="Clear Cages", command=self.clear_cages, width=12).grid(row=0, column=2, padx=8)

        # metrics
        self.metrics_label = tk.Label(root, text="", bg="#f7f7fb", font=("Helvetica", 11))
        self.metrics_label.pack(pady=6)


        self.reset()

    def reset(self):
        # read size safely
        try:
            self.size = int(self.size_entry.get())
            if self.size <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Grid size must be a positive integer. Reset to 4.")
            self.size_entry.delete(0, tk.END)
            self.size_entry.insert(0, "4")
            self.size = 4
        self.grid_obj = KenKenGrid(self.size)
        self.cages_input.clear()
        self.cage_listbox.delete(0, tk.END)
        self.metrics_label.config(text="")
        self.draw_grid()

    def add_cage(self):
        text = self.cage_entry.get().strip()
        if not text:
            messagebox.showerror("Error", "Enter cage definition")
            return
        try:
            parts = text.split(';')
            coords = parts[0].split(',')
            if len(coords) % 2 != 0:
                raise ValueError("Cell coords malformed")
            cells = [(int(coords[i]), int(coords[i+1])) for i in range(0, len(coords), 2)]
            op = parts[1].strip()
            target = int(parts[2])
            self.grid_obj.add_cage(cells, op, target)
            self.cage_listbox.insert(tk.END, text)
            self.cage_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid cage format. Example: 0,0,0,1;+;5\n\n{e}")

    def clear_cages(self):
        self.grid_obj.cages = []
        self.cage_listbox.delete(0, tk.END)
        messagebox.showinfo("Info", "Cages cleared")

    def draw_grid(self):
        # clear
        for w in self.grid_frame.winfo_children():
            w.destroy()
        self.cells = []
        for r in range(self.size):
            row = []
            for c in range(self.size):
                e = tk.Entry(self.grid_frame, width=4, justify='center', font=("Helvetica", 14))
                e.grid(row=r, column=c, padx=4, pady=4)
                row.append(e)
            self.cells.append(row)

    def fill_grid_from_gridobj(self):
        for r in range(self.size):
            for c in range(self.size):
                self.cells[r][c].delete(0, tk.END)
                val = self.grid_obj.get_cell(r, c)
                if val != 0:
                    self.cells[r][c].insert(0, str(val))

    def solve(self):
        algo = self.algo_var.get()
        # copy cages already in grid_obj
        if len(self.grid_obj.get_cages()) == 0:
            if messagebox.askyesno("No cages", "No cages defined. Continue with empty cage set? (Not recommended)"):
                pass
            else:
                return

        # run selected algorithm and measure time
        try:
            if algo == "Backtracking":
                solved, t, iters = solve_backtracking(self.grid_obj)
                if solved:
                    self.fill_grid_from_gridobj()
                    self.metrics_label.config(text=f"Solved by Backtracking | Time: {t:.3f}s | Iterations: {iters}")
                else:
                    messagebox.showerror("Not solved", "Backtracking did not find a solution.")
                    self.metrics_label.config(text=f"Backtracking finished | Time: {t:.3f}s | Iterations: {iters}")
            else:
                ca = CulturalAlgorithm(self.grid_obj, pop_size=200, elite_fraction=0.12, max_gen=1000)
                solved, solution_grid, t, gens = ca.solve(timeout_seconds=8.0)
                # if CA returns a grid (best found), apply it to GUI
                if solution_grid is not None:
                    self.grid_obj = solution_grid
                    self.fill_grid_from_gridobj()
                if solved:
                    self.metrics_label.config(text=f"Solved by Cultural | Time: {t:.3f}s | Generations: {gens}")
                else:
                    self.metrics_label.config(text=f"Cultural finished (best-found) | Time: {t:.3f}s | Generations: {gens}")
                    if not solved:
                        messagebox.showinfo("Partial result", "Cultural algorithm did not find perfect solution; showing best found.")
        except Exception as e:
            messagebox.showerror("Error", f"Solver error: {e}")
