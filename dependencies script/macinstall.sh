#!/bin/bash

# Check for root privileges
if [[ $EUID -ne 0 ]]; then
    echo "Please run with sudo (as root)"
    exit
fi

# Check for macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "This script is intended for macOS only."
    exit
fi

echo "macOS detected"

# Install Homebrew if it's not installed
if ! command -v brew &>/dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

echo "Installing dependencies..."

# Update Homebrew and install dependencies
brew update
brew install python3 git curl clang libimobiledevice usbmuxd
pip3 install pyqt5

# If you have a requirements.txt file for Python packages
if [[ -f "requirements.txt" ]]; then
    pip3 install -r requirements.txt
fi

# Install additional Python packages
pip3 install pyimg4

# Additional steps go here (if any)

echo "Requirements installed successfully!"
echo "Made by UnknownCoder13 with love :)"