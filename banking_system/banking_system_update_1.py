import textwrap
import random

def menu():
    # Mostra o menu e retorna a opção escolhida pelo usuário
    return input(textwrap.dedent("""\
        [1]\tDeposit
        [2]\tWithdraw
        [3]\tCheck Balance
        [4]\tNew Account
        [5]\tList Accounts
        [6]\tNew Customer
        [7]\tExit
    """).strip() + "\nChoose an option: ").strip()

def deposit(balance, statement):
    value = float(input("Enter the amount you want to deposit: "))

    if value < 0:
        print("Invalid value")
    else:
        balance += value
        statement += f"Deposited: ${value}\n"

    return balance, statement

def withdraw(balance, amount_limit, statement, number_of_withdrawals, limit_of_withdrawals):
    if number_of_withdrawals >= limit_of_withdrawals:
        print("You have reached the limit of withdrawals")
        return balance, statement, number_of_withdrawals

    value = float(input("Enter the amount you want to withdraw: "))

    if value < 0:
        print("Invalid value")
    elif value > balance:
        print("Insufficient funds")
    elif value > amount_limit:
        print("You can only withdraw up to $500")
    else:
        balance -= value
        statement += f"Withdrew: ${value}\n"
        number_of_withdrawals += 1

    return balance, statement, number_of_withdrawals

def check_balance(balance, statement):
    print("Statement: ")
    print("No changes made to financial transactions" if not statement else statement)
    print(f"Current balance: ${balance:.2f}")

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

    customers.append({
        "cpf": cpf,
        "name": name,
        "date_of_birth": date_of_birth,
        "age": age,
        "email": email,
        "phone": phone
    })
    print("Customer created successfully")

def filtering_customers(cpf, customers):
    filtered_customer = [customer for customer in customers if customer["cpf"] == cpf]  
    return filtered_customer[0] if filtered_customer else None	

def new_account(bank_branch, accounts, customers):
    cpf = input("Enter your CPF: ")
    customer = filtering_customers(cpf, customers)

    if not customer:
        print("Customer not found")
        return

    account_number = random.randint(1000, 9999)

    accounts.append({
        "name": customer["name"],
        "bank_branch": bank_branch,
        "account_number": account_number,
    })

    print("Account created successfully")
    
def list_accounts(accounts):
    print("List of accounts: ")
    for account in accounts:
        print(account)

def main():
    BANK_BRANCH = "0001"
    LIMIT_OF_WITHDRAWALS = 3

    balance = 0
    statement = ""
    amount_limit = 500
    number_of_withdrawals = 0
    accounts = []
    customers = []

    while True:
        option = menu()

        if option == "1":
            balance, statement = deposit(balance, statement)
        elif option == "2":
            balance, statement, number_of_withdrawals = withdraw(balance, amount_limit, statement, number_of_withdrawals, LIMIT_OF_WITHDRAWALS)
        elif option == "3":
            check_balance(balance, statement)
        elif option == "4":
            new_account(BANK_BRANCH, accounts, customers)
        elif option == "5":
            list_accounts(accounts)
        elif option == "6":
            new_customer(customers)
        elif option == "7":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid option. Please choose a number between 1 and 7.")

main()
