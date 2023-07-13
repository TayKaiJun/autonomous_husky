#!/bin/bash

# SET UP ROS_IP
console_ip=$(ifconfig | grep -A 1 'wl' | tail -1 | cut -d ':' -f 2 | grep -oP 'inet \K[\d.]+')
export ROS_IP="$console_ip"
echo "ROS_IP set to: $ROS_IP"

# SET UP ROS_MASTER_URI
input_IP=$1
export ROS_MASTER_URI="http://$input_IP:11311"
echo "ROS_MASTER_URI set to: $ROS_MASTER_URI"

##################################################