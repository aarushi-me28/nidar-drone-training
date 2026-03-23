import rclpy
from rclpy.node import Node
from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint, VehicleCommand


class TakeoffNode(Node):
    def __init__(self):
        super().__init__('takeoff_node')

        self.offboard_pub = self.create_publisher(OffboardControlMode, '/fmu/in/offboard_control_mode', 10)
        self.setpoint_pub = self.create_publisher(TrajectorySetpoint, '/fmu/in/trajectory_setpoint', 10)
        self.cmd_pub = self.create_publisher(VehicleCommand, '/fmu/in/vehicle_command', 10)

        self.timer = self.create_timer(0.1, self.timer_callback)
        self.counter = 0

    def timer_callback(self):

        # 1. Send OFFBOARD control mode
        offboard = OffboardControlMode()
        offboard.position = True
        offboard.velocity = False
        offboard.acceleration = False
        offboard.attitude = False
        offboard.body_rate = False
        offboard.timestamp = 0
        self.offboard_pub.publish(offboard)

        # 2. Send position setpoint
        setpoint = TrajectorySetpoint()
        setpoint.position = [0.0, 0.0, -2.0]
        setpoint.yaw = 0.0
        setpoint.timestamp = 0
        self.setpoint_pub.publish(setpoint)

        self.get_logger().info(f"Counter: {self.counter}")

        # 3. After some time → switch mode + arm
        if self.counter == 100:
            self.set_mode()

        if self.counter == 110:
            self.arm()    

        if self.counter == 300:
            self.land() 

        if self.counter == 400:
            self.get_logger().info("Takeoff complete! Handing control back to PX4.")   
            raise SystemExit

        self.counter += 1

    def arm(self):
        cmd = VehicleCommand()
        cmd.command = 400 # ARM
        cmd.param1 = 1.0
        cmd.param2 = 6.0
        cmd.target_system = 1
        cmd.target_component = 1
        cmd.source_system = 1
        cmd.source_component = 1
        cmd.from_external = True
        cmd.timestamp = 0
        self.cmd_pub.publish(cmd)

    def set_mode(self):
        cmd = VehicleCommand()
        cmd.command = 176  # SET MODE
        cmd.param1 = 1.0
        cmd.param2 = 6.0   # OFFBOARD
        cmd.target_system = 1
        cmd.target_component = 1
        cmd.source_system = 1
        cmd.source_component = 1
        cmd.from_external = True
        cmd.timestamp = 0
        self.cmd_pub.publish(cmd)

    def land(self):
       # """Switches the vehicle to AUTO.LAND mode."""
        cmd = VehicleCommand()
        cmd.command = 176  # VEHICLE_CMD_DO_SET_MODE
        cmd.param1 = 1.0   # Base mode
        cmd.param2 = 4.0   # PX4_CUSTOM_MAIN_MODE_AUTO
        cmd.param3 = 6.0   # PX4_CUSTOM_SUB_MODE_AUTO_LAND
        cmd.target_system = 1
        cmd.target_component = 1
        cmd.source_system = 1
        cmd.source_component = 1
        cmd.from_external = True
        cmd.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        
        self.cmd_pub.publish(cmd)
        self.get_logger().info("Landing command sent! Handing control back to PX4.")

def main(args=None):
    rclpy.init(args=args)
    node = TakeoffNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()