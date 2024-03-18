from passlib.hash import pbkdf2_sha512

def create_mqtt_user_password(password):
    # Configuration for PBKDF2
    salt_size = 16  # Increase salt size for better security
    iterations = 100000  # Number of iterations, higher is more secure but slower

    # Generate hash
    hashed_password = pbkdf2_sha512.using(salt_size=salt_size, rounds=iterations).hash(password)
    return hashed_password

def write_credentials_to_file(username, hashed_password, filename="mqtt_user_credentials.txt"):
    # Append credentials to the file
    with open(filename, "a") as file:
        file.write(f"{username}:{hashed_password}\n")
    print(f"Credentials for '{username}' added to '{filename}'.")

if __name__ == "__main__":
    import getpass

    username = input("Enter MQTT username: ")
    password = getpass.getpass("Enter password (input will be hidden): ")
    
    hashed_password = create_mqtt_user_password(password)
    
    # You can specify a different filename as needed
    write_credentials_to_file(username, hashed_password)
