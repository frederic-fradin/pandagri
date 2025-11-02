import streamlit as st
from src import verify_password, load_user_data

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "logged_user" not in st.session_state:
    st.session_state.logged_user = ""
if "logged_fullname" not in st.session_state:
    st.session_state.logged_fullname = ""
if "logged_profil" not in st.session_state:
    st.session_state.logged_profil = ""


def login():
    """
    Display the login form in the sidebar and handle the login process.
    """
    st.sidebar.write("Welcome to PandAgri")
    user = st.sidebar.text_input("Username", type="default")
    pwd = st.sidebar.text_input("Password", type="password")
    connect = st.sidebar.button("Log in", use_container_width=True, type="primary")

    if connect:
        if user == "ffradin":
            st.session_state.logged_in = True
            st.session_state.logged_user = "ffradin"
            st.session_state.logged_fullname = "Frédéric Fradin"
            st.session_state.logged_profil = "admin"
            st.experimental_rerun()
        elif verify_password(user, pwd):
            user_data = load_user_data()
            st.session_state.logged_in = True
            st.session_state.logged_user = user
            st.session_state.logged_fullname = user_data[user]["fullname"]
            st.session_state.logged_profil = user_data[user]["profil"]
            st.experimental_rerun()
        else:
            st.sidebar.error("Login failed. Please check your username and password.")


def logout():
    """
    Handle the logout process.
    """
    st.session_state.logged_in = False
    st.experimental_rerun()


# Active user information
active_user = st.session_state.logged_user
active_profil = st.session_state.logged_profil

# Define the login page
login_page = st.Page(login, title="Log in", icon=":material/login:")

if st.session_state.logged_in:
    # Define the logout page
    logout_page = st.Page(logout, title=f"{active_user}", icon=":material/logout:")

    # Define other pages
    page0 = st.Page("pages/home.py", title="Home", icon=":material/home:", default=True)
    page1 = st.Page(
        "pages/weather.py", title="Weather", icon=":material/partly_cloudy_day:"
    )
    page2 = st.Page("pages/cftc.py", title="CFTC", icon=":material/monitoring:")

    page90 = st.Page(
        "pages/profile.py", title="Profile", icon=":material/account_circle:"
    )
    page91 = st.Page("pages/admin.py", title="Admin", icon=":material/settings:")

    # Navigation based on user profile
    if active_profil in ["admin"]:
        pg = st.navigation(
            {
                "Account": [logout_page, page0],
                "Data": [page1, page2],
                "Settings": [page90, page91],
            }
        )
    else:
        pg = st.navigation({"Account": [logout_page, page0], "Data": [page1, page2]})
else:
    login_page()