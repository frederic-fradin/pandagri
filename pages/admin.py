import streamlit as st
from src import load_user_data, save_user_data, create_user, visualize_users, modify_user, delete_user, verify_password

user_types = ['admin', 'trader', 'analyst', 'other']

st.header('Administration')

tab1, tab2 = st.tabs(['GENERAL', 'ACCOUNT'])

with tab2:
    col1, col2, col3 = st.columns([7.5,0.5,2])
    col3.write('')
    admin_view = col3.selectbox("Select Action", ["Create User", "Visualize Users", "Modify User", "Delete User"])

    if admin_view == "Create User":
        usertype = col3.selectbox("User Type:", options=user_types, key='crea1', index=None)
        username = col3.text_input("Username:", key='crea2')
        fullname = col3.text_input("Fullname:", key='crea3')
        password = col3.text_input("Password:", type='password', key='crea4')
        col3.write('')
        if col3.button("Create Account", use_container_width=True):
            message = create_user(username, fullname, usertype, password)
            col3.info(message)
            col1.write('')
            col1.write('User accounts')
            df = visualize_users()
            col1.dataframe(df, use_container_width=True)

    elif admin_view == "Visualize Users":
        col1.write('')
        col1.write('User accounts')
        df = visualize_users()
        col1.dataframe(df, use_container_width=True)

    elif admin_view == "Modify User":
        user_data = load_user_data()
        new_type = col3.selectbox("User Type:", options=user_types, key='mod1')
        username = col3.selectbox("Username:", options=user_data, key='mod2')
        fullname = col3.text_input("Fullname:", key='mod3')
        new_password = col3.text_input("New Password:", type='password', key='mod4')
        col3.write('')
        if col3.button("Modify Account", use_container_width=True):
            message = modify_user(username, fullname, new_type, new_password)
            col3.info(message)

    elif admin_view == "Delete User":
        user_data = load_user_data()
        username = col3.selectbox("Username:", options=user_data, key='del1')
        col3.write('')
        if col3.button("Delete Account", use_container_width=True):
            message = delete_user(username)
            col3.info(message)