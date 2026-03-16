import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class AltitudeSubscriber(Node):
    def __init__(self):
        super().__init__('altitude_subscriber')
        self.subscription = self.create_subscription(
            Float32,
            'drone_altitude',
            self.listener_callback,
            10
        )
    def listener_callback(self, msg):
        self.get_logger().info(f'Received altitude: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = AltitudeSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()