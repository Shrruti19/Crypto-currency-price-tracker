import tkinter as tk
from tkinter import ttk, messagebox
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

# ---- API Config ----
COINS = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Dogecoin": "dogecoin",
    "Cardano": "cardano",
    "Solana": "solana"
}

prices_data = {coin: [] for coin in COINS.keys()}
time_data = []

# ---- Fetch Prices ----
def fetch_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": ",".join(COINS.values()), "vs_currencies": "usd"}
        r = requests.get(url, params=params, timeout=5)
        data = r.json()
        return {name: data[api_id]["usd"] for name, api_id in COINS.items()}
    except Exception as e:
        print("API Error:", e)
        return {}

# ---- Plot Graph ----
def plot_graph():
    coin = coin_choice.get()
    ax.clear()
    ax.plot(time_data, prices_data[coin], marker="o", color="cyan", linewidth=2)
    ax.set_title(f"{coin} Price (USD)", fontsize=12, color="white")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price (USD)")
    ax.grid(True, linestyle="--", alpha=0.6)
    fig.autofmt_xdate()
    canvas.draw()

# ---- Update Prices ----
def update_prices():
    global time_data

    prices = fetch_prices()
    if not prices:
        messagebox.showerror("Error", "Failed to fetch prices")
        root.after(10000, update_prices)
        return

    # update labels
    for coin, lbl in price_labels.items():
        lbl.config(text=f"${prices[coin]:,.2f}")

    # store data for graph
    time_data.append(datetime.datetime.now().strftime("%H:%M:%S"))
    for coin in COINS.keys():
        prices_data[coin].append(prices[coin])

    # keep last 15 points
    if len(time_data) > 15:
        time_data = time_data[-15:]
        for coin in COINS.keys():
            prices_data[coin] = prices_data[coin][-15:]

    # refresh graph
    plot_graph()

    # call again in 10s
    root.after(10000, update_prices)

# ---- UI Setup ----
root = tk.Tk()
root.title("Crypto Dashboard")
root.geometry("900x600")
root.configure(bg="#2c3e50")

header = tk.Label(root, text="📊 Crypto Price Tracker", font=("Arial", 20, "bold"), fg="white", bg="#2c3e50")
header.pack(pady=10)

# Prices Frame
frame_prices = tk.Frame(root, bg="#34495e", bd=3, relief="ridge")
frame_prices.pack(pady=10, padx=10, fill="x")

price_labels = {}
for i, coin in enumerate(COINS.keys()):
    tk.Label(frame_prices, text=coin, font=("Arial", 14, "bold"), fg="white", bg="#34495e").grid(row=0, column=i, padx=20, pady=5)
    lbl = tk.Label(frame_prices, text="Loading...", font=("Arial", 12), fg="cyan", bg="#34495e")
    lbl.grid(row=1, column=i, padx=20, pady=5)
    price_labels[coin] = lbl

# Dropdown for graph
control_frame = tk.Frame(root, bg="#2c3e50")
control_frame.pack(pady=5)
tk.Label(control_frame, text="Select Coin:", font=("Arial", 12), fg="white", bg="#2c3e50").pack(side="left", padx=5)

coin_choice = ttk.Combobox(control_frame, values=list(COINS.keys()), font=("Arial", 12))
coin_choice.set("Bitcoin")
coin_choice.pack(side="left")

# ---- Graph Frame (create ax before using) ----
fig, ax = plt.subplots(figsize=(7,4))
fig.patch.set_facecolor("#2c3e50")
ax.set_facecolor("#2c3e50")
ax.tick_params(colors="white")

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=10)

# Start Updates
update_prices()

root.mainloop()
