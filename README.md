# ROS2 Hand-Eye Calibration

A modular ROS2 package for performing eye-in-hand camera calibration using OpenCV and ChArUco boards.

This project was developed to explore robotics perception, coordinate transformations, and hand-eye calibration in ROS2. The package provides a reusable calibration pipeline that acquires robot poses from TF, estimates camera poses using OpenCV, and computes the camera-to-gripper transformation.

---

## Features

- ROS2 Humble compatible
- Modular software architecture
- Robot pose acquisition using TF2
- ChArUco board detection
- Camera pose estimation using OpenCV
- Hand-eye calibration using `cv2.calibrateHandEye()`
- YAML export of calibration results
- ROS2 services for data collection and calibration

---

## Project Architecture

```
                    +-------------------+
                    |   RGB Camera      |
                    +---------+---------+
                              |
                              v
                   camera_pose.py
                              |
                              v
                    PoseCollector
                     (collector.py)
                     ^           |
                     |           |
            robot_tf.py          |
             (TF2 Buffer)        |
                     |           |
                     +-----------+
                              |
                              v
                 handeye_solver.py
                              |
                              v
                 calibration.yaml
```

---

## Project Structure

```
openarm_handeye/
├── board.py               # ChArUco board creation
├── calibration_node.py    # ROS2 node
├── camera_pose.py         # Camera pose estimation
├── collector.py           # Collects robot/camera pose pairs
├── handeye_solver.py      # OpenCV hand-eye calibration
├── io.py                  # Save calibration to YAML
├── main.py
├── robot_tf.py            # TF2 robot pose lookup
└── transforms.py          # Homogeneous transform utilities
```

---

## ROS Services

### Capture Pose

```
/capture_pose
```

Captures:

- Robot end-effector pose from TF
- Camera pose from ChArUco detection

---

### Solve Calibration

```
/solve_handeye
```

Runs OpenCV's Hand-Eye calibration algorithm using all collected samples.

---

### Clear Dataset

```
/clear_dataset
```

Removes all collected calibration samples.

---

## Technologies

- ROS2 Humble
- Python
- OpenCV
- TF2
- cv_bridge
- NumPy
- YAML

---

## Current Status

### Implemented

- Robot pose acquisition from TF
- ChArUco pose estimation
- Pose pair collection
- OpenCV Hand-Eye calibration
- Calibration result export

### Current Limitation

The package expects a camera image stream on:

```
/camera/image_raw
```

The OpenArm repository currently provides robot description and bringup, but does not include a simulated camera or image publisher.

The package is therefore ready to work with either:

- a physical RGB camera
- or a simulator publishing ROS image topics

---

## Future Work

- Gazebo camera integration
- Automatic image quality filtering
- Support for multiple calibration algorithms
- RViz visualization tools
- Calibration result validation

---

## Skills Demonstrated

- ROS2
- Robotics Software Engineering
- Coordinate Frames
- TF2
- Computer Vision
- OpenCV
- Camera Calibration
- Hand-Eye Calibration
- Software Architecture
- Robotics Perception

---

## License

Apache-2.0
