import datetime
import cv2
from sensor_msgs.msg import Image
from ultralytics import YOLO
from cv_bridge import CvBridge
from std_msgs.msg import String  # Add String import for custom message
import rclpy
from rclpy.node import Node

class YOLOSubscriberNode(Node):
    def __init__(self):
        super().__init__('yolo_subscriber_node')
        self.subscription = self.create_subscription(
            String,
            '/yolo_output',
            self.yolo_output_callback,
            10)
        self.subscription

    def yolo_output_callback(self, msg):
        if 'on' in msg.data:
            self.get_logger().info(f'Detected "on" in YOLO output: {msg.data}')
        else:
            self.get_logger().info('No "on" detected in YOLO output')

def main():
    rclpy.init()
    yolo_subscriber_node = YOLOSubscriberNode()
    rclpy.spin(yolo_subscriber_node)
    yolo_subscriber_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

