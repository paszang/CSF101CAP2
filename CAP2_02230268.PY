
#reference:
#https://www.youtube.com/watch?v=xTh-ln2XhgU&t=459s
#https://www.youtube.com/results?search_query=banking+sysgtem+python+code
#https://www.youtube.com/watch?v=julcNz6rWVc
#https://www.youtube.com/watch?v=2TrDIbwasw8&t=15s
#https://www.youtube.com/watch?v=BRssQPHZMrc


#name: Passang
#department: Mechanical
#student number: 02230268

import os
import random
import json

# Helper function to generate account number and password
def generate_account_number():                               # it will randomly generate an account nmuber for the user
    return str(random.randint(1000000000, 9999999999))        

def generate_password():                                      # like the above line it will provide a user with a password 
    return str(random.randint(1000, 9999))

# Base class for accounts(it is the parent classs which will help in the interitance for the child classes)
class Account:
    def __init__(self, account_number, password, account_type, balance=0):
        self.account_number = account_number
        self.password = password
        self.account_type = account_type
        self.balance = balance

    def deposit(self, amount):                    #helps user to deposit money to their account which initiallly had 0 balance
        self.balance += amount
        print(f"Deposited {amount}. New balance: {self.balance}")

    def withdraw(self, amount):                   #provides the user with a function that gives them the oppotunity to withdraw money from their account
        if amount > self.balance:
            print("Insufficient funds")           #if the amount entered is insufficient then eventually helps in making the user realize that the withdrawing isnt possible
        else:
            self.balance -= amount
            print(f"Withdrew {amount}. New balance: {self.balance}")  #withdraws the entered amount and the provides information about the remaining amount in their account

    def check_balance(self):
        print(f"Current balance: {self.balance}")  #this function helps user check their balance(amount) in their account

    def save_to_file(self):                        # it saves the information for user when they create a new account, in the accounts.txt file
        account_data = {
            "account_number": self.account_number,
            "password": self.password,
            "account_type": self.account_type,
            "balance": self.balance
        }
        with open('accounts.txt', 'a') as f:          #it uses a language from JSON (javascript object notation) it helps in parsing the python 
            f.write(json.dumps(account_data) + '\n')

   
    def load_accounts():                           #this method helps in storing the details for the accounts created in the account.txt file
        accounts = []
        if os.path.exists('accounts.txt'):
            with open('accounts.txt', 'r') as f:
                for line in f:
                    account_data = json.loads(line.strip())
                    if account_data['account_type'] == 'Personal':
                        account = PersonalAccount(account_data['account_number'], account_data['password'], account_data['balance'])
                    elif account_data['account_type'] == 'Business':
                        account = BusinessAccount(account_data['account_number'], account_data['password'], account_data['balance'])
                    accounts.append(account)
        return accounts

# Derived class for Personal Accounts from parent class(Account)
class PersonalAccount(Account):
    def __init__(self, account_number, password, balance=0):
        super().__init__(account_number, password, 'Personal', balance)

# Derived class for Business Accounts
class BusinessAccount(Account):
    def __init__(self, account_number, password, balance=0):
        super().__init__(account_number, password, 'Business', balance)

# Banking application functionality 
class BankingApplication:
    def __init__(self):                            # Initializes the banking application by loading existing accounts from the file.
        self.accounts = Account.load_accounts()

    def create_account(self, account_type):         # Generates an unique account number and a password.
        account_number = generate_account_number()
        password = generate_password()
                                                     # Creates an account object based on the account type.
        if account_type == 'Personal':
            account = PersonalAccount(account_number, password)
        elif account_type == 'Business':                               
            account = BusinessAccount(account_number, password)
        account.save_to_file()                                        # Saves the account details to a file and adds the account to the list of accounts.
        self.accounts.append(account)
        print(f"Account created. Account Number: {account_number}, Password: {password}")

    def login(self, account_number, password):             # Iterates through all the accounts to find a matching account.
        for account in self.accounts:                      # Checks if the account number and password matches.
            if account.account_number == account_number and account.password == password:
                return account                              #returns the matching account.
        print("Invalid account number or password")          # Prints an error message if the account number or password is incorrect.
        return None                                          # Returns None if no matching account is found.

    def send_money(self, from_account, to_account_number, amount):    
        to_account = None                                          # Initializes the receiving account to None.
        for account in self.accounts:                              # Iterates through all the accounts to find the receiving account.
            if account.account_number == to_account_number:        # Sets the receiving account.
               to_account = account
               break                                               # Exits the loop once the account is found.
        if to_account is None:
            print("Receiving account does not exist")          #it gives user the information that the receiving account is inaccessible.
        elif from_account.balance < amount:
            print("Insufficient funds")                        #shows that the amount enterted for transfering is insufficient.
        else:
            from_account.withdraw(amount)                           #withdraws the amount entered from your account
            to_account.deposit(amount)                              # deposits into the account number entered
            print(f"Sent {amount} to account {to_account_number}")  #provides the details for the fund tranfered from one account to the another. 

    def delete_account(self, account):
        self.accounts.remove(account)                      # Removes the specified account from the list of accounts.
        with open('accounts.txt', 'w') as f:               # Opens the 'accounts.txt' file in write mode to update the account data.
            for acc in self.accounts:
                f.write(json.dumps({                       # Writes each account's details to the file in JSON format.
                    "account_number": acc.account_number,
                    "password": acc.password,
                    "account_type": acc.account_type,
                    "balance": acc.balance
                }) + '\n')
        print(f"Account {account.account_number} deleted")   #it now prints the confirmation message that the account has been deleted.

def main():
    app = BankingApplication()                        #Initializes the banking application
    while True: 
      # it is the main application loop.
      # Displays the main menu options.
        print("\nWelcome to the Banking Application")
        print("1. Create Personal Account")
        print("2. Create Business Account")
        print("3. Login")
        print("4. Exit")
        choice = input("Enter your choice: ")   #provides the user with multiple input choices for performing different functions.
        if choice == '1':
            app.create_account('Personal')
        elif choice == '2':
            app.create_account('Business')
        elif choice == '3':
            account_number = input("Enter account number: ")
            password = input("Enter password: ")
            account = app.login(account_number, password) # If the users login they are able to perform different works. 
            if account:
                while True:
                    print("\n1. Deposit")
                    print("2. Withdraw")
                    print("3. Check Balance")
                    print("4. Send Money")
                    print("5. Delete Account")
                    print("6. Logout")
                # seeks input from the user.
                    user_choice = input("Enter your choice: ") 
                    if user_choice == '1':
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)   #deposits entered amount into the account.
                    elif user_choice == '2':
                        amount = float(input("Enter amount to withdraw: "))
                        account.withdraw(amount)   #withdraws money from the account.
                    elif user_choice == '3':
                        account.check_balance()    #enables the user to ckeck their balance.
                    elif user_choice == '4':
                        to_account_number = input("Enter account number to send money: ")
                        amount = float(input("Enter amount to send: "))
                        app.send_money(account, to_account_number, amount)  #this helps in transferring balance from users account to the desired account.
                    elif user_choice == '5':
                        app.delete_account(account)  #provides the user an option to delete their account.
                        break
                    elif user_choice == '6':      # this will log out from the account.
                        break                     # it will exit the loop.
                    else:
                        print("Invalid choice")   # provides the user that the input is invalid.
        elif choice == '4':
            break      # exits the application.
        else:
            print("Invalid choice")  # handles the invalid choices.

if __name__ == "__main__":       # If this script is run directly (not imported), calls the main() function to start the application.
    main()