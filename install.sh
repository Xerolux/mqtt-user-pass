#!/bin/bash

# Ensure the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

# Function to check if a command exists
command_exists() {
    command -v "$@" >/dev/null 2>&1
}

# Check for Python 3 and install if necessary
if command_exists python3; then
    echo "Python 3 is installed."
else
    echo "Python 3 is not installed. Attempting to install Python 3..."
    apt update && apt install -y python3
fi

# Check for pip and install if necessary
if command_exists pip3; then
    echo "pip is installed."
else
    echo "pip is not installed. Attempting to install pip..."
    apt install -y python3-pip
fi

# Define the installation directory and the virtual environment path
INSTALL_DIR="/usr/local/bin"
VENV_PATH="/opt/mqtt_user_manager_venv"

# Get Python3 version
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')

# Function to compare Python versions
version_greater_than_or_equal_to() {
    # Use sort with version sort option and check the first line
    [ "$(printf '%s\n' "$2" "$1" | sort -V | head -n1)" = "$2" ]
}

# Check if Python version is greater than or equal to 3.9
if version_greater_than_or_equal_to "$PYTHON_VERSION" "3.9"; then
    echo "Python version is $PYTHON_VERSION. Creating a virtual environment."
    # Create virtual environment
    python3 -m venv "$VENV_PATH"
    # Activate the virtual environment
    source "$VENV_PATH/bin/activate"
    # Install dependencies inside the virtual environment
    pip install passlib>=1.7.4
    # Deactivate the virtual environment
    deactivate
else
    # Install dependencies globally if Python version is less than 3.9
    echo "Python version is $PYTHON_VERSION. Installing dependencies globally."
    pip3 install passlib>=1.7.4
fi

# Copy the Python script to the installation directory
SCRIPT_NAME="mqtt_user_manager.py" # Replace this with your script's filename
cp "$SCRIPT_NAME" "$INSTALL_DIR/mqtt_user_manager"

# Make the script executable
chmod +x "$INSTALL_DIR/mqtt_user_manager"

echo "Installation completed. You can run the script using 'mqtt_user_manager'"
