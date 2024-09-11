menu = "

    [1] Deposit
    [2] Withdraw
    [3] Check Balance
    [4] Exit
"

balance = 0
amount_limit = 500
statement = ""
number_of_withdrawals = 0
limit_of_withdrawals = 3

while True:
    choice = input(menu)

    if choice == "1":
        value = float(input("Enter the amount you want to deposit: "))

        if value < 0:
            print("Invalid value")
            continue
        else:
            balance += value
            statement += f"Deposited: ${amount}\n"

    elif choice == "2":
        if number_of_withdrawals >= limit_of_withdrawals:
            print("You have reached the limit of withdrawals")
            continue

        if value > amount_limit:
            print("You can only withdraw up to $500")
            continue

        value = float(input("Enter the amount you want to withdraw: "))

        if value < 0:
            print("Invalid value")
            continue
        elif value > balance:
            print("Insufficient funds")
            continue
        else:
            balance -= value
            statement += f"Withdrew: ${amount}\n"
            number_of_withdrawals += 1

    elif choice == "3":
        print(f"Your balance is: ${balance}")
    
    elif choice == "4":
        print("Thank you for using our service")
        break

    else:
        print("Invalid choice")