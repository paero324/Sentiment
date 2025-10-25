# auth.py
import streamlit as st
from db import authenticate_user, register_user, init_db

def show_login():
    """Display login form."""
    st.title("Login to Sentiment Analysis App")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            user_id = authenticate_user(username, password)
            if user_id:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")

def show_register():
    """Display registration form."""
    st.title("Register for Sentiment Analysis App")
    
    with st.form("register_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit_button = st.form_submit_button("Register")
        
        if submit_button:
            if password != confirm_password:
                st.error("Passwords do not match")
            elif register_user(username, password, email):
                st.success("Registration successful! Please login.")
                st.session_state.show_login = True
                st.rerun()
            else:
                st.error("Username or email already exists")

def logout():
    """Logout the current user."""
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.rerun()

def check_auth():
    """Check if user is authenticated."""
    init_db()  # Initialize database if not exists
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.show_login = True
    
    if not st.session_state.logged_in:
        if st.session_state.show_login:
            show_login()
        else:
            show_register()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Go to Login"):
                st.session_state.show_login = True
                st.rerun()
        with col2:
            if st.button("Go to Register"):
                st.session_state.show_login = False
                st.rerun()
        
        return False
    return True
