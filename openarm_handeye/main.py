import rclpy

from .calibration_node import HandEyeCalibrationNode


def main(args=None):
    rclpy.init(args=args)

    node = HandEyeCalibrationNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()