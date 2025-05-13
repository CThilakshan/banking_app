import os
import datetime
import getpass
import hashlib


# Get the current date and time
from datetime import datetime
date_time = datetime.now()

# Dictionaries to store account, customer, and transaction details
accounts = {}
customer_details = {}
transactions = {}
transactions_details={}
users={}

# Starting account number for new accounts
account_number = 550000
customer_number= "customer_0000"
transaction_number= "transaction_0000"
user_number= "user_0000"

# admin credentials
Admin_username = "admin"
Admin_password = "admin123"

# Function for password encryption
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

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
            file.write(f"{acc_num},{details['customer_num']},{details['name']},{details['National_ID']},{details['password']},{details['balance']},{details['datetime']}\n")

# Load customer details from file
def load_customer_details():
    if os.path.exists("customer_details.txt"):
        with open("customer_details.txt", "r") as file:
            for line in file:
                acc_num, customer_id, name, National_ID, password, balance, datetime = line.strip().split(",")
                customer_details[acc_num] = {
                    "customer_id": customer_id,
                    "name": name,
                    "National_ID": National_ID,
                    "password": password,
                    "balance": int(balance),
                    "datetime": datetime
                }
    
# Save all transaction histories to a file
def save_transactions():
    with open("transactions.txt", "w") as file:
        for acc_num, trans_list in transactions.items():  
            for transaction in trans_list:
                file.write(f"{acc_num},{transaction}\n")
def load_transactions():
    if os.path.exists("transactions.txt"):
        with open("transactions.txt", "r") as file:
            for line in file:
                acc_num, transaction = line.strip().split(",", 1)
                if acc_num not in transactions:
                    transactions[acc_num] = []
                transactions[acc_num].append(transaction)

def save_transactions_details():
    with open("transactions_details.txt","w")as file:
        for transaction_id,details in transactions_details.items():
            file.write(f"{transaction_id},{details['acc_num']},{details['date_time']},{details['amount']},{details['Categary']},{details['balance']},{details['access']}\n")
def load_transactions_details():
    if os.path.exists("transactions_details.txt"):
        with open("transactions_details.txt","r") as file:
            for line in file:
                acc_num,transaction_id,date_time,amount,categary,balance,access=line.strip().split(",")
                transactions_details[transaction_id] = {
                    "acc_num": acc_num,
                    "date_time": date_time,
                    "amount": int(amount),
                    "Categary": categary,
                    "balance": int(balance),
                    "access": access
                }

def save_users(user_id, access):
    user_id = str(get_next_user_number())
    from datetime import datetime
    now = datetime.now().strftime('%x %X')
    with open("users.txt", "a") as file:
        file.write(f"{user_id},{access},{now}\n")

def load_users():
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as file:
            for line in file:
                user_id, access, date_time = line.strip().split(",")
                users[user_id] = {
                    "access": access,
                    "date_time": date_time
                }


# Load transaction histories from file


# Generate the next account number        
def get_next_account_number():
    if accounts:
        return max(map(int, accounts.keys())) + 1
    else:
        return 550001
def get_next_customer_number():
    if customer_details:
        numbers = [int(key.replace("customer_", "")) for key in customer_details.keys()]
        next_num = max(numbers) + 1
    else:
        next_num = 1  
    return f"customer_{next_num:04d}" 
def get_next_transaction_number():
    if transactions_details:
        numbers = [int(key.replace("transaction_", "")) for key in transactions_details.keys()]
        next_num = max(numbers) + 1
    else:
        next_num = 1  
    return f"transaction_{next_num:04d}"
def get_next_user_number():
    if users:
        numbers = [int(key.replace("user_", "")) for key in users.keys()]
        next_num = max(numbers) + 1
    else:
        next_num = 1  
    return f"user_{next_num:04d}"

def user(access):
    from datetime import datetime
    user_id = str(get_next_user_number())
    now = datetime.now()
    users[user_id] = {
        "access": access,
        "date_time": now.strftime('%x %X')
    }
    save_users(user_id, access)


    
