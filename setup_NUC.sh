#!/bin/bash

# SET UP ROS_IP
console_ip=$(ifconfig | grep -A 1 'wl' | grep -oP 'inet \K[\d.]+')
export ROS_IP="$console_ip"
echo "ROS_IP set to: $ROS_IP"

##################################################
##### Check if the ptp4l.service is inactive #####
##################################################

max_attempts=3
attempt=0

while ! systemctl is-active --quiet ptp4l.service && ((attempt < max_attempts)); do
  attempt=$((attempt + 1))
  echo "Attempt $attempt to start ptp4l.service"
  systemctl try-reload-or-restart ptp4l.service
  systemctl start ptp4l.service
  sleep 10
done

if systemctl is-active --quiet ptp4l.service; then
  echo "ptp4l.service is active"
else
  echo "Failed to start ptp4l.service after $max_attempts attempts"
fi
