
# ======================================
# MINI PROJECT: STUDENT BUDGET TRACKER
# ======================================

# Fixed expense categories
CATEGORIES = ("Food", "Transport", "Mobile", "Stationery", "Other")


# Function to get a valid positive amount
def get_amount(message):
    amount = float(input(message))

    while amount <= 0:
        print("Amount must be greater than zero.")
        amount = float(input(message))

    return amount


# Function to record expenses
def record_expenses(categories=CATEGORIES):
    expenses = []       # Stores expense amounts
    used_categories = []  # Stores chosen categories

    while True:
        print("\nExpense Categories:")

        # Display available categories
        for i in range(len(categories)):
            print(i + 1, ".", categories[i])

        choice = int(input("Choose category number (0 to finish): "))

        # Stop entering expenses
        if choice == 0:
            break

        # Validate the category number
        if choice < 1 or choice > len(categories):
            print("Invalid category number!")
            continue

        category = categories[choice - 1]
        amount = get_amount("Enter expense amount (PKR): ")

        expenses.append(amount)
        used_categories.append(category)

        print("Expense added successfully!")

    return expenses, used_categories


# Function to calculate total expenses
def calculate_total(expenses):
    total = 0

    for amount in expenses:
        total = total + amount

    return total


# Function to create the final report
def generate_report(budget, expenses, categories, currency="PKR"):
    total_spent = calculate_total(expenses)
    remaining = budget - total_spent

    # Count how many times each category was used
    category_summary = {}

    for i in range(len(categories)):
        category = categories[i]
        amount = expenses[i]

        if category in category_summary:
            category_summary[category] += amount
        else:
            category_summary[category] = amount

    # Display the report
    print("\n========== WEEKLY BUDGET REPORT ==========")
    print("Starting budget:", currency, round(budget, 2))
    print("Total spent:", currency, round(total_spent, 2))
    print("Remaining balance:", currency, round(remaining, 2))

    print("\n--- Spending by Category ---")

    # A set shows each category only once
    unique_categories = set(categories)

    for category in unique_categories:
        print(category, ":", currency, round(category_summary[category], 2))

    # Check whether the budget was exceeded
    if remaining > 0:
        print("\nStatus: You are within your budget!")
    elif remaining == 0:
        print("\nStatus: You used your entire budget.")
    else:
        print("\nStatus: You exceeded your budget!")

    # Store key results in a dictionary
    report = {
        "Budget": budget,
        "Total Spent": total_spent,
        "Remaining": remaining
    }

    return report


# ======================================
# MAIN PROGRAM
# ======================================

print("STUDENT BUDGET & EXPENSE TRACKER")

student_name = input("Enter your name: ").strip().title()
weekly_budget = get_amount("Enter your weekly budget (PKR): ")

# Record expenses
expense_amounts, expense_categories = record_expenses()

# Generate and receive the report
final_report = generate_report(
    budget=weekly_budget,
    expenses=expense_amounts,
    categories=expense_categories
)

print("\nThank you,", student_name + "!")
