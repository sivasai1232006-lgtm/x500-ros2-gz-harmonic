import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node


def generate_launch_description():

    package_share = get_package_share_directory('x500_control')

    world_file = os.path.join(
        package_share,
        'worlds',
        'x500_world.sdf'
    )

    gazebo = ExecuteProcess(
        cmd=[
            'gz',
            'sim',
            '-r',
            world_file
        ],
        output='screen'
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/x500/imu@sensor_msgs/msg/Imu[gz.msgs.IMU',
            '/x500/lidar@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/x500/gps@sensor_msgs/msg/NavSatFix[gz.msgs.NavSat',
            '/model/x500/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
        ],
        output='screen'
    )


    return LaunchDescription([
        gazebo,
        bridge,
    ])