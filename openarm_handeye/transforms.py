import numpy as np
from scipy.spatial.transform import Rotation
import cv2

def transform_to_matrix(transform):
    translation = transform.transform.translation
    rotation = transform.transform.rotation

    t = np.array([
        translation.x,
        translation.y,
        translation.z,
    ])

    R = Rotation.from_quat([
        rotation.x,
        rotation.y,
        rotation.z,
        rotation.w,
    ]).as_matrix()

    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = t

    return T

def rvec_tvec_to_matrix(rvec, tvec):
    """
    Convert OpenCV pose representation (rvec, tvec)
    into a 4x4 homogeneous transformation matrix.
    """

    # Rodrigues vector -> 3x3 rotation matrix
    R, _ = cv2.Rodrigues(rvec)

    # Flatten translation in case it's (3,1)
    t = tvec.reshape(3)

    # Build homogeneous transform
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = t

    return T
def rt_to_matrix(R, t):
    """
    Convert a rotation matrix and translation vector into
    a 4x4 homogeneous transformation matrix.

    Args:
        R: 3x3 rotation matrix.
        t: 3x1 or length-3 translation vector.

    Returns:
        4x4 homogeneous transformation matrix.
    """

    T = np.eye(4)

    T[:3, :3] = R
    T[:3, 3] = t.reshape(3)

    return T
def matrix_to_rt(T):
    """
    Convert a 4x4 homogeneous transformation matrix into
    a rotation matrix and translation vector.
    """

    R = T[:3, :3]
    t = T[:3, 3].reshape(3, 1)

    return R, t