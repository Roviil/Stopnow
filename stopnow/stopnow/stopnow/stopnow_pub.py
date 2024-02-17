import datetime
import cv2
from sensor_msgs.msg import Image
from ultralytics import YOLO
from cv_bridge import CvBridge
from std_msgs.msg import String  # Add String import for custom message
import rclpy
from rclpy.node import Node

CONFIDENCE_THRESHOLD = 0.3
GREEN = (0, 0, 255)
WHITE = (255, 255, 255)

class YOLODetection:
    def __init__(self, label, count):
        self.label = label
        self.count = count

class YOLONode(Node):
    def __init__(self):
        super().__init__('yolo_node')
        self.bridge = CvBridge()
        self.image_publisher = self.create_publisher(Image, 'yolo_image', 10)
        self.detection_publisher = self.create_publisher(String, 'yolo_output', 10)
        self.timer = self.create_timer(0.1, self.process_frame)
        self.model = YOLO('yolov8n.pt')
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.class_list = self.load_class_list()

    def load_class_list(self):
        coco128 = open('/home/jetson/ros2_ws/coco128.txt', 'r')
        data = coco128.read()
        class_list = data.split('\n')
        coco128.close()
        return class_list

    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().error('Cam Error')
            return

        detection = self.model(frame)[0]

        # Count the number of detected objects
        detection_counts = {}
        for data in detection.boxes.data.tolist():
            confidence = float(data[4])
            if confidence < CONFIDENCE_THRESHOLD:
                continue

            label = int(data[5])
            class_name = self.class_list[label]
            if class_name not in detection_counts:
                detection_counts[class_name] = 0
            detection_counts[class_name] += 1

            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), GREEN, 2)
            cv2.putText(frame, f'{class_name} {round(confidence, 2)}%', (xmin, ymin),
                        cv2.FONT_ITALIC, 1, WHITE, 2)

        image_msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        self.image_publisher.publish(image_msg)

        # Publish detection counts as a custom message
        detection_msg = String()
        for class_name, count in detection_counts.items():
            detection_msg.data += f'{count} {class_name}, '

        self.detection_publisher.publish(detection_msg)
        # Show the image using cv2.imshow
        #cv2.imshow('YOLO Output', frame)
        #cv2.waitKey(1)

def main():
    rclpy.init()
    yolo_node = YOLONode()
    rclpy.spin(yolo_node)
    yolo_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

