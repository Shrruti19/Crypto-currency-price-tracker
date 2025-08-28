import requests
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Live crypto prices (text only)
def get_crypto_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin,ethereum,dogecoin,cardano,solana",
            "vs_currencies": "usd"
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        return data
    except:
        return {}

# Show dummy graph
def show_graph():
    prices = [100, 120, 90, 140, 160, 130, 170]  # Dummy data
    fig = Figure(figsize=(5, 3), dpi=100)
    plot = fig.add_subplot(111)
    plot.plot(prices, color="blue", marker="o")
    plot.set_title("Bitcoin Price (Dummy Data)")
    plot.set_xlabel("Time (units)")
    plot.set_ylabel("Price in USD")
    plot.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

# Refresh prices
def refresh_prices():
    data = get_crypto_prices()
    if not data:
        text = "⚠️ Could not fetch live data\nShowing N/A"
    else:
        text = ""
        for coin, value in data.items():
            text += f"{coin.capitalize()}: ${value['usd']}\n"
    price_label.config(text=text)

# Tkinter window
root = tk.Tk()
root.title("Crypto Price Tracker")
root.geometry("500x600")

title = tk.Label(root, text="📈 Crypto Price Tracker", font=("Arial", 16, "bold"))
title.pack(pady=10)

price_label = tk.Label(root, text="", font=("Arial", 12))
price_label.pack(pady=10)

btn_refresh = tk.Button(root, text="Refresh Prices", command=refresh_prices)
btn_refresh.pack(pady=5)

btn_graph = tk.Button(root, text="Show Bitcoin Graph", command=show_graph)
btn_graph.pack(pady=20)

root.mainloop()

def refresh_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin,ethereum,dogecoin,cardano,solana",
            "vs_currencies": "usd"
        }
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        if not data:
            raise Exception("Empty data")
        text = ""
        for coin, value in data.items():
            text += f"{coin.capitalize()}: ${value['usd']}\n"
    except:
        # Fallback dummy prices
        text = "⚠️ Could not fetch live data\nUsing dummy prices\n"
        dummy = {"Bitcoin": 112000, "Ethereum": 4600, "Dogecoin": 0.22, "Cardano": 0.87, "Solana": 215}
        for coin, value in dummy.items():
            text += f"{coin}: ${value}\n"

    price_label.config(text=text)
  
  #UI/UX
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import requests
import random

# -------- Prices Function --------
def get_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids":"bitcoin,ethereum,dogecoin,cardano,solana","vs_currencies":"usd"}
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        if not data:
            raise Exception("Empty data")
        text = ""
        for coin, value in data.items():
            text += f"{coin.capitalize()}: ${value['usd']}\n"
        return text
    except:
        dummy = {"Bitcoin":112000, "Ethereum":4600, "Dogecoin":0.22, "Cardano":0.87, "Solana":215}
        text = "⚠️ Could not fetch live data\nUsing dummy prices\n"
        for coin, value in dummy.items():
            text += f"{coin}: ${value}\n"
        return text

def refresh_prices():
    price_label.config(text=get_prices())

# -------- Graph Function --------
def show_graph():
    coin = coin_var.get()
    base = {"Bitcoin":112000, "Ethereum":4600, "Dogecoin":0.22, "Cardano":0.87, "Solana":215}
    prices = [base.get(coin, 100)]
    for _ in range(23):
        change = random.uniform(-0.1*prices[-1],0.1*prices[-1])
        prices.append(max(prices[-1]+change,0))

    fig = Figure(figsize=(6,3), dpi=100)
    plot = fig.add_subplot(111)
    plot.plot(prices, color="#1f77b4", marker="o")
    plot.set_title(f"{coin} Price (Dummy 24h)", fontsize=14)
    plot.set_xlabel("Time (hourly)", fontsize=12)
    plot.set_ylabel("Price in USD", fontsize=12)
    plot.grid(True, linestyle="--", alpha=0.6)

    global canvas
    try:
        canvas.get_tk_widget().pack_forget()
    except:
        pass
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=5)

# -------- Save Graph Function --------
def save_graph():
    try:
        file = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files","*.png")])
        if file:
            canvas.figure.savefig(file)
    except:
        pass

# -------- Hover Effect --------
def on_enter(e):
    e.widget['background'] = '#16a085'
def on_leave(e):
    e.widget['background'] = '#1abc9c'

# -------- Tkinter Window --------
root = tk.Tk()
root.title("📈 Attractive Crypto Tracker")
root.geometry("700x700")
root.configure(bg="#ecf0f1")

# Header
header = tk.Label(root, text="📈 Crypto Tracker", font=("Helvetica", 24, "bold"), bg="#34495e", fg="white", pady=10)
header.pack(fill="x")

# Prices Frame
prices_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="ridge")
prices_frame.pack(pady=15, padx=20, fill="x")
price_label = tk.Label(prices_frame, text=get_prices(), font=("Helvetica", 12), bg="#ffffff", justify="left")
price_label.pack(pady=10, padx=10)

# Control Frame
control_frame = tk.Frame(root, bg="#ecf0f1")
control_frame.pack(pady=10)

coin_var = tk.StringVar(value="Bitcoin")
coin_dropdown = tk.OptionMenu(control_frame, coin_var, "Bitcoin","Ethereum","Dogecoin","Cardano","Solana")
coin_dropdown.config(width=12, font=("Helvetica",12), bg="#1abc9c", fg="white", bd=0)
coin_dropdown["menu"].config(bg="#1abc9c", fg="white")
coin_dropdown.grid(row=0, column=0, padx=10)

btn_refresh = tk.Button(control_frame, text="Refresh Prices", command=refresh_prices, bg="#1abc9c", fg="white", font=("Helvetica",12,"bold"), bd=0, width=15)
btn_refresh.grid(row=0, column=1, padx=10)
btn_refresh.bind("<Enter>", on_enter)
btn_refresh.bind("<Leave>", on_leave)

btn_graph = tk.Button(control_frame, text="Show Graph", command=show_graph, bg="#3498db", fg="white", font=("Helvetica",12,"bold"), bd=0, width=15)
btn_graph.grid(row=0, column=2, padx=10)
btn_graph.bind("<Enter>", lambda e: e.widget.config(bg="#2980b9"))
btn_graph.bind("<Leave>", lambda e: e.widget.config(bg="#3498db"))

btn_save = tk.Button(control_frame, text="Save Graph", command=save_graph, bg="#e67e22", fg="white", font=("Helvetica",12,"bold"), bd=0, width=15)
btn_save.grid(row=0, column=3, padx=10)
btn_save.bind("<Enter>", lambda e: e.widget.config(bg="#d35400"))
btn_save.bind("<Leave>", lambda e: e.widget.config(bg="#e67e22"))

# Graph Frame
graph_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="ridge")
graph_frame.pack(pady=10, padx=20, fill="both", expand=True)

root.mainloop()

