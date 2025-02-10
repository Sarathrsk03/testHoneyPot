import os
import json
from datetime import datetime
import re
from inotify_simple import INotify, flags

class HoneypotLogReader:
   def __init__(self, log_directory="/var/log/honeypot/"):
       self.log_directory = log_directory
       self.inotify = INotify()
       self.watches = {}
       
   def setup_inotify_watches(self, paths=["/etc", "/var/www", "/home"]):
       watch_flags = flags.CREATE | flags.DELETE | flags.MODIFY | flags.OPEN | flags.CLOSE_WRITE
       for path in paths:
           try:
               wd = self.inotify.add_watch(path, watch_flags)
               self.watches[wd] = path
           except Exception as e:
               print(f"Error watching {path}: {str(e)}")

   def read_inotify_events(self, timeout=100):
       events = []
       for event in self.inotify.read(timeout=timeout):
           event_path = os.path.join(self.watches[event.wd], event.name)
           events.append({
               'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
               'path': event_path,
               'mask': event.mask,
               'flags': [flag for flag in flags.from_mask(event.mask)]
           })
       return events

   def read_filesystem_events(self, log_file="filesystem_events.log"):
       events = []
       try:
           with open(os.path.join(self.log_directory, log_file)) as f:
               for line in f:
                   try:
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
       except FileNotFoundError:
           print(f"Log file {log_file} not found")
       return events

   def read_integrity_logs(self, log_file="integrity.log"):
       modifications = []
       try:
           with open(os.path.join(self.log_directory, log_file)) as f:
               for line in f:
                   try:
                       match = re.match(r'(.*?) - Modified: (.*)', line.strip())
                       if match:
                           modifications.append({
                               'timestamp': match.group(1),
                               'file': match.group(2)
                           })
                   except Exception as e:
                       print(f"Error parsing line: {line} - {str(e)}")
       except FileNotFoundError:
           print(f"Log file {log_file} not found")
       return modifications

   def read_audit_logs(self, log_file="/var/log/audit/audit.log"):
       audit_events = []
       try:
           with open(log_file) as f:
               for line in f:
                   try:
                       if 'type=USER_CMD' in line or 'type=SYSCALL' in line:
                           # Parse key audit log fields
                           fields = {}
                           parts = line.strip().split(' ')
                           for part in parts:
                               if '=' in part:
                                   key, value = part.split('=', 1)
                                   fields[key] = value
                           
                           audit_events.append({
                               'timestamp': datetime.fromtimestamp(float(fields.get('msg_time', 0))),
                               'type': fields.get('type'),
                               'user': fields.get('auid'),
                               'exe': fields.get('exe'),
                               'cmd': fields.get('cmd'),
                               'raw': line.strip()
                           })
                   except Exception as e:
                       print(f"Error parsing audit line: {line} - {str(e)}")
       except FileNotFoundError:
           print(f"Audit log file {log_file} not found")
       return audit_events

   def monitor_realtime(self, callback=None):
       """
       Monitor events in real-time with optional callback
       """
       try:
           while True:
               events = self.read_inotify_events()
               if events:
                   if callback:
                       callback(events)
                   else:
                       print(json.dumps(events, indent=2))
       except KeyboardInterrupt:
           print("\nStopping monitor...")

   def analyze_activity(self):
       """
       Analyze all logged activity
       """
       fs_events = self.read_filesystem_events()
       integrity_events = self.read_integrity_logs()
       audit_events = self.read_audit_logs()
       inotify_events = self.read_inotify_events()
       
       analysis = {
           'filesystem_events': len(fs_events),
           'integrity_violations': len(integrity_events),
           'audit_events': len(audit_events),
           'inotify_events': len(inotify_events),
           'suspicious_files': [e['file'] for e in fs_events if e['action'] in ['MODIFY', 'DELETE']],
           'recent_events': {
               'filesystem': fs_events[-10:],
               'integrity': integrity_events[-10:],
               'audit': audit_events[-10:],
               'inotify': inotify_events[-10:]
           }
       }
       
       return analysis

def log_printer(events):
   """
   Example callback for monitor_realtime
   """
   for event in events:
       print(f"[{event['timestamp']}] {event['path']}: {event['flags']}")

if __name__ == "__main__":
   reader = HoneypotLogReader()
   reader.setup_inotify_watches()
   
   # Example 1: Print real-time events
   print("Monitoring real-time events (Ctrl+C to stop):")
   reader.monitor_realtime(callback=log_printer)
   
   # Example 2: Analyze all activity
   #analysis = reader.analyze_activity()
   #print(json.dumps(analysis, indent=2))
