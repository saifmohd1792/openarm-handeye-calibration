import cv2
import numpy as np

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_srvs.srv import Trigger

from .board import create_charuco_board
from .camera_pose import CameraPoseEstimator
from .collector import PoseCollector
from .handeye_solver import HandEyeSolver
from .io import save_transform
from .robot_tf import RobotTF


class HandEyeCalibrationNode(Node):

    def __init__(self):
        super().__init__("handeye_calibration")

        self.bridge = CvBridge()

        # ---------------- Parameters ----------------

        self.declare_parameter("base_frame", "base_link")
        self.declare_parameter("ee_frame", "tool0")
        self.declare_parameter("image_topic", "/camera/image_raw")
        self.declare_parameter("output_file", "handeye.yaml")

        # ChArUco board parameters
        self.declare_parameter("squares_x", 7)
        self.declare_parameter("squares_y", 5)
        self.declare_parameter("square_length", 0.04)
        self.declare_parameter("marker_length", 0.03)

        base_frame = self.get_parameter("base_frame").value
        ee_frame = self.get_parameter("ee_frame").value
        image_topic = self.get_parameter("image_topic").value
        self.output_file = self.get_parameter("output_file").value

        squares_x = self.get_parameter("squares_x").value
        squares_y = self.get_parameter("squares_y").value
        square_length = self.get_parameter("square_length").value
        marker_length = self.get_parameter("marker_length").value

        # ---------------- Camera Calibration ----------------

        # TODO: Replace with CameraInfo subscription
        self.camera_matrix = np.eye(3)
        self.dist_coeffs = np.zeros((5, 1))

        # ---------------- Board ----------------

        board, aruco_dict = create_charuco_board(
            squares_x=squares_x,
            squares_y=squares_y,
            square_length=square_length,
            marker_length=marker_length,
        )

        # ---------------- Components ----------------

        self.robot_tf = RobotTF(
            self,
            base_frame,
            ee_frame,
        )

        self.camera = CameraPoseEstimator(
            self.camera_matrix,
            self.dist_coeffs,
            board,
            aruco_dict,
        )

        self.collector = PoseCollector(
            self.robot_tf,
            self.camera,
        )

        self.solver = HandEyeSolver()

        # ---------------- State ----------------

        self.latest_image = None

        # ---------------- Subscribers ----------------

        self.subscription = self.create_subscription(
            Image,
            image_topic,
            self.image_callback,
            10,
        )

        # ---------------- Services ----------------

        self.capture_service = self.create_service(
            Trigger,
            "capture_pose",
            self.capture_callback,
        )

        self.solve_service = self.create_service(
            Trigger,
            "solve_handeye",
            self.solve_callback,
        )

        self.clear_service = self.create_service(
            Trigger,
            "clear_dataset",
            self.clear_callback,
        )

        self.get_logger().info("Hand-eye calibration node started.")

    # -------------------------------------------------------
    # Subscribers
    # -------------------------------------------------------

    def image_callback(self, msg):
        self.latest_image = self.bridge.imgmsg_to_cv2(
            msg,
            desired_encoding="bgr8",
        )

    # -------------------------------------------------------
    # Core Functions
    # -------------------------------------------------------

    def capture(self):

        if self.latest_image is None:
            self.get_logger().warning("No image received.")
            return False

        success = self.collector.capture(
            self.latest_image,
        )

        if success:
            self.get_logger().info(
                f"Captured pose pair #{self.collector.count()}"
            )
        else:
            self.get_logger().warning(
                "Failed to capture pose pair."
            )

        return success

    def solve(self):

        robot_poses, camera_poses = self.collector.get_data()

        transform = self.solver.solve(
            robot_poses,
            camera_poses,
        )

        save_transform(
            self.output_file,
            transform,
        )

        self.get_logger().info(
            f"Calibration saved to '{self.output_file}'."
        )

        return transform

    # -------------------------------------------------------
    # Service Callbacks
    # -------------------------------------------------------

    def capture_callback(self, request, response):

        success = self.capture()

        response.success = success

        if success:
            response.message = (
                f"Captured pose pair #{self.collector.count()}"
            )
        else:
            response.message = "Failed to capture pose pair."

        return response

    def solve_callback(self, request, response):

        if self.collector.count() < 3:
            response.success = False
            response.message = (
                f"Need at least 3 pose pairs. "
                f"Currently have {self.collector.count()}."
            )
            return response

        try:
            self.solve()

            response.success = True
            response.message = "Calibration completed successfully."

        except Exception as e:

            response.success = False
            response.message = str(e)

        return response

    def clear_callback(self, request, response):

        self.collector.clear()

        response.success = True
        response.message = "Pose dataset cleared."

        return response