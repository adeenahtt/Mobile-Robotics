#echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrccd ~/ros2_ws/src

#q2-e
# terminal 1- start turtlesim
ros2 run turtlesim turtlesim_node

# terminal 2 — rotate to 45 degrees (0.7854 radians)
ros2 action send_goal /turtle1/rotate_absolute turtlesim/action/RotateAbsolute "{theta: 0.7854}"

# move w 2 m/s
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0}, angular: {z: 0.0}}"

# stop publisher with Ctrl+C

# print current turtle position
ros2 topic echo /turtle1/pose


#-------------------------------------------------------------------------
#q2-f