# Main login function for both admin and customers
def login():
    load_accounts()
    load_customer_details()
    load_transactions()
    load_transactions_details()
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
            print("Do worry your password will not be displayed")
            print("-------------------------------------------------------------------------------------")
            password = getpass.getpass("Enter Admin password: ").strip()
            if username == Admin_username and password == Admin_password:
                admin_menu(access)
                break
            else:
                print("-------------------------------------------------------------------------------------")
                print("----------------------------Invalid admin credentials--------------------------------")
                print("-------------------------------------------------------------------------------------")
                print("\n")
        elif choice == '2':
            try:
                access="customer"
                acc_num = input("\nEnter your account number: ").strip()
                print("Do worry your password will not be displayed")
                print("-------------------------------------------------------------------------------------")
                password = getpass.getpass("Enter your password:").strip()
                hashed_password = hash_password(password)
                if acc_num in customer_details and customer_details[acc_num]["password"] == hashed_password:
                    customer_menu(acc_num,access)
                    break
                else:
                    print("------------------------------------------------------------------------------------")
                    print("----------------------------Invalid account number or password----------------------")
                    print("------------------------------------------------------------------------------------")
                    print("\n")
            except ValueError:
                print("Invalid input.")
        elif choice == '3':
            try:
                print("-------------------------------------------------------------------------------------")
                print("----------------------------Exiting the Banking System-------------------------------")
                print("-------------------------------------------------------------------------------------")
                print("\n")
                break
            except ValueError:
                print("-------------------------------------------------------------------------------------")
                print("----------------------------   Invalid input  ---------------------------------------")
                print("-------------------------------------------------------------------------------------")
                print("\n")

        else:
            print("-------------------------------------------------------------------------------------")  
            print("------------------Invalid option! Please enter 1, 2, or 3----------------------------")
            print("-------------------------------------------------------------------------------------")
            print("\n")
# Menu for admin operations
def admin_menu(access):
    user(access)
    while True:
        print("------------------------------------------------------------------------------------")
        print("---------------------------------Admin Menu ----------------------------------------")
        print("------------------------------------------------------------------------------------")
        print("\n")
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
            print("\n")
            login()
            break
        else:
            print("Invalid choice.")

# Menu for customer operations
def customer_menu(acc_num,access):
    user(access)
    while True:
        print("------------------------------------------------------------------------------------")
        print("-----------------------------------Customer Menu------------------------------------")
        print("------------------------------------------------------------------------------------")
        print("\n")
        print("Customer Menu")
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
            print("\n")
            login()
            break
        else:
            print("Invalid choice.")

