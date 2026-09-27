#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class x500CmdNode(Node): # MODIFY node name

    def __init__(self):
        super().__init__('x500_cmd_node') # MODIFY node name
        self.msg_publisher_ = self.create_publisher(Twist, '/model/x500/cmd_vel', 10)
        self.timer_ = self.create_timer(0.1, self.publish_command)

    def publish_command(self):
        msg = Twist()

        msg.linear.x = -1.00
        msg.linear.y = 0.00
        msg.linear.z = 0.00

        msg.angular.x = 0.00
        msg.angular.y = 0.00
        msg.angular.z = 0.00

        self.msg_publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    #My node
    node = x500CmdNode() # MODIFY node name
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()