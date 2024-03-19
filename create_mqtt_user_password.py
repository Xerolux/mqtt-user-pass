from passlib.hash import pbkdf2_sha512
import getpass

def create_mqtt_user_password(password):
    salt_size = 16
    iterations = 100000

    hashed_password = pbkdf2_sha512.using(salt_size=salt_size, rounds=iterations).hash(password)
    return hashed_password

def username_exists(username, filename="mqtt_user_credentials.txt"):
    with open(filename, "r") as file:
        for line in file:
            stored_username, _ = line.strip().split(":", 1)
            if stored_username == username:
                return True
    return False

def write_credentials_to_file(username, hashed_password, filename="mqtt_user_credentials.txt"):
    if username_exists(username, filename):
        print(f"Error: Username '{username}' already exists. Please use a different username.")
        return False
    with open(filename, "a") as file:
        file.write(f"{username}:{hashed_password}\n")
    print(f"Credentials for '{username}' added to '{filename}'.")
    return True

def delete_user_from_file(username, filename="mqtt_user_credentials.txt"):
    updated_credentials = []
    user_found = False

    with open(filename, "r") as file:
        for line in file:
            stored_username, _ = line.strip().split(":", 1)
            if stored_username != username:
                updated_credentials.append(line)
            else:
                user_found = True

    if user_found:
        with open(filename, "w") as file:
            for credential in updated_credentials:
                file.write(credential)
        print(f"User '{username}' has been removed from '{filename}'.")
    else:
        print(f"User '{username}' not found in '{filename}'.")

def show_user_credentials(username, filename="mqtt_user_credentials.txt"):
    with open(filename, "r") as file:
        for line in file:
            stored_username, hashed_password = line.strip().split(":", 1)
            if stored_username == username:
                print(f"User '{username}' found. Hashed password: {hashed_password}")
                return
    print(f"User '{username}' not found in '{filename}'.")

def show_all_users(filename="mqtt_user_credentials.txt"):
    print("Listing all users:")
    with open(filename, "r") as file:
        for line in file:
            username, _ = line.strip().split(":", 1)
            print(username)

def main_menu():
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
                hashed_password = create_mqtt_user_password(password)
                write_credentials_to_file(username, hashed_password)
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
            break
        else:
            print("Invalid choice, please enter a number between 1 and 5.")

if __name__ == "__main__":
    main_menu()

