"""
This module provides a command-line interface for managing MQTT user credentials. It supports
adding, deleting, and displaying user credentials securely stored with hashed passwords. The
tool utilizes PBKDF2 with SHA-512 for password hashing, ensuring a high level of security for
stored credentials.
"""

import getpass
import re  # For regex pattern matching
from passlib.hash import pbkdf2_sha512

def create_mqtt_user_password(password):
    """
    Hash a password using PBKDF2 with SHA-512.
    
    Parameters:
    - password: The plaintext password to hash.

    Returns:
    - A hashed password.
    """
    salt_size = 16
    iterations = 100000

    hashed_password = pbkdf2_sha512.using(salt_size=salt_size, rounds=iterations).hash(password)
    return hashed_password

def username_exists(username, filename="mqtt_user_credentials.txt"):
    """
    Check if a username already exists in the specified file.
    
    Parameters:
    - username: The username to check.
    - filename: The file in which to check for the username.
    
    Returns:
    - True if the username exists, False otherwise.
    """
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            stored_username, _ = line.strip().split(":", 1)
            if stored_username == username:
                return True
    return False

def write_credentials_to_file(username, hashed_password, filename="mqtt_user_credentials.txt"):
    """
    Write a username and hashed password to the specified file.
    
    Parameters:
    - username: The username to write.
    - hashed_password: The hashed password to write.
    - filename: The file to which the credentials will be written.
    
    Returns:
    - True if writing succeeded, False otherwise (e.g., if username already exists).
    """
    exists_msg = f"Error: Username '{username}' already exists. Please use a different username."
    if username_exists(username, filename):
        print(exists_msg)
        return False
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"{username}:{hashed_password}\n")
    print(f"Credentials for '{username}' added to '{filename}'.")
    return True

def validate_password(password):
    """
    Validate a password based on length and character requirements.
    
    Parameters:
    - password: The password to validate.
    
    Returns:
    - True if the password meets the requirements, False otherwise.
    """
    if (8 <= len(password) <= 16 and re.search("[a-zA-Z]", password) and
        re.search("[0-9]", password)):
        return True
    return False

def show_user_credentials(username, filename="mqtt_user_credentials.txt"):
    """
    Display the hashed password for a specified username.
    
    Parameters:
    - username: The username whose credentials to show.
    - filename: The file from which to read the credentials.
    """
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            stored_username, hashed_password = line.strip().split(":", 1)
            if stored_username == username:
                print(f"User '{username}' found. Hashed password: {hashed_password}")
                return
    print(f"User '{username}' not found in '{filename}'.")

def show_all_users(filename="mqtt_user_credentials.txt"):
    """
    List all usernames in the specified file.
    
    Parameters:
    - filename: The file from which to read the usernames.
    """
    print("Listing all users:")
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            username, _ = line.strip().split(":", 1)
            print(username)

def delete_user_from_file(username, filename="mqtt_user_credentials.txt"):
    """
    Remove a user's credentials from the specified file.
    
    Parameters:
    - username: The username to remove.
    - filename: The file from which to remove the user's credentials.
    """
    updated_credentials = []
    user_found = False

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            stored_username, _ = line.strip().split(":", 1)
            if stored_username != username:
                updated_credentials.append(line)
            else:
                user_found = True

    if user_found:
        with open(filename, "w", encoding="utf-8") as file:
            file.writelines(updated_credentials)
        print(f"User '{username}' has been removed from '{filename}'.")
    else:
        print(f"User '{username}' not found in '{filename}'.")

def main_menu():
    """
    Run the main menu loop for the MQTT User Credentials Manager.
    """
    while True:
        print("\nMQTT User Credentials Manager")
        print("1. Add User")
        print("2. Delete User")
        print("3. Show User Credentials")
        print("4. Show All Users")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            username = input("Enter MQTT username: ")
            if not username_exists(username):
                password = getpass.getpass("Enter password (input will be hidden): ")
                if validate_password(password):
                    hashed_password = create_mqtt_user_password(password)
                    write_credentials_to_file(username, hashed_password)
                else:
                    print("Password must be 8-16 characters long and contain both numbers and letters.")
            else:
                print(f"Username '{username}' already exists. Please choose a different username.")
        elif choice == '2':
            username = input("Enter MQTT username to delete: ")
            delete_user_from_file(username)
        elif choice == '3':
            username = input("Enter MQTT username to show: ")
            show_user_credentials(username)
        elif choice == '4':
            show_all_users()
        elif choice == '5':
            print("Exiting MQTT User Credentials Manager.")
            print("Please restart your MQTT broker for changes to take effect.", end='')
            print("\033[31m\033[0m")
            break
        else:
            print("Invalid choice, please enter a number between 1 and 5.")

if __name__ == "__main__":
    main_menu()
