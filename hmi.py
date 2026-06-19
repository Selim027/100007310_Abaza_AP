import tkinter as tk
from tkinter import ttk
from production_line import MarkerProductionLine
from database import InfluxWriter

class MarkerHMI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ink Marker Production Line HMI")
        self.root.geometry("980x620")
        self.root.configure(bg="#0f172a")
        self.line = MarkerProductionLine()
        self.db = InfluxWriter()
        self.auto_running = False
        self.build_ui()
        self.update_display()

    def build_ui(self):
        frame = tk.Frame(self.root, bg="#111827", padx=28, pady=24)
        frame.pack(fill="both", expand=True, padx=28, pady=28)

        tk.Label(frame, text="Ink Marker Line HMI", fg="white", bg="#111827", font=("Segoe UI", 28, "bold")).pack(anchor="w")
        tk.Label(frame, text="Operator dashboard for marker assembly and quality control", fg="#cbd5e1", bg="#111827", font=("Segoe UI", 12)).pack(anchor="w", pady=(0, 22))

        btn_frame = tk.Frame(frame, bg="#111827")
        btn_frame.pack(anchor="w", pady=(0, 22))
        self.make_button(btn_frame, "START", "#22c55e", self.start).pack(side="left", padx=(0, 14))
        self.make_button(btn_frame, "STOP", "#ef4444", self.stop).pack(side="left", padx=(0, 14))
        self.make_button(btn_frame, "RESET", "#3b82f6", self.reset).pack(side="left", padx=(0, 14))
        self.make_button(btn_frame, "Produce One Marker", "#f59e0b", self.produce_once, width=18).pack(side="left")

        grid = tk.Frame(frame, bg="#111827")
        grid.pack(fill="x")
        self.cards = {}
        labels = ["Machine State", "Current Stage", "Total Parts", "Good Parts", "Defective Parts", "Faulted"]
        for i, label in enumerate(labels):
            card = tk.Frame(grid, bg="#1f2937", padx=18, pady=14, highlightbackground="#334155", highlightthickness=1)
            card.grid(row=i//2, column=i%2, padx=8, pady=8, sticky="ew")
            grid.grid_columnconfigure(i%2, weight=1)
            tk.Label(card, text=label, fg="#94a3b8", bg="#1f2937", font=("Segoe UI", 9)).pack(anchor="w")
            val = tk.Label(card, text="-", fg="#fbbf24", bg="#1f2937", font=("Segoe UI", 16, "bold"))
            val.pack(anchor="w", pady=(4, 0))
            self.cards[label] = val

        self.error_label = tk.Label(frame, text="Latest Error: None", fg="#fecaca", bg="#3f1d1d", anchor="w", padx=12, pady=8, font=("Segoe UI", 11), highlightbackground="#ef4444", highlightthickness=1)
        self.error_label.pack(fill="x", pady=(16, 14))

        tk.Label(frame, text="Production Log", fg="white", bg="#111827", font=("Segoe UI", 13, "bold")).pack(anchor="w")
        self.log = tk.Text(frame, height=8, bg="#020617", fg="#e2e8f0", insertbackground="white", font=("Consolas", 10))
        self.log.pack(fill="both", expand=True, pady=(8,0))

    def make_button(self, parent, text, color, command, width=11):
        return tk.Button(parent, text=text, bg=color, fg="white", activebackground=color, activeforeground="white", relief="flat", width=width, height=2, font=("Segoe UI", 11, "bold"), command=command)

    def start(self):
        self.line.start()
        self.auto_running = True
        self.add_log("Line started")
        self.update_display()
        self.root.after(1200, self.auto_cycle)

    def stop(self):
        self.auto_running = False
        self.line.stop()
        self.add_log("Line stopped")
        self.update_display()

    def reset(self):
        self.auto_running = False
        self.line.reset()
        self.log.delete("1.0", tk.END)
        self.add_log("Line reset")
        self.update_display()

    def produce_once(self):
        if self.line.state != "PRODUCTIVE":
            self.line.start()
        product = self.line.produce_one_marker()
        self.report_product(product)
        self.update_display()

    def auto_cycle(self):
        if self.auto_running and self.line.state == "PRODUCTIVE":
            product = self.line.produce_one_marker()
            self.report_product(product)
            self.update_display()
            if self.line.state == "PRODUCTIVE":
                self.root.after(1200, self.auto_cycle)
            else:
                self.auto_running = False

    def report_product(self, product):
        if not product:
            return
        if product.defective:
            self.add_log(f"Marker #{product.serial_number}: DEFECT - {product.defect_reason}")
        else:
            self.add_log(f"Marker #{product.serial_number}: OK - packaged")

    def add_log(self, message):
        self.log.insert(tk.END, message + "\n")
        self.log.see(tk.END)

    def update_display(self):
        self.cards["Machine State"].config(text=self.line.state)
        self.cards["Current Stage"].config(text=self.line.current_stage)
        self.cards["Total Parts"].config(text=str(self.line.total_parts))
        self.cards["Good Parts"].config(text=str(self.line.good_parts))
        self.cards["Defective Parts"].config(text=str(self.line.defective_parts))
        self.cards["Faulted"].config(text="YES" if self.line.faulted else "NO")
        self.error_label.config(text=f"Latest Error: {self.line.last_error}")
        self.db.write_line_status(self.line)
