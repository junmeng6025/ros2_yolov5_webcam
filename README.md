# YOLOv5 on ROS2
# Pre-requisites
- ROS2 (DISTRO: galactic) installed and sourced
- YOLOv5 requirements satisfied
# Run
- source ros2
    ```bash
    source /opt/ros/galactic/setup.bash
    ```
    > use command `echo ${ROS_DISTRO}` to make sure your current Terminal is sourced to a ROS2 distro, e.g. `galactic`
- compile the workspace first  
    ```bash
    cd ros2_yolov5_webcam/colcon_ws
    colcon build
    ```
- copy the folder `/data` in
    ```bash
    /src/yolov5_detect/yolov5/
    ```
    to
    ```bash
    /install/yolov5_detect/lib/python3.8/site-packages/yolov5/
    ```
- launch the nodes  
    ```bash
    # stay in the /colcon_ws directory
    source install/setup.sh
    ros2 launch yolov5_detect yolo_webcam_detect.launch.py
    ```
- **to friends who comes from the `SONY setup` project:**
    ```bash
    # stay in the /colcon_ws directory
    source install/setup.sh
    ros2 launch yolov5_detect yolo_sony_detect.launch.py
    ```
    to whom who has interest in using an external SONY camera as a substitution of web-camera:  
    [SONY a7r4 setup for Ubuntu](sony_ubuntu_setup.md)

***
below are some notes during development...
# Implement YOLOv5 algorithm to our ROS node
To learning how to build a ros node containing a custom submodule, check these blogs on ROS answer:  
- [Including a Python module in a ROS2 package](https://answers.ros.org/question/367793/including-a-python-module-in-a-ros2-package/)  
- [ROS2 Python relative import of my scritps](https://answers.ros.org/question/349790/ros2-python-relative-import-of-my-scritps/)  
- [All google searching results...](https://www.google.com/search?q=submodules+in+setup.py+ros2&client=ubuntu&hs=0q9&channel=fs&sxsrf=ALiCzsacZQxK4_Va23YuXsC5pibK9ZZAMw%3A1666093937039&ei=cZNOY8P5AcPEkwW1o6f4CQ&ved=0ahUKEwiD9p3K2-n6AhVD4qQKHbXRCZ8Q4dUDCA4&uact=5&oq=submodules+in+setup.py+ros2&gs_lcp=Cgdnd3Mtd2l6EAMyBQgAEKIEOgoIABBHENYEELADOg0IABDkAhDWBBCwAxgBOggIABAIEAcQHjoFCAAQhgM6CAghEMMEEKABSgQITRgBSgQIQRgASgQIRhgBUPIGWLSaAmDJnAJoAnABeACAAbwCiAGoDZIBBzEuOS4wLjGYAQCgAQGgAQLIAQ3AAQHaAQYIARABGAk&sclient=gws-wiz)

**How did I do:** 
***
*the following guide just works, but not so elegant...*
*** 
## 0) re-write a class for YOLOv5 detector `detect_ros.py`
Capsule the detect as a class `Yolov5Detector()`, which would be easier to be implemented in ros node script.  
The `yolov5` folder is placed directly in our package folder, parallel with sub-package folder:
```bash
colcon_ws
├── src
│   ├── yolov5_detect #------------------------ROS package folder
│   │   ├── package.xml
│   │   ├── setup.py
│   │   ├── setup.cfg
│   │   ├── yolov5_detect #----------------ROS package sub-folder
│   │   │   ├── __init__.py
│   │   │   ├── webcam_yolo_sub.py #------------- ROS node script
│   │   │   └── ...
│   │   │
│   │   └── yolov5 #-------------------------the yolov5 submodule
│   │       └── ...
│   │
│   ├── install
│   ├── build
│   └── log
│
└── README.md
```
## 1) modify the `setup.py`
Declare the submodule names in `setup.py` to ensure them to be compiled together into `/install` after **colcon build**:
```python
from setuptools import setup
from setuptools import find_packages

package_name = 'yolov5_detect'
submodules = 'yolov5_detect/yolov5'  # declare the submodule to be build

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ################## MODIFIED ##################
        (os.path.join('share', package_name, 'launch'),
         glob(os.path.join('launch', '*.launch.py'))),
        (os.path.join('share', package_name, 'yolov5'),
         glob(os.path.join('yolov5', '*.*'))),
        ################## MODIFIED ##################
        # this part helps copy the necessary files into /install directory
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jun',
    maintainer_email='mengjun6025@163.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [  # define the entry_points as usual
            'webcam_yolo_pub=yolov5_detect.webcam_yolo_pub:main',
            'webcam_yolo_sub=yolov5_detect.webcam_yolo_sub:main'
        ],
    },
)
```
## 2) modify the `import` part in ALL relevant scripts
To connect the scripts from yolov5's subfolders like `utils` and `models` correctly, we need to switch the **relative path** to **absolute path**, i.e. add `yolov5.` ahead of the folder names **in ALL relevant scripts**:
```python
from utils.plots import Annotator, colors, save_one_box

# --> MODIFY: add '<submodule_name>. ahead

from yolov5.utils.plots import Annotator, colors, save_one_box
```
*Here I managed to do it via running the node again and again and allocate ALL the relevant scripts in the **error messages**.*
## 3) copy the `coco128.yaml` to the `/install` space
copy the folder `/data` containing `.yaml` files in
```bash
/src/yolov5_detect/yolov5/
```
to
```bash
/install/yolov5_detect/lib/python3.8/site-packages/yolov5/
```
