import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class Altitude_Publisher(Node):

    def __init__(self):
        super().__init__('altitude_publisher')
        self.publisher_ = self.create_publisher(Float32, 'drone_altitude', 10)  
        self.timer = self.create_timer(1.0, self.publish_altitude)
        self.altitude = 10.0


    def publish_altitude(self):
        msg = Float32()
        msg.data = self.altitude
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing altitude: {msg.data}')
        self.altitude += 0.5


def main(args=None):
    rclpy.init(args=args)
    node = Altitude_Publisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()