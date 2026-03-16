from launch import LaunchDescription
from launch_ros.actions import Node
def generate_launch_description():
    ld=LaunchDescription()
    altitude_publisher = Node(
        package='drone1_pkg',
        executable='altitude_publisher',
        name='altitude_publisher',
        output='screen'
    )
    altitude_subscriber = Node(
        package='drone1_pkg',
        executable='altitude_subscriber',
        name='altitude_subscriber',
        output='screen'
    )
    ld.add_action(altitude_publisher)
    ld.add_action(altitude_subscriber)
    return ld