#!/bin/bash
nohup python3 api.py &
echo $! > /var/run/mt4-server.pid
service apache2 restart
