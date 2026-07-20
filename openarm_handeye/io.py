import yaml

from scipy.spatial.transform import Rotation


def save_transform(filename, T):
    """
    Save a homogeneous transformation matrix to YAML.

    Args:
        filename: Output YAML file.
        T: 4x4 homogeneous transformation matrix.
    """

    translation = T[:3, 3]

    quaternion = Rotation.from_matrix(
        T[:3, :3]
    ).as_quat()

    data = {
        "translation": {
            "x": float(translation[0]),
            "y": float(translation[1]),
            "z": float(translation[2]),
        },
        "rotation": {
            "x": float(quaternion[0]),
            "y": float(quaternion[1]),
            "z": float(quaternion[2]),
            "w": float(quaternion[3]),
        },
    }

    with open(filename, "w") as f:
        yaml.safe_dump(
            data,
            f,
            sort_keys=False,
        )