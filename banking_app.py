import os
import datetime
import getpass

# Get the current date and time
date_time = datetime.datetime.now()

# Dictionaries to store account, customer, and transaction details
accounts = {}
customer_details = {}
transactions = {}

# Starting account number for new accounts
account_number = 550000

# admin credentials
Admin_username = "admin"
Admin_password = "admin123"

# Save all accounts to a file
def save_accounts():
    with open("accounts.txt", "w") as file:
        for acc_num, details in accounts.items():
            file.write(f"{acc_num},{details['name']},{details['balance']},{details['datetime']}\n")

# Load accounts from file
def load_accounts():
    if os.path.exists("accounts.txt"):
        with open("accounts.txt", "r") as file:
            for line in file:
                acc_num, name, balance, datetime = line.strip().split(",")
                accounts[acc_num] = {
                    "name": name,
                    "balance": int(balance),
                    "datetime": datetime
                }
       
# Save all customer details to a file
def save_customer_details():
    with open("customer_details.txt", "w") as file:
        for acc_num, details in customer_details.items():
            file.write(f"{acc_num},{details['name']},{details['National_ID']},{details['password']},{details['balance']},{details['datetime']}\n")

# Load customer details from file
def load_customer_details():
    if os.path.exists("customer_details.txt"):
        with open("customer_details.txt", "r") as file:
            for line in file:
                acc_num, name, National_ID, password, balance, datetime = line.strip().split(",")
                customer_details[acc_num] = {
                    "name": name,
                    "National_ID": National_ID,
                    "password": password,
                    "balance": int(balance),
                    "datetime": datetime
                }
    
# Save all transaction histories to a file
def save_transactions():
    with open("transactions.txt", "w") as file:
        for acc_num, trans_list in transactions.items():  # Proper unpacking
            for transaction in trans_list:
                file.write(f"{acc_num},{transaction}\n")

# Load transaction histories from file
def load_transactions():
    if os.path.exists("transactions.txt"):
        with open("transactions.txt", "r") as file:
            for line in file:
                acc_num, transaction = line.strip().split(",", 1)
                if acc_num not in transactions:
                    transactions[acc_num] = []
                transactions[acc_num].append(transaction)

# Generate the next account number        
def get_next_account_number():
    if accounts:
        return max(map(int, accounts.keys())) + 1
    else:
        return 550001
    
# Main login function for both admin and customers
def login():
    load_accounts()
    load_customer_details()
    load_transactions()
    while True:
        print("------------------------------------------------------------------------------------")
        print("------------------------Welcome to the Banking System-------------------------------")
        print("------------------------------------------------------------------------------------")
        print("\n1. Admin Login")
        print("2. Customer Login")
        print("3. Exit\n")
        choice = input("Choose login type:").strip()
        print("\n")
        print("------------------------------------------------------------------------------------")
        print("------------------------------------------------------------------------------------")
        print("------------------------------------------------------------------------------------")


        if choice == '1':
            access="admin"
            username = input("\nEnter Admin username: ").strip()
            password = getpass.getpass("Enter Admin password: ").strip()
            if username == Admin_username and password == Admin_password:
                print("------------------------------------------------------------------------------------")
                print("----------------------------Admin login successful----------------------------------")
                print("------------------------------------------------------------------------------------")
                print("\n")
                admin_menu(access)
                break
            else:
                print("-------------------------------------------------------------------------------------")
                print("----------------------------Invalid admin credentials--------------------------------")
                print("-------------------------------------------------------------------------------------")
        elif choice == '2':
            try:
                access="customer"
                acc_num = input("\nEnter your account number: ").strip()
                password = getpass.getpass("Enter your password:").strip()
                if acc_num in customer_details and customer_details[acc_num]["password"] == password:
                    print("------------------------------------------------------------------------------------")
                    print("----------------------------Customer login successful-------------------------------")
                    print("------------------------------------------------------------------------------------")
                    customer_menu(acc_num,access)
                    break
                else:
                    print("------------------------------------------------------------------------------------")
                    print("----------------------------Invalid account number or password----------------------")
                    print("------------------------------------------------------------------------------------")
            except ValueError:
                print("Invalid input.")
        elif choice == '3':
            print("-------------------------------------------------------------------------------------")
            print("----------------------------Exiting the Banking System-------------------------------")
            print("-------------------------------------------------------------------------------------")   
            break
        else:
            print("-------------------------------------------------------------------------------------")  
            print("----------------------------Invalid choice-------------------------------------------")
            print("-------------------------------------------------------------------------------------")

