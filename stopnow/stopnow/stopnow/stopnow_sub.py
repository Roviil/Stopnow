import rclpy
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile
from std_msgs.msg import String
from time import sleep
import datetime
import cv2
from sensor_msgs.msg import Image
from ultralytics import YOLO
from cv_bridge import CvBridge
from rclpy.node import Node

OMO_R1MINI_MAX_LIN_VEL = 0.50

LIN_VEL_STEP_SIZE = 0.01

class YOLOSubscriberNode(Node):
    
    def __init__(self):
        super().__init__('yolo_subscriber_node')
        self.subscription = self.create_subscription(
            String,
            '/yolo_output',
            self.yolo_output_callback,
            10)
        self.subscription
        self.publisher = self.create_publisher(Twist, 'cmd_vel', QoSProfile(depth=10))
        self.low_bound = -OMO_R1MINI_MAX_LIN_VEL
        self.high_bound = OMO_R1MINI_MAX_LIN_VEL
        
        
    def constrain(self, input_vel):
        if input_vel < self.low_bound:
            input_vel = self.low_bound
        elif input_vel > self.high_bound:
            input_vel = self.high_bound
        return input_vel
    
    def yolo_output_callback(self, msg):
        twist = Twist()
        try:
            self.get_logger().info(f'Received YOLO output: {msg.data}')
            target_linear_velocity = 0.1
            control_linear_velocity = self.constrain(target_linear_velocity)
            twist.linear.x = control_linear_velocity
            twist.linear.y = 0.0
            twist.linear.z = 0.0
            if 'on' in msg.data:
                self.get_logger().info('Detected "on" in YOLO output: Pausing for 5 seconds.')
                self.publisher.publish(twist)  # Stop the robot
                sleep(5)
                self.get_logger().info('Resuming movement after pause.')         
            else:
                self.publisher.publish(twist)  # Continue moving
                self.get_logger().info('Continuing movement.')
            twist = Twist()
        except Exception as e:
            self.get_logger().error(f'Error in yolo_output_callback: {e}')


def main():
    rclpy.init()
    print('START MOVING!')
    yolo_subscriber_node = YOLOSubscriberNode()
    rclpy.spin(yolo_subscriber_node)
    yolo_subscriber_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
