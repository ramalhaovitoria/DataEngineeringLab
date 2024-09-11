from abc import ABC, abstractmethod
from datetime import datetime
import random

class Customer:
    def __init__(self, adress, accounts):
        self.adress = adress
        self.accounts = accounts

    def perform_transaction(self, account, transaction):
        transaction.register(account)

    def add_account(self, account):
        self.accounts.append(account)

class IndividualCustomer(Customer):
    def __init__(self, name, cpf, date_of_birth, email, phone, adress):
        super().__init__(adress)
        self.name = name
        self.cpf = cpf
        self.date_of_birth = date_of_birth
        self.email = email  
        self.phone = phone

class Account:
    def __init__(self, account_number, customer):
        self._balance = 0
        self._account_number = account_number
        self._customer = customer
        self._statement = []
        self._bank_number = "00001"

    @classmethod
    def create(cls, customer):
        return cls(customer)
    
    @property
    def balance(self):
        return self._balance
    
    @property
    def account_number(self):
        return random.randint(1000, 9999)
    
    @property
    def customer(self):
        return self._customer
    
    @property
    def statement(self):
        return self._statement
    
    @property
    def bank_number(self):
        return self._bank_number
    
    def deposit(self, value):
        if value > 0:
            self._balance += value
            self._statement.append((datetime.now(), value))
            print("Deposit successful!")
        else:
            print("Invalid value for deposit")
            return False
        
        return True
    
    def withdraw(self, value):
        self._balance = balance
        exceeded_limit = value > self._balance
        if exceeded_limit:
            print("Insufficient funds")
        
        elif value > 0:
            self._balance -= value
            self._statement.append((datetime.now(), -value))
            print("Withdrawal successful!")
        
        else:
            raise ValueError("Invalid value for withdrawal")
        return False

class CheckingAccount(Account):
    def __init__(self, account_number, customer, account_limit = 500, transaction_limit = 3):
        super().__init__(account_number, customer)
        self._account_limit = account_limit
        self._transaction_limit = transaction_limit

    def withdraw(self, value):
        number_of_transactions = len([transaction for transaction in self._statement if transaction["type"] == "withdrawal"])

        limit_exceeded = value > self._account_limit
        transaction_limit_exceeded = number_of_transactions >= self._transaction_limit

        if limit_exceeded:
            print("Withdrawal amount exceeded")
        elif transaction_limit_exceeded:
            print("Number of transactions exceeded")
        else:
            super().withdraw(value)
        
        return False

    def __str__(self):
        return f"Account number: {self.account_number}\nBank number: {self.bank_number}\nBalance: {self.balance}\nHolder: {self.customer}\n"
    
class Statement:
    def __init__(self, account):
        self._account = account
        self._transactions = []
    
    def register(self, transaction):
        self._transactions.append(transaction)
    
    @property
    def transactions(self):
        return self._transactions
    
    def add_transaction(self, transaction):
        self._transactions.append({
            "type": transaction.__class__.__name__,
            "value": transaction.value,
            "timestamp": datetime.now()
        })

class Transaction(ABC):
    @property
    @abstractproperty	
    def value(self):
        pass

    @abstractmethod
    def register(self, account):
        pass

class Deposit(Transaction):
    def __init__(self, value):
        self._value = value
    
    @property
    def value(self):
        return self._value
    
    def register(self, account):
        transaction_successful = account.deposit(self._value)
        
        if transaction_successful:
            account.statement.add_transaction(self)

class Withdrawal(Transaction):
    def __init__(self, value):
        self._value = value
    
    @property
    def value(self):
        return self._value
    
    def register(self, account):
        transaction_successful = account.withdraw(self._value)
        
        if transaction_successful:
            account.statement.add_transaction(self)
        
def menu():
   return input(textwrap.dedent("""\
        [1]\tDeposit
        [2]\tWithdraw
        [3]\tCheck Balance
        [4]\tNew Account
        [5]\tList Accounts
        [6]\tNew Customer
        [7]\tExit
    """).strip() + "\nChoose an option: ").strip()

def filtering_customers(cpf, customers):
    filtered_customer = [customer for customer in customers if customer["cpf"] == cpf]  
    return filtered_customer[0] if filtered_customer else None	

def account_recovery(customer):
    if not customer.accounts:
        print("No accounts found")
        return None
    
    return customer.accounts[0]

def deposit(customer):
    cpf = input("Enter your CPF: ")
    customer = filtering_customers(cpf, customers)

    if not customer:
        print("Customer not found")
        return
    
    value = float(input("Enter the amount you want to deposit: "))
    transaction = Deposit(value)

    account = account_recovery(customer)
    if not account:
        return
    
    customer.perform_transaction(account, transaction)

def withdraw(customers):
    cpf = input("Enter your CPF: ")
    customer = filtering_customers(cpf, customers)

    if not customer:   
        print("Customer not found")
        return
    
    value = float(input("Enter the amount you want to withdraw: "))
    transaction = Withdrawal(value)

    account = account_recovery(customer)
    if not account:
        return
    
    customer.perform_transaction(account, transaction)

def display_statement(customers):
    cpf = input("Enter your CPF: ")
    customer = filtering_customers(cpf, customers)

    if not customer:
        print("Customer not found")
        return
    
    account = account_recovery(customer)
    if not account:
        return
    
    print("Statement: ")
    print("No changes made to financial transactions" if not account.statement.transactions else account.statement.transactions)
    print(f"Current balance: ${account.balance:.2f}")

def new_customer(customers):
    cpf = input("Enter your CPF: ")

    if any(customer["cpf"] == cpf for customer in customers):
        print("Customer already exists")
        return
    
    name = input("Enter your name: ")
    date_of_birth = input("Enter your date of birth: ")
    age = int(input("Enter your age: "))
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")

    customer = IndividualCustomer.append({
        "cpf": cpf,
        "name": name,
        "date_of_birth": date_of_birth,
        "age": age,
        "email": email,
        "phone": phone
    })
    
    customers.append(customer)
    print("Customer created successfully")

def new_account(customers):
    cpf = input("Enter your CPF: ")
    customer = filtering_customers(cpf, customers)

    if not customer:
        print("Customer not found")
        return
    
    account = CheckingAccount.create(customer = customer, account_number = random.randint(1000, 9999))
    customer.add_account(account)
    print("Account created successfully")

def list_accounts(customers):
    print("List of accounts: ")
    for customer in customers:
        print(customer.accounts)

def main():
    customers = []
    while True:
        option = menu()
        
        if option == "1":
            deposit(customers)
        elif option == "2":
            withdraw(customers)
        elif option == "3":
            display_statement(customers)
        elif option == "4":
            new_account(customers)
        elif option == "5":
            list_accounts(customers)
        elif option == "6":
            new_customer(customers)
        elif option == "7":
            break
        else:
            print("Invalid option")

main()