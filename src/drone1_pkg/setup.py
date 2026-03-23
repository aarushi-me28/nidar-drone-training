from setuptools import find_packages, setup

package_name = 'drone1_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='aarushi',
    maintainer_email='25me01028@iitbbs.ac.in',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': ["simple_node = drone1_pkg.simple_node:main",
                            "altitude_publisher = drone1_pkg.altitude_publisher:main",
                            "altitude_subscriber = drone1_pkg.altitude_subscriber:main",
                            "arm_server = drone1_pkg.arm_server:main",
                            "arm_client = drone1_pkg.arm_client:main",
                            "takeoff_node = drone1_pkg.takeoff_node:main",
                            "waypoint_node = drone1_pkg.waypoint_node:main"
        ],
    },
) 
