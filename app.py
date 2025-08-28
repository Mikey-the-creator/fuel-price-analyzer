import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from analyzer import FuelPriceAnalyzer   # import our class


class FuelPriceApp:
    def __init__(self, analyzer):
        self.analyzer = analyzer

        self.root = tk.Tk()
        self.root.title("Fuel Price Analyzer")
        self.root.geometry("450x500")

        # Dropdown for states
        self.state_var = tk.StringVar()
        states = sorted(self.analyzer.df['state'].unique())
        ttk.Label(self.root, text="Select State:").pack(pady=5)
        self.state_menu = ttk.Combobox(self.root, textvariable=self.state_var, values=states)
        self.state_menu.pack(pady=5)

        # Buttons
        ttk.Button(self.root, text="Average Price", command=self.show_average).pack(pady=5)
        ttk.Button(self.root, text="Highest Price", command=self.show_highest).pack(pady=5)
        ttk.Button(self.root, text="Lowest Price", command=self.show_lowest).pack(pady=5)
        ttk.Button(self.root, text="Forecast Next Day", command=self.show_forecast).pack(pady=5)
        ttk.Button(self.root, text="Plot All States", command=self.plot_all).pack(pady=5)
        ttk.Button(self.root, text="Plot Selected State", command=self.plot_state).pack(pady=5)

        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=10)

        # Extra Features
        ttk.Button(self.root, text="Export Summary CSV", command=self.export_summary).pack(pady=5)
        ttk.Button(self.root, text="Detect Spikes", command=self.show_spikes).pack(pady=5)
        ttk.Button(self.root, text="Close Plot", command=self.close_plot).pack(pady=5)

        self.root.mainloop()

    # ----- Button Actions -----

    def show_average(self):
        avg = self.analyzer.average_price()
        messagebox.showinfo("Average Price", f"₦{avg} per litre (national average)")

    def show_highest(self):
        state, price, date = self.analyzer.highest_price()
        messagebox.showinfo("Highest Price", f"{state} had the highest price ₦{price} on {date.date()}")

    def show_lowest(self):
        state, price, date = self.analyzer.lowest_price()
        messagebox.showinfo("Lowest Price", f"{state} had the lowest price ₦{price} on {date.date()}")

    def show_forecast(self):
        state = self.state_var.get()
        if not state:
            messagebox.showwarning("Warning", "Please select a state")
            return
        forecast = self.analyzer.forecast_next(state)
        messagebox.showinfo("Forecast", f"Predicted next price for {state}: ₦{forecast}")

    def plot_all(self):
        self.analyzer.price_trend_plot()

    def plot_state(self):
        state = self.state_var.get()
        if not state:
            messagebox.showwarning("Warning", "Please select a state")
            return
        self.analyzer.price_trend_plot(state)

    def export_summary(self):
        file = self.analyzer.save_summary()
        messagebox.showinfo("Export Successful", f"Summary saved to {file}")

    def show_spikes(self):
        spikes = self.analyzer.detect_spikes()
        if spikes.empty:
            messagebox.showinfo("Spikes", "No significant price spikes detected.")
        else:
            msg = "\n".join([f"{row.state} ({row.date.date()}): Δ₦{row.price_diff:.2f}"
                             for _, row in spikes.iterrows()])
            messagebox.showinfo("Detected Spikes", msg)

    def close_plot(self):
        plt.close("all")
        messagebox.showinfo("Plot Closed", "All open plots have been closed.")


# Run app
if __name__ == "__main__":
    analyzer = FuelPriceAnalyzer("fuel_prices.csv")
    app = FuelPriceApp(analyzer)
