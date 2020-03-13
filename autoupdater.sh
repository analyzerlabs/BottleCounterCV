#!/bin/bash
cd /home/pi/BottleCounterCV
sudo git reset --hard
sudo git pull
sudo python3 /home/pi/BottleCounterCV/main.py
