import math
import tkinter as tk
from tkinter import ttk, messagebox

import customtkinter as ctk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.stats import norm


class NormalDistributionCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Normal Distribution Calculator")
        self.geometry("1220x760")
        self.minsize(1100, 700)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.mu_var = tk.StringVar(value="0")
        self.sigma_var = tk.StringVar(value="1")
        self.calc_type_var = tk.StringVar(value="value_to_prob")
        self.option_var = tk.StringVar(value="left")
        self.input1_var = tk.StringVar(value="1")
        self.input2_var = tk.StringVar(value="2")
        self.result_var = tk.StringVar(value="Probability = 0.8413")

        self._build_ui()
        self.update_input_labels()
        self.calculate()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.left_panel = ctk.CTkFrame(self, corner_radius=18)
        self.left_panel.grid(row=0, column=0, padx=(18, 10), pady=18, sticky="ns")

        self.right_panel = ctk.CTkFrame(self, corner_radius=18)
        self.right_panel.grid(row=0, column=1, padx=(10, 18), pady=18, sticky="nsew")
        self.right_panel.grid_rowconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=0)
        self.right_panel.grid_columnconfigure(0, weight=1)

        self._build_left_panel()
        self._build_right_panel()

    def _build_left_panel(self):
        title = ctk.CTkLabel(
            self.left_panel,
            text="Distribution Characteristics",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        title.pack(anchor="w", padx=18, pady=(18, 12))

        dist_frame = ctk.CTkFrame(self.left_panel, corner_radius=14)
        dist_frame.pack(fill="x", padx=16, pady=(0, 12))
        ctk.CTkLabel(dist_frame, text="Distribution", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=14, pady=(12, 6))
        self.dist_combo = ctk.CTkComboBox(dist_frame, values=["Normal"], state="readonly")
        self.dist_combo.set("Normal")
        self.dist_combo.pack(fill="x", padx=14, pady=(0, 12))

        param_frame = ctk.CTkFrame(self.left_panel, corner_radius=14)
        param_frame.pack(fill="x", padx=16, pady=(0, 12))
        ctk.CTkLabel(param_frame, text="Parameters", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=14, pady=(12, 10))

        self._labeled_entry(param_frame, "Mean (μ)", self.mu_var)
        self._labeled_entry(param_frame, "Std. Dev. (σ)", self.sigma_var)

        ctk.CTkButton(param_frame, text="Reset Distribution", command=self.reset_distribution).pack(fill="x", padx=14, pady=(4, 14))

        calc_type_frame = ctk.CTkFrame(self.left_panel, corner_radius=14)
        calc_type_frame.pack(fill="x", padx=16, pady=(0, 12))
        ctk.CTkLabel(calc_type_frame, text="Type of Calculation", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=14, pady=(12, 10))

        self.value_prob_radio = ctk.CTkRadioButton(
            calc_type_frame,
            text="Input values and calculate probability",
            variable=self.calc_type_var,
            value="value_to_prob",
            command=self.on_mode_change,
        )
        self.value_prob_radio.pack(anchor="w", padx=14, pady=(0, 8))

        self.prob_value_radio = ctk.CTkRadioButton(
            calc_type_frame,
            text="Input probability and calculate values",
            variable=self.calc_type_var,
            value="prob_to_value",
            command=self.on_mode_change,
        )
        self.prob_value_radio.pack(anchor="w", padx=14, pady=(0, 14))

        btn_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        btn_frame.pack(fill="x", padx=16, pady=(8, 16))
        btn_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(btn_frame, text="Calculate", command=self.calculate).grid(row=0, column=0, padx=4, pady=4, sticky="ew")
        ctk.CTkButton(btn_frame, text="Clear", command=self.clear_inputs).grid(row=0, column=1, padx=4, pady=4, sticky="ew")
        ctk.CTkButton(btn_frame, text="Exit", command=self.destroy, fg_color="#d9534f", hover_color="#c9302c").grid(row=0, column=2, padx=4, pady=4, sticky="ew")

    def _build_right_panel(self):
        chart_card = ctk.CTkFrame(self.right_panel, corner_radius=18)
        chart_card.grid(row=0, column=0, padx=16, pady=(16, 10), sticky="nsew")
        chart_card.grid_rowconfigure(1, weight=1)
        chart_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(chart_card, text="Normal Distribution", font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, sticky="w", padx=18, pady=(14, 8))

        self.fig = Figure(figsize=(7.2, 4.4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_card)
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))

        calc_card = ctk.CTkFrame(self.right_panel, corner_radius=18)
        calc_card.grid(row=1, column=0, padx=16, pady=(10, 16), sticky="ew")
        calc_card.grid_columnconfigure(0, weight=1)
        calc_card.grid_columnconfigure(1, weight=0)

        ctk.CTkLabel(calc_card, text="Calculations", font=ctk.CTkFont(size=22, weight="bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=18, pady=(14, 12))

        options_frame = ctk.CTkFrame(calc_card, corner_radius=14)
        options_frame.grid(row=1, column=0, padx=(18, 10), pady=(0, 14), sticky="nsew")

        ctk.CTkLabel(options_frame, text="Probability Options", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=14, pady=(12, 10))

        self.radio1 = ctk.CTkRadioButton(options_frame, text="X ≤ q", variable=self.option_var, value="left", command=self.on_option_change)
        self.radio2 = ctk.CTkRadioButton(options_frame, text="X > q", variable=self.option_var, value="right", command=self.on_option_change)
        self.radio3 = ctk.CTkRadioButton(options_frame, text="q1 < X ≤ q2", variable=self.option_var, value="between", command=self.on_option_change)
        self.radio4 = ctk.CTkRadioButton(options_frame, text="X ≤ q1   OR   X > q2", variable=self.option_var, value="outside", command=self.on_option_change)

        for rb in [self.radio1, self.radio2, self.radio3, self.radio4]:
            rb.pack(anchor="w", padx=14, pady=4)

        self.result_label = ctk.CTkLabel(
            options_frame,
            textvariable=self.result_var,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1f4fbf",
        )
        self.result_label.pack(anchor="w", padx=14, pady=(16, 14))

        input_frame = ctk.CTkFrame(calc_card, corner_radius=14)
        input_frame.grid(row=1, column=1, padx=(10, 18), pady=(0, 14), sticky="ne")

        ctk.CTkLabel(input_frame, text="Input", font=ctk.CTkFont(size=15, weight="bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=14, pady=(12, 10))

        self.input1_label = ctk.CTkLabel(input_frame, text="Value")
        self.input1_label.grid(row=1, column=0, sticky="w", padx=(14, 8), pady=6)
        self.input1_entry = ctk.CTkEntry(input_frame, textvariable=self.input1_var, width=120)
        self.input1_entry.grid(row=1, column=1, sticky="e", padx=(8, 14), pady=6)

        self.input2_label = ctk.CTkLabel(input_frame, text="Value 2")
        self.input2_entry = ctk.CTkEntry(input_frame, textvariable=self.input2_var, width=120)

        ctk.CTkButton(input_frame, text="Run", command=self.calculate).grid(row=4, column=0, columnspan=2, sticky="ew", padx=14, pady=(12, 14))

        self.input1_entry.bind("<Return>", lambda event: self.calculate())
        self.input2_entry.bind("<Return>", lambda event: self.calculate())

    def _labeled_entry(self, parent, label, variable):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(0, 10))
        ctk.CTkLabel(row, text=label).pack(anchor="w")
        entry = ctk.CTkEntry(row, textvariable=variable)
        entry.pack(fill="x", pady=(6, 0))
        entry.bind("<Return>", lambda event: self.calculate())
        return entry

    def reset_distribution(self):
        self.mu_var.set("0")
        self.sigma_var.set("1")
        self.calc_type_var.set("value_to_prob")
        self.option_var.set("left")
        self.input1_var.set("1")
        self.input2_var.set("2")
        self.update_input_labels()
        self.calculate()

    def clear_inputs(self):
        self.input1_var.set("")
        self.input2_var.set("")
        self.result_var.set("Result will appear here")
        self.plot_distribution()

    def on_mode_change(self):
        self.update_input_labels()
        self.calculate()

    def on_option_change(self):
        self.update_input_labels()
        self.calculate()

    def update_input_labels(self):
        mode = self.calc_type_var.get()
        option = self.option_var.get()
        two_inputs = option in {"between", "outside"}

        if mode == "value_to_prob":
            self.input1_label.configure(text="Value:" if not two_inputs else "Value 1:")
            self.input2_label.configure(text="Value 2:")
        else:
            self.input1_label.configure(text="Probability:" if not two_inputs else "Probability 1:")
            self.input2_label.configure(text="Probability 2:")

        if two_inputs:
            self.input2_label.grid(row=2, column=0, sticky="w", padx=(14, 8), pady=6)
            self.input2_entry.grid(row=2, column=1, sticky="e", padx=(8, 14), pady=6)
        else:
            self.input2_label.grid_forget()
            self.input2_entry.grid_forget()

    def get_parameters(self):
        try:
            mu = float(self.mu_var.get())
            sigma = float(self.sigma_var.get())
        except ValueError:
            raise ValueError("Mean and standard deviation must be numeric.")

        if sigma <= 0:
            raise ValueError("Standard deviation must be greater than 0.")

        return mu, sigma

    def calculate(self):
        try:
            mu, sigma = self.get_parameters()
            mode = self.calc_type_var.get()
            option = self.option_var.get()

            if mode == "value_to_prob":
                result_text, shade_data = self.calculate_probability(mu, sigma, option)
            else:
                result_text, shade_data = self.calculate_values(mu, sigma, option)

            self.result_var.set(result_text)
            self.plot_distribution(mu, sigma, shade_data)
        except Exception as e:
            self.result_var.set("Error: invalid input")
            self.plot_distribution()
            if str(e):
                # non-blocking would be nicer, but messagebox is fine for validation here
                pass

    def calculate_probability(self, mu, sigma, option):
        dist = norm(loc=mu, scale=sigma)

        if option == "left":
            q = float(self.input1_var.get())
            p = dist.cdf(q)
            return f"Probability = {p:.4f}", {"mode": "left", "q": q}

        if option == "right":
            q = float(self.input1_var.get())
            p = 1 - dist.cdf(q)
            return f"Probability = {p:.4f}", {"mode": "right", "q": q}

        q1 = float(self.input1_var.get())
        q2 = float(self.input2_var.get())
        if q1 > q2:
            q1, q2 = q2, q1

        if option == "between":
            p = dist.cdf(q2) - dist.cdf(q1)
            return f"Probability = {p:.4f}", {"mode": "between", "q1": q1, "q2": q2}

        p = dist.cdf(q1) + (1 - dist.cdf(q2))
        return f"Probability = {p:.4f}", {"mode": "outside", "q1": q1, "q2": q2}

    def calculate_values(self, mu, sigma, option):
        dist = norm(loc=mu, scale=sigma)

        if option == "left":
            p = float(self.input1_var.get())
            self._validate_probability(p)
            q = dist.ppf(p)
            return f"Value = {q:.4f}", {"mode": "left", "q": q}

        if option == "right":
            p = float(self.input1_var.get())
            self._validate_probability(p)
            q = dist.ppf(1 - p)
            return f"Value = {q:.4f}", {"mode": "right", "q": q}

        p1 = float(self.input1_var.get())
        p2 = float(self.input2_var.get())
        self._validate_probability(p1)
        self._validate_probability(p2)

        if option == "between":
            q1 = dist.ppf(p1)
            q2 = dist.ppf(p2)
            q_low, q_high = sorted([q1, q2])
            area = dist.cdf(q_high) - dist.cdf(q_low)
            return f"Values = ({q_low:.4f}, {q_high:.4f}) | Area = {area:.4f}", {
                "mode": "between",
                "q1": q_low,
                "q2": q_high,
            }

        q1 = dist.ppf(p1)
        q2 = dist.ppf(1 - p2)
        q_low, q_high = sorted([q1, q2])
        area = dist.cdf(q_low) + (1 - dist.cdf(q_high))
        return f"Values = ({q_low:.4f}, {q_high:.4f}) | Area = {area:.4f}", {
            "mode": "outside",
            "q1": q_low,
            "q2": q_high,
        }

    @staticmethod
    def _validate_probability(p):
        if not (0 < p < 1):
            raise ValueError("Probability must be between 0 and 1.")

    def plot_distribution(self, mu=0, sigma=1, shade_data=None):
        self.ax.clear()

        x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 800)
        y = norm.pdf(x, mu, sigma)

        self.ax.plot(x, y, linewidth=2)

        if shade_data:
            mode = shade_data.get("mode")
            if mode in {"left", "right"}:
                q = shade_data["q"]
                if mode == "left":
                    xs = x[x <= q]
                else:
                    xs = x[x > q]
                ys = norm.pdf(xs, mu, sigma)
                self.ax.fill_between(xs, ys, alpha=0.85)
                self.ax.axvline(q, linestyle="--", linewidth=1.2)
            elif mode in {"between", "outside"}:
                q1 = shade_data["q1"]
                q2 = shade_data["q2"]
                if mode == "between":
                    xs = x[(x >= q1) & (x <= q2)]
                    ys = norm.pdf(xs, mu, sigma)
                    self.ax.fill_between(xs, ys, alpha=0.85)
                else:
                    xs_left = x[x <= q1]
                    ys_left = norm.pdf(xs_left, mu, sigma)
                    xs_right = x[x >= q2]
                    ys_right = norm.pdf(xs_right, mu, sigma)
                    self.ax.fill_between(xs_left, ys_left, alpha=0.85)
                    self.ax.fill_between(xs_right, ys_right, alpha=0.85)
                self.ax.axvline(q1, linestyle="--", linewidth=1.2)
                self.ax.axvline(q2, linestyle="--", linewidth=1.2)

        self.ax.set_title("Normal Distribution", fontsize=16, pad=12)
        self.ax.set_xlabel("X", fontsize=12)
        self.ax.set_ylabel("Density", fontsize=12)
        self.ax.grid(alpha=0.25)
        self.fig.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    app = NormalDistributionCalculator()
    app.mainloop()
