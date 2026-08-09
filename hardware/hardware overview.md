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
- Rear-mounted IR sensing for parking
- DC drive motor with electronic speed and direction control
- Servo-based front Ackermann steering
- L298N motor driver
- 3-cell LiPo battery
- LEGO Technic mechanical structure
- Custom electronics mounting and organized wiring

The main design philosophy was to use the **minimum practical hardware while extracting as much information as possible from the camera and IMU**. This reduces wiring, power consumption, calibration requirements, and potential failure points.

The final system is designed to support the **Open Challenge, Obstacle Challenge, navigation, and parking** requirements.

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

We selected the Raspberry Pi because it provides enough processing capability to perform real-time computer vision while still allowing the robot to remain compact.

---

### Locomotion & Actuation

The robot uses a **four-wheel chassis with rear-wheel drive and front Ackermann steering**.

#### Drive System

A DC drive motor provides propulsion to the rear drivetrain.

The drive system was selected and tuned around the balance between:

- Speed
- Torque
- Acceleration
- Controllability
- Power consumption

Rather than optimizing only for maximum speed, we focused on predictable movement because the robot must maintain control while following the track and navigating obstacles.

#### Steering System

The front wheels use an **Ackermann steering arrangement** controlled by a servo.

The steering servo is mechanically connected to the front steering linkage. This allows the inner and outer front wheels to follow different turning radii during corners.

This was particularly important for our robot because the steering system has to respond accurately to camera-based positional corrections.

---

### Motor Driver

The drive motor is controlled using an **L298N motor driver**.

The motor driver provides:

- Forward and reverse motor control
- PWM speed control
- Electrical isolation between the Raspberry Pi control signals and the motor load

The Raspberry Pi sends direction and PWM commands to the driver, which then controls the drive motor.

The motor direction uses:

- **IN1 → GPIO 24**
- **IN2 → GPIO 23**

Motor speed is controlled using:

- **ENA / PWM → GPIO 18**

---

### Power Management

The robot uses a **3-cell LiPo battery** as its primary power source.

The battery must supply the drive motor, steering servo, Raspberry Pi, camera, IMU, and other electronics.

Our power strategy was based on keeping the system efficient rather than adding unnecessary hardware.

The main goals were:

- Keep the battery sufficiently light.
- Provide enough current during acceleration and turning.
- Maintain stable voltage for the Raspberry Pi.
- Reduce unnecessary sensor power consumption.
- Prevent the drivetrain from compromising the control electronics.

The minimal sensor architecture helps us keep the overall power budget manageable.

---

### Sensors

Our final sensor configuration is intentionally minimal.

#### Raspberry Pi Camera Module 3 Wide

The camera is the robot's main perception system.

It is used for:

- Wall detection
- Track perception
- Coloured obstacle detection
- Navigation
- Parking-marker detection
- Position estimation

We tested multiple colour representations during development, including **RGB, BGR, HSV, and LAB**. LAB was selected for the final colour-detection pipeline because it gave us the most consistent results during testing.

#### BNO055 IMU

The BNO055 provides heading and orientation feedback.

It is mainly used for:

- Heading stabilization
- Turn consistency
- 90° turn alignment
- Orientation feedback during manoeuvres

The IMU is mounted on the **left side of the robot**.

#### Rear IR Sensor

The IR sensor is positioned at the **rear of the robot** and is primarily used as an additional reference during the parking sequence.

The camera remains responsible for the main parking perception while the IR sensor provides additional positional information.

---

### Camera System

The **Raspberry Pi Camera Module 3 Wide** is centrally mounted above the robot.

The camera is positioned approximately:

- **26 cm above the ground**
- **10° downward from horizontal**
- **Centred on the robot**

This mounting arrangement gives the camera a consistent field of view while keeping both the track and important objects visible.

The camera is used as a multi-purpose sensor rather than dedicating separate hardware to each task.

The computer vision pipeline uses OpenCV to process the image and extract:

- Colour regions
- Wall positions
- Obstacle positions
- Target points
- Parking markers

Keeping the camera fixed is important because changes in camera height or angle would change the image geometry used by our algorithms.

---

### Custom Electronics & Wiring

The electronics are mounted on a central platform above the mechanical chassis.

The electronics layout was designed to:

- Keep wiring organized.
- Keep wires away from moving mechanisms.
- Make components accessible during testing.
- Reduce loose connections.
- Keep the main electronics close to the centre of the robot.

The Raspberry Pi, motor driver, IMU connections, power electronics, and supporting wiring are arranged so that individual systems can be isolated during troubleshooting.

