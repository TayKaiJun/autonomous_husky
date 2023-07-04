# INSTALLATION GUIDE

This document is for recording the actions done to integrate all the required systems (Husky, Outster LiDAR, FAST-LIO 2.0, AEDE, and TARE Planner) together on **ROS Noetic**.
> 📘 All packages should be added to the `catkin_ws/src` directory

## Husky

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

## Ouster Integration

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


## Fast-LIO Integration

### Installations:

1.  `sudo apt install libpcl-dev` (this is for Point Cloud Library)
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