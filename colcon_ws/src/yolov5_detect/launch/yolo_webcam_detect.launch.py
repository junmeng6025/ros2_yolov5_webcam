from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():              # 自动生成launch文件的函数
    return LaunchDescription([                  # 返回launch文件的描述信息
        Node(                                   # 配置一个节点的启动
            package='usb_cam',                  # 节点所在的功能包
            executable='usb_cam_node_exe',            # 节点的可执行文件
        ),
        Node(                                   # 配置一个节点的启动
            package='yolov5_detect',               # 节点所在的功能包
            executable='webcam_yolo_sub',           # 节点的可执行文件名
        )
    ])
