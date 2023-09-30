# Fan-Manager
Python Fan Manager for Servers

# Dependancies
ipmitool
python3

# Install
move fan-manager.service to /etc/systemd/system

systemctl daemon-reload
systemctl enable /etc/systemd/system/fan-manager.service
systemctl start fan-manager.service

# Tested on 
Dell R720, R720XD, R730XD

