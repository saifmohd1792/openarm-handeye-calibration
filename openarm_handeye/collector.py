import numpy as np


class PoseCollector:
    """
    Collects synchronized robot and camera poses
    for hand-eye calibration.
    """

    def __init__(
        self,
        robot_tf,
        camera_pose_estimator,
    ):
        self.robot_tf = robot_tf
        self.camera_pose_estimator = camera_pose_estimator

        self.robot_poses = []
        self.camera_poses = []

    def capture(self, image):
        """
        Capture one synchronized robot/camera pose pair.

        Args:
            image: OpenCV image from the camera.

        Returns:
            True if capture succeeded.
            False otherwise.
        """

        print("========== CAPTURE START ==========")

        print("Getting robot pose...")
        robot_pose = self.robot_tf.get_pose()

        if robot_pose is None:
            print("❌ Robot pose lookup failed.")
            return False

        print("✅ Robot pose acquired.")

        print("Estimating camera pose...")
        camera_pose = self.camera_pose_estimator.estimate_pose(image)

        if camera_pose is None:
            print("❌ Camera pose estimation failed.")
            return False

        print("✅ Camera pose estimated.")

        self.robot_poses.append(robot_pose)
        self.camera_poses.append(camera_pose)

        print(f"Collected pose pair #{len(self.robot_poses)}")
        print("=========== CAPTURE END ===========")

        return True

    def clear(self):
        """Remove all collected poses."""

        self.robot_poses.clear()
        self.camera_poses.clear()

    def count(self):
        """Return number of collected pose pairs."""

        return len(self.robot_poses)

    def get_data(self):
        """
        Return collected data.

        Returns:
            robot_poses, camera_poses
        """

        return self.robot_poses, self.camera_poses