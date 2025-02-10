import os
import json
from datetime import datetime
import re

class HoneypotLogReader:
    def __init__(self, log_directory="/var/log/honeypot/"):
        self.log_directory = log_directory
        
    def read_filesystem_events(self, log_file="filesystem_events.log"):
        events = []
        with open(os.path.join(self.log_directory, log_file)) as f:
            for line in f:
                try:
                    # Parse timestamp, user, action, and file path
                    match = re.match(r'(.*?) - User:(.*?) - Action:(.*?) - File:(.*)', line.strip())
                    if match:
                        events.append({
                            'timestamp': match.group(1),
                            'user': match.group(2),
                            'action': match.group(3),
                            'file': match.group(4)
                        })
                except Exception as e:
                    print(f"Error parsing line: {line} - {str(e)}")
        return events

    def read_integrity_logs(self, log_file="integrity.log"):
        modifications = []
        with open(os.path.join(self.log_directory, log_file)) as f:
            for line in f:
                try:
                    # Parse timestamp and modified file
                    match = re.match(r'(.*?) - Modified: (.*)', line.strip())
                    if match:
                        modifications.append({
                            'timestamp': match.group(1),
                            'file': match.group(2)
                        })
                except Exception as e:
                    print(f"Error parsing line: {line} - {str(e)}")
        return modifications

    def read_audit_logs(self, log_file="/var/log/audit/audit.log"):
        audit_events = []
        with open(log_file) as f:
            for line in f:
                if 'type=USER_CMD' in line or 'type=SYSCALL' in line:
                    audit_events.append(line.strip())
        return audit_events

    def analyze_activity(self):
        fs_events = self.read_filesystem_events()
        integrity_events = self.read_integrity_logs()
        audit_events = self.read_audit_logs()
        
        return {
            'filesystem_events': len(fs_events),
            'integrity_violations': len(integrity_events),
            'audit_events': len(audit_events),
            'suspicious_files': [e['file'] for e in fs_events if e['action'] in ['MODIFY', 'DELETE']],
            'recent_events': fs_events[-10:]  # Last 10 events
        }

# Usage example
if __name__ == "__main__":
    reader = HoneypotLogReader()
    activity = reader.analyze_activity()
    print(json.dumps(activity, indent=2))
