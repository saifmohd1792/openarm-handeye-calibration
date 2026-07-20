import cv2
import numpy as np
import cv2
import numpy as np

from .transforms import rvec_tvec_to_matrix


class CameraPoseEstimator:
    """
    Estimates the pose of a ChArUco board with respect to the camera.

    Returns:
        4x4 homogeneous transformation matrix (numpy.ndarray)
    """

    def __init__(
        self,
        camera_matrix: np.ndarray,
        dist_coeffs: np.ndarray,
        board,
        aruco_dict,
    ):
        self.camera_matrix = camera_matrix
        self.dist_coeffs = dist_coeffs

        self.board = board

        self.detector = cv2.aruco.ArucoDetector(
            aruco_dict,
            cv2.aruco.DetectorParameters(),
        )

    def estimate_pose(self, image):
        """
        Estimate board pose from an image.

        Returns:
            4x4 transformation matrix if successful
            None otherwise
        """

        # Detect ArUco markers
        corners, ids, _ = self.detector.detectMarkers(image)

        if ids is None or len(ids) == 0:
            return None

        # Interpolate ChArUco corners
        success, charuco_corners, charuco_ids = (
            cv2.aruco.interpolateCornersCharuco(
                markerCorners=corners,
                markerIds=ids,
                image=image,
                board=self.board,
                cameraMatrix=self.camera_matrix,
                distCoeffs=self.dist_coeffs,
            )
        )

        # Need enough corners for a stable pose estimate
        if success < 4:
            return None

        # Estimate board pose
        valid, rvec, tvec = cv2.aruco.estimatePoseCharucoBoard(
            charucoCorners=charuco_corners,
            charucoIds=charuco_ids,
            board=self.board,
            cameraMatrix=self.camera_matrix,
            distCoeffs=self.dist_coeffs,
            rvec=None,
            tvec=None,
        )

        if not valid:
            return None

        return rvec_tvec_to_matrix(rvec, tvec)