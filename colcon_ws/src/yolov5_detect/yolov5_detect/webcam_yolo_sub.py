#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from yolov5_detect.image_utils import *
from yolov5.detect_ros import Yolov5Detector
import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

import sys
sys.path.append(
    "/home/jun/ros2_guyue/colcon_ws/install/yolov5_detect/lib/python3.8/site-packages/yolov5_detect")


QUEUE_SZ = 10
RATE = 0.01

LOWER_RED = np.array([0, 90, 128])
UPPER_RED = np.array([180, 255, 255])

# yolodetector = detect_ros.Yolov5Detector()
# labels = []


class ImageSubscriber(Node):
    def __init__(self, name):
        super().__init__(name)
        self.subscriber_ = self.create_subscription(
            Image, 'image_raw', self.listener_callback, QUEUE_SZ)
        self.cv_bridge = CvBridge()
        self.counter = 0

        self.current_image_frame = None
        self.detector = Yolov5Detector()
        self.labels = []

    def yolo_detect(self, cvImage):
        self.current_image_frame = cvImage
        image_np = np.swapaxes(self.current_image_frame, 0, 2)  # [C,W,H]
        image_np = np.swapaxes(image_np, 1, 2)  # [C,H,W]
        image_tensor = torch.from_numpy(image_np).type(
            torch.float32)  # np.Array -> torch.Tensor
        image_tensor = paddingImage(image_tensor)
        image_np = image_tensor.numpy()  # torch.Tensor -> np.Array

        cvImgRet, detect, labels = self.detector.detectImage(
            image_np, self.current_image_frame, needProcess=True)  # cvImgRet is ready to plot
        self.labels = detect
        cv2.imshow("object", cvImgRet)
        # cv2.imshow("object", self.current_image_frame)
        cv2.waitKey(10)

    def listener_callback(self, data):
        img_cap = self.cv_bridge.imgmsg_to_cv2(data, 'bgr8')
        self.get_logger().info("Receiving video frame [#%04d]; img resolution (%d, %d)" % (
            self.counter, img_cap.shape[0], img_cap.shape[1]))
        self.yolo_detect(img_cap)
        # self.get_logger().info("%s" % self.labels[:, 0])
        # label syntax: x, y, w, h, conf, cls
        self.counter += 1


def main(args=None):
    rclpy.init(args=args)
    node = ImageSubscriber("webcam_yolo_sub")

    try:
        while rclpy.ok():
            rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()
