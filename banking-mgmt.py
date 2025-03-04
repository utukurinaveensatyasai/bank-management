import json
import os
import getpass
import tkinter as tk
from tkinter import messagebox

FILE_NAME = "accounts.json"

# Load accounts from JSON
def load_accounts():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return {}

# Save accounts to JSON
def save_accounts(accounts):
    with open(FILE_NAME, "w") as file:
        json.dump(accounts, file, indent=4)

# GUI Class for Bank System
class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Management System")
        self.root.geometry("400x500")
        self.accounts = load_accounts()

        self.main_menu()

    def main_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="🏦 Welcome to the Bank", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Login", command=self.login_screen, width=20).pack(pady=5)
        tk.Button(self.root, text="Create Account", command=self.create_account_screen, width=20).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit, width=20).pack(pady=5)

    def login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="🔐 Login", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Account Number").pack()
        self.acc_number = tk.Entry(self.root)
        self.acc_number.pack()

        tk.Label(self.root, text="Password").pack()
        self.password = tk.Entry(self.root, show="*")
        self.password.pack()

        tk.Button(self.root, text="Login", command=self.login, width=15).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu, width=15).pack()

    def create_account_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="🆕 Create Account", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Account Number").pack()
        self.new_acc_number = tk.Entry(self.root)
        self.new_acc_number.pack()

        tk.Label(self.root, text="Account Holder Name").pack()
        self.new_acc_holder = tk.Entry(self.root)
        self.new_acc_holder.pack()

        tk.Label(self.root, text="Set Password").pack()
        self.new_password = tk.Entry(self.root, show="*")
        self.new_password.pack()

        tk.Button(self.root, text="Create", command=self.create_account, width=15).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu, width=15).pack()

    def login(self):
        acc_number = self.acc_number.get()
        password = self.password.get()

        if acc_number in self.accounts and self.accounts[acc_number]["password"] == password:
            self.current_account = acc_number
            self.account_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid Account Number or Password")

    def create_account(self):
        acc_number = self.new_acc_number.get()
        acc_holder = self.new_acc_holder.get()
        password = self.new_password.get()

        if acc_number in self.accounts:
            messagebox.showerror("Error", "Account Number Already Exists")
        else:
            self.accounts[acc_number] = {
                "account_holder": acc_holder,
                "password": password,
                "balance": 0,
                "transactions": []
            }
            save_accounts(self.accounts)
            messagebox.showinfo("Success", "Account Created Successfully!")
            self.main_menu()

    def account_menu(self):
        self.clear_screen()
        tk.Label(self.root, text=f"🏦 Welcome, {self.accounts[self.current_account]['account_holder']}", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="Deposit Money", command=self.deposit_screen, width=20).pack(pady=5)
        tk.Button(self.root, text="Withdraw Money", command=self.withdraw_screen, width=20).pack(pady=5)
        tk.Button(self.root, text="Check Balance", command=self.check_balance, width=20).pack(pady=5)
        tk.Button(self.root, text="Transaction History", command=self.show_transactions, width=20).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.main_menu, width=20).pack(pady=10)

    def deposit_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="💰 Deposit Money", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Amount").pack()
        self.deposit_amount = tk.Entry(self.root)
        self.deposit_amount.pack()
        tk.Button(self.root, text="Deposit", command=self.deposit, width=15).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.account_menu, width=15).pack()

    def deposit(self):
        amount = float(self.deposit_amount.get())
        self.accounts[self.current_account]["balance"] += amount
        self.accounts[self.current_account]["transactions"].append(f"Deposited: ₹{amount}")
        save_accounts(self.accounts)
        messagebox.showinfo("Success", "Amount Deposited Successfully")
        self.account_menu()

    def withdraw_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="💸 Withdraw Money", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Amount").pack()
        self.withdraw_amount = tk.Entry(self.root)
        self.withdraw_amount.pack()
        tk.Button(self.root, text="Withdraw", command=self.withdraw, width=15).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.account_menu, width=15).pack()

    def withdraw(self):
        amount = float(self.withdraw_amount.get())
        if amount > self.accounts[self.current_account]["balance"]:
            messagebox.showerror("Error", "Insufficient Balance")
        else:
            self.accounts[self.current_account]["balance"] -= amount
            self.accounts[self.current_account]["transactions"].append(f"Withdrawn: ₹{amount}")
            save_accounts(self.accounts)
            messagebox.showinfo("Success", "Amount Withdrawn Successfully")
        self.account_menu()

    def check_balance(self):
        balance = self.accounts[self.current_account]["balance"]
        messagebox.showinfo("Balance", f"Your Balance: ₹{balance}")

    def show_transactions(self):
        transactions = self.accounts[self.current_account]["transactions"]
        history = "\n".join(transactions) if transactions else "No Transactions Yet"
        messagebox.showinfo("Transactions", history)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Run GUI
root = tk.Tk()
app = BankApp(root)
root.mainloop()
