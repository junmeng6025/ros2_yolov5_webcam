#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

QUEUE_SZ = 10
FPS = 30
RATE = 1.0/FPS


class ImagePublisher(Node):
    def __init__(self, name):
        super().__init__(name)
        self.publisher_ = self.create_publisher(Image, 'image_raw', QUEUE_SZ)
        self.timer = self.create_timer(RATE, self.timer_callback)
        self.cap = cv2.VideoCapture(0)  # for SONY camera device: 2
        self.cv_bridge = CvBridge()
        self.counter = 0

    def timer_callback(self):
        if not self.cap.isOpened():
            self.get_logger().error("Cannot open camera")

        ret, frame = self.cap.read()
        if ret:
            self.publisher_.publish(
                self.cv_bridge.cv2_to_imgmsg(frame, 'bgr8'))  # encodeing mode is also bgr8
        else:
            self.get_logger().error("Can't receive frame (stream end?). Exiting ...")

        self.get_logger().info("Publishing video frame [#%04d]" % self.counter)
        self.counter += 1


def main(args=None):
    rclpy.init(args=args)
    node = ImagePublisher("webcam_yolo_pub")

    try:
        while rclpy.ok():
            rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()
