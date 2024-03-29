#!/usr/bin/env bash
# Techno Installer Project
# This Project Aims to Simplify the environment construction of raspberry pi boards in any Technopark Projects.
# Author: Yaakov Azat Copyright: 2019 Azat Artificial Intelligence, LLP.
echo ''
echo '    _             _      _    ___' 
echo '    / \   ______ _| |_   / \  |_ _|'
echo '   / _ \ |_  / _` | __| / _ \  | | '
echo '  / ___ \ / / (_| | |_ / ___ \ | | '
echo ' /_/   \_\___\__,_|\__/_/   \_\___|'
echo ''
echo 'Technopark Raspberry IoT controlkit Installer'
echo 'Copyright: 2019 Azat Artificial Intelligence'
echo '....Al-Farabi Kazakh National University....'
echo ''
echo 'initializing...'
echo -ne '#####                     (33%)\r'
    sleep 1
    echo -ne '#############             (66%)\r'
    sleep 1
    echo -ne '#######################   (100%)\r'
    echo -ne '\n'
if [ "$(uname)" == "Darwin" ]
then
    echo 'Mac OS detected...'
    echo ''
    echo 'skipping...'
    echo ''
    echo 'Please run this software within a raspberry pi or an android device'
    echo ''
    echo 'Rolling back:'

    echo -ne '#####                     (33%)\r'
    sleep 1
    echo -ne '#############             (66%)\r'
    sleep 1
    echo -ne '#######################   (100%)\r'
    echo -ne '\n'
    cd /
else
    echo "Linux/Unix platform detected..."
    echo ''
    echo 'Start installing Python3 on raspberry pi...'
    sudo apt install python3 -y
    echo 'Python3 installed.'
    sudo apt install python3-dev -y
    echo 'Python3 Development Version Installed.'
    sudo apt install python3-pip -y
    echo 'pip3 installed'
    sudo apt install python3-venv
    echo 'Python3 virtualenv installed'
    sudo apt install git
    echo 'Git installed successfully'
    echo 'Detecting File systems and file versions...'
    echo 'Done!'
    echo ''
    echo 'Creating Driver Source files...'
    echo 'Downloading SI1145 driver source files...'
    git clone https://github.com/THP-JOE/Python_SI1145 azt/techno/si1145
    echo 'SI1145 source files downloaded!'
    echo 'creating python3 virtualenv...'
    echo 'virtualenv activated!'
    cd ./azt/techno/si1145/ && sudo python3 setup.py install
    echo 'SI45 drivers installed successfully!'
    echo 'Done!'
    echo 'Installing AzatAI Technopark IOT controller:'
    sleep 1
    echo -ne '#####                     (33%)\r'
    cd / && git clone https://github.com/yaakovazat/techno azt/techno/bin
    sleep 1
    echo -ne '#############             (66%)\r'
    sleep 1
    echo -ne '#######################   (100%)\r'
    echo 'Done!'
fi