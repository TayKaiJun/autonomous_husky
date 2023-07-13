#!/bin/python3

import os
import yaml
from rich.console import Console
from rich.table import Table, Column
from rich.text import Text
import time
import requests

table = Table(
    Column('Check'),
    Column('Result'),
    box=None)

##########

def lidarConnectivityCheck():
    global LIDAR_CONNECTED, LIDAR_HOSTNAME
    # Read config file for the lidar's address and ping it
    with open('./catkin_ws/src/startup/config/config.yaml','r') as config_file:
        params_dict = yaml.safe_load(config_file)
    LIDAR_HOSTNAME = params_dict['os_node']['sensor_hostname']
    response = os.system("ping -c 1 -w 1 " + LIDAR_HOSTNAME + " > /dev/null")
    if response == 0:
        table.add_row(Text('LIDAR CONN', style='white on green'), 'Connected to lidar ({}).'.format(LIDAR_HOSTNAME))
        LIDAR_CONNECTED = True
    else:
        table.add_row(Text('LIDAR CONN', style='white on red'), 'Not connected to lidar ({}).'.format(LIDAR_HOSTNAME))
        LIDAR_CONNECTED = False
     

def nucPtpCheck():
    global PTP_ON

    response = os.system("systemctl is-active --quiet ptp4l.service")
    if response == 0:
        table.add_row(Text('NUC PTP', style='white on green'), 'NUC PTP service is active.')
        PTP_ON = True
    else:
        table.add_row(Text('NUC PTP', style='white on red'), 'NUC PTP service is inactive.')
        PTP_ON = False

def lidarTimeCheck():
    global LIDAR_CONNECTED, LIDAR_TIME_OK
    if not LIDAR_CONNECTED:
        table.add_row(Text('LIDAR TIMESYNC', style='white on red'), 'Lidar not connected.')
        LIDAR_TIME_OK = False
        return
    
    nuc_time = time.time()
    response = requests.get('http://{}/api/v1/system/time'.format(LIDAR_HOSTNAME))
    data = response.json()
    lidar_time_mode = data['sensor']['timestamp']['mode']
    lidar_time = data['sensor']['timestamp']['time']
    time_diff = abs(lidar_time - nuc_time)
    
    if lidar_time_mode != 'TIME_FROM_PTP_1588':
        table.add_row(Text('LIDAR TIME', style='white on red'), 'Lidar not using PTP timesync. Time diff: {}'.format(time_diff))
        LIDAR_TIME_OK = False
    else:
        if time_diff > 0.5: # 500ms difference is acceptable
            table.add_row(Text('LIDAR TIME', style='white on red'), 'Lidar time not yet synced. Time diff: {}'.format(time_diff))
        else:
            table.add_row(Text('LIDAR TIME', style='white on green'), 'Lidar time synced. Time diff: {}'.format(time_diff))

##########
	
if __name__ == '__main__':
    lidarConnectivityCheck()
    nucPtpCheck()
    lidarTimeCheck()
    console = Console()
    console.print(table)
