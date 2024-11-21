import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the page title and layout
st.set_page_config(page_title="Energy Consumption Visualization", layout="centered")

# Set the style for plots
sns.set(style="whitegrid")

# Hardcoded credentials for simplicity
USER_CREDENTIALS = {
    "user1": "password1",
    "user2": "password2"
}

# Comprehensive CSS to remove background and padding
st.markdown(
    """
    <style>
    /* Custom styles for the app */
    .block-container {
        background-color: transparent !important;
        padding: 0 !important;
    }
    .logout-button {
        background-color: #f48c06;
        color: white;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to verify login credentials
def verify_login(username, password):
    return USER_CREDENTIALS.get(username) == password

# Login state management
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# Main logic
if not st.session_state.logged_in:
    st.markdown('<h2>Login</h2>', unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if verify_login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome {username}!")
        else:
            st.error("Invalid username or password.")
else:
    st.sidebar.title("Options")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()

    # Load dataset from URL
    data_url = "https://raw.githubusercontent.com/aishvipareek/ECDanalysis/refs/heads/main/energy-consumption-2020-1.csv"
    try:
        df = pd.read_csv(data_url)
    except Exception as e:
        st.error(f"Error loading dataset from URL. Please check the URL or your internet connection. Error details: {e}")
        st.stop()

    # Visualization options
    st.sidebar.subheader("Visualization Options")
    option = st.sidebar.radio("Choose Visualization Type", ["📈 Static Visualization", "📉 Dynamic Visualization"])

    if option == "📈 Static Visualization":
        st.markdown("### Static Visualization")
        selected_columns = st.multiselect("Select columns to visualize:", df.columns)

        if st.button("Show Static Visualization"):
            if selected_columns:
                plt.figure(figsize=(10, 5))
                for column in selected_columns:
                    plt.plot(df[column], label=column)
                plt.legend()
                plt.title("Static Visualization")
                plt.xlabel("Index")
                plt.ylabel("Values")
                st.pyplot(plt)
            else:
                st.warning("Please select at least one column to visualize.")

    elif option == "📉 Dynamic Visualization":
        st.markdown("### Dynamic Visualization")
        uploaded_file_1 = st.file_uploader("Upload the first CSV file", type=["csv"])
        uploaded_file_2 = st.file_uploader("Upload the second CSV file", type=["csv"])

        if uploaded_file_1 and uploaded_file_2:
            try:
                df1 = pd.read_csv(uploaded_file_1)
                df2 = pd.read_csv(uploaded_file_2)
                st.write("Data from the first file:", df1.head())
                st.write("Data from the second file:", df2.head())

                selected_cols1 = st.multiselect("Select columns from first file:", df1.columns)
                selected_cols2 = st.multiselect("Select columns from second file:", df2.columns)

                if selected_cols1 and selected_cols2:
                    plt.figure(figsize=(10, 5))
                    for col in selected_cols1:
                        plt.plot(df1[col], label=f"File 1: {col}")
                    for col in selected_cols2:
                        plt.plot(df2[col], label=f"File 2: {col}")
                    plt.legend()
                    plt.title("Dynamic Visualization Comparison")
                    st.pyplot(plt)
                else:
                    st.warning("Please select columns from both files for comparison.")
            except Exception as e:
                st.error(f"Error processing files: {e}")
