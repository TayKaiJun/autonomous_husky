#include <ros/ros.h>
#include <string>
#include <geometry_msgs/Twist.h>
#include <geometry_msgs/TwistStamped.h>

std::string input_topic{}; // TwistStamped
std::string output_topic{}; // Twist

ros::Publisher* cmdVelModifiedPubPtr{ nullptr };

void modifierCallback(const geometry_msgs::TwistStampedConstPtr& msg){
    // removes header information including time stamp
    auto pub_msg{ msg->twist };

    cmdVelModifiedPubPtr->publish(pub_msg);
}

int main(int argc, char** argv){
    ros::init(argc, argv, "twist_unstamp_node");
    ros::NodeHandle nh;
    ros::NodeHandle nhPrivate = ros::NodeHandle("~");

    nhPrivate.param<std::string>("input_topic", input_topic, "/cmd_vel_throttled");
    nhPrivate.param<std::string>("output_topic", output_topic, "/mcu/command/manual_twist");

    ros::Subscriber cmdVelSub = nh.subscribe(input_topic, 5, modifierCallback);

    ros::Publisher cmdVelModifiedPub = nh.advertise<geometry_msgs::Twist>(output_topic, 5);
    cmdVelModifiedPubPtr = &cmdVelModifiedPub;
    ros::spin();

    return 0;
}