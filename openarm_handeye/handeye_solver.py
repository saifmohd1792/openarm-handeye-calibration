import cv2

from .transforms import (
    matrix_to_rt,
    rt_to_matrix,
)


class HandEyeSolver:
    """
    Solves the hand-eye calibration problem.

    Returns:
        4x4 homogeneous transformation matrix representing
        the camera pose with respect to the robot end-effector.
    """

    def solve(
        self,
        robot_poses,
        camera_poses,
        method=cv2.CALIB_HAND_EYE_TSAI,
    ):
        """
        Solve the hand-eye calibration problem.

        Args:
            robot_poses: List of 4x4 transforms from
                gripper to robot base.
            camera_poses: List of 4x4 transforms from
                calibration target to camera.
            method: OpenCV hand-eye calibration method.

        Returns:
            4x4 homogeneous transformation matrix.
        """

        if len(robot_poses) != len(camera_poses):
            raise ValueError(
                "Robot poses and camera poses must have the same length."
            )

        if len(robot_poses) < 3:
            raise ValueError(
                "At least 3 pose pairs are required."
            )

        R_gripper2base = []
        t_gripper2base = []

        R_target2cam = []
        t_target2cam = []

        # Convert robot poses
        for pose in robot_poses:
            R, t = matrix_to_rt(pose)

            R_gripper2base.append(R)
            t_gripper2base.append(t)

        # Convert camera poses
        for pose in camera_poses:
            R, t = matrix_to_rt(pose)

            R_target2cam.append(R)
            t_target2cam.append(t)

        # Solve the AX = XB problem
        R_cam2gripper, t_cam2gripper = cv2.calibrateHandEye(
            R_gripper2base=R_gripper2base,
            t_gripper2base=t_gripper2base,
            R_target2cam=R_target2cam,
            t_target2cam=t_target2cam,
            method=method,
        )

        return rt_to_matrix(
            R_cam2gripper,
            t_cam2gripper,
        )