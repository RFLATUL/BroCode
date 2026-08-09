# HARDWARE OVERVIEW

Detailed overview of the hardware architecture of our WRO Future Engineers robot.

---

## Table of Contents

- [Overview](#overview)
- [Hardware Overview](#hardware-overview)
  - [Processing Unit](#processing-unit)
  - [Locomotion & Actuators](#locomotion--actuators)
  - [Motor Driver](#motor-driver)
  - [Power Management](#power-management)
  - [Sensors](#sensors)
  - [Camera System](#camera-system)
  - [IMU System](#imu-system)
  - [IR Sensor](#ir-sensor)
  - [Custom Electronics & PCB](#custom-electronics--pcb)
  - [Mechanical Structure](#mechanical-structure)
  - [User Interface](#user-interface)
- [Sensor Placement](#sensor-placement)
- [Dimensions & Physical Layout](#dimensions--physical-layout)
- [Wiring & Raspberry Pi Pin Mapping](#wiring--raspberry-pi-pin-mapping)
- [Bill of Materials](#bill-of-materials)
- [Engineering Decisions](#engineering-decisions)
  - [Why We Chose a Minimal Sensor Configuration](#why-we-chose-a-minimal-sensor-configuration)
  - [Why We Use the Camera as the Main Perception System](#why-we-use-the-camera-as-the-main-perception-system)
  - [Why We Selected the BNO055](#why-we-selected-the-bno055)
  - [Why We Use a LEGO Technic Chassis](#why-we-use-a-lego-technic-chassis)
  - [Why We Use the White Electronics Cover](#why-we-use-the-white-electronics-cover)
- [Hardware–Software Integration](#hardwaresoftware-integration)
- [Hardware Reliability](#hardware-reliability)

---

## Overview

Our robot is designed around **simplicity, reliability, modularity, and controlled performance**.

The hardware integrates:

- **Raspberry Pi 4** as the main processing unit
- **Raspberry Pi Camera Module 3 Wide** as the primary perception system
- **BNO055 IMU** for heading and orientation feedback
- **Rear-mounted IR sensor** for additional parking feedback
- **LEGO Medium Motor** for rear-wheel propulsion
- **Robokits India Ultra Torque servo** for front Ackermann steering
- **TB6612FNG motor driver**
- **3-cell LiPo battery**
- **LEGO Technic-based mechanical structure**
- Custom electronics mounting and organized wiring

Our main hardware philosophy was to use the **minimum practical sensor configuration** and make the camera perform as many perception tasks as possible. This reduces wiring, power consumption, calibration requirements, and potential failure points.

The final hardware is designed to support our autonomous navigation, obstacle handling, lap counting, and parking systems.

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
- Controlling the drive motor through the TB6612FNG.
- Controlling the steering servo.
- Managing the autonomous state machine.

The Raspberry Pi was selected because it provides enough processing capability for real-time computer vision while remaining compact enough for the robot.

---

### Locomotion & Actuators

The robot uses a **four-wheel chassis with rear-wheel drive and front Ackermann steering**.

#### Drive System

A **LEGO Medium Motor** provides propulsion through the rear drivetrain.

The LEGO Medium Motor is controlled electronically through the TB6612FNG motor driver. The drive system was tuned around the balance between:

- Speed
- Torque
- Acceleration
- Controllability
- Power consumption

Our objective was not simply maximum speed. Predictable acceleration and controllable movement are more important because the robot must continuously correct its trajectory while navigating the field.

#### Steering System

The front wheels use an **Ackermann steering arrangement** controlled by a **Robokits India Ultra Torque servo**.

The steering servo is mechanically linked to the front steering mechanism. This allows the inner and outer wheels to follow different turning radii during a corner and provides predictable steering during 90° turns.

The steering system is especially important because the camera-based navigation system continuously changes the steering command according to the detected position of the robot.

---

### Motor Driver

The drive motor is controlled using an **TB6612FNG motor driver**.

The driver provides:

- Motor direction control
- PWM speed control
- Controlled switching between forward and reverse operation

The Raspberry Pi controls the motor driver using three GPIO signals:

- **IN1 → GPIO 24**
- **IN2 → GPIO 23**
- **ENA / PWM → GPIO 18**

GPIO 24 and GPIO 23 determine motor direction, while GPIO 18 provides PWM speed control.

---

### Power Management

The robot uses a **3-cell LiPo battery** as its main power source.

The battery supplies the drivetrain and the regulated electronics required by the Raspberry Pi, camera, IMU, servo, and other onboard components.

Our power strategy focuses on using the available power efficiently rather than adding unnecessary hardware.

The main objectives are:

- Maintain stable power to the Raspberry Pi.
- Provide sufficient current to the drive motor and steering servo.
- Minimize unnecessary sensor power consumption.
- Reduce voltage fluctuations during acceleration and steering.
- Maintain consistent operation throughout a run.

The minimal sensor configuration helps keep the overall power budget manageable.

---

### Sensors

Our final sensing system is intentionally minimal and is built around three main sensing components.

#### Raspberry Pi Camera Module 3 Wide

The camera is the robot's **primary perception system**.

It is used for:

- Wall detection
- Track perception
- Coloured obstacle detection
- Navigation
- Parking-marker detection
- Position estimation

During development, we tested different colour representations including **RGB, BGR, HSV, and LAB**. LAB was ultimately selected because it gave the most consistent colour separation during our testing.

#### BNO055 IMU

The **BNO055** provides orientation and heading feedback.

It is used mainly for:

- Heading stabilization
- Turn consistency
- 90° turn alignment
- Orientation feedback during manoeuvres

The BNO055 communicates with the Raspberry Pi through the I²C interface.

#### Rear IR Sensor

An **IR sensor is mounted at the rear of the robot**.

It provides additional positional feedback during the parking sequence. The camera remains the primary parking perception system, while the rear IR sensor provides an additional reference during the final positioning stage.

---

### Camera System

The robot uses the **Raspberry Pi Camera Module 3 Wide** as its main visual sensor.

The camera is:

- Centrally mounted on the robot.
- Approximately **26 cm above the ground**.
- Tilted approximately **10° downward from horizontal**.

This position gives the camera a consistent field of view while allowing it to see the track, walls, coloured obstacles, and parking area.

The camera is deliberately used for multiple tasks instead of adding separate sensors for every type of detection.

OpenCV processes the camera feed to extract:

- Colour regions
- Wall positions
- Obstacle positions
- Navigation target points
- Parking markers

Keeping the camera fixed is important because changes in height or angle change the image geometry used by the vision algorithms.

---

### IMU System

The **BNO055 IMU** is mounted on the **left side of the robot**.

It communicates with the Raspberry Pi using I²C:

- **SDA → GPIO 2**
- **SCL → GPIO 3**

The IMU provides heading information that complements the camera.

The camera gives the robot information about its position relative to visible features, while the IMU provides orientation information. Together, they improve the consistency of turns and alignment.

---

### IR Sensor

The IR sensor is mounted at the **rear of the robot**.

Its main purpose is to provide additional positional information during parking.

The sensor is not intended to replace the camera. Instead, it provides another reference that can be used during the final parking sequence.

The IR sensor is connected as a GPIO input; the uploaded engineering documentation does not specify its GPIO number, so no pin number is assumed here.

---

### Custom Electronics & PCB

The electronics are mounted on a central platform above the mechanical chassis.

The electronics layout was designed to:

- Keep wiring organized.
- Keep wires away from moving mechanisms.
- Keep components accessible during testing.
- Reduce loose connections.
- Keep the main electronics close to the centre of the robot.
- Simplify troubleshooting.

The central electronics platform contains the Raspberry Pi, motor driver, power electronics, and sensor connections.

Cooling and physical protection are also considered because the Raspberry Pi performs continuous image processing during autonomous operation.

---

### Mechanical Structure

The robot uses a **LEGO Technic-based chassis** with supporting custom structures for the drivetrain, steering, electronics, and camera.

The mechanical design prioritizes:

- Rigidity
- Low weight
- Balanced weight distribution
- Modularity
- Easy repair
- Easy modification
- Predictable steering
- Stable sensor mounting

The LEGO structure allows us to quickly change the position of components during development without rebuilding the complete robot.

The camera support is reinforced to reduce movement and vibration because the camera position directly affects computer-vision performance.

---

### User Interface

Physical buttons are included as part of the robot's control interface for starting, stopping, and resetting the system where required.

The autonomous control itself is handled by the Raspberry Pi once the robot is running.

---

## Sensor Placement

Sensor placement was treated as part of the system design because the physical position of each sensor affects its measurements.

| Component | Placement | Purpose |
|---|---|---|
| Camera Module 3 Wide | Centre, ~26 cm high, 10° downward | Main visual perception |
| BNO055 IMU | Left side of chassis | Heading and orientation |
| IR Sensor | Rear of robot | Parking reference |

The camera and IMU are kept fixed once calibrated so that their measurements remain consistent between tests.

---

## Dimensions & Physical Layout

The robot is arranged around three main physical areas.

### Front

- Ackermann steering mechanism
- Front wheels
- Camera support structure

### Centre

- Raspberry Pi 4
- TB6612FNG motor driver
- Power electronics
- BNO055 IMU
- Main wiring

### Rear

- Rear drivetrain
- Rear wheels
- IR parking sensor
- Battery and supporting connections

The raised camera structure is kept rigid while the main electronics are kept as close to the chassis as practical.

---

## Wiring & Raspberry Pi Pin Mapping

The Raspberry Pi 4 acts as the central controller.

| Component | Raspberry Pi Connection |
|---|---|
| Drive Motor IN1 | **GPIO 24** |
| Drive Motor IN2 | **GPIO 23** |
| Motor Enable / PWM | **GPIO 18** |
| Steering Servo | **GPIO 25** |
| BNO055 SDA | **GPIO 2** |
| BNO055 SCL | **GPIO 3** |
| Camera Module 3 | **CSI interface** |
| Rear IR Sensor | GPIO input |

The Raspberry Pi sends motor direction and PWM commands to the TB6612FNG, while GPIO 25 controls the steering servo.

The BNO055 uses the Raspberry Pi's I²C bus.

The camera connects directly through the CSI interface.

---

## Bill of Materials

| Component | Quantity | Purpose |
|---|---:|---|
| Raspberry Pi 4 | 1 | Main controller |
| Raspberry Pi Camera Module 3 Wide | 1 | Computer vision |
| BNO055 IMU | 1 | Heading and orientation |
| TB6612FNG Motor Driver | 1 | Drive motor control |
| LEGO Medium Motor | 1 | Propulsion |
| Robokits India Ultra Torque Servo | 1 | Front steering |
| Rear IR Sensor | 1 | Parking reference |
| 3S LiPo Battery | 1 | Main power source |
| LEGO Technic Parts | Multiple | Chassis and mechanisms |
| Custom electronics / mounting board | 1 | Electronics integration |
| Wiring and connectors | As required | Electrical connections |
| Physical buttons | As required | Start/stop/reset interface |

---

## Engineering Decisions

### Why We Chose a Minimal Sensor Configuration

One of our main engineering goals was to avoid adding sensors simply because they were available.

We considered additional distance-sensing approaches such as ToF, ultrasonic, and LiDAR, but adding them would increase:

- Wiring
- Power consumption
- Calibration requirements
- Software complexity
- Mechanical complexity
- Potential failure points

Instead, we focused on making the camera capable of performing multiple perception tasks while using the BNO055 for orientation feedback and the rear IR sensor for additional parking information.

This allowed us to keep the robot compact and the power budget under control.

---

### Why We Use the Camera as the Main Perception System

The camera provides a large amount of information from a single sensor.

Instead of using separate sensors for walls, coloured obstacles, and parking, the camera can provide visual information for all of these tasks.

During development we tested:

**RGB → BGR → HSV → LAB**

LAB was ultimately selected because it was the most consistent colour space during our testing.

This became one of the most important engineering decisions in the robot because the camera is responsible for a large part of the robot's autonomous perception.

---

### Why We Selected the BNO055

The BNO055 was selected because the robot requires reliable orientation feedback during turns and alignment.

Unlike using the camera alone, the IMU gives the robot an independent measurement of its heading.

This is particularly useful during controlled 90° turns, where small orientation errors can significantly change the robot's final position.

The BNO055 therefore complements rather than replaces the camera.

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

It is also lightweight, sufficiently rigid for our application, and easy to repair or modify during competition preparation.

---

### Why We Use the White Electronics Cover

During early camera testing, the camera could sometimes interpret the electronics, wiring, or coloured components on the electronics platform as part of the track or as an obstacle.

Instead of solving every false detection through software, we also changed the physical environment seen by the camera.

A white cover was added above the electronics to create a more visually consistent background and reduce false detections.

This is an example of using a **mechanical/hardware change to solve a computer-vision problem**.

---

## Hardware–Software Integration

The Raspberry Pi acts as the central interface between the robot's hardware and software.

The information flow is:

**Camera → OpenCV → Wall / Colour Position**

**BNO055 → Heading → Orientation Correction**

**Vision + IMU → Navigation / Control → Servo + Motor**

The Raspberry Pi receives camera frames through the CSI interface and heading information through I²C.

It then processes this information through the navigation and control algorithms and generates commands for the motor driver and steering servo.

The result is a closed-loop system:

**Sense → Process → Decide → Act → Correct**

The robot continuously senses its environment, processes the information, adjusts its movement, and repeats the process without human intervention.

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

The robot was designed so that components can be accessed quickly during testing and troubleshooting.

Reducing the number of sensors also reduces the number of possible electrical and software failure points.

---

## Hardware Design Philosophy

The final hardware architecture is the result of repeated testing and iteration.

Rather than building the robot around the maximum possible number of sensors and components, we focused on making each selected component perform a clear purpose.

The final architecture therefore combines:

**Mechanical stability + minimal sensing + camera-based perception + IMU feedback + controlled actuation**

This approach keeps the robot compact and allows us to focus our development effort on the software and control algorithms that directly affect competition performance.
