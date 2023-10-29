#!/bin/bash/
if [ "$EUID" -ne 0 ]
  then
  echo "Please run with SUDO (as root)"
  exit
fi
if [[ -f "/etc/lsb-release" || -f "/etc/debian_version" ]]
    then
        echo "Linux Ubuntu detected and is supported"
    else
        echo "This Linux Distro is not supported, exiting..."
        exit
    fi
echo "This script automatically installs all required dependencies for Sunstorm!"
sudo add-apt-repository universe && sudo apt update && sudo apt install python3 && sudo apt install python3-pyqt5 && pip3 install -r requirements.txt && sudo apt-get update && sudo apt install libimobiledevice-utils libusbmuxd-tools git curl python3-pip unzip clang -y && python3 -m pip install pyimg4 && sudo wget http://nz2.archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2.17_amd64.deb && sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2.17_amd64.deb && sudo rm libssl1.1_1.1.1f-1ubuntu2.17_amd64.deb

echo "Requirements installed Successfully!"
echo "Made by UnknownCoder13 with love :)"