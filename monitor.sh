#!/bin/bash
# Save as monitor.sh

MONITORED_DIRS="/etc /var/www /home"
LOG_FILE="/var/log/honeypot/filesystem_events.log"

inotifywait -m -r $MONITORED_DIRS \
  -e create -e modify -e delete -e open -e attrib -e move \
  --format '%T %w%f %e %u' --timefmt '%Y-%m-%d %H:%M:%S' \
  | while read datetime path action user
do
    echo "$datetime - User:$user - Action:$action - File:$path" >> $LOG_FILE
    
    # Alert on suspicious activities
    case "$action" in
        "MODIFY"|"DELETE")
            if [[ "$path" == *"/etc/"* ]]; then
                logger -p auth.alert "Critical file modification: $path by $user"
            fi
            ;;
    esac
done
