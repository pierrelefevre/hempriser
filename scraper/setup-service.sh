#!/bin/bash

# Check if the script is run as root
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# Setup paths
SERVICE_FILE="$(dirname "$(realpath "$0")")/bostadspriser.service"
SERVICE_DEST="/etc/systemd/system/bostadspriser.service"

START_ALL_FILE="$(dirname "$(realpath "$0")")/start-all.sh"
START_ALL_DEST="/usr/bin/start-all.sh"

SCRAPER_DIR="/etc"
SCRAPER_SYMLINK_TARGET="${SCRAPER_DIR}/scraper"

# Copy service file
cp "$SERVICE_FILE" "$SERVICE_DEST"

# Copy start-all script
cp "$START_ALL_FILE" "$START_ALL_DEST"

# Copy scraper context with .env
## Check if the symbolic link already exists
if [ ! -L "$SCRAPER_SYMLINK_TARGET" ]; then
    ln -s "$(pwd)" "$SCRAPER_SYMLINK_TARGET"
fi

# Reload systemd to recognize new service
systemctl daemon-reload

# Enable and start the service
systemctl enable bostadspriser.service
systemctl start bostadspriser.service

echo "Service installed and started successfully."
