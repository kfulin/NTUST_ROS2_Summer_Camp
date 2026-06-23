import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math
import time

class MotionNode(Node):

    def __init__(self):
        super().__init__('motion_node')

        self.pub = self.create_publisher(JointState, '/joint_states', 10)
        self.timer = self.create_timer(0.05, self.timer_callback)

        self.start_time = time.time()

    def timer_callback(self):
        t = time.time() - self.start_time

        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()

        # URDF joint names
        msg.name = [
            'joint1',
            'joint2',
            'joint3',
            'joint4',
            'finger_left_joint',
            'finger_right_joint'
        ]

        # arm motion (smooth)
        j1 = math.sin(t) * 1.0
        j2 = math.sin(t * 0.7) * 0.8
        j3 = math.sin(t * 0.5) * 0.6
        j4 = math.sin(t * 0.3) * 0.5

        # gripper (OPEN/CLOSE)
        grip = 0.02 * (math.sin(t * 2.0) + 1.0)  # 0 ~ 0.04

        msg.position = [
            j1,
            j2,
            j3,
            j4,
            grip,
            grip
        ]

        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = MotionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()