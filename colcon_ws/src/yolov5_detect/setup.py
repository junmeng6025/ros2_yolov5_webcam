from setuptools import setup
from setuptools import find_packages
from glob import glob
import os

package_name = 'yolov5_detect'
submodules = 'yolov5_detect/yolov5'

setup(
    name=package_name,
    version='0.0.0',
    # packages=[package_name, submodules],
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
         glob(os.path.join('launch', '*.launch.py'))),
        (os.path.join('share', package_name, 'yolov5'),
         glob(os.path.join('yolov5', '*.*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jun',
    maintainer_email='mengjun6025@163.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'webcam_yolo_pub=yolov5_detect.webcam_yolo_pub:main',
            'webcam_yolo_sub=yolov5_detect.webcam_yolo_sub:main'
        ],
    },
)
