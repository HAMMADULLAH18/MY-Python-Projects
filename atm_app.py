
import streamlit as st

st.set_page_config(
    page_title="ATM Simulator",
    page_icon="🏧",
    layout="centered"
)

# Initial ATM settings
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.tries = 0
    st.session_state.balance = 10000
    st.session_state.blocked = False
    st.session_state.message = ""
    st.session_state.message_type = "info"

st.title("🏧 ATM Simulator")
st.caption("A practice ATM application built with Python and Streamlit")

# Helper function to show feedback
def show_message():
    if st.session_state.message:
        message_type = st.session_state.message_type

        if message_type == "success":
            st.success(st.session_state.message)
        elif message_type == "error":
            st.error(st.session_state.message)
        elif message_type == "warning":
            st.warning(st.session_state.message)
        else:
            st.info(st.session_state.message)


# PIN verification
if st.session_state.blocked:
    st.error("Too many failed attempts. Your card is blocked.")

elif not st.session_state.authenticated:
    st.subheader("🔐 Secure Login")
    st.write(f"Attempts remaining: {3 - st.session_state.tries}")

    with st.form("pin_form"):
        entered_pin = st.text_input(
            "Enter your 4-digit PIN",
            type="password",
            max_chars=4
        )
        login_clicked = st.form_submit_button("Login")

    if login_clicked:
        if entered_pin == "1234":
            st.session_state.authenticated = True
            st.session_state.message = "PIN accepted."
            st.session_state.message_type = "success"
        else:
            st.session_state.tries += 1

            if st.session_state.tries >= 3:
                st.session_state.blocked = True
                st.session_state.message = (
                    "Too many failed attempts. Your card is blocked."
                )
                st.session_state.message_type = "error"
            else:
                remaining = 3 - st.session_state.tries
                st.session_state.message = (
                    f"Invalid PIN. You have {remaining} tries left."
                )
                st.session_state.message_type = "error"

    show_message()

# ATM menu after successful login
else:
    st.success("PIN accepted. Welcome!")

    st.metric("Available Balance", f"Rs. {st.session_state.balance:,}")

    choice = st.radio(
        "Select an ATM operation",
        [
            "Check Balance",
            "Withdraw Money",
            "Deposit Money",
            "Exit"
        ],
        horizontal=False
    )

    if choice == "Check Balance":
        if st.button("Show Balance"):
            st.info(
                f"Your current balance is "
                f"Rs. {st.session_state.balance:,}."
            )

    elif choice == "Withdraw Money":
        st.subheader("Withdraw Money")

        amount = st.number_input(
            "Enter withdrawal amount (Rs.)",
            min_value=0,
            step=500,
            value=500
        )

        if st.button("Withdraw"):
            if amount <= 0:
                st.error("Withdrawal amount must be greater than zero.")
            elif amount % 500 != 0:
                st.error("Amount must be a multiple of 500.")
            elif amount > st.session_state.balance:
                st.error("Insufficient balance.")
            else:
                st.session_state.balance -= int(amount)
                st.success(
                    f"Withdrawal successful! New balance: "
                    f"Rs. {st.session_state.balance:,}."
                )

    elif choice == "Deposit Money":
        st.subheader("Deposit Money")

        amount = st.number_input(
            "Enter deposit amount (Rs.)",
            min_value=0,
            step=500,
            value=500,
            key="deposit_amount"
        )

        if st.button("Deposit"):
            if amount <= 0:
                st.error("Deposit amount must be greater than zero.")
            else:
                st.session_state.balance += int(amount)
                st.success(
                    f"Deposit successful! New balance: "
                    f"Rs. {st.session_state.balance:,}."
                )

    elif choice == "Exit":
        st.info("Thank you for using the ATM.")

        if st.button("Exit ATM"):
            st.session_state.authenticated = False
            st.session_state.tries = 0
            st.session_state.message = "You have safely exited the ATM."
            st.session_state.message_type = "success"
            st.rerun()

    show_message()