# Menu for admin operations
def admin_menu(access):
    while True:
        print("Admin Menu")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Show Balance")
        print("5. Transaction History")
        print("6. Logout")
        choice = input("Choose an option:(1-6) ").strip()
        print("\n")
        if choice == '1':
            create_account()
        elif choice == '2':
            deposit_money(None,access)
        elif choice == '3':
            withdraw_money(None,access)
        elif choice == '4':
            show_balance(None,access)
        elif choice == '5':
            transaction_history(None,access)
        elif choice == '6':
            print("Logging out...")
            login()
        else:
            print("Invalid choice.")

# Menu for customer operations
def customer_menu(acc_num,access):
    while True:
        print("\nCustomer Menu")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Account to Account Transfer")
        print("4. Show Balance")
        print("5. Transaction History")
        print("6. Logout\n")
        choice = input("Choose an option:(1-6) ").strip()
        print("\n")
        if choice == '1':
            deposit_money(acc_num,access)
        elif choice == '2':
            withdraw_money(acc_num,access)
        elif choice == '3':
            account_to_account_transfer(acc_num,access)
        elif choice == '4':
            show_balance(acc_num)
        elif choice == '5':
            transaction_history(acc_num)
        elif choice == '6':
            print("-------------------------------------------------------------------------------------")
            print("----------------------------Logging out----------------------------------------------")
            print("-------------------------------------------------------------------------------------")
            login()
        else:
            print("Invalid choice.")

# Create a new account (admin only)
def create_account():
    print("------------------------------------------------------------------------------------")
    print("----------------------------Create New Account--------------------------------------")
    print("------------------------------------------------------------------------------------")

    name = input("Enter your name: ").strip()
    National_ID = input("Enter your National ID Card Number: ").strip()
    password = input("Enter your password: ").strip()
    initial_balance = int(input("Enter initial deposit amount: "))

    if initial_balance < 0:
        print("-------------------------------------------------------------------------------------")  
        print("--------------------------Initial deposit cannot be negative-------------------------")
        print("-------------------------------------------------------------------------------------")
        return

    acc_num = str(get_next_account_number())

    # Store new customer details
    customer_details[acc_num] = {
        "name": name,
        "National_ID": National_ID,
        "password": password,
        "balance": initial_balance,
        "datetime":date_time.strftime('%x %X')
    }

    # Store new account details
    accounts[acc_num] = {
        "name": name,
        "balance": initial_balance,
        "datetime":date_time.strftime('%x %X'),
    }
    # Initialize transaction history for the account
    transactions[acc_num] = [f"{date_time.strftime('%x %X')} - Deposited: {initial_balance}, Balance: {initial_balance}, Access: admin"]
    
    # Save all data to files
    save_accounts()
    save_customer_details()
    save_transactions
    print("-------------------------------------------------------------------------------------")
    print(f"Account created successfully. Your account number is {acc_num}.")
    print(f"Account password is {password}.")
    print(f"Initial balance is {initial_balance}.")
    print("-------------------------------------------------------------------------------------")

# Deposit money into an account (admin or customer)
def deposit_money(acc_num=None,access=None):
    print("------------------------------------------------------------------------------------")
    print("----------------------------Deposit Money-------------------------------------------")
    print("------------------------------------------------------------------------------------")
    deposit_acnum = input("Enter your account number: ").strip()
    if acc_num == deposit_acnum or access == "admin":
        acc_num=deposit_acnum
        try:
            amount = int(input("Enter amount to deposit: "))
            if acc_num in accounts and amount > 0:
                accounts[acc_num]["balance"] += amount
                transactions[acc_num].append(f"{date_time.strftime('%x %X')} - Deposited: {amount}, Balance: {accounts[acc_num]['balance']}, Access:{access}")
                save_accounts()
                save_transactions()
                print("-------------------------------------------------------------------------------------")
                print(f"Deposited {amount} to account {acc_num}. New balance: {accounts[acc_num]['balance']}")
                print("-------------------------------------------------------------------------------------")
        except ValueError:
                print("-------------------------------------------------------------------------------------")
                print("---------------------------------Invalid input---------------------------------------")
                print("-------------------------------------------------------------------------------------")
                
    else:
        print("-------------------------------------------------------------------------------------")
        print("----------------------------Invalid account number-----------------------------------")
        print("-------------------------------------------------------------------------------------")

