import streamlit as st
import os
import pandas as pd
import pickle
import json
from cryptography.fernet import Fernet

directory = os.path.dirname(os.path.abspath(__file__))

USERS_FILE_PATH = os.path.join(directory, '../data/processed/user_data.pkl')
KEYS_FILE_PATH = os.path.join(directory, '../data/processed/secret.key')
SETTINGS_FILE_PATH = os.path.join(directory, '../data/processed/user_settings.json')

user_types = ['admin', 'trader', 'analyst', 'other']

# ------------ PASSWORD ------------------

# Manage the encryption key
def load_or_create_key():
    if os.path.exists(KEYS_FILE_PATH):
        with open(KEYS_FILE_PATH, 'rb') as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(KEYS_FILE_PATH, 'wb') as f:
            f.write(key)
        return key

# Key generation for encryption
def generate_key():
    return Fernet.generate_key()

# Load user data from a pickle file
def load_user_data():
    try:
        with open(USERS_FILE_PATH, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}

# Save user data to a pickle file
def save_user_data(user_data):
    with open(USERS_FILE_PATH, 'wb') as f:
        pickle.dump(user_data, f)

# Hash the password
def hash_password(password):
    key = load_or_create_key()
    f = Fernet(key)
    return f.encrypt(password.encode()).decode()

# Create a new user account
def create_user(username, fullname, usertype, password):
    hashed_password = hash_password(password)
    user_data = load_user_data()
    user_data[username] = {'fullname': fullname, 'profil': usertype, 'password': hashed_password}
    save_user_data(user_data)
    message = "User created successfully!"
    return message

# Visualize all users in a DataFrame
def visualize_users():
    user_data = load_user_data()
    df = pd.DataFrame.from_dict(user_data, orient='index')
    df.drop(columns='password', inplace=True)
    return df

# Modify a user account
def modify_user(username, fullname, new_type, new_password):
    user_data = load_user_data()
    if username in user_data:
        key = generate_key()
        hashed_password = hash_password(new_password, key)
        user_data[username] = {'fullname': fullname, 'profil': new_type, 'password': hashed_password}
        save_user_data(user_data)
        message = "User modified successfully!"
    else:
        message = "User not found!"
    
    return message

# Delete a user account
def delete_user(username):
    user_data = load_user_data()
    if username in user_data:
        del user_data[username]
        save_user_data(user_data)
        message = "User deleted successfully!"
    else:
        message = "User not found!"
    
    return message

# Verify the password
def verify_password(username, plaintext_password):
    user_data = load_user_data()
    
    if username in user_data:
        key = load_or_create_key()  # Use the same key as stored
        f = Fernet(key)

        # Retrieve the stored encrypted password
        stored_hashed_password = user_data[username]['password']
        
        # Attempt to decrypt the stored password
        try:
            decrypted_password = f.decrypt(stored_hashed_password.encode()).decode()
            # Compare the decrypted password with the plaintext password provided by the user
            return decrypted_password == plaintext_password
        except Exception:
            return False  # Decryption failed, indicating an incorrect password
    else:
        return False  # User not found


# ------------ PREFERENCES ------------------

def load_user_settings():
    """Load the JSON file containing all user settings."""
    if not os.path.exists(SETTINGS_FILE_PATH):
        return {}
    with open(SETTINGS_FILE_PATH, 'r') as f:
        return json.load(f)

def save_user_settings(settings):
    """Save the settings dictionary to the JSON file."""
    with open(SETTINGS_FILE_PATH, 'w') as f:
        json.dump(settings, f, indent=4)

def get_user_settings(username):
    """Retrieve settings for a specific user."""
    settings = load_user_settings()
    return settings.get(username, {})

def set_user_settings(username, new_settings):
    """Create or update settings for a specific user."""
    settings = load_user_settings()
    settings[username] = new_settings
    save_user_settings(settings)

def update_user_settings(username, key, value):
    """Update a specific setting for a user."""
    settings = load_user_settings()
    if username in settings:
        settings[username][key] = value
    else:
        settings[username] = {key: value}
    save_user_settings(settings)

def add_more_user_settings(username, key, value):
    """Update a specific setting for a user."""
    settings = load_user_settings()
    if username in settings:
        concat_value = settings[username][key] + list(value.split(';'))
        settings[username][key] = concat_value
    else:
        settings[username] = {key: [value]}
    save_user_settings(settings)

def delete_user_settings(username):
    """Delete all settings for a specific user."""
    settings = load_user_settings()
    if username in settings:
        del settings[username]
    save_user_settings(settings)