import textwrap
import random
from abc import ABC, abstractmethod
from datetime import datetime

class Customer:
    def __init__(self, address, phone_number):
        self._address = address
        self._phone_number = phone_number
    
    def perform_transaction(self, account_number, transaction_type):
        transaction_type.register(account_number)
        transaction_type.display_info()
    
    def add_account(self, account_number):
        self.account_number.append(account_number)

class Individual(Customer):
    def __init__(self, name, date_of_birth, address, phone_number, cpf):
        super().__init__(name, address, phone_number)
        self._name = name
        self._date_of_birth = date_of_birth
        self._cpf = cpf
    
    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Date of Birth: {self.date_of_birth}")
        print(f"Address: {self.address}")
        print(f"Phone Number: {self.phone_number}")
        print(f"CPF: {self.cpf}")
        print(f"Account Number: {self.account_number}")

class Account:
    def __init__(self, account_number, customer):
        self._account_number = account_number
        self._balance = 0
        self._bank_branch = "0001"
        self._customer = customer
        self._statement = Statement()

    @classmethod
    def create_account(cls, customer):
        account_number = cls.generate_account_number()
        account = cls(account_number, customer)
        customer.add_account(account_number)
        return account

    def generate_account_number():
        return random.randint(10000, 99999)

    @property
    def balance(self):
        return self._balance
    
    @property
    def account_number(self):
        return self._account_number
    
    @property
    def bank_branch(self):
        return self._bank_branch
    
    @property
    def customer (self):
        return self._customer
    
    @property   
    def statement(self):
        return self._statement
    
    def deposit(self, amount):
        self.amount = amount
        if amount > 0:
            self.balance += amount
            print("Sucessful deposit")
            return True
        else:
            print("Invalid amount")
            return False
    
    def withdraw(self, amount):
        self.amount = amount
        overdrawn_balance = amount > self.balance

        if overdrawn_balance:
            print("Insufficient funds")
        
        elif amount > 0:
            self.balance -= amount
            print("Sucessful withdrawal")
            return True

        else:
            print("Invalid amount")
            return False

class Statement:
    def __init__(self):
        self.transactions = []
    
    @property
    def transactions(self):
        return self._transactions
    
    def add_transaction(self, transaction):
        self.transactions.append(
            {
                "transaction_type": transaction.transaction_type,
                "amount": transaction.amount,
                "timestamp": datetime.now().strftime("%d-%M-%Y %H:%M:%S"),
            }
        )

    def display(self):
        for transaction in self.transactions:
            print(transaction)

class AccountType(Account):
    def __init__(self, account_number, customer, _limit_amount = 500.0, _limit_withdraw_number = 3):
        super().__init__(account_number, customer)
        self._limit_amount = _limit_amount
        self._limit_withdraw_number = _limit_withdraw_number
        
    def withdraw(self, amount):
        number_of_withdrawals = len([transaction for transaction in self.statement.transactions if transaction["transaction_type"] == "withdraw"])
        
        overdrawn_limit_amount = amount > self._limit_amount
        overdrawn_limit_number = number_of_withdrawals >= self._limit_withdraw_number

        if overdrawn_limit_amount or overdrawn_limit_number:
            print("Operation not allowed")
            return False
        else:
            return super().withdraw(amount)
    
    def __str__(self):
        return f"""\
        Bank Branch:\t{self._bank_branch}
        Account:\t\t{self._account_number}
        Name:\t{self._customer.name}
    """

class Transaction(ABC):
    def __init__(self, amount):
        self.amount = amount
    
    @property
    def amount(self):
        return self._amount
    
    @abstractmethod
    def register(self, account_number):
        pass
    
    @abstractmethod
    def display_info(self):
        pass

class Deposit(Transaction):
    def __init__(self, _amount):
        self._amount = _amount
    
    @property
    def _amount(self):
        return self._amount
    
    def register(self, _account_number):
        account = self.get_account(_account_number)
        sucess = account.deposit(self.amount)
        
        if sucess:
            account.statement.add_transaction(self)

