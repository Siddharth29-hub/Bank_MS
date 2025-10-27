# ==========================================
#   Bank Account Management System
#   Author: Siddharth Sharma
#   Technologies: Python, OOP, Exception Handling, File Handling
# ==========================================

import json
import os


# ================================
# Base Class - BankAccount
# ================================
class BankAccount:
    def __init__(self, account_number, name, balance=0.0):
        self.account_number = account_number
        self.name = name
        self.__balance = balance  # Private variable for encapsulation

    # ---------- Encapsulation (Private Variable Access via Methods) ----------
    def deposit(self, amount):
        """Deposit money into account"""
        try:
            if amount <= 0:
                raise ValueError("Deposit amount must be positive.")
            self.__balance += amount
            print(f"₹{amount} deposited successfully!")
        except ValueError as e:
            print("Error:", e)

    def withdraw(self, amount):
        """Withdraw money from account"""
        try:
            if amount <= 0:
                raise ValueError("Withdrawal amount must be positive.")
            if amount > self.__balance:
                raise ValueError("Insufficient balance!")
            self.__balance -= amount
            print(f"₹{amount} withdrawn successfully!")
        except ValueError as e:
            print("Error:", e)

    def get_balance(self):
        """Abstraction: Only method can access private balance"""
        return self.__balance

    def display_account_info(self):
        """Display account details"""
        print("\n===== Account Details =====")
        print(f"Account Number: {self.account_number}")
        print(f"Account Holder: {self.name}")
        print(f"Current Balance: ₹{self.__balance:.2f}")
        print("===========================\n")

    # ---------- File Handling ----------
    def save_to_file(self):
        """Save account data to JSON file"""
        data = {
            "type": "BankAccount",
            "account_number": self.account_number,
            "name": self.name,
            "balance": self.__balance
        }
        with open(f"{self.account_number}.json", "w") as file:
            json.dump(data, file, indent=4)
        print("Account data saved successfully!")

    @staticmethod
    def load_from_file(account_number):
        """Load account data dynamically as BankAccount or SavingsAccount"""
        filename = f"{account_number}.json"
        if os.path.exists(filename):
            with open(filename, "r") as file:
                data = json.load(file)
                # Dynamic object creation based on type
                if data.get("type") == "SavingsAccount":
                    return SavingsAccount(
                        data["account_number"],
                        data["name"],
                        data["balance"],
                        data.get("interest_rate", 0.05)
                    )
                else:
                    return BankAccount(
                        data["account_number"],
                        data["name"],
                        data["balance"]
                    )
        else:
            print("Account not found!")
            return None


# ================================
# Derived Class - SavingsAccount (Inheritance + Polymorphism)
# ================================
class SavingsAccount(BankAccount):
    def __init__(self, account_number, name, balance=0.0, interest_rate=0.05):
        super().__init__(account_number, name, balance)
        self.interest_rate = interest_rate

    def calculate_interest(self):
        """Polymorphism: Additional feature for SavingsAccount"""
        interest = self.get_balance() * self.interest_rate
        print(f"Annual Interest (@{self.interest_rate*100:.0f}%): ₹{interest:.2f}")
        return interest

    def save_to_file(self):
        """Override: Save with account type and interest rate"""
        data = {
            "type": "SavingsAccount",
            "account_number": self.account_number,
            "name": self.name,
            "balance": self.get_balance(),
            "interest_rate": self.interest_rate
        }
        with open(f"{self.account_number}.json", "w") as file:
            json.dump(data, file, indent=4)
        print("Savings account data saved successfully!")


# ================================
# Utility Functions (Modular Programming)
# ================================
def create_account():
    print("\n=== Create New Account ===")
    acc_num = input("Enter Account Number: ")
    name = input("Enter Account Holder Name: ")

    try:
        initial_deposit = float(input("Enter Initial Deposit Amount: ₹"))
        print("\n1. Normal Bank Account\n2. Savings Account (5% Interest)")
        acc_type = input("Choose Account Type (1 or 2): ")

        if acc_type == '2':
            account = SavingsAccount(acc_num, name, initial_deposit)
        else:
            account = BankAccount(acc_num, name, initial_deposit)

        account.save_to_file()
        print(f"Account for {name} created successfully!")

    except ValueError:
        print("Please enter a valid numeric amount!")


def deposit_money():
    acc_num = input("\nEnter Account Number: ")
    account = BankAccount.load_from_file(acc_num)
    if account:
        try:
            amount = float(input("Enter amount to deposit: ₹"))
            account.deposit(amount)
            account.save_to_file()
        except ValueError:
            print("Please enter a valid numeric amount!")


def withdraw_money():
    acc_num = input("\nEnter Account Number: ")
    account = BankAccount.load_from_file(acc_num)
    if account:
        try:
            amount = float(input("Enter amount to withdraw: ₹"))
            account.withdraw(amount)
            account.save_to_file()
        except ValueError:
            print("Please enter a valid numeric amount!")


def check_balance():
    acc_num = input("\nEnter Account Number: ")
    account = BankAccount.load_from_file(acc_num)
    if account:
        account.display_account_info()


def calculate_interest():
    acc_num = input("\nEnter Account Number: ")
    account = BankAccount.load_from_file(acc_num)
    if account and isinstance(account, SavingsAccount):
        account.calculate_interest()
    else:
        print("Interest calculation is only available for Savings Accounts!")


# ================================
# Main Program (Menu Driven)
# ================================
def main():
    while True:
        print("""
========================================
   Welcome to Bank Account Management
========================================
1. Create New Account
2. Deposit Money
3. Withdraw Money
4. Check Account Balance
5. Calculate Interest (Savings Account)
6. Exit
========================================
""")
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            create_account()
        elif choice == '2':
            deposit_money()
        elif choice == '3':
            withdraw_money()
        elif choice == '4':
            check_balance()
        elif choice == '5':
            calculate_interest()
        elif choice == '6':
            print("Thank you for using our banking system. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 6.")


# ================================
# Entry Point
# ================================
if __name__ == "__main__":
    main()
