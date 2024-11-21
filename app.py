import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set the page title and layout
st.set_page_config(page_title="Energy Consumption Visualization", layout="centered")

# Set the style for plots
sns.set(style="whitegrid")

# Hardcoded credentials for simplicity
USER_CREDENTIALS = {
    "user1": "password1",
    "user2": "password2"
}

# Function to verify login credentials
def verify_login(username, password):
    return USER_CREDENTIALS.get(username) == password

# Function to handle "Forgot Password"
def forgot_password():
    st.warning("Password reset functionality is not implemented yet. Please contact support.")

# Main app layout
st.markdown('<div class="login-container">', unsafe_allow_html=True)
st.markdown('<div class="welcome-header">🔋 Welcome to the Energy Consumption App 🔋</div>', unsafe_allow_html=True)

# Login state management
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    # Display login form with improved login header
    st.markdown('<div class="login-header">🔑 Please Log In</div>', unsafe_allow_html=True)
    
    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")

    if st.button("Login", key='login_button'):
        if verify_login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username  # Store username in session state
            st.success(f"🎉 Welcome {username}! You are logged in.")
        else:
            st.error("🚫 Invalid username or password. Please try again.")
    
    # Forgot password button with action
    if st.button("Forgot Password?", key='forgot_password_button'):
        forgot_password()

else:
    st.success(f"🎉 Welcome back, {st.session_state.username}!")

    # Dataset load from URL
    data_url = "https://raw.githubusercontent.com/aishvipareek/ECDanalysis/refs/heads/main/energy-consumption-2020-1.csv"
    try:
        df = pd.read_csv(data_url)
    except Exception as e:
        st.error(f"Error: Could not load the dataset from the URL. Details: {e}")
        st.stop()

    # Sidebar for visualization type selection
    st.sidebar.header("📊 Visualization Options")
    option = st.sidebar.radio("Choose Visualization Type", ["📈 Static Visualization", "📉 Dynamic Visualization"])

    # Sidebar content based on user selection
    if option == "📈 Static Visualization":
        st.sidebar.markdown('<div class="viz-header">📊 Static Visualization</div>', unsafe_allow_html=True)
    elif option == "📉 Dynamic Visualization":
        st.sidebar.markdown('<div class="viz-header">📉 Dynamic Visualization</div>', unsafe_allow_html=True)

    # Add About Us, User Guide, and Help & Support sections in the sidebar
    st.sidebar.markdown("### About Us")
    st.sidebar.markdown("We are dedicated to providing insights into energy consumption data to help improve sustainability.")
    st.sidebar.markdown("---")  # Line separator

    st.sidebar.markdown("### User Guide")
    st.sidebar.markdown("1. Log in with your credentials.\n2. Select a visualization type.\n3. Choose your desired columns and parameters for analysis.")
    st.sidebar.markdown("---")  # Line separator

    st.sidebar.markdown("### Help & Support")
    st.sidebar.markdown("For assistance, please contact us at: aishvipareek05@gmail.com\nPhone: +9158645236")
    st.sidebar.markdown("---")  # Line separator

    # Logout button in the sidebar
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("You have logged out successfully.")

    # Visualization Options
    if option == "📈 Static Visualization":
        st.markdown('<div class="viz-header">📊 Static Visualization</div>', unsafe_allow_html=True)
        st.write("Select one or more columns and view a static chart.")

        # Column selection for static visualization
        selected_static_columns = st.multiselect("Select columns for static visualization:", df.columns)

        if st.button("Show Static Visualization"):
            st.markdown(f'<div class="chart-title">Static Visualization for {", ".join(selected_static_columns)}</div>', unsafe_allow_html=True)
            plt.figure(figsize=(10, 5))
            
            for column in selected_static_columns:
                plt.plot(df[column], label=column)  # Plot each selected column
            plt.legend()  # Show legend for each column
            plt.title('Line Chart of Selected Columns')
            plt.xlabel('Index')
            plt.ylabel('Values')
            st.pyplot(plt)

    # Dynamic Visualization with two file uploads and comparison
    elif option == "📉 Dynamic Visualization":
        st.markdown('<div class="viz-header">📉 Dynamic Visualization</div>', unsafe_allow_html=True)

        # File upload widget for the user to upload two datasets
        uploaded_file_1 = st.file_uploader("Upload the first CSV file", type=["csv"])
        uploaded_file_2 = st.file_uploader("Upload the second CSV file", type=["csv"])

        if uploaded_file_1 is not None and uploaded_file_2 is not None:
            try:
                # Load both files
                df1 = pd.read_csv(uploaded_file_1)
                df2 = pd.read_csv(uploaded_file_2)

                # Display first few rows of both datasets
                st.write("📊 Data from File 1:")
                st.dataframe(df1.head())
                st.write("📊 Data from File 2:")
                st.dataframe(df2.head())

                # Allow user to select chart type for dynamic data
                chart_type = st.radio("Select Chart Type", ("Line", "Bar", "Pie"))

                # Allow user to select columns for plotting
                selected_column_1 = st.selectbox("Select column from File 1", df1.columns)
                selected_column_2 = st.selectbox("Select column from File 2", df2.columns)

                # Handling mixed-type columns by selecting specific columns for plotting
                if chart_type == "Line":
                    st.write("📈 Line Chart of the data:")
                    plt.figure(figsize=(10, 5))
                    plt.plot(df1[selected_column_1], label=selected_column_1)
                    plt.plot(df2[selected_column_2], label=selected_column_2)
                    plt.legend()
                    plt.title('Line Chart of Selected Columns')
                    plt.xlabel('Index')
                    plt.ylabel('Values')
                    st.pyplot(plt)

                elif chart_type == "Bar":
                    st.write("📊 Bar Chart of the data:")
                    df_combined = pd.DataFrame({selected_column_1: df1[selected_column_1], selected_column_2: df2[selected_column_2]})
                    st.bar_chart(df_combined)

                elif chart_type == "Pie":
                    st.write("🍰 Pie Chart of the data:")
                    fig, ax = plt.subplots(figsize=(8, 8))
                    df1.set_index(selected_column_1).plot.pie(y=selected_column_2, autopct='%1.1f%%', ax=ax)
                    st.pyplot(fig)

            except Exception as e:
                st.error(f"Error: Could not process the uploaded files. Details: {e}")

