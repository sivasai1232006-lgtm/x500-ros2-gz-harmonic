# X500 ROS 2 + Gazebo Simulation

ROS 2 Humble + Gazebo Harmonic simulation of an X500 UAV with keyboard-based velocity control and simulated IMU, LiDAR, and GPS sensors.

## Features

- X500 UAV simulation in Gazebo Harmonic
- Keyboard-based UAV velocity control
- Simulated IMU
- Simulated LiDAR
- Simulated GPS / NavSat
- ROS 2 ↔ Gazebo communication using `ros_gz_bridge`
- Launch files for simplified simulation
- Raw sensor readings available through ROS 2 topics

## Requirements

- Ubuntu
- ROS 2 Humble
- Gazebo Harmonic
- `ros_gz_bridge`
- Python 3

## Repository Structure

    x500_control/
    ├── x500_control/
    │   ├── __init__.py
    │   ├── keyboard_node.py
    │   └── x500_twist_pub.py
    │
    ├── launch/
    │   ├── bridge.launch.py
    │   └── simulation.launch.py
    │
    ├── worlds/
    │   └── x500_world.sdf
    │
    ├── resource/
    │   └── x500_control
    │
    ├── package.xml
    ├── setup.py
    ├── setup.cfg
    ├── README.md
    └── .gitignore

## Installation

Create or use an existing ROS 2 workspace:

    mkdir -p ~/your_ws/src
    cd ~/your_ws/src

Clone the repository:

    git clone https://github.com/YOUR_USERNAME/x500-ros2-gazebo.git

Build the package:

    cd ~/your_ws
    colcon build --packages-select x500_control

Source the workspace:

    source ~/your_ws/install/setup.bash

## Running the Simulation

The main simulation launch file starts Gazebo and all required ROS-Gazebo bridges.

Run:

    ros2 launch x500_control simulation.launch.py

This starts:

- Gazebo Harmonic
- IMU bridge
- LiDAR bridge
- GPS bridge
- X500 `cmd_vel` bridge

## Keyboard Control

The keyboard node requires direct access to the terminal, so it is run separately.

Open a second terminal and source the workspace:

    source ~/your_ws/install/setup.bash

Run:

    ros2 run x500_control keyboard

The keyboard node publishes velocity commands to:

    /model/x500/cmd_vel

using:

    geometry_msgs/msg/Twist

The command is forwarded to Gazebo through `ros_gz_bridge`.

Normal workflow:

Terminal 1:

    source ~/your_ws/install/setup.bash
    ros2 launch x500_control simulation.launch.py

Terminal 2:

    source ~/your_ws/install/setup.bash
    ros2 run x500_control keyboard

## Sensors

### IMU

ROS 2 topic:

    /x500/imu

Message type:

    sensor_msgs/msg/Imu

View IMU readings:

    ros2 topic echo /x500/imu

The IMU provides:

- Orientation
- Angular velocity
- Linear acceleration

Check the publishing rate:

    ros2 topic hz /x500/imu

### LiDAR

ROS 2 topic:

    /x500/lidar

Message type:

    sensor_msgs/msg/LaserScan

View LiDAR readings:

    ros2 topic echo /x500/lidar

Current configuration:

- 360 horizontal samples
- 360° horizontal field of view
- 0.1 m minimum range
- 30 m maximum range
- 10 Hz update rate

Gazebo also publishes:

    /x500/lidar/points

for the point-cloud representation.

### GPS

ROS 2 topic:

    /x500/gps

Message type:

    sensor_msgs/msg/NavSatFix

View GPS readings:

    ros2 topic echo /x500/gps

The GPS uses the geographic origin specified in the Gazebo world through spherical coordinates.

## ROS-Gazebo Bridges

The project uses `ros_gz_bridge` to communicate between Gazebo and ROS 2.

Sensor data flows from Gazebo to ROS 2:

    Gazebo IMU
        ↓
    /x500/imu
        ↓
    sensor_msgs/msg/Imu

    Gazebo LiDAR
        ↓
    /x500/lidar
        ↓
    sensor_msgs/msg/LaserScan

    Gazebo GPS
        ↓
    /x500/gps
        ↓
    sensor_msgs/msg/NavSatFix

Keyboard commands flow from ROS 2 to Gazebo:

    Keyboard Node
        ↓
    /model/x500/cmd_vel
        ↓
    geometry_msgs/msg/Twist
        ↓
    ros_gz_bridge
        ↓
    Gazebo
        ↓
    X500

All bridges are started automatically by:

    ros2 launch x500_control simulation.launch.py

## Useful Commands

List ROS 2 topics:

    ros2 topic list

Check topic information:

    ros2 topic info /x500/imu

Check IMU publishing rate:

    ros2 topic hz /x500/imu

Check LiDAR publishing rate:

    ros2 topic hz /x500/lidar

Check GPS publishing rate:

    ros2 topic hz /x500/gps

View IMU data:

    ros2 topic echo /x500/imu

View LiDAR data:

    ros2 topic echo /x500/lidar

View GPS data:

    ros2 topic echo /x500/gps

View keyboard velocity commands:

    ros2 topic echo /model/x500/cmd_vel

## Launch Files

### simulation.launch.py

Starts:

- Gazebo Harmonic
- IMU bridge
- LiDAR bridge
- GPS bridge
- X500 `cmd_vel` bridge

Run:

    ros2 launch x500_control simulation.launch.py

### bridge.launch.py

Starts only the ROS-Gazebo bridges.

Run:

    ros2 launch x500_control bridge.launch.py

This is useful when Gazebo is started manually.

## Current Scope

The current project focuses on:

1. X500 UAV simulation in Gazebo Harmonic
2. Keyboard-based UAV control
3. IMU integration
4. LiDAR integration
5. GPS integration
6. ROS 2 ↔ Gazebo communication
7. Reading raw sensor data through ROS 2

The sensor data is currently only being generated and read. No sensor fusion or autonomous behavior is implemented yet.

The project currently does not include:

- Sensor fusion
- EKF
- SLAM
- Autonomous localization
- Obstacle avoidance
- Autonomous navigation
- Multi-UAV coordination

## Future Work

Possible future extensions include:

- Multiple X500 UAVs
- UAV-to-UAV communication
- Sensor fusion
- Localization
- Obstacle detection
- Autonomous waypoint navigation
- Multi-UAV coordination
- Safety monitoring
- Coordinated UAV inspection

## Author

Siva
