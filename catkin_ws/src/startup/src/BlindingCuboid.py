#! /bin/python3

import rospy
from sensor_msgs.msg import PointCloud2, PointField
import sensor_msgs.point_cloud2 as pc2
import numpy as np

# Getting param from ros
x_blind_max = rospy.get_param("/pc6/blind_fil/blind_x_max",0.8)
y_blind_max = rospy.get_param("/pc6/blind_fil/blind_y_max",0.8)
z_blind_max = rospy.get_param("/pc6/blind_fil/blind_z_max",0.8)
x_blind_min = rospy.get_param("/pc6/blind_fil/blind_x_min",-0.8)
y_blind_min = rospy.get_param("/pc6/blind_fil/blind_y_min",-0.8)
z_blind_min = rospy.get_param("/pc6/blind_fil/blind_z_min",-0.8)
lidar_topic = rospy.get_param("/pc6/blind/lidar_topic", '/ouster/points')
filter_topic = rospy.get_param("pc6/blind/filter_topic", '/os_cloud_node/points_filtered')

fields = [
        PointField(name="x", offset=0, datatype=PointField.FLOAT32, count=1),
        PointField(name="y", offset=4, datatype=PointField.FLOAT32, count=1),
        PointField(name="z", offset=8, datatype=PointField.FLOAT32, count=1),
        PointField(name="intensity", offset=12, datatype=PointField.FLOAT32, count=1),
        PointField(name="t", offset=16, datatype=PointField.UINT32, count=1),
        PointField(name="reflectivity", offset=20, datatype=PointField.UINT16, count=1),
        PointField(name="ring", offset=22, datatype=PointField.UINT8, count=1),
        PointField(name="ambient", offset=23, datatype=PointField.UINT16, count=1),
        PointField(name="range", offset=25, datatype=PointField.UINT32, count=1)
    ]

def process_lidar_data(point_cloud):

    
    point_cloud_arr = np.array(list(pc2.read_points(point_cloud, field_names=("x", "y", "z", "intensity","t","reflectivity","ring","ambient","range"), skip_nans=False)))
    filtered_pts = filter_points(point_cloud_arr)
    

    publish_filtered_points(filtered_pts,point_cloud.header)


def filter_points(point_cloud_arr):
    filter_point = []
    for point in point_cloud_arr:
        x, y, z, intensity, t, reflectivity, ring, ambient, rng = point

        # Making a shape for the blind
        if x_blind_min < x < x_blind_max and y_blind_min < y < y_blind_max and z_blind_min < z < z_blind_max:
            continue
        else:
            filter_point.append([x,y,z, intensity, int(t), int(reflectivity), int(ring), int(ambient), int(rng)])

    return filter_point

def publish_filtered_points(filtered_pts, header):
    cloud_msg = pc2.create_cloud(header, fields, filtered_pts)

    filtered.publish(cloud_msg)

# Running

if __name__ == '__main__':
    # Initialise the ROS node
    rospy.init_node('blind_filter')
    

    # Set up the LiDAR subscriber
    # lidar_topic = '/os_cloud_node/points'
    rospy.Subscriber(lidar_topic, PointCloud2, process_lidar_data)

    # Set up the filtered points publisher
    # filter_topic = '/os_cloud_node/points_filtered'
    filtered = rospy.Publisher(filter_topic, PointCloud2, queue_size=100)

    # Spin ROS node
    rospy.spin()