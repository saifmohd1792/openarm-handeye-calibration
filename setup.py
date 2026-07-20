from setuptools import find_packages, setup

package_name = 'openarm_handeye'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        (
            'share/' + package_name,
            ['package.xml'],
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='saifm',
    maintainer_email='saifm@todo.todo',
    description='ROS2 hand-eye calibration package',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'handeye_calibration = openarm_handeye.main:main',
        ],
    },
)