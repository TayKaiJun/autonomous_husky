# CHANGE LOG

### 03/07/23

- edited FAST_LIO/config/ouster64.yaml:
    - lid_topic:  `"/ouster/points"` instead of `"/os_cloud_node/points"`
    - imu_topic:  `"/ouster/imu"` instead of `"/os_cloud_node/imu"`
    - because rostopic info showed that `/os_cloud_node/points` had no publisher (i.e. no data was being pushed to the topic)
- edited mapping_ouster64.launch:
    - `<remap from="/Odometry" to="/fast_lio/Odometry"/>` <br>
    so that this odometry data can be added to localization.yaml in husky_control/config to be fused together
        -   control.launch calls robot_localization pkg and its ekf_localization node to fuse sensor data
    - **check if this is actually needed**
- tried to add odometry info to localization.yaml but didn't work
    - might need to do some frame transformation to make this work
    - figure out how to test this since current implementation is only tested in Gazebo simulation while using physical LiDAR

### 04/07/23

#### Husky packages
Comparing husky_nav/husky_base.launch (on the NUC) & husky_base/base.launch (mine)
- port needs to be set to `/dev/ttyUSB0`
- control_frequency is different 20 for NUC and 10 for original code, but no change was made

Comparing husky_nav/control.launch (on the NUC) & husky_control/control.launch (mine)
- commented out `multimaster` related lines, `laser_enabled` lines, `realsense_enabled` lines, `urdf_extras` lines, and other simulation related lines.

Comparing husky_nav/teleop.launch (on the NUC) & husky_control/teleop.launch (mine)
- commented out `<group>`lines that switches teleop controller types
- only kept `<rosparam command="load" file="$(find husky_control)/config/teleop_logitech.yaml" />`

Comparing husky_nav/config/husky_control/teleop_logitech.yaml (on the NUC) & husky_control/config/teleop_logitech.yaml (mine)
- joy_nonde needs to be set to `dev: /dev/input/js0`

#### AEDE package

- the correct topic name should be updated in the loam_interface.launch, otherwise do the following:
    - remapped `/odometry/filtered` to `/state_estimation` in `FAST_LIO/launch/mapping_ouster64.launch`
    - remapped `/cloud_registered` to `/registered_scan` in `husky_control/launch/control.launch`
- TO-DO: Adjust 'minRelZ' and 'maxRelZ' in 'aede/src/local_planner/launch/local_planner.launch'. (The default sensor height is set at 0.75m above the ground in the vehicle simulator and the registered scans are cropped at the height of -0.5m and 0.25m w.r.t. the sensor.)
- commented out loading of ps3.launch in the system_real_robot.launch file


### MAJOR CHANGE
- **(referenced from `sv_nuc/launch/sv.launch`)** added a new startup folder with a husky_autonomous.launch and twist_unstamp.cpp
    - startup.launch used to call all the launch files required
        - note `<node pkg="tf" type="static_transform_publisher" name="cameraInitPublisher" args="0 0 0 0 0 0 map camera_init 100" />` to `FAST_LIO/launch/mapping_ouster64.launch` to transform fast_lio's camera_init frame to the map to be used by the husky's localization.yaml
    - twist_unstamp.cpp is to remove the header from the `geometry_msgs::TwistStamped` to `geometry_msgs::Twist`
- **(TO BE VERIFIED)** added `map_frame: map` to `husky_control/config/localization.yaml`
- in `aede/src/local_planner/src/pathFollower.cpp`, cmd_vel is published as aede/cmd_vel instead so that husky does not attempt to use the output TwistStamped cmd_vel from AEDE and have mismatch in message type

### 05/07/23

- changed `ouster64.yaml` blind parameter to 1.2 so that husky will so that the Husky will not be treated as an obstacle (TODO: Tune this value)
- made `startup` package to run everything from one launch file
    - `twist_unstamp` node made to extract the Twist typed message from the output of AEDE in order to control the Husky
- stop rviz launch from ouster-ros and fastlio: see `husky_autonomous.launch`
    - for ouster, `<arg name="viz" value="false" />`
    - for fast-lio, `<arg name="rviz" value="false" />`
