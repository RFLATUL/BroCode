# HARDWARE OVERVIEW

Detailed overview of the hardware architecture of our WRO Future Engineers robot.

---

## Table of Contents

- [Overview](#overview)
- [Hardware Overview](#hardware-overview)
  - [Processing Unit](#processing-unit)
  - [Locomotion & Actuation](#locomotion--actuation)
  - [Motor Driver](#motor-driver)
  - [Power Management](#power-management)
  - [Sensors](#sensors)
  - [Camera System](#camera-system)
  - [Custom Electronics & Wiring](#custom-electronics--wiring)
  - [Mechanical Structure](#mechanical-structure)
  - [Sensor Placement](#sensor-placement)
- [Dimensions & Physical Layout](#dimensions--physical-layout)
- [Wiring & Pin Mapping](#wiring--pin-mapping)
- [Bill of Materials](#bill-of-materials)
- [Engineering Decisions](#engineering-decisions)
  - [Why We Chose a Minimal Sensor Configuration](#why-we-chose-a-minimal-sensor-configuration)
  - [Why We Use the Camera as the Main Perception System](#why-we-use-the-camera-as-the-main-perception-system)
  - [Why We Use a LEGO Technic Chassis](#why-we-use-a-lego-technic-chassis)
  - [Why We Use the White Electronics Cover](#why-we-use-the-white-electronics-cover)
- [Hardware Reliability](#hardware-reliability)

---

## Overview

Our robot is designed around **simplicity, reliability, modularity, and controlled performance**.

The hardware integrates:

- Raspberry Pi 4 as the main processing unit
- Raspberry Pi Camera Module 3 Wide as the primary perception system
- BNO055 IMU for heading and orientation feedback
- DC drive motor for propulsion
- Servo-based front Ackermann steering
- L298N motor driver
- 3-cell LiPo battery
- LEGO Technic mechanical structure
- Custom electronics mounting and organized wiring

Our main hardware philosophy was to use the **minimum practical sensor configuration while extracting as much information as possible from the camera and IMU**. This reduces wiring, power consumption, calibration requirements, and potential failure points.

The final system is designed to support the **Open Challenge, Obstacle Challenge, autonomous navigation, and parking**.

---

## Hardware Overview

### Processing Unit

The robot uses a **Raspberry Pi 4** as its central processing unit.

The Raspberry Pi is responsible for:

- Processing the camera feed in real time.
- Running OpenCV computer vision.
- Processing BNO055 orientation data.
- Running navigation and steering algorithms.
- Making obstacle and track decisions.
- Controlling the drive motor through the L298N.
- Controlling the steering servo.
- Managing the overall autonomous state machine.

We selected the Raspberry Pi because it gives us enough processing capability for real-time computer vision while still allowing the robot to remain compact.

---

### Locomotion & Actuation

The robot uses a **four-wheel chassis with rear-wheel drive and front Ackermann steering**.

#### Drive System

A DC drive motor provides propulsion to the rear drivetrain.

The drive system was selected around the balance between:

- Speed
- Torque
- Acceleration
- Controllability
- Power consumption

We did not want to optimize only for maximum speed. For our robot, predictable acceleration and controllable movement are more important because the robot has to maintain its trajectory while following the track and navigating obstacles.

#### Steering System

The front wheels use an **Ackermann steering arrangement** controlled by a servo.

The steering servo is mechanically connected to the front steering linkage. This allows the inner and outer wheels to follow different turning radii during a corner.

This was particularly important for our design because the steering system needs to respond accurately to camera-based positional corrections. A predictable mechanical relationship between servo movement and wheel angle makes the software control much easier to tune.

---

### Motor Driver

The drive motor is controlled using an **L298N motor driver**.

The motor driver provides:

- Forward and reverse motor control
- PWM speed control
- Controlled motor actuation from the Raspberry Pi

The Raspberry Pi sends the direction and PWM commands to the motor driver.

The motor direction uses:

- **IN1 → GPIO 24**
- **IN2 → GPIO 23**

Motor speed is controlled through:

- **ENA / PWM → GPIO 18**

This gives the software direct control over both the direction and speed of the drive motor.

---

### Power Management

The robot uses a **3-cell LiPo battery** as its primary power source.

The battery supplies the drive motor, steering servo, Raspberry Pi, camera, IMU, and supporting electronics.

Our power strategy was built around keeping the system efficient rather than adding unnecessary hardware. The main goals were to:

- Keep the robot lightweight.
- Provide sufficient current during acceleration and turning.
- Maintain stable power for the Raspberry Pi.
- Reduce unnecessary electrical loads.
- Reserve sufficient power for the drivetrain and steering.

The minimal sensor architecture also helps keep the overall power budget manageable.

---

### Sensors

Our final sensor architecture is intentionally minimal and is built around two primary sensing systems.

#### Raspberry Pi Camera Module 3 Wide

The camera is the robot's main perception system.

It is used for:

- Wall detection
- Track perception
- Coloured obstacle detection
- Navigation
- Parking-marker detection
- Position estimation

During development, we tested multiple colour representations including **RGB, BGR, HSV, and LAB**.

LAB was ultimately selected for our final colour-detection pipeline because it gave us the most consistent results during testing, particularly when lighting, shadows, and reflections changed.

#### BNO055 IMU

The BNO055 provides heading and orientation feedback.

It is mainly used for:

- Heading stabilization
- Turn consistency
- 90° turn alignment
- Orientation feedback during manoeuvres

The IMU is mounted on the **left side of the chassis** and communicates with the Raspberry Pi through I²C.

---

### Camera System

The **Raspberry Pi Camera Module 3 Wide** is centrally mounted above the robot.

The camera is positioned approximately:

- **26 cm above the ground**
- **10° downward from horizontal**
- **Centred on the robot**

This mounting arrangement gives the camera a consistent forward field of view while keeping the relevant track area visible.

The camera is used as a multi-purpose perception system rather than using separate sensors for each task.

Our OpenCV pipeline processes the image to extract:

- Colour regions
- Wall positions
- Obstacle positions
- Target points
- Parking markers

Keeping the camera fixed is particularly important because our vision algorithms depend on consistent image geometry.

---

### Custom Electronics & Wiring

The electronics are mounted on a central platform above the mechanical chassis.

The layout was designed to:

- Keep wiring organized.
- Keep wires away from moving mechanisms.
- Make components accessible during testing.
- Reduce loose connections.
- Keep the main electronics close to the centre of the robot.

The Raspberry Pi, motor driver, power electronics, IMU connections, and supporting wiring are arranged so that individual systems can be isolated during troubleshooting.

A protective **white cover** is also placed above the electronics. This was added after we found that the camera could sometimes interpret the coloured electronics and wiring as visual features on the track.

---

### Mechanical Structure

The robot uses a **LEGO Technic-based chassis** with custom structural arrangements for the drivetrain, steering, electronics, and camera support.

The mechanical design was developed around:

- Rigidity
- Low weight
- Modularity
- Easy repair
- Easy modification
- Predictable steering
- Stable sensor mounting

The LEGO structure allowed us to change component positions quickly during development without having to rebuild the entire robot.

The camera support is reinforced to reduce movement and vibration because even small changes in camera position can affect the consistency of the vision system.

---

### Sensor Placement

Sensor placement was treated as part of the overall system design rather than simply placing components wherever there was available space.

| Component | Placement | Purpose |
|---|---|---|
| Camera Module 3 Wide | Centre, ~26 cm high, 10° downward | Main visual perception |
| BNO055 IMU | Left side of chassis | Heading and orientation |

The camera's position was kept fixed throughout testing so that the relationship between image coordinates and the physical track remained consistent.

The BNO055 is also securely mounted so that its orientation does not change during operation.

---

## Dimensions & Physical Layout

The robot was designed to remain compact while providing enough space for the drivetrain, steering mechanism, electronics, battery, and camera support.

The physical layout is organized around three main areas:

### Front

- Ackermann steering mechanism
- Front wheels
- Camera support structure

### Centre

- Raspberry Pi
- Motor driver
- Power electronics
- BNO055 IMU
- Main wiring

### Rear

- Drive system
- Rear wheels
- Battery
- Supporting electrical connections

The final dimensions are maintained according to the competition requirements and the physical configuration of the robot.

---

## Wiring & Pin Mapping

The Raspberry Pi 4 is the central controller of the robot.

| Component | Raspberry Pi Connection |
|---|---|
| Drive Motor IN1 | GPIO 24 |
| Drive Motor IN2 | GPIO 23 |
| Motor Enable / PWM | GPIO 18 |
| Steering Servo | GPIO 25 |
| BNO055 SDA | GPIO 2 |
| BNO055 SCL | GPIO 3 |
| Camera Module 3 | CSI interface |

The wiring was kept as simple as possible to reduce potential failure points.

The motor driver receives motor direction and PWM commands from the Raspberry Pi, while GPIO 25 provides the steering servo control signal.

The BNO055 communicates through the Raspberry Pi's I²C interface.

---

## Bill of Materials

| Component | Quantity | Purpose |
|---|---:|---|
| Raspberry Pi 4 | 1 | Main controller |
| Raspberry Pi Camera Module 3 Wide | 1 | Computer vision |
| BNO055 IMU | 1 | Heading and orientation |
| L298N Motor Driver | 1 | Drive motor control |
| DC Drive Motor | 1 | Propulsion |
| Steering Servo | 1 | Front steering |
| 3S LiPo Battery | 1 | Main power source |
| LEGO Technic Parts | Multiple | Chassis and mechanisms |
| Custom electronics board / mounting | 1 | Electronics integration |
| Wiring and connectors | As required | Electrical connections |

---

## Engineering Decisions

### Why We Chose a Minimal Sensor Configuration

One of our main engineering goals was to avoid adding sensors simply because they were available.

We considered the advantages of additional distance sensors, but adding more hardware would increase:

- Wiring
- Power consumption
- Calibration requirements
- Software complexity
- Mechanical complexity
- Potential failure points

Instead, we focused on making the camera capable of performing multiple perception tasks while using the BNO055 for orientation feedback.

This gave us a simpler system while still providing the information required for autonomous navigation.

---

### Why We Use the Camera as the Main Perception System

The camera provides a large amount of information from a single sensor.

Instead of using separate sensors for walls, coloured obstacles, and parking, the camera can provide visual information for all of these tasks.

During development we tested:

**RGB → BGR → HSV → LAB**

LAB was ultimately selected because it provided the most consistent colour separation during our testing under different lighting conditions.

This made the camera one of the most important parts of our robot architecture.

It also meant that improving our computer vision algorithms could improve several parts of the robot at the same time without adding more hardware.

---

### Why We Use a LEGO Technic Chassis

We chose LEGO Technic as the main structural platform because it gives us a high level of modularity.

During development, we frequently changed:

- Camera mounting
- Steering geometry
- Electronics placement
- Structural supports
- Component positions

LEGO allowed us to make these changes quickly without rebuilding the entire chassis.

The parts are also lightweight, strong enough for our application, and easy to replace or modify during competition preparation.

For us, this was a better option than using a fixed off-the-shelf chassis because the robot changed significantly during development.

---

### Why We Use the White Electronics Cover

During early camera testing, we found that the camera could sometimes detect the electronics, wiring, or coloured components on the electronics platform as part of the track or as an obstacle.

We initially considered solving this entirely through software by changing the detection thresholds. However, changing the thresholds also affected legitimate track and obstacle detection.

We therefore changed the physical environment seen by the camera instead.

A white cover was added above the electronics to create a more visually consistent region and reduce false detections.

This was a good example of using a **mechanical solution to solve a computer-vision problem** instead of adding unnecessary software complexity.

---

## Hardware Reliability

Reliability was considered throughout the hardware design.

The main reliability measures include:

- Rigid camera mounting
- Secure IMU mounting
- Protected electronics
- Wiring kept away from moving parts
- Modular LEGO construction
- Accessible electronics
- Minimal sensor count
- Stable power distribution
- Repeated mechanical and electrical testing

The robot was designed so that components can be accessed and replaced quickly during testing.

Our overall hardware philosophy is:

> **Keep the robot simple, keep the sensing purposeful, and make every component easy to test and maintain.**

---

## Hardware Design Philosophy

The final hardware architecture is the result of repeated testing and iteration.

Rather than building the robot around the maximum possible number of sensors or components, we focused on making each part of the system perform its intended function reliably.

The final architecture therefore combines:

**Mechanical stability + minimal sensing + camera-based perception + IMU feedback + controlled actuation**

This approach keeps the robot compact and allows us to focus our development effort on improving the software and control algorithms that directly affect competition performance.
