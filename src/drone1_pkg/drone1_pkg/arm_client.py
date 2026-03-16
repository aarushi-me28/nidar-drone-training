import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger


class ArmClient(Node):

    def __init__(self):
        super().__init__('arm_client')

        self.client = self.create_client(Trigger, 'arm_drone')

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')

        self.request = Trigger.Request()

        self.send_request()


    def send_request(self):

        future = self.client.call_async(self.request)

        rclpy.spin_until_future_complete(self, future)

        response = future.result()

        self.get_logger().info(
            f'Service response: {response.message}'
        )


def main(args=None):
    rclpy.init(args=args)

    node = ArmClient()

    rclpy.shutdown()


if __name__ == '__main__':
    main()