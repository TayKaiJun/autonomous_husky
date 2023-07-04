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