class Withdraw(Transaction):
    def __init__(self, _amount):
        self._amount = _amount
    
    @property
    def amount(self):
        return self._amount
    
    def register(self, account_number):
        account = self.get_account(account_number)
        sucess = account.withdraw(self.amount)
        
        if sucess:
            account.statement.add_transaction(self)

def menu ():
    return input(textwrap.dedent("""
    1 - Withdraw
    2 - Deposit
    3 - Statement
    4 - New account
    5 - List accounts
    6 - New Customer
    7 - Exit
    """))

def customer_filter(customers, cpf):
    customer_filtered = [customers for customers in customers if customers.cpf == cpf]
    return customer_filtered[0] if customer_filtered else None

def recover_customer_account(customer):
    if not customer.accounts:
        print("Account not found.")
        return

    return customer.accounts[0]

def deposit(customers):
    cpf = input("Enter the CPF (numbers only): ")
    customer = customer_filter(customers, cpf)

    if not customer:
        print("Customer not found.")
        return
    
    amount = float(input("Enter the deposit amount: "))
    transaction = Deposit(amount)

    account = recover_customer_account(customer)
    if not account:
        print("Account not found.")
        return
    
    customer.perform_transaction(account.account_number, transaction)

def withdraw(customers):
    cpf = input("Enter the CPF (numbers only): ")
    customer = customer_filter(customers, cpf)

    if not customer:
        print("Customer not found.")
        return
    
    amount = float(input("Enter the withdrawal amount: "))
    transaction = Withdraw(amount)

    account = recover_customer_account(customer)
    if not account:
        print("Account not found.")
        return
    
    customer.perform_transaction(account.account_number, transaction)
    
def statement(customers):
    cpf = input("Enter the CPF (numbers only): ")
    customer = customer_filter(customers, cpf)

    if not customer:
        print("Customer not found.")
        return
    
    account = recover_customer_account(customer)
    if not account:
        print("Account not found.")
        return
    
    account.statement.display()
    
    statement = ""
    if not transactions:
        statement = "No transactions"
    else:
        for transaction in transactions:
            statement += f"{transaction['transaction_type']} - {transaction['amount']} - {transaction['timestamp']}\n"
    
    print(statement)
    print(f"Balance: $ {account.balance:.2f}")

def new_customer(customers):
    cpf = input("Enter the CPF (numbers only): ")
    customer = customer_filter(customers, cpf)
    
    if customer:
        print("Customer already registered.")
        return
    
    name = input("Enter the name: ")
    date_of_birth = input("Enter the date of birth (dd/mm/yyyy): ")
    address = input("Enter the address: ")
    phone_number = input("Enter the phone number: ")

    customer = Individual(name, date_of_birth, address, phone_number, cpf)
    customers.append(customer)
    print(f"Customer {name} created successfully.")

def new_account(customers):
    cpf = input("Enter the CPF (numbers only): ")
    customer = customer_filter(customers, cpf)

    if not customer:
        print("Customer not found.")
        return
    
    account = Account.create_account(customer)
    print(f"Account {account.account_number} created successfully.")

def list_accounts(customers):
    for customer in customers:
        print(f"Name: {customer.name}")
        print(f"CPF: {customer.cpf}")
        print(f"Accounts: {customer.accounts}")
        print()

def main():
    customers = []
    accounts = []
    
    while True:
        opcao = menu()
        
        if opcao == "1":
            withdraw(customers)            
            
        elif opcao == "2":
            deposit(customers)

        elif opcao == "3":
            statement(customers)
        
        elif opcao == "4":
            new_account(customers)
        
        elif opcao == "5":
            account_number = len(accounts) + 1
            new_account(account_number, customers, accounts)
            
        elif opcao == "6":
            list_accounts(customers)
        
        elif opcao == "7":
            print("Exiting...")
            break

        else:
            print("Invalid option")

main()