- fixed inconsistent naming of twist_unstamp node


**ADDED TARE PLANNER**
- added `husky.yaml`
    - copy of the `garage.yaml` file but `kAutoStart` set to false instead
        - TO-DO: Must find out where to set this autostart value to be true later
- added `explore_husky.launch` 
    - set `scenario` arg to be `husky` so that the tare_planner_node will be loaded with the `husky.yaml` correctly


### 10/07/23
- tested setup in open space
    - discovered that error is due to odometry in the visualizer is drifting from the actual robot position
    - might have problem with time synchronization, solution is to use ptp (adapted from SV_NUC):
        ```
        sudo apt install linuxptp
        sudo nano /lib/systemd/system/ptp4l.service # change 'eth0' to whatever ethernet port the lidar will be connected to
        sudo systemctl start ptp4l.service 

        # if the above line did not work, try
        sudo systemctl try-restart-or-reload ptp4l.service

        # to check if ptp is working
        systemctl is-active ptp4l.service
        ```
        - for checking if a port is suitable for changing the config file for (ref: https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/system_administrators_guide/ch-configuring_ptp_using_ptp4l)
            ```
            sudo apt-get install ethtool
            ethtool -T <PORT NAME>
            ```
### 12/07/23
- odometry drift was due to wrong odometry input -> odometry input for AEDE should be the lidar's odometry data as generated by the fast-package
    - i.e. should be `<param name="stateEstimationTopic" type="string" value="/Odometry" />`in loam_interface.launch
- ptp4l should be active to synchronize the timing between the lidar and the NUC
- AEDE and TARE will be ran on the NUC while their visualization will be done on the remote PC.

### 13/07/23
- added bash_aliases.txt to note down aliases to be added to ~/.bashrc for shortcuts to commands
- added scripts to load NUC and computer quickly
    - `setup_NUC.sh` will find its own IP, set ROS_IP, start ptp4l.service
    - `setup_this.sh` will take in 1 argument, the IP address of the NUC, and use it to set ROS_MASTER_URI. it also finds its own IP and set ROS_IP
- added `preflight.py` to check for LiDAR connection, PTP4L status, and time synchronization between NUC and LiDAR.

- increased max_velocity of husky in control.yaml to 1.5

### 14/07/23

- changed blind radius to 0.8 -> blind radius of lidar is 0.8m due to hardware limitation. even with the lidar moved to the center of the robot, blind radius of lidar will already cover the husky
- in fast-lio's preprocess.h, changed  `uint8_t` to `uint16_t` for ouster's point ring field to fix `Failed to match field 'ring'` message when running fastlio package

### 24/07/23

Testing set up:
- AEDE Local_planner:
    - <arg name="maxSpeed" value="1.0" />
    - <arg name="autonomySpeed" value="1.0" />
    - <arg name="vehicleLength" value="1.0" />
    - <arg name="vehicleWidth" value="0.70" />

- TARE CONFIG: (Basing off sv_nuc_full_params)
    - kLookAheadDistance : 8
    - kKeyposeCloudDwzFilterLeafSize : 0.2
    - kRushHomeDist : 5
    - kFrontierClusterTolerance : 1.0
    - kFrontierClusterMinSize : 10
    - kUseCoverageBoundaryOnFrontier : false
    - kSurfaceCloudDwzLeafSize : 0.3
    - kCollisionCloudDwzLeafSize : 0.2
    - the following keypose_graph values were attempted but causes TARE to crash
        - keypose_graph/kAddNodeMinDist : 1.0
        - keypose_graph/kAddNonKeyposeNodeMinDist : 0.5
        - keypose_graph/kAddEdgeConnectDistThr : 3.0
        - keypose_graph/kAddEdgeToLastKeyposeDistThr : 3.0
        - keypose_graph/kAddEdgeVerticalThreshold : 1.0
        - keypose_graph/kAddEdgeCollisionCheckResolution : 0.4
        - keypose_graph/kAddEdgeCollisionCheckRadius : 0.4

