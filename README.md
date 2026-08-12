# BroCode

This repository contains the engineering documentation, software, hardware design, testing process, and development history of our autonomous robot for the **WRO Future Engineers 2026** category.

Our robot was developed with a focus on autonomous navigation, computer vision, mechanical stability, controlled steering, obstacle management, parking, reliability, and repeatable performance.

The purpose of this repository is not only to show the final robot, but also to document **why** we made our major engineering decisions, what alternatives we considered, what problems we encountered, how we tested them, and how the design evolved.

Our development process follows:

**Design → Build → Test → Identify Problem → Analyse → Modify → Retest**

## Engineering Evidence Map

This repository is organised around the complete engineering cycle rather than only the final robot. A judge can follow the project from **requirements → design → hardware → sensing → software → testing → iteration → final validation → reproducibility**.

The documentation deliberately separates:
- **What the robot does**
- **Why each major design choice was made**
- **What was tested**
- **What changed after testing**
- **How the final system can be understood and reproduced**

Where numerical test data has not been formally recorded, the repository does not present invented measurements as experimental results. Recorded performance figures are identified explicitly.



| <br>Front view | <br>Side view | <br>Top view | <br>Rear view |
| -------------- | ------------- | ------------ | ------------- |

---

# Table of Contents

## 1. Project & Team