A protective white cover is also mounted above the electronics to reduce the chance of the camera interpreting the coloured electronics and wiring as track features or obstacles.

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

The chassis allows us to quickly change component positions during development without rebuilding the entire robot.

The camera support is reinforced so that vibration and movement do not significantly change the camera's position.

---

### Sensor Placement

Sensor placement was treated as part of the overall system design rather than simply attaching sensors wherever space was available.

| Component | Placement | Purpose |
|---|---|---|
| Camera Module 3 Wide | Centre, ~26 cm high, 10° downward | Main visual perception |
| BNO055 IMU | Left side of chassis | Heading and orientation |
| IR sensor | Rear of robot | Parking reference |

Keeping the camera and IMU fixed is especially important because calibration depends on their physical orientation.

---

## Dimensions & Physical Layout

The robot was designed to remain compact while providing enough space for the drivetrain, steering mechanism, electronics, battery, and camera mount.

The final physical layout is organized around three main areas:

**Front**
- Ackermann steering mechanism
- Front wheels
- Camera support structure

**Centre**
- Raspberry Pi
- Motor driver
- Power electronics
- BNO055 IMU
- Main wiring

**Rear**
- Drive system
- Rear wheels
- IR parking sensor
- Battery and supporting connections

Exact competition dimensions are maintained according to the applicable WRO requirements and the final physical configuration.

---

## Wiring & Pin Mapping

The Raspberry Pi 4 is the central controller for the robot.

| Component | Raspberry Pi Connection |
|---|---|
| Drive Motor IN1 | GPIO 24 |
| Drive Motor IN2 | GPIO 23 |
| Motor Enable / PWM | GPIO 18 |
| Steering Servo | GPIO 25 |
| BNO055 SDA | GPIO 2 |
| BNO055 SCL | GPIO 3 |
| Camera Module 3 | CSI interface |
| Rear IR | GPIO input |

The wiring was kept as simple as possible to reduce potential failure points.

The motor driver receives the motor direction and PWM commands from the Raspberry Pi, while the steering servo receives its control signal directly from GPIO 25.

The BNO055 uses the Raspberry Pi's I²C interface.

---

## Bill of Materials

| Component | Quantity | Purpose |
|---|---:|---|
| Raspberry Pi 4 | 1 | Main controller |
| Raspberry Pi Camera Module 3 Wide | 1 | Computer vision |
| BNO055 IMU | 1 | Heading/orientation |
| L298N Motor Driver | 1 | Drive motor control |
| DC Drive Motor | 1 | Propulsion |
| Steering Servo | 1 | Front steering |
| Rear IR Sensor | 1 | Parking reference |
| 3S LiPo Battery | 1 | Main power source |
| LEGO Technic Parts | Multiple | Chassis and mechanisms |
| Custom electronics board / mounting | 1 | Electronics integration |
| Wiring and connectors | As required | Electrical connections |

---

## Engineering Decisions

### Why We Chose a Minimal Sensor Configuration

One of our main engineering goals was to avoid adding sensors simply because they were available.

We considered the advantages of distance sensors such as ToF and ultrasonic sensors, but adding them would increase:

- Wiring
- Power consumption
- Calibration requirements
- Software complexity
- Mechanical complexity
- Potential failure points

Instead, we focused on making the camera capable of performing multiple perception tasks while using the BNO055 for orientation feedback.

This gave us a simpler system while still providing the information required for autonomous operation.

---

### Why We Use the Camera as the Main Perception System

The camera provides a large amount of information from a single sensor.

Instead of using separate sensors for walls, coloured obstacles, and parking, the camera can provide visual information for all of these tasks.

During development we tested:

**RGB → BGR → HSV → LAB**

LAB was ultimately selected because it was the most consistent during our testing under different lighting conditions.

This made the camera one of the most important parts of our robot architecture.

---

### Why We Use a LEGO Technic Chassis

We chose LEGO Technic as the main structural platform because it gives us a high level of modularity.

During development, we frequently changed:

- Sensor positions
- Camera mounting
- Steering geometry
- Electronics placement
- Structural supports

LEGO allowed us to make these changes quickly without rebuilding the entire chassis.

The parts are also lightweight, strong enough for our application, and easy to replace during competition preparation.

---

### Why We Use the White Electronics Cover

During early camera testing, we found that the camera could sometimes detect the electronics, wiring, or coloured components on the electronics platform as part of the track or as an obstacle.

Instead of trying to solve every false detection through software, we also changed the physical environment seen by the camera.

A white cover was added above the electronics to create a visually consistent background and reduce false detections.

This is an example of a hardware change being used to solve a software/computer-vision problem.

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

