pin = "1234"
balance = 10000
tries = 0

while tries < 3:
    entered_pin = input("Enter your pin: ")
    if entered_pin == pin:
        print("Pin accepted.")
        break

    tries += 1
    print(f"Invalid pin. You have {3 - tries} tries left.")

if tries == 3:
    print("Too many failed attempts. Your card is blocked.")
else:
    while True:
        print("\nATM Menu")
        print("1. Check balance")
        print("2. Withdraw money")
        print("3. Deposit money")
        print("4. Exit")
        choice = input("Choose an option (1-4): ")

        if choice == "1":
            print(f"Your current balance is {balance}.")
        elif choice == "2":
            try:
                amount = int(input("Enter the amount you want to withdraw: "))
            except ValueError:
                print("Please enter a valid whole number.")
                continue

            if amount <= 0:
                print("Withdrawal amount must be greater than zero.")
            elif amount % 500 != 0:
                print("Amount must be a multiple of 500.")
            elif amount > balance:
                print("Insufficient balance.")
            else:
                balance -= amount
                print(f"Withdrawal successful. Your new balance is {balance}.")
        elif choice == "3":
            try:
                amount = int(input("Enter the amount you want to deposit: "))
            except ValueError:
                print("Please enter a valid whole number.")
                continue

            if amount <= 0:
                print("Deposit amount must be greater than zero.")
            else:
                balance += amount
                print(f"Deposit successful. Your new balance is {balance}.")
        elif choice == "4":
            print("Thank you for using the ATM.")
            break
        else:
            print("Invalid option. Please choose a number from 1 to 4.")