- [Engineering Evidence Map](#engineering-evidence-map)

- [Team](https://github.com/RFLATUL/BroCode#team)
- [Project Overview](https://github.com/RFLATUL/BroCode#project-overview)
- [Engineering Objectives](https://github.com/RFLATUL/BroCode#engineering-objectives)
- [Overall Robot Architecture](https://github.com/RFLATUL/BroCode#overall-robot-architecture)

## 2. Mobility & Mechanical Design

- [Mobility & Mechanical Design](https://github.com/RFLATUL/BroCode#mobility--mechanical-design)
- [Mobility and Drive System](https://github.com/RFLATUL/BroCode#mobility-and-drive-system)
- [Steering System](https://github.com/RFLATUL/BroCode#steering-system)
- [Mechanical Design Decisions](https://github.com/RFLATUL/BroCode#mechanical-design-decisions)
- [Why We Chose LEGO](https://github.com/RFLATUL/BroCode#why-we-chose-lego)
- [Mechanical Testing](https://github.com/RFLATUL/BroCode#mechanical-testing)

## 3. Power & Sensor Architecture

- [Power & Sensor Architecture](https://github.com/RFLATUL/BroCode#power--sensor-architecture)
- [Power Budget and Distribution](https://github.com/RFLATUL/BroCode#power-budget-and-distribution)
- [Sensor Architecture](https://github.com/RFLATUL/BroCode#sensor-architecture)
- [Sensor Selection and Trade-offs](https://github.com/RFLATUL/BroCode#sensor-selection-and-trade-offs)
- [Sensor Placement](https://github.com/RFLATUL/BroCode#sensor-placement)
- [Camera Calibration](https://github.com/RFLATUL/BroCode#camera-calibration)
- [IMU Calibration](https://github.com/RFLATUL/BroCode#imu-calibration)
- [Sensor Testing and Reliability](https://github.com/RFLATUL/BroCode#sensor-testing-and-reliability)

## 4. Software Architecture & Obstacle Strategy

- [Software Architecture & Obstacle Strategy](https://github.com/RFLATUL/BroCode#software-architecture--obstacle-strategy)
- [Software Modules](https://github.com/RFLATUL/BroCode#software-modules)
- [Master State Machine](https://github.com/RFLATUL/BroCode#master-state-machine)
- [Computer Vision](https://github.com/RFLATUL/BroCode#computer-vision)
- [Colour Detection](https://github.com/RFLATUL/BroCode#colour-detection)
- [Wall and Lane Following](https://github.com/RFLATUL/BroCode#wall-and-lane-following)
- [Steering and Speed Control](https://github.com/RFLATUL/BroCode#steering-and-speed-control)
- [Lap Counting and Debouncing](https://github.com/RFLATUL/BroCode#lap-counting-and-debouncing)
- [Obstacle Detection and Strategy](https://github.com/RFLATUL/BroCode#obstacle-detection-and-strategy)
- [Red / Green Obstacle Recognition](https://github.com/RFLATUL/BroCode#red--green-obstacle-recognition)
- [Obstacle-Side Decision Logic](https://github.com/RFLATUL/BroCode#obstacle-side-decision-logic)
- [Obstacle Avoidance and Recovery](https://github.com/RFLATUL/BroCode#obstacle-avoidance-and-recovery)
- [Open Challenge Strategy](https://github.com/RFLATUL/BroCode#open-challenge-strategy)
- [Parking Strategy](https://github.com/RFLATUL/BroCode#parking-strategy)
- [IMU-Based Parking Alignment](https://github.com/RFLATUL/BroCode#imu-based-parking-alignment)
- [Edge Cases and Failure Handling](https://github.com/RFLATUL/BroCode#edge-cases-and-failure-handling)

## 5. Testing, Systems Thinking & Engineering Decisions

- [Testing, Validation & Tuning](https://github.com/RFLATUL/BroCode#testing-validation--tuning)
- [Testing Methodology](https://github.com/RFLATUL/BroCode#testing-methodology)
- [Testing Metrics](https://github.com/RFLATUL/BroCode#testing-metrics)
- [Colour Threshold Testing](https://github.com/RFLATUL/BroCode#colour-threshold-testing)
- [Steering Parameter Tuning](https://github.com/RFLATUL/BroCode#steering-parameter-tuning)
- [Obstacle Detection Testing](https://github.com/RFLATUL/BroCode#obstacle-detection-testing)
- [Lap Counting Testing](https://github.com/RFLATUL/BroCode#lap-counting-testing)
- [Parking Testing](https://github.com/RFLATUL/BroCode#parking-testing)
- [Software Iterations](https://github.com/RFLATUL/BroCode#software-iterations)
- [Systems Thinking & Engineering Decisions](https://github.com/RFLATUL/BroCode#systems-thinking--engineering-decisions)
- [Engineering Constraints](https://github.com/RFLATUL/BroCode#engineering-constraints)
- [Engineering Trade-offs](https://github.com/RFLATUL/BroCode#engineering-trade-offs)
- [Design Evolution](https://github.com/RFLATUL/BroCode#design-evolution)
- [Problems → Solutions → Results](https://github.com/RFLATUL/BroCode#problems--solutions--results)
- [Risk and Failure Analysis](https://github.com/RFLATUL/BroCode#risk-and-failure-analysis)
- [Risk Mitigation](https://github.com/RFLATUL/BroCode#risk-mitigation)
- [Evidence-Based Engineering Decisions](https://github.com/RFLATUL/BroCode#evidence-based-engineering-decisions)

## 6. Reproducibility & GitHub Quality

- [Final System Architecture](https://github.com/RFLATUL/BroCode#final-system-architecture)
- [Final Hardware Specifications](https://github.com/RFLATUL/BroCode#final-hardware-specifications)
- [Bill of Materials](https://github.com/RFLATUL/BroCode#bill-of-materials)
- [Reproducibility & GitHub Quality](https://github.com/RFLATUL/BroCode#reproducibility--github-quality)
- [Software Setup](https://github.com/RFLATUL/BroCode#software-setup)
- [Version Control](https://github.com/RFLATUL/BroCode#version-control)
- [Testing Workflow](https://github.com/RFLATUL/BroCode#testing-workflow)
- [Final Performance Validation](https://github.com/RFLATUL/BroCode#final-performance-validation)
- [Final Robot](https://github.com/RFLATUL/BroCode#final-robot)
- [Engineering Philosophy](https://github.com/RFLATUL/BroCode#engineering-philosophy)
- [Conclusion](https://github.com/RFLATUL/BroCode#conclusion)

---

# Team

## BroCode

### 1. Tanish Kothari --- Software

Primary responsibilities:



### 2. Vihaan Kothari --- Hardware

Primary responsibilities:



Both members contributed to the overall robot strategy, testing, debugging, design decisions, system integration, and development of the final robot.

---

# Project Overview

The WRO Future Engineers challenge requires the robot to navigate the track autonomously while responding to changing conditions.

The **Open Challenge** requires the robot to navigate changing internal wall configurations. The **Obstacle Challenge** additionally requires the robot to recognise red and green obstacles, obey the required side of the track, and complete the parking task.

Because the environment is not completely fixed, our robot was designed around closed-loop control rather than a sequence of pre-programmed movements.

The robot continuously obtains information from its sensors, processes that information, makes a navigation decision, and changes its movement accordingly.

The overall control loop is:



This allows the robot to respond to the actual state of the track instead of replaying a predetermined route.

---

# Engineering Objectives

Our main engineering objectives were:



---

# Overall Robot Architecture

The robot is divided into five closely connected subsystems:



The systems are not independent. Camera position affects the field of view available to the software, steering geometry affects the relationship between a software command and vehicle movement, and motor selection affects the speed and acceleration that the control system can safely use.

This interaction between subsystems was considered throughout development.

---

# Mobility & Mechanical Design

The robot uses a hybrid structure made from **LEGO Technic components and custom 3D-printed parts**.

The LEGO structure was selected because it allowed the team to rapidly change the chassis geometry during development. Components could be moved, reinforced, or replaced without rebuilding the complete robot.

Custom 3D-printed components were used where standard LEGO geometry did not provide the required solution. These included motor mounting and housing components, camera mounting and protection, and other custom structural parts.

The mechanical design was based on five requirements:

- **Rigidity:** prevent chassis movement from changing steering or camera geometry.
- **Compactness:** remain small and manoeuvrable within competition constraints.
- **Modularity:** allow components to be modified and repaired quickly.
- **Accessibility:** keep electronics and mechanical components easy to reach.
- **Stability:** distribute the battery and major electronics to keep the centre of mass controlled.

The approximate base footprint is **22 cm × 12 cm**. The camera is mounted approximately **26 cm above the floor**, with its optical axis angled approximately **10° downward from horizontal**.

The stated robot mass during development was approximately **800 g**.

The mechanical system was treated as part of the control system: changes in chassis rigidity, motor behaviour, steering geometry, and camera position directly affect the performance of the vision and navigation software.

# Mobility and Drive System

The robot uses a **LEGO Medium Motor** for propulsion.

The LEGO Medium Motor was selected because it integrates directly with the LEGO Technic drivetrain while providing sufficient speed and torque for the robot's intended operating range.

The main specifications considered were:

- **Operating voltage:** approximately 9 V
- **No-load speed:** approximately 250 RPM
- **Torque:** approximately 815 g·cm
- **Encoder resolution:** approximately 1°
- **Primary role:** rear-wheel propulsion

The encoder also provides the possibility of using rotational feedback for more accurate movement and turning control.

The motor-selection requirement was not to maximise a single specification. The team instead considered **speed, torque, mass, integration, controllability, and mechanical compatibility** together.

![Engineering flowchart 3](assets/03_torque.svg)

The final LEGO Medium Motor configuration provided the most practical balance for the robot's compact LEGO-based drivetrain.

# Steering System

Steering is provided by the **RoboKits India UltraTorque Servo**, mounted securely on the front of the robot. The servo was selected for its high torque and precise angular control, allowing the robot to make fast and accurate steering corrections.

The main servo specifications used during selection were:

- **Operating voltage:** 7.2–8.4 V
- **Operating speed:** 0.13 sec/60° at 7.2 V; 0.10 sec/60° at 8.4 V
- **No-load current:** 250 mA at 7.2 V; 300 mA at 8.4 V
- **Stall torque:** 21 kg·cm at 7.2 V; 25 kg·cm at 8.4 V
- **Stall current:** 3.2 A at 7.2 V; 3.5 A at 8.4 V
- **Idle current:** 4 mA at 7.2 V; 5 mA at 8.4 V

Mechanical play was treated as an important source of error. If the linkage or servo mounting moves under load, the same software command can produce different physical steering angles.

The steering loop is:

![Engineering flowchart 4](assets/04_steering_loop.svg)

Mechanical geometry and software parameters were tuned together because changing the steering geometry changes the relationship between servo angle and vehicle motion.

# Mechanical Design Decisions

## Motor Selection

We considered several motor options during development.

### N20 DC Motor

The N20 was attractive because of its compact size and low weight, but it did not provide enough torque for the final robot under load.

### REV NEO 550

The NEO 550 offered much higher power, but it introduced additional size, weight, and control hardware that were unnecessary for the final robot.

### LEGO Medium Motor

The LEGO Medium Motor provided the strongest overall match to the team's mechanical constraints because it integrated directly with the LEGO Technic chassis and provided sufficient propulsion performance without adding unnecessary mechanical or electrical complexity.

### Final Choice: LEGO Medium Motor

The final decision was based on the complete drivetrain requirement rather than the highest advertised RPM or torque. The relevant trade-offs were **speed, torque, weight, integration, reliability, and ease of modification**.

The decision chain was:

**Requirement → Alternatives → Physical integration and testing → Trade-off → Final selection**

# Why We Chose LEGO

The LEGO chassis was designed from scratch for our robot.

We selected LEGO because it provided:



During development, being able to change the chassis quickly was more valuable to us than using a completely fixed custom frame.

This allowed us to test different motor, camera, sensor, and structural configurations without rebuilding the complete robot.

---

# Mechanical Testing

Mechanical testing was performed after major changes to the drivetrain, chassis, and steering system.

We evaluated:



When inconsistent behaviour appeared, we first checked for a mechanical cause before changing software parameters.

This prevented software tuning from being used to hide mechanical instability.

---

# Power & Sensor Architecture

| <br>7.4 V rechargeable battery | <br>5 V buck converter | <br>Custom electronics board |
| ------------------------------ | ---------------------- | ---------------------------- |

The robot uses a **7.4 V, 1500 mAh Li-ion rechargeable battery pack**.

The battery feeds the power distribution system, which provides the appropriate supply to the motor system and regulated electronics.

The main architecture is:



The Raspberry Pi requires a stable regulated supply because voltage drops can cause instability or unexpected resets.

The motor power path and regulated electronics path were therefore treated separately.

---

# Power Budget and Distribution

The robot's power architecture was designed around a **7.4 V, 1500 mAh rechargeable Li-ion battery pack** and regulated low-voltage electronics.

![5 V buck converter and custom electronics](assets/component_buck.png)
![Custom electronics board](assets/component_pcb.png)

The main loads are the Raspberry Pi, camera, BNO055 IMU, IR sensors, steering servo, motor driver, and drive motor.

![Power distribution table](assets/table_power.svg)

The drive motor is expected to be the dominant variable load, especially during acceleration and steering. The Raspberry Pi and camera form the main continuous electronics load.

The main risks considered were:

![Power risks](assets/power_risks.svg)

- Battery voltage drop
- Motor current spikes
- Raspberry Pi brownouts
- Electrical noise
- Loose connections
- Insufficient regulator capacity

The power system was tested with the motor operating because stability at idle alone would not demonstrate competition readiness.

**Important engineering constraint:** the team treats the battery and regulator selection as a system-level decision. Increasing motor demand affects battery loading, voltage regulation, processor stability, and therefore the reliability of perception and control.

# Sensor Architecture

| <br>Raspberry Pi Camera Module 3 Wide | <br>BNO055 IMU | <br>IR sensors | <br>VEX limit switches |
| ------------------------------------- | -------------- | -------------- | ---------------------- |



The robot uses multiple sensors because no single sensor provides reliable information for every part of the challenge.

The main sensing systems are:



Each sensor has a defined role.



The camera is the primary perception sensor. The IMU provides orientation information, while the IR sensors provide close-range feedback where visual positioning becomes less reliable.

---

# Sensor Selection and Trade-offs

## Camera



The camera provides substantially more environmental information than a single distance sensor.

It can be used for:



Its main limitation is sensitivity to lighting, exposure, and colour thresholds.

## BNO055 IMU



The BNO055 provides orientation information using internal sensor fusion.

It is useful for:



Its readings can still be affected by calibration and the robot's mounting environment.

## IR Sensors



IR sensors are simple and fast for short-range detection.

They are particularly useful during parking when the robot is close to the parking boundary.

Their limitation is that they provide much less environmental information than the camera.

## Limit Switches



Limit switches provide simple physical feedback and an additional fail-safe if the robot unexpectedly interacts with an object.

---

# Sensor Placement

<img src="assets/sensor_placement.png" alt="Sensor placement on robot" width="850">

Sensor placement was based on the geometry of the task rather than simply available space.

### Camera

The camera is mounted at the front, centred on the robot, approximately **26 cm above the floor**, and pointed approximately **10° downward from horizontal**.

![Camera mount geometry](assets/camera_mount_specs.svg)

The **10° angle was calculated using trigonometry**. The team measured the camera height above the ground and the maximum useful detection distance, then used the tangent relationship to determine the downward angle required to keep the relevant track surface within the camera's field of view.

During early testing, vibration caused small movements in the image. The camera support was subsequently reinforced with additional LEGO Technic beams so that the camera geometry remained consistent during operation.

The centred mounting keeps the camera coordinate system aligned with the robot's centreline.

### BNO055

The BNO055 is mounted securely on the **left side of the robot**. Its position is kept fixed so that the sensor coordinate frame remains consistent after calibration.

### IR Sensors

The IR sensors are placed toward the **rear of the robot** and are primarily used for close-range parking detection and alignment.

### Limit Switches

The limit switches are positioned so that unexpected physical interaction can be detected and used as a fail-safe condition.

# Camera Calibration

Camera calibration and colour testing were performed using images captured from the actual robot and track.

We initially tested RGB/BGR-based colour detection. We found that these approaches were sensitive to changes in lighting and exposure.

We then tested HSV because it separates hue from brightness.

Finally, we tested LAB colour space and selected it for the colour-detection approach that was most consistent during our testing.

The general processing pipeline is:



Thresholds were tuned using real camera data instead of relying only on theoretical colour values.

This was one of the most important parts of our development because camera reliability affects navigation, obstacle recognition, and parking.

---

# IMU Calibration

The BNO055 is calibrated before navigation testing.

The robot is kept stationary during the initial calibration process so that a stable reference can be established.

The IMU is then tested by rotating the robot manually and checking whether the reported heading changes consistently with the physical movement.

Calibration is important because incorrect orientation information can cause the robot to steer in the wrong direction or over-correct during turns.

The IMU is therefore used as a feedback source and is not treated as a replacement for visual information.

---

# Sensor Testing and Reliability

Sensor testing was performed independently before full-system testing.

![Sensor testing](assets/sensor_tests.svg)

### Camera
The camera was tested for colour separation, false detections, lighting variation, detection distance, region-of-interest behaviour, and consistency of detected positions.

### BNO055
The IMU was tested for heading consistency, stationary behaviour, response during turns, and repeatability after restarting.

### IR Sensors
The IR sensors were tested for short-range response, detection consistency, parking alignment, and false readings.

### Limit Switches
The limit switches were tested for physical activation, electrical response, software response, and recovery behaviour.

Testing sensors independently allowed the team to identify whether a failure originated from sensing, software, or the physical system before performing integrated autonomous tests.

The design uses complementary sensing rather than depending on one measurement:
**camera → environment**, **IMU → orientation**, **IR → close-range alignment**, **limit switches → fail-safe contact detection**.

# Software Architecture & Obstacle Strategy

The robot software is modular rather than being one large program.

The main software layers are:

![Software architecture](assets/07_software_arch.svg)

The main functional modules are:

![Software module structure](assets/08_software_structure.svg)

This structure makes it possible to test and modify individual systems without rewriting the complete program.

The architecture follows a closed-loop principle:

**Perception → State estimation → Decision → Control → Actuation → New sensor data**

This separation also reduces the risk that a change to one function will unintentionally change unrelated behaviour.

# Software Modules

The intended software organisation is:



Each module has a defined responsibility, making debugging and future changes easier.

---

# Master State Machine

The master state machine provides the overall structure of the robot's behaviour.

![Engineering flowchart 9](assets/09_master_fsm.svg)

The state machine separates normal driving, obstacle handling, recovery, lap completion, parking, and stopping into distinct behaviours.

This prevents unrelated behaviours from interfering with one another. For example, parking logic should not activate while the robot is still completing its laps.

The state machine also provides defined places for recovery behaviour when perception becomes temporarily unreliable.

# Computer Vision



Computer vision is one of the main parts of our robot.

The Raspberry Pi Camera Module 3 Wide provides the visual input and OpenCV is used to process the images.

The main vision tasks are:



Regions of interest are used where appropriate to reduce unnecessary processing and focus the algorithm on areas relevant to navigation.

---

# Colour Detection

We tested multiple colour representations during development.

RGB/BGR thresholding was investigated first, but colour classification became inconsistent under changes in lighting and exposure.

HSV was then tested because it separates hue from brightness.

LAB was ultimately selected for the colour-detection approach that gave the most consistent results during our testing.

The process is:



The detected colour region is then converted into information that can be used by the navigation system.

---

# Wall and Lane Following

The robot continuously estimates the position of relevant track boundaries using the camera.

A target position is generated from the detected wall or lane geometry.

The difference between the target position and the detected position becomes the steering error.



The controller converts this error into a steering command.

This allows the robot to continuously correct its path rather than relying on fixed steering angles.

---

# Steering and Speed Control

The steering system uses feedback.

If the robot is far from the desired path, the controller increases the steering correction.

If the robot is close to the desired path, the correction becomes smaller.

The basic proportional relationship is:



A proportional controller was selected because our primary requirement was fast, predictable correction.

Too little correction caused drift, while too much correction caused oscillation.

Steering parameters were therefore tuned experimentally.

Speed is also coordinated with steering. Higher speed can be used when the robot is stable and the path is clear, while sharp turns or uncertain perception can justify reducing speed.

The objective is not maximum motor speed; it is the highest speed that remains reliably controllable.

---

# Lap Counting and Debouncing

Lap counting is handled in software using visual markers and a debounce condition.

Without debouncing, the same marker could be detected in multiple consecutive camera frames and incorrectly increase the lap count several times.

The logic is:



This prevents a single physical marker from producing multiple lap counts.

---

# Obstacle Detection and Strategy

In the Obstacle Challenge, the robot identifies coloured obstacles using computer vision.

The two relevant colours represent different side-obedience requirements.

The obstacle pipeline is:

![Engineering flowchart 14](assets/14_obstacle_pipeline.svg)

The robot uses the detected obstacle colour as an input to the navigation decision rather than treating colour detection as an isolated vision feature.

The strategy therefore connects three stages:

**Recognition → Required side → Safe path / recovery**

This separation makes it possible to test perception and navigation independently.

# Red / Green Obstacle Recognition

The software uses separate colour masks to distinguish the two obstacle colours.

The detected obstacle is classified according to its colour, and that classification affects the required path.

The exact side decision is implemented in the obstacle strategy module so that recognition and navigation remain separate software functions.

---

# Obstacle-Side Decision Logic

The robot considers obstacle colour together with the current driving state and visible track geometry.

The decision process is:



This allows the robot to respond to obstacle position rather than relying on fixed obstacle coordinates.

---

# Obstacle Avoidance and Recovery

Obstacle avoidance is divided into three stages.

### 1. Approach

The robot detects the obstacle and prepares for the required path change.

### 2. Pass

The robot moves around the obstacle while maintaining clearance.

### 3. Recover

After passing the obstacle, the robot gradually returns toward the normal path.

Gradual recovery is important because an immediate large steering correction can cause oscillation or overshoot.

If the obstacle temporarily disappears from the camera after being detected, the robot retains the current avoidance state for a short period rather than immediately returning to normal navigation.

This prevents one missed frame from producing an incorrect path change.

---

# Open Challenge Strategy

The Open Challenge can contain different internal wall configurations.

Our robot therefore does not depend on fixed coordinates for wall positions.

Instead, it continuously detects visible wall geometry and adjusts its path.



This allows the navigation system to adapt to different track layouts.

---

# Parking Strategy

Parking was one of the most difficult parts of the design because the robot must transition from high-confidence lap navigation into a controlled final alignment.

The parking development approach combines:

![Parking inputs](assets/parking_inputs.svg)

The intended sequence is:

![Engineering flowchart 17](assets/17_parking_strategy.svg)

The camera provides the main environmental information while the IMU and IR sensors provide additional feedback during the final alignment stage.

The team also plans to use a **rear-facing camera** as an additional visual source for parking detection. Its purpose is to improve the robot's awareness of the parking area while reversing and provide another reference for final alignment.

# IMU-Based Parking Alignment

The BNO055 is used to estimate the robot's orientation during parking.

The robot compares its current heading with the desired parking orientation.

The heading error is then used to determine whether an additional steering correction is required.

This is useful because camera-only alignment can become less reliable when the robot is very close to the parking boundaries.

The IMU therefore provides an independent orientation reference during the final manoeuvre.

---

# Edge Cases and Failure Handling

We considered situations where the normal navigation assumptions can fail.

### Camera temporarily loses the wall

The robot retains the previous valid steering information and avoids making an extreme correction from a single bad frame.

### False colour detection

Colour detections are filtered using thresholding and region checks instead of accepting every coloured pixel.

### Multiple obstacle detections

The system evaluates relevant detected obstacle regions rather than treating every coloured region as a separate obstacle.

### Sensor noise

Sensor readings are interpreted over time rather than relying on one isolated measurement.

### Excessive steering

Steering output is limited so that one erroneous measurement cannot produce an extreme command.

### Robot becomes misaligned

The recovery state reduces aggressive movement and attempts to return to a stable visual path.

### Limit switch activation

A physical limit switch can provide an additional indication of unexpected physical interaction.

---

# Testing, Validation & Tuning

Testing was treated as an engineering process rather than a final verification step.

Our development cycle was:

![Engineering flowchart 18](assets/18_test_cycle.svg)

The core rule was to change one major variable at a time wherever practical. This made it easier to determine whether a change actually improved the robot.

The testing cycle therefore followed:

**Problem → Hypothesis → Controlled change → Test → Compare → Keep / Revert → Document**

# Testing Methodology

Testing was divided into:



### Full-System Testing

The complete robot was tested with all systems operating simultaneously because success of individual subsystems does not guarantee success of the complete system.

---

# Testing Metrics

We used measurable categories to evaluate changes rather than judging improvements only by appearance.

The main performance metrics were:

![Testing metrics](assets/performance_metrics.svg)

These included:

- Lap completion rate
- Lap time
- Obstacle-avoidance success
- Obstacle contacts
- Parking success
- Steering stability
- Recovery events
- False obstacle detections
- Incorrect lap counts
- Electrical stability during continuous operation

For software tuning, we looked particularly at the trade-off between:

![Engineering flowchart 19](assets/19_response_tradeoff.svg)

A parameter was not considered better simply because it increased speed. The objective was to improve speed while maintaining reliable completion.

# Colour Threshold Testing

Colour thresholds were tested using actual camera frames captured from the robot.

The process was:



This reduced the chance that the robot would depend on one ideal lighting condition.

---

# Steering Parameter Tuning

Steering parameters were tuned through repeated driving tests.

The main failure modes were:

### Too little correction

The robot slowly drifted away from the desired path.

### Too much correction

The robot oscillated from side to side.

### Excessive steering at high speed

The robot could over-correct before the next useful camera update.

The final approach was therefore to balance steering gain with robot speed.

---

# Obstacle Detection Testing

Obstacle testing was performed by changing:



The objective was to verify that the software did not simply recognise the colour but actually used it to make the correct navigation decision.

---

# Lap Counting Testing

Lap counting was tested specifically for repeated detections.

A marker visible across several frames should still count as only one lap event.

The debounce logic was therefore tested by:



The final system accepts a new lap only after the previous detection has cleared.

---

# Parking Testing

Parking was tested separately from normal driving.

The main parameters considered were:



The parking algorithm was adjusted through repeated attempts rather than relying on one successful run.

The objective was to determine which combination of camera information, IMU heading, and IR feedback produced the most repeatable final alignment.

---

# Software Iterations

The software evolved through multiple iterations.

The important principle was that changes were made in response to observed behaviour.

A simplified development sequence was:



Each stage added functionality while preserving previously working behaviour.

---

# Systems Thinking & Engineering Decisions

We treated the robot as one integrated system rather than as separate mechanical, electrical, sensor, and software projects.

For example:



Similarly:



A change in one subsystem can therefore affect another subsystem.

This interaction was considered when making design decisions.

---

# Engineering Constraints

The major constraints we worked under were:



Instead of optimising one subsystem independently, we looked for solutions that worked within the complete system.

---

# Engineering Trade-offs

## Speed vs Stability

A faster robot can produce a better lap time, but higher speed reduces the time available for steering correction.

We therefore prioritised controllable speed over maximum possible speed.

## Motor Performance vs Integration

The LEGO Medium Motor was not selected simply because it was the most powerful option considered. It provided a practical balance between propulsion performance, weight, direct LEGO integration, and ease of modification.

## Camera Information vs Processing

A wider camera view provides more environmental information but also increases the amount of image that must be processed.

The camera was positioned and processed using relevant regions of interest to keep the system practical.

## LEGO Modularity vs Custom Construction

A fully custom chassis could provide more fixed geometry, but LEGO allowed the team to change the robot much faster during development.

We therefore used LEGO for the main structure and 3D printing where custom geometry was necessary.

## Sensor Quantity vs Complexity

Adding more sensors can provide more redundancy, but it also increases wiring, processing, and possible failure points.

We therefore gave each sensor a specific purpose rather than adding sensors without a defined role.

# Design Evolution

The robot was developed through repeated changes rather than as one final design.

### Early Design

The initial objective was to create a vehicle capable of moving and steering.

### Intermediate Design

Driving tests were used to identify issues with:

![Intermediate design issues](assets/design_problems.svg)

### Improved Design

The team introduced targeted changes based on observed failures:

![Improved design features](assets/design_improvements.svg)

### Final Design

The final system combines:

![Final design](assets/final_design.svg)

![Final system components](assets/final_system.svg)

The key engineering principle was that each iteration was intended to solve an observed problem rather than add complexity without a defined purpose.

# Problems → Solutions → Results



---

# Why We Used a White Electronics Cover

During camera testing, the camera could sometimes see the colours and components of the electronics.

This created false visual information.

The problem was particularly important because our software relies on colour and object detection.

We therefore added a white cover over the electronics area.

The cover reduced unwanted visual features and made the camera view more consistent.

This was an example of a mechanical change solving a software perception problem.

---

# Risk and Failure Analysis

We considered the following major failure modes:

![Risk and failure analysis](assets/table_risk.svg)

| Risk | Potential effect | Mitigation |
|---|---|---|
| Camera temporarily loses wall | Incorrect steering | Retain previous valid information and use recovery behaviour |
| False colour detection | Wrong navigation decision | Thresholding, region checks and filtering |
| Motor current spike / voltage drop | Pi instability or reset | Regulated electronics supply and organised power distribution |
| Mechanical vibration | Unstable camera or steering geometry | Reinforced mounts and rigid chassis |
| Steering oscillation | Loss of lane stability | Steering limits and parameter tuning |
| Repeated lap detection | Incorrect lap count | Debouncing |
| Sensor failure/noise | Missing or incorrect feedback | Complementary sensing and recovery logic |
| Robot becomes misaligned | Loss of normal path | Recovery state and controlled correction |

For example, camera failure cannot always be prevented, so the software avoids making an extreme decision based on one bad frame.

Mechanical movement is reduced through stronger mounting, while software tuning is performed only after the mechanical system is stable.

This prevents software parameters from being used to hide mechanical problems.

# Final System Architecture



This architecture separates perception, decision-making, and actuation while maintaining feedback between them.

---

# Final Hardware Specifications

![Final hardware specifications](assets/table_specs.svg)

The final system uses:

- **Controller:** Raspberry Pi 4B, 4 GB
- **Drive motor:** LEGO Medium Motor
- **Steering:** RoboKits India UltraTorque Servo
- **Motor driver:** TB6612FNG
- **Camera:** Raspberry Pi Camera Module 3 Wide
- **IMU:** BNO055
- **IR sensors:** 4
- **Limit switches:** 2
- **Battery:** 7.4 V, 1500 mAh rechargeable Li-ion
- **Regulation:** 5 V, 3 A buck converter
- **Chassis:** LEGO Technic + custom 3D-printed components
- **Approximate weight:** 800 g during development
- **Approximate base footprint:** 22 × 12 cm
- **Camera height:** approximately 26 cm
- **Camera angle:** approximately 10° downward from horizontal

# Reproducibility & GitHub Quality

A second team should be able to understand and reproduce the robot using the documentation provided in this repository.

The documentation covers:

![Reproducibility checklist](assets/reproducibility.svg)

- Hardware architecture
- Bill of materials
- CAD and custom mechanical parts
- LEGO assembly information
- Wiring and pin mapping
- Sensor placement
- Sensor calibration
- Software architecture
- Software modules
- Testing workflow
- Engineering decisions

The mechanical documentation explains how the chassis and custom components fit together.

The electrical documentation explains how the battery, regulators, motor driver, controller, and sensors are connected.

The software documentation explains how those electrical components are controlled by the program.

The exact GPIO and interface mapping should be maintained in the dedicated wiring and pin-mapping documentation so that hardware changes do not require rewriting the main README.

The repository is intended to be navigable in the following order:

**Final Robot → System Architecture → Mechanical → Electronics → Sensors → Software → Obstacle Strategy → Testing → Design Evolution → Engineering Decisions → Reproducibility**

This keeps the judge journey focused on engineering evidence rather than only presentation.

# Software Setup

The software is intended to run on the Raspberry Pi.

The basic setup process is:

![Engineering flowchart 25](assets/25_setup.svg)

The software is divided into modules so that individual components can be tested before running the complete autonomous program.

A reproducible setup should verify the hardware first, then sensor communication, then camera processing, and finally the complete autonomous program. This reduces the chance of diagnosing a system-level problem as a software-only problem.

# Version Control

GitHub is used as part of the engineering process rather than only as a location for the final code.

Significant development changes should be recorded through meaningful commits.

Examples of useful commit messages include:

![Version control workflow](assets/26_commits.svg)

A useful commit should communicate what changed and, where relevant, why it changed.

This allows the repository to show the engineering process instead of only presenting a final code dump.

The intended engineering history is:

**Initial architecture → Hardware prototype → Sensor integration → Vision development → Steering development → Obstacle logic → Parking → Testing and tuning → Final documentation**

For submission, the repository's actual Git history should be retained so that the engineering progression can be verified rather than inferred from the README alone.

# Testing Workflow

Our standard testing workflow is:

![Testing workflow](assets/27_testing_workflow.svg)

The workflow is:

**Define problem → Create test → Run baseline → Record behaviour → Identify likely cause → Change relevant subsystem → Repeat same test → Compare → Keep/revert → Document**

This prevents random tuning and makes engineering decisions traceable.

The same principle was applied across mechanical, electrical, sensing, software, obstacle, parking, and full-system testing.

# Evidence-Based Engineering Decisions

Important decisions were based on observed robot behaviour and testing.

### Motor

The **LEGO Medium Motor** was selected because it provided sufficient propulsion performance while integrating directly with the LEGO Technic drivetrain. Smaller alternatives were considered for compactness, while more powerful alternatives were considered for performance, but the final decision prioritised the complete system balance.

### Chassis

LEGO was selected because rapid modification and repair were important during development.

### Camera

The wide camera was selected because the robot needs to observe the track and obstacles ahead while driving.

### IMU

The BNO055 was selected because orientation feedback is useful for steering stability and parking alignment.

### IR Sensors

IR sensors were used for close-range information where camera-based positioning becomes less reliable.

### Camera Mount

The camera height and approximately 10° downward angle were selected from measured geometry. The angle was calculated using the camera height and useful detection distance rather than chosen arbitrarily.

### White Electronics Cover

The white cover was added after observing that the camera could incorrectly interpret electronics as environmental features.

These decisions follow the engineering chain:

![Evidence-based engineering decision chain](assets/28_decision_chain.svg)

**Problem → Alternatives → Testing → Trade-off → Engineering Decision → Retest**

# Final Performance Validation

**Current Open Challenge reference:** approximately **35 seconds per open-round lap**.

This is the main recorded performance figure currently available to us. Other performance metrics are not presented as measured values unless they have been formally recorded.

The final robot is evaluated across the same major areas used during development:

![Final performance metrics](assets/performance_metrics.svg)

### Mechanical
Stable chassis, consistent steering, reliable drivetrain, and secure component mounting.

### Electrical
Stable regulated power, reliable motor operation, reliable sensor communication, and organised wiring.

### Sensors
Reliable camera detection, calibrated IMU, functional IR feedback, and functional physical switches.

### Software
Modular architecture, master state machine, computer vision, steering control, obstacle strategy, lap counting, parking logic, and recovery handling.

### Full System

The final test is performed with all subsystems operating simultaneously because individual subsystem success does not guarantee full-system success.

**Evidence discipline:** the repository distinguishes between recorded performance and engineering expectations. This prevents estimated values from being presented as measured competition results.

# Final Robot

<img src="assets/final_design.svg" alt="Final robot architecture" width="850">

<table><tr><td align="center"><img src="assets/robot_front_card.png" width="240"><br><sub>Front</sub></td><td align="center"><img src="assets/robot_side_card.png" width="240"><br><sub>Side</sub></td><td align="center"><img src="assets/robot_top_card.png" width="240"><br><sub>Top</sub></td><td align="center"><img src="assets/robot_rear_card.png" width="240"><br><sub>Rear</sub></td></tr></table>

![Final robot views](assets/robot_views.png)

Our final robot is the result of repeated mechanical, electrical, sensor, and software iterations.

The final design combines:

![Final system components](assets/final_system.svg)

The most important feature of the design is the interaction between these systems.

The camera provides information about the environment.

The IMU provides information about robot orientation.

The IR sensors provide close-range feedback.

The software combines these inputs to determine the robot's state.

The control system converts that state into steering and speed commands.

The mechanical system then produces the physical movement.

This creates a closed-loop autonomous vehicle.

# Engineering Philosophy

The main lesson from developing this robot was that making a robot work once is different from engineering a robot that works repeatedly.

Our development therefore focused on:

![Engineering philosophy](assets/engineering_philosophy.svg)

- Understanding why failures occurred
- Testing individual subsystems
- Making changes based on evidence
- Considering mechanical and software interactions
- Designing for repairability
- Reducing single points of failure
- Documenting decisions
- Retesting after modifications

Whenever possible, we followed:

**Problem → Analysis → Solution → Test → Result**

rather than simply changing components until the robot appeared to work.

The goal of the repository is therefore not only to present a successful robot, but to preserve the reasoning that produced it.

## Advanced Engineering Evidence

The repository is designed around the evidence expected at the advanced engineering level:

**Requirements → Alternatives → Design → Implementation → Testing → Failure analysis → Iteration → Validation → Reproducibility**

The strongest evidence in the repository is therefore placed next to the engineering decision it supports rather than separated from the explanation.

# Conclusion

BroCode's WRO Future Engineers robot was developed as an integrated engineering system rather than as a collection of individual components.

The mechanical system provides the stability and movement required by the software.

The electrical system provides controlled and reliable power.

The sensors provide information about both the environment and the robot.

The software converts that information into decisions.

The control system converts those decisions into physical movement.

Testing connects all of these systems together and allows weaknesses to be identified and corrected.

Our final design is the result of continuous iteration between mechanical design, electronics, sensing, software, and control.

The purpose of this repository is to preserve that engineering process and make the final robot understandable, reproducible, and useful to anyone who wants to study or build upon the project.
