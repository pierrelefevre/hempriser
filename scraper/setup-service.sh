#!/bin/bash

# Check if the script is run as root
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# Path to the systemd service file
SERVICE_FILE="$(dirname "$(realpath "$0")")/bostadspriser.service"
SERVICE_DEST="/etc/systemd/system/bostadspriser.service"

START_ALL_FILE="$(dirname "$(realpath "$0")")/start-all.sh"
START_ALL_DEST="/usr/bin/start-all.sh"

sudo cp "$SERVICE_FILE" "$SERVICE_DEST"
sudo cp "$START_ALL_FILE" "$START_ALL_DEST"

# Reload systemd to recognize new service
sudo systemctl daemon-reload

# Enable and start the service
sudo systemctl enable bostadspriser.service
sudo systemctl start bostadspriser.service

echo "Service installed and started successfully."