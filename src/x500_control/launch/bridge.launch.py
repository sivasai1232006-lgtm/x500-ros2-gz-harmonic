from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            # IMU: Gazebo -> ROS 2
            '/x500/imu@sensor_msgs/msg/Imu[gz.msgs.IMU',

            # LiDAR: Gazebo -> ROS 2
            '/x500/lidar@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',

            # GPS: Gazebo -> ROS 2
            '/x500/gps@sensor_msgs/msg/NavSatFix[gz.msgs.NavSat',

            # cmd_vel: ROS 2 -> Gazebo
            '/model/x500/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
        ],
        output='screen'
    )

    return LaunchDescription([
        bridge
    ])