# Create a new account (admin only)
def create_account():
    print("------------------------------------------------------------------------------------")
    print("----------------------------Create New Account--------------------------------------")
    print("------------------------------------------------------------------------------------")
    print("\n")
    name = input("Enter your name: ").strip()
    National_ID = input("Enter your National ID Card Number: ").strip()
    password = input("Enter your password: ").strip()
    hashed_password = hash_password(password)
    initial_balance = int(input("Enter initial deposit amount: "))

    if initial_balance < 0:
        print("-------------------------------------------------------------------------------------")  
        print("--------------------------Initial deposit cannot be negative-------------------------")
        print("-------------------------------------------------------------------------------------")
        print("\n")
        return

    acc_num = str(get_next_account_number())
    customer_num = str(get_next_customer_number())
    transaction_num = str(get_next_transaction_number())
    # Store new customer details
    customer_details[acc_num] = {
        "customer_num": customer_num,
        "name": name,
        "National_ID": National_ID,
        "password": hashed_password,
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
    
    transactions_details[transaction_num] = {
        "acc_num": acc_num, 
        "date_time": date_time.strftime('%x %X'),
        "amount": initial_balance,
        "Categary": "Deposit",
        "balance": initial_balance,
        "access": "admin"
    }
    
    # Save all data to files
    save_accounts()
    save_customer_details()
    save_transactions()
    save_transactions_details()
    print("-------------------------------------------------------------------------------------")
    print(f"Account created successfully. Your account number is {acc_num}.")
    print(f"Account password is {password}.")
    print(f"Initial balance is {initial_balance}.")
    print("-------------------------------------------------------------------------------------")
    print("\n")

# Deposit money into an account (admin or customer)
def deposit_money(acc_num=None,access=None):
    print("------------------------------------------------------------------------------------")
    print("----------------------------Deposit Money-------------------------------------------")
    print("------------------------------------------------------------------------------------")
    print("\n")
    deposit_acnum = input("Enter your account number: ").strip()
    if acc_num == deposit_acnum or access == "admin":
        acc_num=deposit_acnum
        try:
            amount = int(input("Enter amount to deposit: "))
            if acc_num in accounts and amount > 0:
                transaction_num= str(get_next_transaction_number())
                accounts[acc_num]["balance"] += amount
                transactions[acc_num].append(f"{date_time.strftime('%x %X')} - Deposited: {amount}, Balance: {accounts[acc_num]['balance']}, Access:{access}")
                transactions_details[transaction_num] = {
                    "acc_num": acc_num,
                    "date_time": date_time.strftime('%x %X'),
                    "amount": amount,
                    "Categary": "Deposit",
                    "balance": accounts[acc_num]["balance"],
                    "access": access
                    }

                save_accounts()
                save_transactions()
                save_transactions_details()
                print("-------------------------------------------------------------------------------------")
                print(f"Deposited {amount} to account {acc_num}. New balance: {accounts[acc_num]['balance']}")
                print("-------------------------------------------------------------------------------------")
                print("\n")
            else:
                print("\n")
                print("-------------------------------------------------------------------------------------")
                print("----------------------------Invalid account number or amount------------------------")
                print("-------------------------------------------------------------------------------------")
                print("\n")
        except ValueError:
                print("-------------------------------------------------------------------------------------")
                print("---------------------------------Invalid input---------------------------------------")
                print("-------------------------------------------------------------------------------------")
                print("\n")
                
    else:
        print("-------------------------------------------------------------------------------------")
        print("----------------------------Invalid account number-----------------------------------")
        print("-------------------------------------------------------------------------------------")
        print("\n")

# Withdraw money from an account (admin or customer)
def withdraw_money(acc_num=None,access=None):
    print("------------------------------------------------------------------------------------")
    print("----------------------------Withdraw Money------------------------------------------")
    print("------------------------------------------------------------------------------------")
    print("\n")
    withdraw_acnum = input("Enter your account number: ").strip()
    if acc_num== withdraw_acnum or access =="admin":
        try:
            acc_num=withdraw_acnum
            amount = int(input("Enter amount to withdraw: "))
            if acc_num in accounts and 0 < amount <= accounts[acc_num]["balance"]:
                accounts[acc_num]["balance"] -= amount
                transactions[acc_num].append(f"{date_time.strftime('%x %X')} - Withdrawn: {amount}, Balance: {accounts[acc_num]['balance']}, Access: {access}")
                transaction_num= str(get_next_transaction_number())
                transactions_details[transaction_num] = {
                    "acc_num": acc_num,
                    "date_time": date_time.strftime('%x %X'),
                    "amount": amount,
                    "Categary": "withdraw",
                    "balance": accounts[acc_num]["balance"],
                    "access": access
                    }
                save_accounts()
                save_transactions()
                save_transactions_details()
                print("-------------------------------------------------------------------------------------")
                print(f"Withdrew {amount} from account {acc_num}. New balance: {accounts[acc_num]['balance']}")
                print("-------------------------------------------------------------------------------------")
                print("\n")
            else:
                print("-------------------------------------------------------------------------------------")
                print("-------------------------------insufficient balance----------------------------------")
                print("-------------------------------------------------------------------------------------") 
                print("\n") 
        except ValueError:
            print("Invalid input.")
    else:
        print("-------------------------------------------------------------------------------------")
        print("-------------------------------Invalid account number--------------------------------")
        print("-------------------------------------------------------------------------------------")
        print("\n")

# Transfer money between accounts (customer)
def account_to_account_transfer(acc_num=None,access=None):
    print("-------------------------------------------------------------------------------------")
    print("----------------------------Account to Account Transfer------------------------------")
    print("-------------------------------------------------------------------------------------")
    print("\n")
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
                transaction_num= str(get_next_transaction_number())
                transactions_details[transaction_num] = {
                    "acc_num": from_acc_num,
                    "date_time": date_time.strftime('%x %X'),
                    "amount": amount,
                    "Categary": "Transfer Out",
                    "balance": accounts[acc_num]["balance"],
                    "access": access
                    }
                transactions_details[transaction_num] = {
                    "acc_num": to_acc_num,
                    "date_time": date_time.strftime('%x %X'),
                    "amount": amount,
                    "Categary": "Transfer IN",
                    "balance": accounts[acc_num]["balance"],
                    "access": access
                    }
                save_accounts()
                save_transactions()
                save_transactions_details()
                print("-------------------------------------------------------------------------------------")
                print(f"Transferred {amount} from account {from_acc_num} to account {to_acc_num}.")
                print("-------------------------------------------------------------------------------------")
                print("\n")
            else:
                print("-------------------------------------------------------------------------------------")
                print("                             insufficient balance                                    ")
                print("-------------------------------------------------------------------------------------")
                print("\n")
        except ValueError:
            print("-------------------------------------------------------------------------------------")
            print("                                 Invalid input                                       ")
            print("-------------------------------------------------------------------------------------")
            print("\n")
            
    else:
        print("-------------------------------------------------------------------------------------")
        print("                            Invalid account numbers                                  ")
        print("-------------------------------------------------------------------------------------")
        print("\n")
        
# Show balance of an account (admin or customer)
def show_balance(acc_num=None,access=None):
    print("------------------------------------------------------------------------------------")
    print("----------------------------Show Balance--------------------------------------------")
    print("------------------------------------------------------------------------------------")
    print("\n")

    show_num = input("Enter your account number: ").strip()
    if acc_num== show_num or access=="admin":
        try:
            if show_num in accounts:
                print("-------------------------------------------------------------------------------------")
                print(f"Account {show_num} balance: {accounts[show_num]['balance']}") 
                print("-------------------------------------------------------------------------------------")
                print("\n")
        except ValueError:
            print("-------------------------------------------------------------------------------------")
            print("-------------------------------- Invalid input --------------------------------------")
            print("-------------------------------------------------------------------------------------")
            print("Invalid input.")
            print("\n")
    else:
        print("-------------------------------------------------------------------------------------")
        print("----------------------------Invalid account number-----------------------------------")
        print("-------------------------------------------------------------------------------------")
        print("\n")

# Show transaction history of an account (admin or customer)
def transaction_history(acc_num=None,access=None):
    print("------------------------------------------------------------------------------------")
    print("----------------------------Transaction History-------------------------------------")
    print("------------------------------------------------------------------------------------")
    print("\n")
    transaction_acc=input("Enter your account number: ").strip()
    if acc_num== transaction_acc or access=="admin":
        acc_num=transaction_acc
        if acc_num in accounts:
            print("-------------------------------------------------------------------------------------")
            print(f"Transaction history for account {acc_num}:")
            print("-------------------------------------------------------------------------------------")
            print("\n")
            for transaction in transactions[acc_num]:
                print(transaction)
    else:
        print("-------------------------------------------------------------------------------------")
        print("----------------------------Invalid account number-----------------------------------")
        print("-------------------------------------------------------------------------------------")
        print("\n")

# Start the application by calling the login function
login()

