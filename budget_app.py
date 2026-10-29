import streamlit as st
import pandas as pd
import csv
import io
from datetime import datetime

# ==========================================
# STUDENT BUDGET & EXPENSE TRACKER
# Streamlit Web Application
# ==========================================

CATEGORIES = ("Food", "Transport", "Mobile", "Stationery", "Other")

st.set_page_config(
    page_title="Student Budget Tracker",
    page_icon="💰",
    layout="wide"
)

# ------------------------------------------
# 1. Initialize session state
# ------------------------------------------

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "student_name" not in st.session_state:
    st.session_state.student_name = ""

if "weekly_budget" not in st.session_state:
    st.session_state.weekly_budget = 10000.0

if "expense_counter" not in st.session_state:
    st.session_state.expense_counter = 0


# ------------------------------------------
# 2. Page heading
# ------------------------------------------

st.title("💰 Student Budget & Expense Tracker")
st.write(
    "Manage your weekly budget, record expenses, "
    "and understand your spending habits."
)

st.divider()


# ------------------------------------------
# 3. Student profile and budget
# ------------------------------------------

st.sidebar.header("👤 Student Profile")

with st.sidebar.form("profile_form"):
    student_name = st.text_input(
        "Student name",
        value=st.session_state.student_name
    )

    weekly_budget = st.number_input(
        "Weekly budget (PKR)",
        min_value=1.0,
        value=float(st.session_state.weekly_budget),
        step=500.0
    )

    save_profile = st.form_submit_button("Save Profile")

if save_profile:
    if not student_name.strip():
        st.sidebar.error("Please enter your name.")
    else:
        st.session_state.student_name = student_name.strip().title()
        st.session_state.weekly_budget = weekly_budget
        st.sidebar.success("Profile and budget saved!")


if st.session_state.student_name:
    st.subheader(f"Welcome, {st.session_state.student_name}! 👋")
else:
    st.info("Enter your name and weekly budget in the sidebar to get started.")


# ------------------------------------------
# 4. Add a new expense
# ------------------------------------------

st.header("➕ Record a New Expense")

with st.form("expense_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        category = st.selectbox(
            "Select expense category",
            CATEGORIES
        )

    with col2:
        amount = st.number_input(
            "Expense amount (PKR)",
            min_value=0.0,
            value=0.0,
            step=100.0
        )

    description = st.text_input(
        "Description (optional)",
        placeholder="Example: Lunch, bus fare, notebooks"
    )

    add_expense = st.form_submit_button("Add Expense")

if add_expense:
    if amount <= 0:
        st.error("Expense amount must be greater than zero.")
    else:
        st.session_state.expense_counter += 1

        new_expense = {
            "ID": st.session_state.expense_counter,
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Category": category,
            "Description": description.strip() or category,
            "Amount (PKR)": float(amount)
        }

        st.session_state.expenses.append(new_expense)

        st.success(
            f"Expense added: PKR {amount:,.2f} for {category}."
        )


st.divider()


# ------------------------------------------
# 5. Calculate budget summary
# ------------------------------------------

st.header("📊 Budget Dashboard")

expenses = st.session_state.expenses

total_spent = sum(
    expense["Amount (PKR)"] for expense in expenses
)

remaining = st.session_state.weekly_budget - total_spent

budget = st.session_state.weekly_budget

col1, col2, col3 = st.columns(3)

col1.metric(
    "Weekly Budget",
    f"PKR {budget:,.2f}"
)

col2.metric(
    "Total Spent",
    f"PKR {total_spent:,.2f}"
)

col3.metric(
    "Remaining Balance",
    f"PKR {remaining:,.2f}",
    delta=f"{remaining:,.2f} PKR"
)

# Budget status
if remaining > 0:
    st.success("✅ You are within your budget!")
elif remaining == 0:
    st.warning("⚠️ You have used your entire budget.")
else:
    st.error(
        f"🚨 You exceeded your budget by PKR {abs(remaining):,.2f}."
    )

# Progress bar
if budget > 0:
    spending_percentage = total_spent / budget
    st.write("Budget usage")
    st.progress(min(spending_percentage, 1.0))
    st.write(f"{spending_percentage * 100:.1f}% of your budget used.")


# ------------------------------------------
# 6. Spending by category
# ------------------------------------------

st.divider()
st.header("📈 Spending by Category")

category_summary = {}

for category_name in CATEGORIES:
    category_total = sum(
        expense["Amount (PKR)"]
        for expense in expenses
        if expense["Category"] == category_name
    )

    category_summary[category_name] = category_total

summary_data = [
    {
        "Category": category_name,
        "Total Spent (PKR)": category_total
    }
    for category_name, category_total in category_summary.items()
]

summary_df = pd.DataFrame(summary_data)

col1, col2 = st.columns(2)

with col1:
    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True
    )

with col2:
    if total_spent > 0:
        chart_data = summary_df.set_index("Category")
        st.bar_chart(chart_data)
    else:
        st.info("Add an expense to see your spending chart.")


# ------------------------------------------
# 7. Transaction history
# ------------------------------------------

st.divider()
st.header("📋 Transaction History")

if expenses:
    history_df = pd.DataFrame(expenses)

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

    # Remove an expense if needed
    st.subheader("Remove an Expense")

    expense_options = {
        (
            f"ID {expense['ID']} | "
            f"{expense['Category']} | "
            f"PKR {expense['Amount (PKR)']:,.2f} | "
            f"{expense['Description']}"
        ): expense["ID"]
        for expense in expenses
    }

    selected_expense = st.selectbox(
        "Select the expense to remove",
        list(expense_options.keys())
    )

    if st.button("🗑️ Remove Selected Expense"):
        selected_id = expense_options[selected_expense]

        st.session_state.expenses = [
            expense
            for expense in st.session_state.expenses
            if expense["ID"] != selected_id
        ]

        st.success("Expense removed successfully.")
        st.rerun()

    # --------------------------------------
    # 8. Download CSV report
    # --------------------------------------

    csv_buffer = io.StringIO()

    fieldnames = [
        "ID",
        "Date",
        "Category",
        "Description",
        "Amount (PKR)"
    ]

    writer = csv.DictWriter(
        csv_buffer,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(expenses)

    st.download_button(
        label="📥 Download Expense Report (CSV)",
        data=csv_buffer.getvalue(),
        file_name="student_budget_report.csv",
        mime="text/csv"
    )

else:
    st.info("No expenses recorded yet. Add your first expense above.")


# ------------------------------------------
# 9. Final report
# ------------------------------------------

st.divider()
st.header("📝 Weekly Budget Report")

st.write(f"**Student:** {st.session_state.student_name or 'Not entered'}")
st.write(f"**Starting budget:** PKR {budget:,.2f}")
st.write(f"**Total expenses:** PKR {total_spent:,.2f}")
st.write(f"**Remaining balance:** PKR {remaining:,.2f}")
st.write(f"**Number of transactions:** {len(expenses)}")

st.caption(
    "Note: This is a learning application. "
    "Expenses are stored in the current session and are not "
    "saved permanently in a database."
)