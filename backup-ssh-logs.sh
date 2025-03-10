#!/bin/bash

# Define variables
DATE=$(date -d "yesterday" +"%Y-%m-%d")  # Get yesterday's date since we're running at midnight
LOG_DIR="/var/log/ssh_archives"
FILENAME="ssh_log_${DATE}.txt"
OUTPUT_PATH="${LOG_DIR}/${FILENAME}"

# Create log directory if it doesn't exist
mkdir -p $LOG_DIR

# Extract SSH logs from the previous day (00:00:00 to 23:59:59) from system logs
# This works for most Linux distributions but may need adjustment based on your system
if [ -f "/var/log/auth.log" ]; then
    # Debian/Ubuntu systems
    grep "$(date -d "yesterday" +"%b %e")" /var/log/auth.log | grep -i "ssh" > "$OUTPUT_PATH"
elif [ -f "/var/log/secure" ]; then
    # Red Hat/CentOS systems
    grep "$(date -d "yesterday" +"%b %e")" /var/log/secure | grep -i "ssh" > "$OUTPUT_PATH"
else
    # Alternative method using journalctl (systemd-based systems)
    journalctl --since="$(date -d "yesterday" +"%Y-%m-%d 00:00:00")" --until="$(date -d "yesterday" +"%Y-%m-%d 23:59:59")" -u sshd > "$OUTPUT_PATH"
fi

# Add header to the log file
sed -i "1i # SSH Log for ${DATE} #\n" "$OUTPUT_PATH"

# Add a summary of login attempts at the end of the file
echo -e "\n\n# SUMMARY #" >> "$OUTPUT_PATH"
echo "Successful logins: $(grep -c "Accepted" "$OUTPUT_PATH")" >> "$OUTPUT_PATH"
echo "Failed logins: $(grep -c "Failed password" "$OUTPUT_PATH")" >> "$OUTPUT_PATH"
echo "Invalid users: $(grep "Invalid user" "$OUTPUT_PATH" | wc -l)" >> "$OUTPUT_PATH"

# Set permissions to restrict access
chmod 600 "$OUTPUT_PATH"

# Log that the backup was created
logger "SSH log for ${DATE} has been archived to ${OUTPUT_PATH}"
