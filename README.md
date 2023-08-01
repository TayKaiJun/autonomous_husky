# INSTALLATION GUIDE

This document is for recording the actions done to integrate all the required systems (Husky, Outster LiDAR, FAST-LIO 2.0, AEDE, and TARE Planner) together on **ROS Noetic**.
> 📘 All packages should be added to the `catkin_ws/src` directory


1.1 Husky
=========

1.1 Husky
=========

Source code: https://github.com/husky/husky/tree/noetic-devel

## Brief explanation of packages

- **husky_bringup**: installation and integration package
- **husky_base**: driver
- husky_gazebo: simulator bringup using Gazebo GUI
- husky-viz: vizualization configuration
- **husky_control**: controller configuration
- husky_description: URDF (Unified Robotics Description Format) description
- husky_msgs: messages (`HuskyStatus` exposes the status info)
- husky_navigation: autonomous mapping & navigation demos

*Bolded packages are the important ones used for operating the robot (TBV)*


1.2 Ouster
======================

1.2 Ouster
======================

### Installations:

```
git submodule add https://github.com/ouster-lidar/ouster-ros.git
source /opt/ros/noetic/setup.bash
cd ../.. # back to /catkin_ws
catkin_make --cmake-args -DCMAKE_BUILD_TYPE=Release
```

### Running:

- First run `source devel/setup.bash` (ensure that the it's the devel in the catkin_ws directory)
- LiDAR must be connected then run:
    ```
    roslaunch ouster_ros sensor.launch  \
    sensor_hostname:=os1-122011000244.local
    metadata:=<json file name>          #<path to rosbag file>  optional
    ```
- If bag file is being used instead
    ```
    roslaunch ouster_ros replay.launch
    bag_file:=<path to rosbag file>
    metadata:=<json file name>          # optional if bag file already contains metadata topic
    ```
- to see the topics being published, open another terminal, source the same bash file then run `rostopic list`


1.3 Fast-LIO2.0
===============
1.3 Fast-LIO2.0
===============

### Installations:

1.  `sudo apt install libpcl-dev` (this is for Point Cloud Library)
2.  `sudo apt install libeigen3-dev`
2.  `sudo apt install libeigen3-dev`
    - Alternatively, download tar.gz file from [Eigen source](https://eigen.tuxfamily.org/index.php?title=Main_Page) 
    - Untar using `tar -xzf <tarfile name>`
    - See instructions in `INSTALL.txt` in the untarred folder
3. Intall livox_ros driver *(TO-DO: See if this part can be removed from the source code)*
    - First install [Livox SDK](https://github.com/Livox-SDK/Livox-SDK) and follow installation instructions in `README.md`
        - This does not have to be in the main repo but needs to be done on the OS used
    - Next, add livox driver to our `catkin_ws/src` directory using `git submodule add https://github.com/Livox-SDK/livox_ros_driver.git ws_livox/src`
    - Run the following
        ```
        cd ws_livox
        catkin_make
        ```
4. Go back to `catkin_ws/src`
    - Add Fast-LIO package using `git submodule add git clone https://github.com/hku-mars/FAST_LIO.git`
    - do the following:
        ```
        cd FAST_LIO
        git submodule update --init
        ```
    - If running FAST-LIO separately only with LiDAR, continue with the following:
        ```
        cd ../..
        source ../ws_livox/devel/setup.sh
        catkin_make
        ```
    - Else, running `source devel/setup.bash` in our catkin workspace, followed by `catkin_make` will automatically build the required files accordingly too so the previous step will be unnecessary.

### Running

```
source devel/setup.bash
roslaunch fast_lio mapping_ouster64.launch
```


1.4 Autonomous Exploration Development Environment (AEDE)
=========================================================

Clone source code: 
```
git clone https://github.com/HongbiaoZ/autonomous_exploration_development_environment.git
git checkout distribution
catkin_make
```
Change topic names in loam_interface.launch to match the topic names published by the Husky's Odometry data and Fast-LIO's PointCloud data:
- remapped `/odometry/filtered` to `/state_estimation` in `FAST_LIO/launch/mapping_ouster64.launch`
- remapped `/cloud_registered` to `/registered_scan` in `husky_control/launch/control.launch`

### Running
When running on the Husky
```
source devel/setup.sh
roslaunch vehicle_simulator system_real_robot.launch
```

2 Integrated Launcher
=====================

- Run `catkin_create_pkg startup roscpp` to make a new startup package
- In the `/launch` folder, add `autonomous_husky_startup.launch`
    - This launch file will call all the other launch files required, namely: `husky_base` (which also calls husky_control and husky_teleop internally), ouster-ros's `sensor.launch`, fast-lio's `mapping_ouster64.launch`, AEDE's `system_real_robot.launch`
- In the `/src` folder, add `twist_unstamp.cpp`
    - This is to extract the Twist data and publish it to the /cmd_vel topic to be used for controlling the husky

3 Operating the Autonomous Husky
================================

### Semi-automated setup for deployment
1. One time setup (refer to `bash_aliases.txt`)
    - Add aliases to ~/.bashrc in PC:
    ```
    alias cd_pc='cd ~/Documents/autonomous_husky/catkin_ws'
    alias source_husky_pc='source ~/Documents/autonomous_husky/catkin_ws/devel/setup.bash'
    ```
    - Add aliases to ~/.bashrc in NUC:
    ```
    alias cd_nuc='cd ~/kaijuntay/autonomous_husky/catkin_ws'
    alias source_husky_nuc='source ~/kaijuntay/autonomous_husky/catkin_ws/devel/setup.bash'
    ```
    - `source ~/.bashrc` in either console to use the alias commands for easier life when testing

2. On the NUC:
    ```
    source setup_nuc.sh
    python3 preflight.py
    cd catkin_ws
    source devel/setup.bash   #or source_husky_nuc
    ```
    After running the above, preflight should show all tests passed and also display the IP address of the NUC to be used in the next step.

3. On the PC:
    ```
    source setup_this.sh <NUC_IP> # this sets up the ROS_IP and ROS_MASTER_URI
    cd catkin_ws
    source devel/setup.bash
    ```
4. To run everything:
    - In the **ssh** terminal:
        ```
        roslaunch startup autonomous_husky_startup.launch
        ```
        All the nodes needed should be launched
        
        > Note that either the e_stop should be activated or the bumper of the controller should be held on to otherwise robot will start moving automatically.
    - In the main PC:
        ```
        roslaunch startup visualize_aede.launch
        roslaunch startup visualize_tare.launch
        ```
> Note: Since `/cmd_vel` has a lower priority than the `joy_teleop/cmd_vel` input from the controller, simply pressing the left bumper on the controller when AEDE is manoeuvring the robot will override the AEDE's control