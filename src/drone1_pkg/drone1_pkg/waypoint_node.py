import rclpy
from rclpy.node import Node
from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint, VehicleCommand
import math

class WaypointNode(Node):
    def __init__(self):
        super().__init__('waypoint_node')
        
        # Publishers
        self.offboard_pub = self.create_publisher(OffboardControlMode, '/fmu/in/offboard_control_mode', 10)
        self.setpoint_pub = self.create_publisher(TrajectorySetpoint, '/fmu/in/trajectory_setpoint', 10)
        self.cmd_pub = self.create_publisher(VehicleCommand, '/fmu/in/vehicle_command', 10)

        # Mission Variables
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.counter = 0
        self.state = "STARTUP"
        
        # --- FLIGHT PLAN ---
        self.flight_shape = "square" # Change to "square", "triangle", or "figure8"
        self.altitude = -5.0          
        self.ticks_per_wp = 50        # Default: Wait 5 seconds at each point
        self.waypoints = self.generate_waypoints(self.flight_shape)
        self.current_wp_index = 0

    def generate_waypoints(self, shape):
        """Returns a list of [x, y, z] coordinates."""
        z = self.altitude
        
        if shape == "square":
            self.ticks_per_wp = 50  # Stay at each corner for 5 seconds
            return [
                [0.0, 0.0, z], [5.0, 0.0, z], [5.0, 5.0, z], [0.0, 5.0, z], [0.0, 0.0, z]
            ]
            
        elif shape == "triangle":
            self.ticks_per_wp = 50
            return [
                [0.0, 0.0, z], [5.0, 0.0, z], [0.0, 5.0, z], [0.0, 0.0, z]
            ]
            
        elif shape == "figure8":
            self.get_logger().info("Generating smooth Figure 8 curve...")
            self.ticks_per_wp = 1   # UPDATE TARGET EVERY 0.1 SECONDS!
            waypoints = []
            
            duration_sec = 30.0     # Take 30 seconds to fly the whole figure 8
            hz = 10.0               # Our timer runs at 10 Hz
            total_steps = int(duration_sec * hz) # 300 total waypoints!
            
            amplitude = 5.0         # 5 meter radius loops
            
            for i in range(total_steps):
                # Calculate 't' so it goes exactly from 0 to 2*Pi over the 30 seconds
                t = (i / total_steps) * (2 * math.pi)
                
                # Parametric equations for Figure 8 (Lissajous curve)
                x = amplitude * math.sin(t)
                y = amplitude * math.sin(2 * t)
                
                waypoints.append([x, y, z])
                
            return waypoints

        return [[0.0, 0.0, z]]

    def timer_callback(self):
        # 1. Always stream offboard heartbeat
        self.publish_offboard_control_mode()
        
        if self.state == "LANDED_COMPLETE":
            raise SystemExit

        # 2. Startup & Arming Sequence
        if self.state == "STARTUP":
            if self.counter == 10:
                self.get_logger().info("Setting OFFBOARD mode...")
                self.set_mode()
            elif self.counter == 15:
                self.get_logger().info("Arming...")
                self.arm()
                self.state = "NAVIGATING"
                self.get_logger().info(f"Starting {self.flight_shape} mission!")
                self.counter = 0 

        # 3. Navigating the Waypoints
        elif self.state == "NAVIGATING":
            target = self.waypoints[self.current_wp_index]
            self.publish_trajectory_setpoint(target[0], target[1], target[2])
            
            if self.counter > 0 and self.counter % self.ticks_per_wp == 0:
                self.current_wp_index += 1
                
                if self.current_wp_index >= len(self.waypoints):
                    self.get_logger().info("Trajectory complete. Initiating landing.")
                    self.state = "LANDING"
                elif self.ticks_per_wp > 1:
                    # Only print if we are doing a slow shape, otherwise it spams the terminal!
                    self.get_logger().info(f"Moving to WP {self.current_wp_index}")

        # 4. Landing
        elif self.state == "LANDING":
            self.land()
            self.state = "LANDED_COMPLETE"

        self.counter += 1

    
    def publish_offboard_control_mode(self):
        msg = OffboardControlMode()
        msg.position = True
        msg.velocity = False
        msg.acceleration = False
        msg.attitude = False
        msg.body_rate = False
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.offboard_pub.publish(msg)

    def publish_trajectory_setpoint(self, x, y, z):
        msg = TrajectorySetpoint()
        msg.position = [x, y, z]
        msg.yaw = 0.0
        # Unused setpoints MUST be set to NaN
        msg.velocity = [float('nan'), float('nan'), float('nan')]
        msg.acceleration = [float('nan'), float('nan'), float('nan')]
        msg.jerk = [float('nan'), float('nan'), float('nan')]
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.setpoint_pub.publish(msg)

    def arm(self):
        self.send_vehicle_command(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, 1.0)

    def set_mode(self):
        self.send_vehicle_command(VehicleCommand.VEHICLE_CMD_DO_SET_MODE, 1.0, 6.0)

    def land(self):
        self.send_vehicle_command(VehicleCommand.VEHICLE_CMD_DO_SET_MODE, 1.0, 4.0, 6.0)

    def send_vehicle_command(self, command, p1=0.0, p2=0.0, p3=0.0):
        msg = VehicleCommand()
        msg.command = command
        msg.param1 = p1
        msg.param2 = p2
        msg.param3 = p3
        msg.target_system = 1
        msg.target_component = 1
        msg.source_system = 1
        msg.source_component = 1
        msg.from_external = True
        msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.cmd_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = WaypointNode()
    
    try:
        rclpy.spin(node)
    except SystemExit:
        node.get_logger().info("Mission Complete. Shutting down node.")
        
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
