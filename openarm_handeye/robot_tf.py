import rclpy

from tf2_ros import Buffer
from tf2_ros import TransformException
from tf2_ros import TransformListener

from .transforms import transform_to_matrix


class RobotTF:
    """
    Retrieves the robot end-effector pose from the TF tree.

    Returns:
        4x4 homogeneous transformation matrix (numpy.ndarray)
    """

    def __init__(
        self,
        node,
        base_frame: str,
        ee_frame: str,
    ):
        self.node = node

        self.base_frame = base_frame
        self.ee_frame = ee_frame

        self.buffer = Buffer()
        self.listener = TransformListener(
            self.buffer,
            self.node,
        )

    def get_pose(self):
        """
        Returns the current end-effector pose with respect
        to the robot base frame.

        Returns:
            np.ndarray (4x4) if successful
            None if the transform is unavailable
        """

        try:
            transform = self.buffer.lookup_transform(
                self.base_frame,
                self.ee_frame,
                rclpy.time.Time(),
            )

            return transform_to_matrix(transform)

        except TransformException as e:
            self.node.get_logger().error(
                f"Failed to lookup transform "
                f"{self.base_frame} -> {self.ee_frame}: {e}"
            )
            return None