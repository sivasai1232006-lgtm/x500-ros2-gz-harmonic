#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

import sys
import select
import termios
import tty


class KeyboardNode(Node):

    def __init__(self):
        super().__init__('keyboard_node')

        self.publisher = self.create_publisher(
            Twist,
            '/model/x500/cmd_vel',
            10
        )

        # Speeds
        self.horizontal_speed = 1.0
        self.vertical_speed = 0.5
        self.yaw_speed = 0.5

        # Current commanded velocity
        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0
        self.yaw_rate = 0.0

        # Publish at 20 Hz
        self.timer = self.create_timer(
            0.05,
            self.publish_command
        )

        # Save terminal settings
        self.settings = termios.tcgetattr(sys.stdin)

        # Put terminal into raw mode
        tty.setcbreak(sys.stdin.fileno())

        self.get_logger().info('X500 Keyboard Controller started')
        self.get_logger().info('W/S = X direction')
        self.get_logger().info('A/D = Y direction')
        self.get_logger().info('R/F = Up/Down')
        self.get_logger().info('Q/E = Yaw left/right')
        self.get_logger().info('SPACE = Stop')
        self.get_logger().info('CTRL+C = Quit')

    def read_keyboard(self):

        key = None

        # Check whether a key is waiting
        if select.select([sys.stdin], [], [], 0)[0]:
            key = sys.stdin.read(1)

        return key

    def process_key(self, key):

        if key is None:
            return

        # Forward
        if key == 'w':
            self.vx = self.horizontal_speed
            self.vy = 0.0
            self.vz = 0.0
            self.yaw_rate = 0.0

        # Backward
        elif key == 's':
            self.vx = -self.horizontal_speed
            self.vy = 0.0
            self.vz = 0.0
            self.yaw_rate = 0.0

        # Left
        elif key == 'a':
            self.vx = 0.0
            self.vy = self.horizontal_speed
            self.vz = 0.0
            self.yaw_rate = 0.0

        # Right
        elif key == 'd':
            self.vx = 0.0
            self.vy = -self.horizontal_speed
            self.vz = 0.0
            self.yaw_rate = 0.0

        # Up
        elif key == 'r':
            self.vx = 0.0
            self.vy = 0.0
            self.vz = self.vertical_speed
            self.yaw_rate = 0.0

        # Down
        elif key == 'f':
            self.vx = 0.0
            self.vy = 0.0
            self.vz = -self.vertical_speed
            self.yaw_rate = 0.0

        # Yaw left
        elif key == 'q':
            self.vx = 0.0
            self.vy = 0.0
            self.vz = 0.0
            self.yaw_rate = self.yaw_speed

        # Yaw right
        elif key == 'e':
            self.vx = 0.0
            self.vy = 0.0
            self.vz = 0.0
            self.yaw_rate = -self.yaw_speed

        # Stop
        elif key == ' ':
            self.vx = 0.0
            self.vy = 0.0
            self.vz = 0.0
            self.yaw_rate = 0.0

            self.get_logger().info('STOP')

    def publish_command(self):

        key = self.read_keyboard()

        self.process_key(key)

        msg = Twist()

        msg.linear.x = self.vx
        msg.linear.y = self.vy
        msg.linear.z = self.vz

        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = self.yaw_rate

        self.publisher.publish(msg)

    def destroy_node(self):

        # Restore terminal settings
        termios.tcsetattr(
            sys.stdin,
            termios.TCSADRAIN,
            self.settings
        )

        super().destroy_node()


def main(args=None):

    rclpy.init(args=args)

    node = KeyboardNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()