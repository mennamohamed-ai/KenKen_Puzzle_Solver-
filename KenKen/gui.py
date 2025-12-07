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

class ScrollableFrame(tk.Frame):
    """Frame قابل للتمرير"""
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)
        
        # إنشاء Canvas و Scrollbar
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, bg="#f7f7fb")
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f7f7fb")
        
        # ربط ScrollableFrame بالCanvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # ترتيب العناصر
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # تحديث scrollregion عند تغيير حجم النافذة
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        
        # تفعيل التمرير بالماوس
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)
    
    def _on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
    
    def _on_mousewheel(self, event):
        # دعم Windows و Mac
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

class KenKenGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("KenKen Solver")
        self.root.geometry("780x600")  # تصغير الارتفاع الافتراضي
        self.root.configure(bg="#f7f7fb")
        
        # إنشاء ScrollableFrame
        self.scrollable = ScrollableFrame(root)
        self.scrollable.pack(fill="both", expand=True)
        
        # استخدام scrollable_frame بدلاً من root
        content = self.scrollable.scrollable_frame

        self.size = 4
        self.grid_obj = KenKenGrid(self.size)
        self.cells = []
        self.cages_input = []
        self.cage_text_labels = {}  # لحفظ Labels النصوص
        # ألوان مختلفة للأقفاص
        self.cage_colors = [
            "#FFE5E5",  # أحمر فاتح
            "#E5F3FF",  # أزرق فاتح
            "#E5FFE5",  # أخضر فاتح
            "#FFF5E5",  # برتقالي فاتح
            "#F0E5FF",  # بنفسجي فاتح
            "#FFE5F5",  # وردي فاتح
            "#E5FFFF",  # سماوي فاتح
            "#FFFFE5",  # أصفر فاتح
            "#E5E5FF",  # أزرق فاتح جداً
            "#FFE5FF",  # وردي فاتح جداً
        ]

        # header
        header = tk.Label(content, text="🧩 KenKen Solver", font=("Helvetica", 22, "bold"), bg="#f7f7fb")
        header.pack(pady=12)

        # settings frame
        settings = tk.Frame(content, bg="#f7f7fb")
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
        cage_frame = tk.LabelFrame(content, text="Add Cage (cells;op;target)", padx=10, pady=8, bg="#f7f7fb")
        cage_frame.pack(pady=8, fill="x", padx=12)
        tk.Label(cage_frame, text="                                       Example: 0,0,0,1;+;5", bg="#f7f7fb").pack(anchor="w")
        self.cage_entry = tk.Entry(cage_frame, width=60)
        self.cage_entry.pack(side="left", padx=116, pady=6)
        tk.Button(cage_frame, text="Add Cage", command=self.add_cage, bg="#2e7d32", fg="white").pack(side="left", padx=6)

        # cage list
        self.cage_listbox = tk.Listbox(content, height=6, width=80)
        self.cage_listbox.pack(pady=6)

        # grid area - using Canvas for drawing cage borders
        self.grid_frame = tk.Frame(content, bg="#f7f7fb")
        self.grid_frame.pack(pady=10)
        self.canvas = None
        self.cell_size = 60  # حجم كل خلية بالبكسل
        self.cage_labels = {}  # لحفظ تسميات الأقفاص

        # buttons
        btn_frame = tk.Frame(content, bg="#f7f7fb")
        btn_frame.pack(pady=6)
        tk.Button(btn_frame, text="Solve", command=self.solve, bg="#0b8457", fg="white", width=12).grid(row=0, column=0, padx=8)
        tk.Button(btn_frame, text="Reset", command=self.reset, bg="#c62828", fg="white", width=12).grid(row=0, column=1, padx=8)
        tk.Button(btn_frame, text="Clear Cages", command=self.clear_cages, width=12).grid(row=0, column=2, padx=8)

        # metrics
        self.metrics_label = tk.Label(content, text="", bg="#f7f7fb", font=("Helvetica", 11))
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
        # تحديث scrollregion بعد إعادة الرسم
        self.scrollable.scrollable_frame.update_idletasks()
        self.scrollable.canvas.configure(scrollregion=self.scrollable.canvas.bbox("all"))

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
            # تحديث ألوان الخلايا بعد إضافة القفص
            self.update_cage_colors()
            # تحديث scrollregion
            self.scrollable.scrollable_frame.update_idletasks()
            self.scrollable.canvas.configure(scrollregion=self.scrollable.canvas.bbox("all"))
        except Exception as e:
            messagebox.showerror("Error", f"Invalid cage format. Example: 0,0,0,1;+;5\n\n{e}")

    def clear_cages(self):
        self.grid_obj.cages = []
        self.cage_listbox.delete(0, tk.END)
        # تحديث الألوان بعد مسح الأقفاص
        self.update_cage_colors()
        messagebox.showinfo("Info", "Cages cleared")

    def draw_grid(self):
        # clear
        for w in self.grid_frame.winfo_children():
            w.destroy()
        self.cells = []
        self.cage_labels = {}
        
        # إنشاء Canvas لرسم الخطوط
        canvas_size = self.size * self.cell_size + 20
        self.canvas = tk.Canvas(self.grid_frame, width=canvas_size, height=canvas_size, 
                                bg="white", highlightthickness=0)
        self.canvas.pack()
        
        # رسم الخلايا والحدود الرقيقة
        for r in range(self.size):
            row = []
            for c in range(self.size):
                x1 = c * self.cell_size + 10
                y1 = r * self.cell_size + 10
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # رسم الحدود الرقيقة للخلايا
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="#cccccc", width=1)
                
                # إنشاء Entry widget داخل Canvas
                e = tk.Entry(self.grid_frame, width=3, justify='center', 
                            font=("Helvetica", 14), borderwidth=0, highlightthickness=0, bg="white")
                e.place(x=x1+2, y=y1+2, width=self.cell_size-4, height=self.cell_size-4)
                row.append(e)
            self.cells.append(row)
        
        # إنشاء Label للنص داخل الخلايا (للأقفاص)
        self.cage_text_labels = {}
        
        # رسم الخطوط السميكة حول الأقفاص وإظهار العملية والهدف
        self.draw_cage_borders()
    
    def draw_cage_borders(self):
        """رسم الحدود السميكة حول الأقفاص وإظهار العملية والهدف"""
        if self.canvas is None:
            return
        
        cages = self.grid_obj.get_cages()
        border_width = 3
        
        # إنشاء مجموعة من جميع الخلايا في الأقفاص
        all_caged_cells = set()
        for cage in cages:
            all_caged_cells.update(cage['cells'])
        
        # رسم الحدود بين الخلايا
        for r in range(self.size):
            for c in range(self.size):
                cell = (r, c)
                x1 = c * self.cell_size + 10
                y1 = r * self.cell_size + 10
                x2 = (c + 1) * self.cell_size + 10
                y2 = (r + 1) * self.cell_size + 10
                
                # الحد الأيمن - رسم إذا كانت الخلية المجاورة في قفص مختلف أو خارج القفص
                if c < self.size - 1:
                    right_cell = (r, c + 1)
                    cell_cage = next((i for i, cage in enumerate(cages) if cell in cage['cells']), -1)
                    right_cage = next((i for i, cage in enumerate(cages) if right_cell in cage['cells']), -1)
                    if cell_cage != right_cage:
                        self.canvas.create_line(x2, y1, x2, y2, width=border_width, fill="black")
                
                # الحد السفلي - رسم إذا كانت الخلية المجاورة في قفص مختلف أو خارج القفص
                if r < self.size - 1:
                    bottom_cell = (r + 1, c)
                    cell_cage = next((i for i, cage in enumerate(cages) if cell in cage['cells']), -1)
                    bottom_cage = next((i for i, cage in enumerate(cages) if bottom_cell in cage['cells']), -1)
                    if cell_cage != bottom_cage:
                        self.canvas.create_line(x1, y2, x2, y2, width=border_width, fill="black")
        
        # رسم الحدود الخارجية للشبكة
        self.canvas.create_line(10, 10, self.size * self.cell_size + 10, 10, 
                               width=border_width, fill="black")
        self.canvas.create_line(10, 10, 10, self.size * self.cell_size + 10, 
                               width=border_width, fill="black")
        self.canvas.create_line(self.size * self.cell_size + 10, 10, 
                               self.size * self.cell_size + 10, self.size * self.cell_size + 10, 
                               width=border_width, fill="black")
        self.canvas.create_line(10, self.size * self.cell_size + 10, 
                               self.size * self.cell_size + 10, self.size * self.cell_size + 10, 
                               width=border_width, fill="black")
        
        # إظهار العملية والهدف داخل كل قفص
        # حذف Labels القديمة أولاً
        for label in self.cage_text_labels.values():
            label.destroy()
        self.cage_text_labels.clear()
        
        for idx, cage in enumerate(cages):
            cells = cage['cells']
            if not cells:
                continue
            
            # تحويل العملية إلى رمز
            op_symbol = {
                '+': '+',
                '-': '-',
                '*': '×',
                '/': '÷',
                '=': '='
            }.get(cage['op'], cage['op'])
            
            # نص العملية والهدف (العملية أولاً ثم الهدف)
            cage_text = f"{op_symbol}{cage['target']}"
            
            # موضع النص داخل القفص في الزاوية العلوية اليسرى من أول خلية
            first_cell = cells[0]
            r, c = first_cell
            
            # موضع النص داخل الخلية (في الزاوية العلوية اليسرى)
            x = c * self.cell_size + 10 + 3
            y = r * self.cell_size + 10 + 3
            
            # إنشاء Label للنص
            label = tk.Label(self.grid_frame, text=cage_text, 
                           font=("Helvetica", 9, "bold"), 
                           bg="white", fg="black",
                           borderwidth=0, highlightthickness=0)
            label.place(x=x, y=y)
            
            # حفظ المرجع
            self.cage_text_labels[first_cell] = label
            self.cage_labels[first_cell] = label
    
    def update_cage_colors(self):
        """تحديث ألوان الخلايا بناءً على الأقفاص"""
        # إعادة رسم الشبكة مع الحدود
        if self.canvas is not None:
            self.draw_cage_borders()
        
        # إعادة تعيين جميع الخلايا للون الأبيض
        for r in range(self.size):
            for c in range(self.size):
                if self.cells and r < len(self.cells) and c < len(self.cells[r]):
                    self.cells[r][c].config(bg="white")
        
        # تطبيق الألوان على كل قفص
        cages = self.grid_obj.get_cages()
        for idx, cage in enumerate(cages):
            color = self.cage_colors[idx % len(self.cage_colors)]
            for (r, c) in cage['cells']:
                if 0 <= r < self.size and 0 <= c < self.size:
                    if self.cells and r < len(self.cells) and c < len(self.cells[r]):
                        self.cells[r][c].config(bg=color)
            # تحديث لون Label النص إذا كان موجوداً
            if cage['cells'] and cage['cells'][0] in self.cage_text_labels:
                self.cage_text_labels[cage['cells'][0]].config(bg=color)

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