# Withdraw money from an account (admin or customer)
def withdraw_money(acc_num=None,access=None):
    print("------------------------------------------------------------------------------------")
    print("----------------------------Withdraw Money------------------------------------------")
    print("------------------------------------------------------------------------------------")
    withdraw_acnum = input("Enter your account number: ").strip()
    if acc_num== withdraw_acnum or access =="admin":
        try:
            acc_num=withdraw_acnum
            amount = int(input("Enter amount to withdraw: "))
            if acc_num in accounts and 0 < amount <= accounts[acc_num]["balance"]:
                accounts[acc_num]["balance"] -= amount
                transactions[acc_num].append(f"{date_time.strftime('%x %X')} - Withdrawn: {amount}, Balance: {accounts[acc_num]['balance']}, Access: {access}")
                save_accounts()
                save_transactions()
                print("-------------------------------------------------------------------------------------")
                print(f"Withdrew {amount} from account {acc_num}. New balance: {accounts[acc_num]['balance']}")
                print("-------------------------------------------------------------------------------------")
            else:
                print("-------------------------------------------------------------------------------------")
                print("-------------------------------insufficient balance----------------------------------")
                print("-------------------------------------------------------------------------------------")  
        except ValueError:
            print("Invalid input.")
    else:
        print("-------------------------------------------------------------------------------------")
        print("-------------------------------Invalid account number--------------------------------")
        print("-------------------------------------------------------------------------------------")

# Transfer money between accounts (customer)
def account_to_account_transfer(acc_num=None,access=None):
    print("-------------------------------------------------------------------------------------")
    print("----------------------------Account to Account Transfer------------------------------")
    print("-------------------------------------------------------------------------------------")
    from_acc_num = input("Enter your account number: ").strip()
    if acc_num==from_acc_num or access=="admin": 
        try:
            to_acc_num = input("Enter the account number to transfer to: ").strip()
            amount = int(input("Enter amount to transfer: "))

            if from_acc_num in accounts and to_acc_num in accounts and 0 < amount <= accounts[from_acc_num]["balance"]:
                accounts[from_acc_num]["balance"] -= amount
                accounts[to_acc_num]["balance"] += amount
                transactions[from_acc_num].append(f"{date_time.strftime('%x %X')} - Transferred Rs.{amount} to account {to_acc_num},balance: {accounts[from_acc_num]['balance']}")
                transactions[to_acc_num].append(f"{date_time.strftime('%x %X')} - Received Rs.{amount} from account {from_acc_num},balance: {accounts[to_acc_num]['balance']}")
                save_accounts()
                save_transactions()
                print("-------------------------------------------------------------------------------------")
                print(f"Transferred {amount} from account {from_acc_num} to account {to_acc_num}.")
                print("-------------------------------------------------------------------------------------")
            else:
                print("-------------------------------------------------------------------------------------")
                print("---------------------------- insufficient balance -----------------------------------")
                print("-------------------------------------------------------------------------------------")
        except ValueError:
            print("-------------------------------------------------------------------------------------")
            print("-------------------------------- Invalid input --------------------------------------")
            print("-------------------------------------------------------------------------------------")
            
    else:
        print("-------------------------------------------------------------------------------------")
        print("----------------------------Invalid account numbers----------------------------------")
        print("-------------------------------------------------------------------------------------")
        
# Show balance of an account (admin or customer)
def show_balance(acc_num=None,access=None):
    print("------------------------------------------------------------------------------------")
    print("----------------------------Show Balance--------------------------------------------")
    print("------------------------------------------------------------------------------------")

    show_num = input("Enter your account number: ").strip()
    if acc_num== show_num or access=="admin":
        try:
            if show_num in accounts:
                print("-------------------------------------------------------------------------------------")
                print(f"Account {show_num} balance: {accounts[show_num]['balance']}") 
                print("-------------------------------------------------------------------------------------")
        except ValueError:
            print("-------------------------------------------------------------------------------------")
            print("-------------------------------- Invalid input --------------------------------------")
            print("-------------------------------------------------------------------------------------")
            print("Invalid input.")
    else:
        print("-------------------------------------------------------------------------------------")
        print("----------------------------Invalid account number-----------------------------------")
        print("-------------------------------------------------------------------------------------")

# Show transaction history of an account (admin or customer)
def transaction_history(acc_num=None,access=None):
    print("------------------------------------------------------------------------------------")
    print("----------------------------Transaction History-------------------------------------")
    print("------------------------------------------------------------------------------------")
    transaction_acc=input("Enter your account number: ").strip()
    if acc_num== transaction_acc or access=="admin":
        acc_num=transaction_acc
        if acc_num in accounts:
            print("-------------------------------------------------------------------------------------")
            print(f"Transaction history for account {acc_num}:")
            print("-------------------------------------------------------------------------------------")
            for transaction in transactions[acc_num]:
                print(transaction)
    else:
        print("-------------------------------------------------------------------------------------")
        print("----------------------------Invalid account number-----------------------------------")
        print("-------------------------------------------------------------------------------------")

# Start the application by calling the login function
login()

