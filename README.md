
# FRA502_LV1_Passakorn
FRA502 ROS project LV1 by passakorn Rattanagulvaranon 60340500031

# Dependencies
* Ubuntu 20.04
* ROS Noetic
* gazebo_ros version 11.5
* rvis 1.14.7(noetic)

Launch robot in Rvis

`roslaunch robot_description display.launch`

launch gazebo (with created world)

`roslaunch robot_gazebo robot_sim_gazebo.launch`

Use teleop node *note: run roslaunch or rosmaster before

`rosrun robot_description teleop_twist.py`

# ROS topic
/cmd_vel  geometry_msgs/Twist

/dew_ros_robot/camera1/image_raw    sensor_msgs/Image
/dew_ros_robot/laser/scan     sensor_msgs/LaserScan

action | ros topic | type
------------ | ------------- |---------------
velocity command | /cmd_vel  | geometry_msgs/Twist
camera sensor| /dew_ros_robot/camera1/image_raw | sensor_msgs/Image
laserscan sensor| /dew_ros_robot/laser/scan| sensor_msgs/LaserScan

# ROS rpq-graph

![rosgraph](https://user-images.githubusercontent.com/56964016/120067040-af689100-c0a3-11eb-8a1c-4fc25fb9b822.png)





