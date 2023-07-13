#!/bin/bash

source devel/setup.bash

# SET UP ROS_IP
console_ip=$(hostname -I | awk '{print $1}')
export ROS_IP="$console_ip"
# echo "ROS_IP set to: $ROS_IP"

# Check if the ptp4l.service is inactive
if ! systemctl is-active --quiet ptp4l.service; then
  echo "ptp4l.service is inactive"
  systemctl try-reload-or-restart ptp4l.service
  systemctl start ptp4l.service
else
  echo "ptp4l.service is active"
fi

