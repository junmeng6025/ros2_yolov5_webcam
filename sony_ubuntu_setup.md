# SONY a7r4 Setup
If you have already finished with the installing and build part and **just want to run the camera**, scroll down and start from **Run** part.
## 1) Connect SONY a7r4 to Ubuntu

follow the guide https://hanspinckaers.com/using-a-sony-alpha-camera-as-a-webcam-in-ubuntu

### Make sure you have `ffmpeg`: 
```bash
sudo apt-get install ffmpeg
```
### Install latest release gphoto2: 
https://github.com/gonzalo/gphoto2-updater
```bash
wget https://raw.githubusercontent.com/gonzalo/gphoto2-updater/master/gphoto2-updater.sh && wget https://raw.githubusercontent.com/gonzalo/gphoto2-updater/master/.env && chmod +x gphoto2-updater.sh && sudo ./gphoto2-updater.sh
```

### Install v4l2loopback from source (see README.md)
https://github.com/umlaeute/v4l2loopback 
```bash
git clone <repo-link>
cd v4l2loopback
make
```
This should give you a file named `v4l2loopback.ko` in the current folder `/v4l2loopback`, which is the kernel module.  
If success, go ahead:
```bash
# stay in dir /v4l2loopback
sudo make install
sudo depmod -a
```
### Run
```bash
# stay in dir /v4l2loopback
sudo modprobe v4l2loopback
# check lookback devices
ls -1 /sys/devices/virtual/video4linux
```
> make sure `video2` is in the returned message
### Enable kernel extension: 
```bash
sudo modprobe v4l2loopback exclusive_caps=1 max_buffers=2
```
- Launch webcam:
```bash
gphoto2 --stdout --capture-movie | ffmpeg -i - -vcodec rawvideo -pix_fmt yuv420p -threads 8 -f v4l2 /dev/video2
```
### visualize the video in VLC
follow the guide [here](https://www.crackedthecode.co/how-to-use-your-dslr-as-a-webcam-in-linux/#:~:text=Now%2C open the VLC application%2C select the Media Menu -> Capture Device (Ctrl%2Bc).)

## 2) write a python script to capture the video stream using OpenCV
referenced OpenCV document: https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html
### copy the code of the first block "Capture Video from Camera"
```python
import numpy as np
import cv2 as cv

GREY_MODE = False

cap = cv.VideoCapture(2)  # modify the device ID here
if not cap.isOpened():
      print("Cannot open camera")
      exit()
while True:
      # Capture frame-by-frame
      ret, frame = cap.read()
      # if frame is read correctly ret is True
      if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
      # Our operations on the frame come here
      gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

      # Display the resulting frame
      if GREY_MODE:
            cv.imshow('frame', grey)
      else:
            cv.imshow('frame', frame)
            
      if cv.waitKey(1) == ord('q'):
            break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
```
### modify the device ID  
here for example when I launched **gphoto2**, the device name here is '/dev/video2'. so I changed 
```python
cap = cv.VideoCapture(0)
```
as
```python
cap = cv.VideoCapture(2)
```
in the code above.  
Finally, save the .py file
### launch SONY camera as webcam like mentioned above:
make sure to connect camera to laptop and set up the USB connection mode of camera correctly before running the command:
```bash
gphoto2 --stdout --capture-movie | ffmpeg -i - -vcodec rawvideo -pix_fmt yuv420p -threads 8 -f v4l2 /dev/video2
```
### run the .py script we've just wrote

## 3) Test the connection with ROS2
Test the SONY-ROS2 connection with a [YOLOv5 integrated ROS2 program](https://github.com/junmeng6025/ros2_yolov5_webcam), which I wrote for another project.  
The result would be like this:  
<img src = "README/sony-yolo-3.png">  
