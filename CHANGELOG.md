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
