import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger


class ArmServer(Node):

    def __init__(self):
        super().__init__('arm_server')

        self.srv = self.create_service(
            Trigger,
            'arm_drone',
            self.arm_callback
        )


    def arm_callback(self, request, response):

        self.get_logger().info("Drone arming requested")

        response.success = True
        response.message = "Drone armed successfully"

        return response


def main(args=None):
    rclpy.init(args=args)

    node = ArmServer()

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == '__main__':
    main()