# Modifying blind in FAST_LIO
## Lidar blind radius (blind_chg & blind_filter)
---
### blind_chg
For blind_chg folder, it changes the code in FAST_LIO_QUGV file.

**Note: Have to overwrite the src file in FAST_LIO_QUGV**
#### 
Shift the following files:
- laserMapping.cpp
- preprocess.cpp
- preprocess.h
####
into FAST_LIO file in the src of FAST_LIO_UGV

### Have the launch file be added into ouster_ros file

rebuild the workspace

```
 catkin build
 ```

### incase of an error
clean up the catkin ws, then rebuild the catkin ws

```
catkin clean
catkin build
```

---
### blind_filter
For blind_filter package, it does a filtering in the package through BlindingCuboid.py which take in a lidar_topic (pointcloud2) called "/os_cloud_node/points" and passing out a filter_topic (pointcloud2) called "/os_cloud_node/points_filtered"

**For Development purposes, click [here](blind_filter/README.md) for more instructions**

### Running Procedure
1. Install this package onto your workspace
2. Build the package
    ```
    source /opt/ros/noetic/setup.bash
    catkin build 
    ```
3. Source the devel file from the workspace ```source devel/setup.bash```
4. Run the code by,
    ```
    rosrun blind_filter BlindingCuboid.py
    ```
### The error below will appear upon sending into FAST_LIO. However, everything will be working properly.
![](docs/laser_mapping_error_log.png)
---