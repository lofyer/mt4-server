#!/bin/bash
nohup python3 api.py &
service apache2 restart
