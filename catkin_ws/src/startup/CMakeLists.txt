cmake_minimum_required(VERSION 3.0.2)
project(startup)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES startup
  CATKIN_DEPENDS roscpp rospy std_msgs
#  DEPENDS system_lib

)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

add_executable(twist_unstamp src/twist_unstamp.cpp)
target_link_libraries(twist_unstamp ${catkin_LIBRARIES})
