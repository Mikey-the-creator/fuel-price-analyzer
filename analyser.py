import pandas as pd
import matplotlib.pyplot as plt


class FuelPriceAnalyzer:
    def __init__(self, csv_file):
        """Load dataset from CSV."""
        self.df = pd.read_csv(csv_file)
        self.df['date'] = pd.to_datetime(self.df['date'])

    # --------- Basic Analysis ---------

    def average_price(self):
        """Return the national average fuel price."""
        return round(self.df['price'].mean(), 2)

    def price_by_state(self, state):
        """Return all price records for a given state."""
        return self.df[self.df['state'].str.lower() == state.lower()]

    def highest_price(self):
        """Return state/date/price of the highest record."""
        row = self.df.loc[self.df['price'].idxmax()]
        return row['state'], row['price'], row['date']

    def lowest_price(self):
        """Return state/date/price of the lowest record."""
        row = self.df.loc[self.df['price'].idxmin()]
        return row['state'], row['price'], row['date']

    # --------- Advanced Analysis ---------

    def forecast_next(self, state):
        """Predict next day's price using simple moving average (last 3 days)."""
        data = self.price_by_state(state).sort_values("date")
        if len(data) < 3:
            return None  # not enough data
        forecast = data["price"].rolling(window=3).mean().iloc[-1]
        return round(forecast, 2)

    def detect_spikes(self, threshold=50):
        """Detect price jumps > threshold (₦)."""
        self.df["price_diff"] = self.df.groupby("state")["price"].diff()
        spikes = self.df[self.df["price_diff"].abs() > threshold]
        return spikes

    def save_summary(self, filename="fuel_summary.csv"):
        """Save average fuel price per state to CSV."""
        summary = self.df.groupby("state")["price"].mean().reset_index()
        summary.to_csv(filename, index=False)
        return filename

    # --------- Visualization ---------

    def price_trend_plot(self, state=None):
        """Plot fuel price trends. If state is None, plot all states."""
        if state:
            data = self.price_by_state(state)
            plt.plot(data["date"], data["price"], marker="o", label=state)
            plt.title(f"Fuel Price Trend in {state}")
        else:
            for s in self.df['state'].unique():
                data = self.price_by_state(s)
                plt.plot(data["date"], data["price"], marker="o", label=s)
            plt.title("Fuel Price Trends by State")

        plt.xlabel("Date")
        plt.ylabel("Price (₦/Litre)")
        plt.legend()
        plt.grid(True)

        # Make plot fullscreen
        mng = plt.get_current_fig_manager()
        try:
            mng.full_screen_toggle()
        except:
            try:
                mng.window.state('zoomed')
            except:
                pass

        plt.show()
