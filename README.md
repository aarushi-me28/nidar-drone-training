

# 🚁 NIDAR Drone System Training

This repository contains my work for the **NIDAR (National Innovation Challenge for Drone Application and Research)** Disaster Management Drone System training at RISC.

The project is divided into three main components:
- ROS2 software development  
- CAD design of drone components  
- Electronics design and integration  

---

# 📂 Repository Structure

## 🧠 ROS2 Packages
Location: `src/`

Contains the ROS2 code for the drone system.

### 📦 drone1_pkg
Nodes implemented:
- simple_node  
- altitude_publisher  
- altitude_subscriber  
- arm_server  
- arm_client  
- takeoff_node  
- waypoint_node  

### 📦 drone_sim
Contains ROS2 launch files to run multiple nodes.

---

# 📅 Week 0 – ROS2 Fundamentals

## Task 1 – ROS2 Workspace and Node
![](screenshots/week0/rostask1.png)

## Task 2 – Publisher and Subscriber Communication
![](screenshots/week0/rostask2.png)

## Task 3 – Service and Client Communication
![](screenshots/week0/rostask3services.png)

## Task 4 – Launch File Execution
![](screenshots/week0/rostask4launch.png)

---

# 🛠️ CAD Designs

## 📅 Week 0  
Location: `cad/week0`

### Motor Mount
![](cad/week0/motor_mount.png)

### Motor Mount Drawing
![](cad/week0/drawing_motor_mount.png)

### Propeller
![](cad/week0/propeller.png)

### Battery Block
![](cad/week0/battery_block.png)

### Motor Assembly
![](cad/week0/motor_assembly.png)

### Camera Bracket
![](cad/week0/camera_bracket.png)

### Electronics Plate
![](cad/week0/electronics_plate.png)

---

## 📅 Week 1  
Location: `cad/week1`

### Basic Drone Model (Front)
![](cad/week1/basic_drone_model_frontside.png)

### Basic Drone Model (Back)
![](cad/week1/basic_drone_model.png)

👉 [Onshape Project Link](https://cad.onshape.com/documents/a0f7c9af46a198cc56af469d/w/b3925598f5c5c9bbdfd05818/e/9312e9408b08bb7651e16f4f?renderMode=0&uiState=69c16d33fed5b8f664953900)
---
# 🔗 Onshape CAD Link

View full CAD models here:  
👉 [Onshape Project Link](PASTE_YOUR_LINK_HERE)

## 🚁 Drone Architecture Selection

For the scout drone, both the number of rotors (quadcopter, hexacopter, octocopter) and frame geometries (X, H, Deadcat) were evaluated based on mission requirements such as camera visibility, stability, weight, and efficiency.

A quadcopter configuration was selected over hexacopter and octocopter designs. A quadcopter uses only four motors and ESCs, making it lighter and more power-efficient, which helps maximize flight time during surveillance operations. It also has lower system complexity, making it easier to design, assemble, and maintain. Since the scout drone primarily carries a camera and communication system, the additional lifting capacity of hexacopters or octocopters is not required. Although multi-rotor systems with more motors provide redundancy in case of motor failure, they increase weight, cost, and power consumption unnecessarily for this application. Therefore, a quadcopter provides the best balance between efficiency, simplicity, and performance.

For frame geometry, X, H, and Deadcat configurations were considered. The X frame provides excellent symmetry and stability but obstructs the camera’s field of view due to front propellers. The H frame offers more space for electronics but is slightly heavier and still does not fully eliminate propeller visibility. The Deadcat frame, however, angles the front arms outward, ensuring an unobstructed forward-facing camera view.

Since camera visibility is the most critical requirement for a surveillance drone, the Deadcat configuration was selected. Although it introduces slight asymmetry, modern flight controllers can compensate for this and maintain stable flight.

**Final Selection:** Quadcopter with Deadcat frame configuration.

## 🛠️ Frame Design Justification (Week 1 CAD)

The drone frame was designed with a focus on structural stability, camera visibility, and efficient component integration.

The central plate has dimensions of 120 mm × 100 mm and is vertically symmetric to maintain balance and uniform load distribution. Adequate space is provided within the central plate to accommodate essential electronics such as the flight controller, power distribution components, and wiring.

The arm geometry is designed to improve both stability and camera visibility. The front arms are oriented at relatively lower angles, while the rear arms are positioned at higher angles. Specifically, the upper arms are oriented at approximately 30° with respect to the horizontal, while the lower arms are oriented at approximately 45°. This configuration ensures that the front propellers remain outside the camera’s field of view, thereby enabling unobstructed surveillance.

Structural ribs have been incorporated into the frame to enhance rigidity without significantly increasing weight. These ribs improve load distribution across the frame and reduce deformation during flight.

Provision for wire routing has also been included in the design. Dedicated channels and spacing in the front section of the frame allow organized wire management, reducing clutter and minimizing the risk of wire damage.

Motor mounting regions are designed to ensure proper spacing between motors and sufficient propeller clearance, preventing interference during operation.

Overall, the design achieves a balance between lightweight construction, structural strength, and functional integration required for a scout drone.


---

# ⚙️ System Architecture & Electronics

📄 [Mission and System Architecture](electronics/MissionAndSystemArchitecture.pdf)  
📄 [Electronics – Week 1](electronics/nidar_week1.pdf)

---

# 👩‍💻 Author

**Aarushi**  
NIDAR Drone Training Project