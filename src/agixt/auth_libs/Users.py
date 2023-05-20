import os
import json
import bcrypt
import streamlit as st
from auth_libs.Cfig import Cfig

CFIG = Cfig()

USER_FILE = "user_data.json"

def load_users():
    """
    Loads the user data from the user file.
    If the user file doesn't exist, triggers the initial user setup.
    Returns the loaded user data.
    """
    if not os.path.exists(USER_FILE):
        # Initial user setup
        st.write("Admin Account Setup")
        admin_email = st.text_input("Enter the admin email")
        admin_password = st.text_input("Enter the admin password", type="password")
        confirm_password = st.text_input("Confirm the admin password", type="password")
        if st.button("Create Admin Account"):
            if admin_password != confirm_password:
                st.error("Password and confirm password do not match.")
            else:
                admin_password_hash = bcrypt.hashpw(admin_password.encode(), bcrypt.gensalt())
                admin_data = {
                    "email": admin_email,
                    "password_hash": admin_password_hash.decode(),
                    "admin": True
                }
                user_data = {
                    "users": [admin_data]
                }
                save_user_data(user_data)
                st.success("Admin account created successfully!")
                return user_data
    else:
        with open(USER_FILE, "r") as file:
            user_data = json.load(file)
    return user_data

def save_user_data(user_data):
    """
    Saves the user data to the user file.
    """
    with open(USER_FILE, "w") as file:
        json.dump(user_data, file, indent=4)

def configure_auth_settings():
    """
    Prompts the admin to configure the authentication settings.
    """
    st.write("Auth/Login Settings Configuration")
    setup_cfg = st.radio("Auth/Login Settings", ("No Login", "Single-User Login", "Multi-User Private Registration", "Multi-User Public Registration"), 0)
    if st.button("Build Config"):
        CFIG.set_auth_setup_config(setup_cfg)
        st.success("Auth/Login settings configured!")
        st.experimental_rerun()
    st.stop()

def check_admin_configured():
    """
    Checks if the admin configuration is already done.
    Returns True if configured, False otherwise.
    """
    return CFIG.is_auth_setup_configured()