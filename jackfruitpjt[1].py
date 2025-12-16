import tkinter as tk
from tkinter import messagebox
import threading
import time
import random

BOTS = ["Alex", "John", "Rahul", "Sara"]
users_db = {}  # username : password


class AuctionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auction System")
        self.root.geometry("600x650")

        self.current_bid = 0
        self.highest_bidder = "None"
        self.time_left = 0
        self.user_purse = 0
        self.bots_purse = {}

        self.login_page()

    # ---------------- LOGIN PAGE ----------------
    def login_page(self):
        self.clear()
        tk.Label(self.root, text="LOGIN", font=("Arial", 20)).pack(pady=20)

        tk.Label(self.root, text="Username").pack()
        self.login_user = tk.Entry(self.root)
        self.login_user.pack()

        tk.Label(self.root, text="Password").pack()
        self.login_pass = tk.Entry(self.root, show="*")
        self.login_pass.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)
        tk.Button(self.root, text="Register", command=self.register_page).pack()

    def login(self):
        username = self.login_user.get()
        password = self.login_pass.get()

        if username not in users_db:
            messagebox.showerror("Error", "User not registered")
        elif users_db[username] != password:
            messagebox.showerror("Error", "Password is wrong")
        else:
            self.current_user = username
            self.setup_page()

    # ---------------- REGISTER PAGE ----------------
    def register_page(self):
        self.clear()
        tk.Label(self.root, text="REGISTER", font=("Arial", 20)).pack(pady=20)

        tk.Label(self.root, text="Username").pack()
        self.reg_user = tk.Entry(self.root)
        self.reg_user.pack()

        tk.Label(self.root, text="Password").pack()
        self.reg_pass = tk.Entry(self.root, show="*")
        self.reg_pass.pack()

        tk.Button(self.root, text="Create Account", command=self.register).pack(pady=10)
        tk.Button(self.root, text="Back to Login", command=self.login_page).pack()

    def register(self):
        username = self.reg_user.get()
        password = self.reg_pass.get()

        if not username or not password:
            messagebox.showerror("Error", "Fields cannot be empty")
        elif username in users_db:
            messagebox.showerror("Error", "User already exists")
        else:
            users_db[username] = password
            messagebox.showinfo("Success", "Registration successful")
            self.login_page()

    # ---------------- SETUP PAGE ----------------
    def setup_page(self):
        self.clear()
        tk.Label(self.root, text="Auction Setup", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.root, text="Item Name").pack()
        self.item_entry = tk.Entry(self.root)
        self.item_entry.pack()

        tk.Label(self.root, text="Base Price").pack()
        self.base_price_entry = tk.Entry(self.root)
        self.base_price_entry.pack()

        tk.Label(self.root, text="Auction Time (seconds)").pack()
        self.time_entry = tk.Entry(self.root)
        self.time_entry.pack()

        tk.Label(self.root, text="Your Purse Amount").pack()
        self.user_purse_entry = tk.Entry(self.root)
        self.user_purse_entry.pack()

        self.bot_entries = {}
        tk.Label(self.root, text="Bot Purse Amounts", font=("Arial", 14)).pack(pady=10)

        for bot in BOTS:
            tk.Label(self.root, text=f"{bot} Purse").pack()
            entry = tk.Entry(self.root)
            entry.pack()
            self.bot_entries[bot] = entry

        tk.Button(self.root, text="Start Auction", command=self.start_auction).pack(pady=20)

    # ---------------- START AUCTION ----------------
    def start_auction(self):
        try:
            self.item_name = self.item_entry.get()
            self.current_bid = int(self.base_price_entry.get())
            self.time_left = int(self.time_entry.get())
            self.user_purse = int(self.user_purse_entry.get())

            self.bots_purse = {}
            for bot in BOTS:
                self.bots_purse[bot] = int(self.bot_entries[bot].get())

            if not self.item_name:
                raise ValueError

        except:
            messagebox.showerror("Error", "Invalid input")
            return

        self.highest_bidder = "None"
        self.auction_page()

        threading.Thread(target=self.bot_bidding, daemon=True).start()
        self.update_timer()

    # ---------------- AUCTION PAGE ----------------
    def auction_page(self):
        self.clear()
        tk.Label(self.root, text="LIVE AUCTION", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.root, text=f"Item: {self.item_name}", font=("Arial", 14)).pack()

        self.bid_label = tk.Label(self.root, text=f"Current Bid: ₹{self.current_bid}")
        self.bid_label.pack()

        self.bidder_label = tk.Label(self.root, text=f"Highest Bidder: {self.highest_bidder}")
        self.bidder_label.pack()

        self.timer_label = tk.Label(self.root, text=f"Time Left: {self.time_left}s")
        self.timer_label.pack(pady=10)

        self.purse_label = tk.Label(self.root, text=f"Your Purse: ₹{self.user_purse}")
        self.purse_label.pack()

        tk.Label(self.root, text="Enter Your Bid Amount").pack()
        self.bid_entry = tk.Entry(self.root)
        self.bid_entry.pack()

        tk.Button(self.root, text="Place Bid", command=self.user_bid).pack(pady=10)

    # ---------------- USER BID ----------------
    def user_bid(self):
        try:
            bid_amount = int(self.bid_entry.get())
        except:
            messagebox.showerror("Error", "Enter a valid number")
            return

        if bid_amount <= self.current_bid:
            messagebox.showerror("Error", "Bid must be higher than current bid")
        elif bid_amount > self.user_purse:
            messagebox.showerror("Error", "Insufficient purse")
        else:
            self.user_purse -= (bid_amount - self.current_bid)
            self.current_bid = bid_amount
            self.highest_bidder = self.current_user
            self.refresh()

    # ---------------- BOT BIDDING ----------------
    def bot_bidding(self):
        while self.time_left > 0:
            time.sleep(random.randint(2, 4))
            bot = random.choice(BOTS)

            if self.bots_purse[bot] > self.current_bid:
                bid = self.current_bid + random.randint(200, 1000)
                if bid <= self.bots_purse[bot]:
                    self.bots_purse[bot] -= (bid - self.current_bid)
                    self.current_bid = bid
                    self.highest_bidder = bot
                    self.refresh()

    # ---------------- TIMER ----------------
    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time Left: {self.time_left}s")
            self.root.after(1000, self.update_timer)
        else:
            messagebox.showinfo(
                "Auction Ended",
                f"Item: {self.item_name}\nWinner: {self.highest_bidder}\nWinning Bid: ₹{self.current_bid}"
            )
            self.login_page()

    # ---------------- UTIL ----------------
    def refresh(self):
        self.bid_label.config(text=f"Current Bid: ₹{self.current_bid}")
        self.bidder_label.config(text=f"Highest Bidder: {self.highest_bidder}")
        self.purse_label.config(text=f"Your Purse: ₹{self.user_purse}")

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# ---------------- RUN APP ----------------
root = tk.Tk()
app = AuctionApp(root)
root.mainloop()
