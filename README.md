# BroCode

This repository contains the engineering documentation, software,
hardware design, testing process, and development history of our
autonomous robot for the **WRO Future Engineers 2026** category.

Our robot was developed with a focus on autonomous navigation, computer
vision, mechanical stability, controlled steering, obstacle management,
parking, reliability, and repeatable performance.

The purpose of this repository is not only to show the final robot, but
also to document **why** we made our major engineering decisions, what
alternatives we considered, what problems we encountered, how we tested
them, and how the design evolved.

Our development process follows:

**Design → Build → Test → Identify Problem → Analyse → Modify → Retest**

------------------------------------------------------------------------

# Table of Contents

-   [Team](#team)
-   [Project Overview](#project-overview)
-   [Engineering Objectives](#engineering-objectives)
-   [Overall Robot Architecture](#overall-robot-architecture)
-   [Mechanical Architecture](#mechanical-architecture)
-   [Mobility and Drive System](#mobility-and-drive-system)
-   [Steering System](#steering-system)
-   [Mechanical Design Decisions](#mechanical-design-decisions)
-   [Mechanical Testing](#mechanical-testing)
-   [Power Architecture](#power-architecture)
-   [Power Budget and Distribution](#power-budget-and-distribution)
-   [Sensor Architecture](#sensor-architecture)
-   [Sensor Selection and Trade-offs](#sensor-selection-and-trade-offs)
-   [Sensor Placement](#sensor-placement)
-   [Camera Calibration](#camera-calibration)
-   [IMU Calibration](#imu-calibration)
-   [Sensor Testing and Reliability](#sensor-testing-and-reliability)
-   [Software Architecture](#software-architecture)
-   [Software Modules](#software-modules)
-   [Master State Machine](#master-state-machine)
-   [Computer Vision](#computer-vision)
-   [Colour Detection](#colour-detection)
-   [Wall and Lane Following](#wall-and-lane-following)
-   [Steering and Speed Control](#steering-and-speed-control)
-   [Lap Counting and Debouncing](#lap-counting-and-debouncing)
-   [Obstacle Detection and Strategy](#obstacle-detection-and-strategy)
-   [Obstacle-Side Decision Logic](#obstacle-side-decision-logic)
-   [Obstacle Avoidance and Recovery](#obstacle-avoidance-and-recovery)
-   [Parking Strategy](#parking-strategy)
-   [Edge Cases and Failure Handling](#edge-cases-and-failure-handling)
-   [Testing and Tuning](#testing-and-tuning)
-   [Systems Thinking and Engineering
    Decisions](#systems-thinking-and-engineering-decisions)
-   [Engineering Trade-offs](#engineering-trade-offs)
-   [Design Evolution](#design-evolution)
-   [Problems → Solutions → Results](#problems--solutions--results)
-   [Risk and Failure Analysis](#risk-and-failure-analysis)
-   [Final System Architecture](#final-system-architecture)
-   [Final Hardware Specifications](#final-hardware-specifications)
-   [Bill of Materials](#bill-of-materials)
-   [Repository Structure](#repository-structure)
-   [Hardware and Software
    Reproducibility](#hardware-and-software-reproducibility)
-   [Version Control](#version-control)
-   [Testing Workflow](#testing-workflow)
-   [Evidence-Based Engineering
    Decisions](#evidence-based-engineering-decisions)
-   [Final Robot](#final-robot)
-   [Engineering Philosophy](#engineering-philosophy)
-   [Team Responsibilities](#team-responsibilities)
-   [Documentation Checklist](#documentation-checklist)
-   [Conclusion](#conclusion)

------------------------------------------------------------------------

# Team

## BroCode

### 1. Tanish Kothari --- Software

Primary responsibilities:

-   Software architecture
-   Python programming
-   Computer vision
-   Camera processing
-   Colour detection
-   Navigation logic
-   Steering control
-   IMU software integration
-   Obstacle detection and strategy
-   Parking logic
-   Software testing and debugging
-   GitHub documentation

### 2. Vihaan Kothari --- Hardware

Primary responsibilities:

-   Mechanical design
-   LEGO Technic construction
-   Chassis development
-   Drive mechanism
-   Steering mechanism
-   Electronics integration
-   Sensor mounting
-   Wiring
-   Mechanical testing
-   Hardware modifications

Both members contributed to the overall robot strategy, testing,
debugging, design decisions, system integration, and development of the
final robot.

------------------------------------------------------------------------

# Project Overview

The WRO Future Engineers challenge requires the robot to navigate the
track autonomously while responding to changing conditions.

The **Open Challenge** requires the robot to navigate changing internal
wall configurations. The **Obstacle Challenge** additionally requires
the robot to recognise red and green obstacles, obey the required side
of the track, and complete the parking task.

Because the environment is not completely fixed, our robot was designed
around closed-loop control rather than a sequence of pre-programmed
movements.

The robot continuously obtains information from its sensors, processes
that information, makes a navigation decision, and changes its movement
accordingly.

The overall control loop is:

``` text
Sensors
   ↓
Perception
   ↓
State Estimation
   ↓
Decision Making
   ↓
Control
   ↓
Actuation
   ↓
New Sensor Data
   ↓
Repeat
```

This allows the robot to respond to the actual state of the track
instead of replaying a predetermined route.

------------------------------------------------------------------------

# Engineering Objectives

Our main engineering objectives were:

1.  Build a mechanically stable and predictable vehicle.
2.  Create a reliable steering mechanism.
3.  Balance motor torque and speed instead of maximising only one.
4.  Keep the robot compact and lightweight.
5.  Make the chassis modular so mechanical changes could be made
    quickly.
6.  Use computer vision as the primary source of environmental
    information.
7.  Use the IMU and IR sensors as complementary feedback.
8.  Create a reliable power distribution system.
9.  Build modular software so individual systems could be tested
    independently.
10. Document the final robot sufficiently for another team to understand
    and reproduce it.

------------------------------------------------------------------------

# Overall Robot Architecture

The robot is divided into five closely connected subsystems:

``` text
                    ┌─────────────────────┐
                    │   Raspberry Pi 4B   │
                    │   Main Controller   │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ↓                 ↓                 ↓
       Camera System       BNO055 IMU       IR Sensors
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ↓
                     Perception / Fusion
                               ↓
                       Decision / FSM
                               ↓
                     Steering + Speed
                               ↓
              ┌─────────────────────────┐
              │       Actuators         │
              │                         │
              │ Drive Motor + Gearbox   │
              │ Steering Servo          │
              └─────────────────────────┘

Battery
   ↓
Power Distribution
   ↓
Voltage Regulation
   ↓
Raspberry Pi / Sensors / Electronics
```

The systems are not independent. Camera position affects the field of
view available to the software, steering geometry affects the
relationship between a software command and vehicle movement, and motor
selection affects the speed and acceleration that the control system can
safely use.

This interaction between subsystems was considered throughout
development.

------------------------------------------------------------------------

# Mechanical Architecture

The robot uses a hybrid structure made from **LEGO Technic components
and custom 3D-printed parts**.

The LEGO structure was selected because it allowed us to rapidly change
the chassis geometry during development. Components could be moved,
reinforced, or replaced without rebuilding the complete robot.

Custom 3D-printed components were used where standard LEGO geometry did
not provide the required solution. These included motor mounting and
housing components, camera mounting/protection, and other custom
structural parts.

The mechanical design was based on three requirements:

-   **Rigidity** --- the chassis should not flex enough to change
    steering geometry.
-   **Compactness** --- the robot should remain small and manoeuvrable.
-   **Modularity** --- components should be easy to modify and repair.

The approximate base footprint is **22 cm × 12 cm**. The camera is
mounted approximately **26 cm above the floor**, with its optical axis
angled approximately **10° downward from horizontal**.

The stated robot mass during development was approximately **650--700
g**.

------------------------------------------------------------------------

# Mobility and Drive System

The robot uses a **D360 brushed DC motor with a 22:1 gearbox** for
propulsion.

The gearbox was important because the robot needs useful wheel torque
while still maintaining practical speed.

The basic relationship considered during motor selection was:

``` text
Wheel Torque ≈ Motor Torque × Gear Ratio × Transmission Efficiency
```

Increasing the gear ratio increases available wheel torque but reduces
output speed.

Our objective was not to select the motor with the highest advertised
RPM or torque. We needed a combination that provided:

-   Useful straight-line speed
-   Sufficient acceleration
-   Reliable movement through corners
-   Enough torque to avoid stalling
-   Reasonable weight
-   Compact integration

The D360 with the 22:1 gearbox provided the most suitable balance for
our robot.

------------------------------------------------------------------------

# Steering System

Steering is provided by a **REV Robotics 2000 Series Dual Mode Servo**
mounted using a GoBILDA servo frame.

The steering mechanism requires controlled angular positioning, so the
servo provides a more appropriate interface than a simple uncontrolled
motor.

Mechanical play was treated as an important source of error. If the
linkage or servo mounting moves under load, the same software command
can produce different physical steering angles.

The steering loop is:

``` text
Camera / IMU Data
       ↓
Calculate Heading / Position Error
       ↓
Determine Steering Error
       ↓
Control Algorithm
       ↓
Servo Angle
       ↓
Robot Direction
```

Mechanical geometry and software parameters were tuned together because
changing the steering geometry changes the relationship between servo
angle and vehicle motion.

------------------------------------------------------------------------

# Mechanical Design Decisions

## Motor Selection

We considered several motor options.

### N20 DC Motor

Advantages:

-   Small
-   Lightweight
-   Easy to mount

Disadvantages:

-   Insufficient torque under the load of our final robot.

### REV NEO 550

Advantages:

-   High power
-   Strong performance

Disadvantages:

-   Larger and heavier
-   Required additional control hardware
-   More complex than necessary for our design

### LEGO Medium Motor

Advantages:

-   Easy LEGO integration
-   Simple mounting

Disadvantages:

-   Lower performance for our required speed and torque balance

### Final Choice: D360 + 22:1 Gearbox

The D360 solution provided the best overall balance between speed,
torque, weight, size, and integration simplicity.

The decision was based on the complete drivetrain requirement rather
than a single motor specification.

------------------------------------------------------------------------

# Why We Chose LEGO

The LEGO chassis was designed from scratch for our robot.

We selected LEGO because it provided:

-   High modularity
-   Fast prototyping
-   Easy repair
-   Easy component relocation
-   Strong structural elements
-   Simple mechanical iteration

During development, being able to change the chassis quickly was more
valuable to us than using a completely fixed custom frame.

This allowed us to test different motor, camera, sensor, and structural
configurations without rebuilding the complete robot.

------------------------------------------------------------------------

# Mechanical Testing

Mechanical testing was performed after major changes to the drivetrain,
chassis, and steering system.

We evaluated:

-   Straight-line stability
-   Acceleration behaviour
-   Turning behaviour
-   Steering response
-   Mechanical play
-   Motor mounting stability
-   Chassis rigidity
-   Wheel alignment
-   Camera mounting stability

When inconsistent behaviour appeared, we first checked for a mechanical
cause before changing software parameters.

This prevented software tuning from being used to hide mechanical
instability.

------------------------------------------------------------------------

# Power Architecture

The robot uses a **7.4 V, 1500 mAh Li-ion battery pack**.

The battery feeds the power distribution system, which provides the
appropriate supply to the motor system and regulated electronics.

The main architecture is:

``` text
7.4 V Battery
     │
     ├──────────────→ Motor Driver → Drive Motor
     │
     ↓
Buck Converter
     │
     └──────────────→ 5 V Electronics
                         │
                         ├── Raspberry Pi
                         ├── Camera
                         ├── Sensors
                         └── Other peripherals
```

The Raspberry Pi requires a stable regulated supply because voltage
drops can cause instability or unexpected resets.

The motor power path and regulated electronics path were therefore
treated separately.

------------------------------------------------------------------------

# Power Budget and Distribution

The major electrical loads are:

  Component         Supply / Path            Function
  ----------------- ------------------------ -----------------------
  Raspberry Pi 4B   5 V regulated            Main processing
  Camera            Raspberry Pi supply      Computer vision
  BNO055            Regulated logic supply   Orientation feedback
  IR sensors        Regulated logic supply   Close-range detection
  Limit switches    GPIO                     Physical feedback
  Motor driver      Battery-side supply      Motor control
  Drive motor       Battery-side supply      Propulsion
  Steering servo    Regulated supply         Steering

The main power risks identified were:

-   Battery voltage drop
-   Motor current spikes
-   Raspberry Pi brownouts
-   Electrical noise
-   Loose connections
-   Insufficient regulator capacity

Power connections were secured, regulated supplies were used for
sensitive electronics, and the wiring was organised to reduce accidental
disconnections.

The power system was tested with the motor running because a power
system that is stable only when the motor is idle is not sufficient for
competition operation.

------------------------------------------------------------------------

# Sensor Architecture

The robot uses multiple sensors because no single sensor provides
reliable information for every part of the challenge.

The main sensing systems are:

-   **Raspberry Pi Camera Module 3 Wide**
-   **BNO055 IMU**
-   **4 IR sensors**
-   **2 VEX limit switches**

Each sensor has a defined role.

  -----------------------------------------------------------------------
  Sensor                              Main Purpose
  ----------------------------------- -----------------------------------
  Pi Camera                           Vision, track interpretation,
                                      obstacle recognition, parking

  BNO055 IMU                          Orientation and heading feedback

  IR Sensors                          Short-range detection and parking
                                      alignment

  Limit Switches                      Physical fail-safe feedback
  -----------------------------------------------------------------------

The camera is the primary perception sensor. The IMU provides
orientation information, while the IR sensors provide close-range
feedback where visual positioning becomes less reliable.

------------------------------------------------------------------------

# Sensor Selection and Trade-offs

## Camera

The camera provides substantially more environmental information than a
single distance sensor.

It can be used for:

-   Wall detection
-   Lane interpretation
-   Coloured obstacle recognition
-   Marker detection
-   Parking-area detection

Its main limitation is sensitivity to lighting, exposure, and colour
thresholds.

## BNO055 IMU

The BNO055 provides orientation information using internal sensor
fusion.

It is useful for:

-   Heading correction
-   Turn stabilisation
-   Alignment
-   Parking

Its readings can still be affected by calibration and the robot's
mounting environment.

## IR Sensors

IR sensors are simple and fast for short-range detection.

They are particularly useful during parking when the robot is close to
the parking boundary.

Their limitation is that they provide much less environmental
information than the camera.

## Limit Switches

Limit switches provide simple physical feedback and an additional
fail-safe if the robot unexpectedly interacts with an object.

------------------------------------------------------------------------

# Sensor Placement

Sensor placement was based on the geometry of the task rather than
simply available space.

### Camera

The camera is:

-   Mounted at the front of the robot
-   Centred on the robot
-   Approximately **26 cm above the floor**
-   Pointed approximately **10° downward from horizontal**

The centred mounting keeps the camera coordinate system aligned with the
robot's centreline.

The height and angle provide a forward field of view while allowing the
software to observe relevant track features before the robot reaches
them.

### BNO055

The BNO055 is mounted securely on the **left side of the robot**.

Its position is kept fixed so that the sensor's coordinate frame remains
consistent after calibration.

### IR Sensors

The IR sensors are placed toward the **rear of the robot** and are
primarily used for close-range parking detection and alignment.

### Limit Switches

The limit switches are positioned so that an unexpected physical
interaction can be detected.

------------------------------------------------------------------------

# Camera Calibration

Camera calibration and colour testing were performed using images
captured from the actual robot and track.

We initially tested RGB/BGR-based colour detection. We found that these
approaches were sensitive to changes in lighting and exposure.

We then tested HSV because it separates hue from brightness.

Finally, we tested LAB colour space and selected it for the
colour-detection approach that was most consistent during our testing.

The general processing pipeline is:

``` text
Camera Frame
     ↓
Image Pre-processing
     ↓
Colour Space Conversion
     ↓
Colour Threshold
     ↓
Binary Mask
     ↓
Noise Filtering
     ↓
Relevant Region Detection
     ↓
Position / Colour Classification
     ↓
Navigation Decision
```

Thresholds were tuned using real camera data instead of relying only on
theoretical colour values.

This was one of the most important parts of our development because
camera reliability affects navigation, obstacle recognition, and
parking.

------------------------------------------------------------------------

# IMU Calibration

The BNO055 is calibrated before navigation testing.

The robot is kept stationary during the initial calibration process so
that a stable reference can be established.

The IMU is then tested by rotating the robot manually and checking
whether the reported heading changes consistently with the physical
movement.

Calibration is important because incorrect orientation information can
cause the robot to steer in the wrong direction or over-correct during
turns.

The IMU is therefore used as a feedback source and is not treated as a
replacement for visual information.

------------------------------------------------------------------------

# Sensor Testing and Reliability

Sensor testing was performed independently before full-system testing.

### Camera

We tested:

-   Colour separation
-   False detections
-   Lighting variation
-   Detection distance
-   Region-of-interest size
-   Stability of detected positions

### BNO055

We tested:

-   Heading consistency
-   Stationary behaviour
-   Response during turns
-   Repeatability after restarting

### IR Sensors

We tested:

-   Short-range response
-   Detection consistency
-   Parking alignment
-   False readings

### Limit Switches

We tested:

-   Physical activation
-   Electrical response
-   Software response
-   Recovery behaviour

Testing sensors independently allowed us to determine whether a failure
originated from sensing, software, or the physical system.

------------------------------------------------------------------------

# Software Architecture

The robot software is modular rather than being one large program.

The main software layers are:

``` text
Hardware Interface
       ↓
Sensor Acquisition
       ↓
Perception
       ↓
State Estimation
       ↓
Navigation
       ↓
Control
       ↓
Motor / Servo Output
```

The main functional modules are:

1.  Camera acquisition
2.  Image processing
3.  Colour detection
4.  Wall / lane detection
5.  IMU interface
6.  IR sensor interface
7.  Steering controller
8.  Speed control
9.  Lap counting
10. Obstacle recognition
11. Obstacle-side decision
12. Obstacle avoidance
13. Parking detection
14. Parking alignment
15. Recovery handling
16. Main state machine

This structure makes it possible to test and modify individual systems
without rewriting the complete program.

------------------------------------------------------------------------

# Software Modules

The intended software organisation is:

``` text
Software/
│
├── Main/
│   └── Main Control Program
│
├── Computer Vision/
│   ├── Camera Input
│   ├── Colour Detection
│   ├── Wall Detection
│   └── Obstacle Detection
│
├── Sensors/
│   ├── BNO055
│   ├── IR Sensors
│   └── Limit Switches
│
├── Control/
│   ├── Steering
│   └── Speed
│
├── Obstacle/
│   ├── Recognition
│   ├── Side Decision
│   └── Avoidance
│
└── Parking/
    ├── Detection
    ├── Alignment
    └── Final Positioning
```

Each module has a defined responsibility, making debugging and future
changes easier.

------------------------------------------------------------------------

# Master State Machine

The master state machine provides the overall structure of the robot's
behaviour.

``` text
                 ┌──────────────┐
                 │    START     │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │ INITIALISE   │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │    DRIVE     │
                 └──────┬───────┘
                        ↓
             ┌──────────┴──────────┐
             ↓                     ↓
       ┌───────────┐         ┌──────────────┐
       │ OBSTACLE  │         │   RECOVERY   │
       │ DETECTED  │         │              │
       └─────┬─────┘         └──────┬───────┘
             ↓                      │
       ┌───────────┐                │
       │  AVOID    │────────────────┘
       └─────┬─────┘
             ↓
       ┌──────────────┐
       │ LAP COMPLETE │
       └──────┬───────┘
              ↓
       ┌──────────────┐
       │ THREE LAPS?  │
       └──────┬───────┘
          NO  │   YES
              │
              ↓
        ┌─────────────┐
        │   PARKING   │
        └──────┬──────┘
               ↓
        ┌─────────────┐
        │    STOP     │
        └─────────────┘
```

The state machine prevents unrelated behaviours from interfering with
one another.

For example, parking logic should not activate while the robot is still
completing its laps.

------------------------------------------------------------------------

# Computer Vision

Computer vision is one of the main parts of our robot.

The Raspberry Pi Camera Module 3 Wide provides the visual input and
OpenCV is used to process the images.

The main vision tasks are:

-   Wall detection
-   Lane interpretation
-   Colour recognition
-   Obstacle recognition
-   Marker detection
-   Parking detection

Regions of interest are used where appropriate to reduce unnecessary
processing and focus the algorithm on areas relevant to navigation.

------------------------------------------------------------------------

# Colour Detection

We tested multiple colour representations during development.

RGB/BGR thresholding was investigated first, but colour classification
became inconsistent under changes in lighting and exposure.

HSV was then tested because it separates hue from brightness.

LAB was ultimately selected for the colour-detection approach that gave
the most consistent results during our testing.

The process is:

``` text
Image
 ↓
Colour Space Conversion
 ↓
Colour Threshold
 ↓
Binary Mask
 ↓
Noise Filtering
 ↓
Contour / Region Detection
 ↓
Centroid / Position
```

The detected colour region is then converted into information that can
be used by the navigation system.

------------------------------------------------------------------------

# Wall and Lane Following

The robot continuously estimates the position of relevant track
boundaries using the camera.

A target position is generated from the detected wall or lane geometry.

The difference between the target position and the detected position
becomes the steering error.

``` text
Target Position
      -
Detected Position
      =
Steering Error
```

The controller converts this error into a steering command.

This allows the robot to continuously correct its path rather than
relying on fixed steering angles.

------------------------------------------------------------------------

# Steering and Speed Control

The steering system uses feedback.

If the robot is far from the desired path, the controller increases the
steering correction.

If the robot is close to the desired path, the correction becomes
smaller.

The basic proportional relationship is:

``` text
Steering Output = Kp × Error
```

A proportional controller was selected because our primary requirement
was fast, predictable correction.

Too little correction caused drift, while too much correction caused
oscillation.

Steering parameters were therefore tuned experimentally.

Speed is also coordinated with steering. Higher speed can be used when
the robot is stable and the path is clear, while sharp turns or
uncertain perception can justify reducing speed.

The objective is not maximum motor speed; it is the highest speed that
remains reliably controllable.

------------------------------------------------------------------------

# Lap Counting and Debouncing

Lap counting is handled in software using visual markers and a debounce
condition.

Without debouncing, the same marker could be detected in multiple
consecutive camera frames and incorrectly increase the lap count several
times.

The logic is:

``` text
Marker Detected
      ↓
Is Detection New?
   /       \
 NO         YES
 ↓           ↓
Ignore    Count Lap
             ↓
       Wait for Marker
       to Leave Region
             ↓
       Ready for Next Lap
```

This prevents a single physical marker from producing multiple lap
counts.

------------------------------------------------------------------------

# Obstacle Detection and Strategy

In the Obstacle Challenge, the robot identifies coloured obstacles using
computer vision.

The two relevant colours represent different side-obedience
requirements.

The obstacle pipeline is:

``` text
Camera
  ↓
Colour Space Conversion
  ↓
Red / Green Masks
  ↓
Contour Detection
  ↓
Obstacle Position
  ↓
Colour Classification
  ↓
Required Side
  ↓
Avoidance Path
```

The robot uses the detected obstacle colour as an input to the
navigation decision rather than treating colour detection as an isolated
vision feature.

------------------------------------------------------------------------

# Red / Green Obstacle Recognition

The software uses separate colour masks to distinguish the two obstacle
colours.

The detected obstacle is classified according to its colour, and that
classification affects the required path.

The exact side decision is implemented in the obstacle strategy module
so that recognition and navigation remain separate software functions.

------------------------------------------------------------------------

# Obstacle-Side Decision Logic

The robot considers obstacle colour together with the current driving
state and visible track geometry.

The decision process is:

``` text
Obstacle Detected
       ↓
Identify Colour
       ↓
Determine Required Side
       ↓
Check Current Robot Position
       ↓
Calculate Safe Path
       ↓
Change Steering Target
       ↓
Avoid Obstacle
       ↓
Return to Normal Path
```

This allows the robot to respond to obstacle position rather than
relying on fixed obstacle coordinates.

------------------------------------------------------------------------

# Obstacle Avoidance and Recovery

Obstacle avoidance is divided into three stages.

### 1. Approach

The robot detects the obstacle and prepares for the required path
change.

### 2. Pass

The robot moves around the obstacle while maintaining clearance.

### 3. Recover

After passing the obstacle, the robot gradually returns toward the
normal path.

Gradual recovery is important because an immediate large steering
correction can cause oscillation or overshoot.

If the obstacle temporarily disappears from the camera after being
detected, the robot retains the current avoidance state for a short
period rather than immediately returning to normal navigation.

This prevents one missed frame from producing an incorrect path change.

------------------------------------------------------------------------

# Open Challenge Strategy

The Open Challenge can contain different internal wall configurations.

Our robot therefore does not depend on fixed coordinates for wall
positions.

Instead, it continuously detects visible wall geometry and adjusts its
path.

``` text
Detect Wall
    ↓
Estimate Robot Position
    ↓
Calculate Desired Path
    ↓
Steer
    ↓
Re-detect Wall
    ↓
Correct
```

This allows the navigation system to adapt to different track layouts.

------------------------------------------------------------------------

# Parking Strategy

Parking was one of the most difficult parts of our design.

Our goal was to use the camera effectively while keeping the sensor
system as simple as possible.

The current parking development approach combines:

-   Camera detection
-   IMU orientation
-   IR feedback
-   Controlled steering

The intended sequence is:

``` text
Three Laps Complete
       ↓
Identify Parking Area
       ↓
Align With Parking Direction
       ↓
Reduce Speed
       ↓
Use Camera + IMU
       ↓
Use IR for Close-Range Confirmation
       ↓
Correct Orientation
       ↓
Enter Parking Space
       ↓
Final Alignment
       ↓
STOP
```

The camera provides the main environmental information while the IMU and
IR sensors provide additional feedback during the final alignment stage.

------------------------------------------------------------------------

# IMU-Based Parking Alignment

The BNO055 is used to estimate the robot's orientation during parking.

The robot compares its current heading with the desired parking
orientation.

The heading error is then used to determine whether an additional
steering correction is required.

This is useful because camera-only alignment can become less reliable
when the robot is very close to the parking boundaries.

The IMU therefore provides an independent orientation reference during
the final manoeuvre.

------------------------------------------------------------------------


# Edge Cases and Failure Handling

We considered situations where the normal navigation assumptions can
fail.

### Camera temporarily loses the wall

The robot retains the previous valid steering information and avoids
making an extreme correction from a single bad frame.

### False colour detection

Colour detections are filtered using thresholding and region checks
instead of accepting every coloured pixel.

### Multiple obstacle detections

The system evaluates relevant detected obstacle regions rather than
treating every coloured region as a separate obstacle.

### Sensor noise

Sensor readings are interpreted over time rather than relying on one
isolated measurement.

### Excessive steering

Steering output is limited so that one erroneous measurement cannot
produce an extreme command.

### Robot becomes misaligned

The recovery state reduces aggressive movement and attempts to return to
a stable visual path.

### Limit switch activation

A physical limit switch can provide an additional indication of
unexpected physical interaction.

------------------------------------------------------------------------

# Testing and Tuning

Testing was treated as an engineering process rather than a final
verification step.

Our development cycle was:

``` text
Build
 ↓
Test
 ↓
Measure
 ↓
Identify Failure
 ↓
Change One Variable
 ↓
Retest
 ↓
Compare
```

Changing one major variable at a time made it easier to determine
whether a change actually improved the robot.

------------------------------------------------------------------------

# Testing Methodology

Testing was divided into:

### Mechanical Testing

-   Chassis rigidity
-   Wheel alignment
-   Steering response
-   Motor mounting
-   Turning behaviour

### Electrical Testing

-   Battery output
-   Regulated voltage
-   Motor operation
-   Raspberry Pi stability
-   Sensor power

### Sensor Testing

-   Camera detection
-   Colour thresholds
-   IMU orientation
-   IR response
-   Limit switches

### Software Testing

-   State transitions
-   Steering control
-   Lap counting
-   Obstacle recognition
-   Parking logic
-   Recovery states

### Full-System Testing

The complete robot was tested with all systems operating simultaneously
because success of individual subsystems does not guarantee success of
the complete system.

------------------------------------------------------------------------

# Testing Metrics

We used measurable categories to evaluate changes rather than judging
improvements only by appearance.

The main performance metrics were:

-   Lap completion rate
-   Lap time
-   Number of obstacle-avoidance successes
-   Number of obstacle contacts
-   Parking success rate
-   Steering stability
-   Number of recovery events
-   Number of false obstacle detections
-   Number of incorrect lap counts
-   Electrical stability during continuous operation

For software tuning, we looked particularly at the trade-off between:

``` text
Fast Response
      ↕
Stable Response
```

A parameter was not considered better simply because it increased speed.
The objective was to improve speed while maintaining reliable
completion.

------------------------------------------------------------------------

# Colour Threshold Testing

Colour thresholds were tested using actual camera frames captured from
the robot.

The process was:

1.  Capture an image.
2.  Convert it to the selected colour space.
3.  Apply an initial colour range.
4.  Observe the detected region.
5.  Adjust thresholds.
6.  Test under different lighting conditions.
7.  Verify that the detected region corresponds to the intended object.
8.  Retest on the physical track.

This reduced the chance that the robot would depend on one ideal
lighting condition.

------------------------------------------------------------------------

# Steering Parameter Tuning

Steering parameters were tuned through repeated driving tests.

The main failure modes were:

### Too little correction

The robot slowly drifted away from the desired path.

### Too much correction

The robot oscillated from side to side.

### Excessive steering at high speed

The robot could over-correct before the next useful camera update.

The final approach was therefore to balance steering gain with robot
speed.

------------------------------------------------------------------------

# Obstacle Detection Testing

Obstacle testing was performed by changing:

-   Obstacle colour
-   Obstacle position
-   Robot approach angle
-   Robot speed
-   Distance from obstacle

The objective was to verify that the software did not simply recognise
the colour but actually used it to make the correct navigation decision.

------------------------------------------------------------------------

# Lap Counting Testing

Lap counting was tested specifically for repeated detections.

A marker visible across several frames should still count as only one
lap event.

The debounce logic was therefore tested by:

-   Approaching the marker slowly
-   Approaching quickly
-   Remaining near the marker
-   Passing the marker multiple times

The final system accepts a new lap only after the previous detection has
cleared.

------------------------------------------------------------------------

# Parking Testing

Parking was tested separately from normal driving.

The main parameters considered were:

-   Entry alignment
-   Robot heading
-   Steering angle
-   IR sensor response
-   Final position
-   Final orientation

The parking algorithm was adjusted through repeated attempts rather than
relying on one successful run.

The objective was to determine which combination of camera information,
IMU heading, and IR feedback produced the most repeatable final
alignment.

------------------------------------------------------------------------

# Software Iterations

The software evolved through multiple iterations.

The important principle was that changes were made in response to
observed behaviour.

A simplified development sequence was:

``` text
Basic steering
      ↓
Improved wall detection
      ↓
Proportional steering
      ↓
Speed / steering coordination
      ↓
Obstacle recognition
      ↓
Obstacle-side logic
      ↓
Recovery states
      ↓
Parking integration
```

Each stage added functionality while preserving previously working
behaviour.

------------------------------------------------------------------------

# Systems Thinking and Engineering Decisions

We treated the robot as one integrated system rather than as separate
mechanical, electrical, sensor, and software projects.

For example:

``` text
Motor
 ↓
Vehicle Speed
 ↓
Camera Motion
 ↓
Image Processing
 ↓
Steering Error
 ↓
Servo Command
 ↓
Vehicle Direction
 ↓
New Camera Image
```

Similarly:

``` text
Battery
 ↓
Voltage Regulation
 ↓
Raspberry Pi
 ↓
Camera Processing
 ↓
Navigation
 ↓
Motor Command
 ↓
Motor Current
 ↓
Battery Load
```

A change in one subsystem can therefore affect another subsystem.

This interaction was considered when making design decisions.

------------------------------------------------------------------------

# Engineering Constraints

The major constraints we worked under were:

-   Limited robot size
-   Limited weight
-   Limited battery capacity
-   Limited processing resources
-   Real-time camera processing
-   Mechanical space
-   Steering precision
-   Competition time
-   Changing track geometry
-   Random obstacle placement
-   Autonomous operation

Instead of optimising one subsystem independently, we looked for
solutions that worked within the complete system.

------------------------------------------------------------------------

# Engineering Trade-offs

## Speed vs Stability

A faster robot can produce a better lap time, but higher speed reduces
the time available for steering correction.

We therefore prioritised controllable speed over maximum possible speed.

## Torque vs Speed

A higher gear ratio provides more torque but reduces wheel speed.

We selected the 22:1 gearbox because the robot needed enough torque to
accelerate and maintain motion while still having useful speed.

## Camera Information vs Processing

A wider camera view provides more environmental information but also
increases the amount of image that must be processed.

The camera was positioned and processed using relevant regions of
interest to keep the system practical.

## LEGO Modularity vs Custom Construction

A fully custom chassis could provide more fixed geometry, but LEGO
allowed us to change the robot much faster during development.

We therefore used LEGO for the main structure and 3D printing where
custom geometry was necessary.

## Sensor Quantity vs Complexity

Adding more sensors can provide more redundancy, but it also increases
wiring, processing, and possible failure points.

We therefore gave each sensor a specific purpose rather than adding
sensors without a defined role.

------------------------------------------------------------------------

# Design Evolution

The robot was developed through repeated changes rather than as one
final design.

### Early Design

The initial objective was to create a vehicle capable of moving and
steering.

### Intermediate Design

Driving tests identified issues with:

-   Torque
-   Steering consistency
-   Sensor placement
-   Camera visibility
-   Wiring organisation

### Improved Design

We introduced:

-   Gear reduction
-   More stable motor mounting
-   Improved steering mounting
-   Better sensor positioning
-   Custom printed components
-   Electronics protection
-   More structured software

### Final Design

The final system combines:

-   LEGO chassis
-   Custom 3D-printed components
-   D360 + 22:1 gearbox
-   REV servo steering
-   Raspberry Pi 4B
-   Pi Camera Module 3 Wide
-   BNO055 IMU
-   IR sensors
-   Limit switches
-   Regulated power distribution
-   Modular software architecture

------------------------------------------------------------------------

# Problems → Solutions → Results

  -----------------------------------------------------------------------
  Problem                 Solution                Result
  ----------------------- ----------------------- -----------------------
  Insufficient torque     22:1 gearbox            Better drivetrain
                                                  response

  Camera saw electronics  White electronics cover Cleaner visual input
  as track features

  Chassis changes were    LEGO modular structure  Faster iteration
  difficult

  Motor mounting movement Custom 3D-printed mount Improved alignment

  Steering instability    Improved mounting and   More predictable
                          software tuning         steering

  False colour detections Colour-space            More reliable detection
                          thresholding and
                          filtering

  Repeated lap detection  Debouncing              Correct lap counting

  Parking alignment       IMU orientation feedback       More controlled parking
  uncertainty

  Wiring complexity       Organised electronics   Cleaner connections
                          board

  Mechanical flex         Structural              More consistent
                          reinforcement           steering
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# Why We Used a White Electronics Cover

During camera testing, the camera could sometimes see the colours and
components of the electronics.

This created false visual information.

The problem was particularly important because our software relies on
colour and object detection.

We therefore added a white cover over the electronics area.

The cover reduced unwanted visual features and made the camera view more
consistent.

This was an example of a mechanical change solving a software perception
problem.

------------------------------------------------------------------------

# Risk and Failure Analysis

We considered the following major failure modes:

  -----------------------------------------------------------------------
  Failure Mode      Cause             Effect            Mitigation
  ----------------- ----------------- ----------------- -----------------
  Raspberry Pi      Motor current     Software stops    Regulated power
  brownout          spike                               system

  Motor stall       Insufficient      Robot stops       Gear reduction
                    torque

  Camera false      Electronics /     Wrong navigation  White cover +
  detection         lighting                            filtering

  Steering          Excessive gain    Robot loses path  Parameter tuning
  oscillation

  Missed obstacle   Poor colour       Incorrect route   Colour testing +
                    detection                           filtering

  Repeated lap      Same marker       Incorrect state   Debouncing
  count             detected
                    repeatedly

  IMU error         Calibration /     Heading error     Calibration +
                    interference                        visual feedback

  IR false reading  Surface /         Parking error     Multi-sensor
                    distance                            interpretation
                    variation

  Loose wire        Vibration         Sensor / motor    Secured and
                                      failure           organised wiring

  Mechanical flex   Chassis movement  Steering          Structural
                                      inconsistency     reinforcement

  Sensor failure    Hardware fault    Missing feedback  Redundancy /
                                                        recovery
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# Risk Mitigation

Our risk mitigation strategy follows:

``` text
Identify Failure
      ↓
Reduce Probability
      ↓
Provide Recovery
```

For example, camera failure cannot always be prevented, so the software
avoids making an extreme decision based on one bad frame.

Mechanical movement is reduced through stronger mounting, while software
tuning is performed only after the mechanical system is stable.

This prevents software parameters from being used to hide mechanical
problems.

------------------------------------------------------------------------

# Final System Architecture

``` text
                         ┌─────────────────┐
                         │ Raspberry Pi 4B │
                         └────────┬────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ↓                   ↓                   ↓
        Pi Camera 3          BNO055 IMU          IR Sensors
              │                   │                   │
              └───────────────────┼───────────────────┘
                                  ↓
                         Sensor Processing
                                  ↓
                        Computer Vision
                                  ↓
                         State Estimation
                                  ↓
                         Master FSM
                                  ↓
                    ┌─────────────┴─────────────┐
                    ↓                           ↓
              Steering Control             Speed Control
                    ↓                           ↓
              REV Servo                  TB6612FNG
                                                ↓
                                           D360 Motor
                                                ↓
                                             Gearbox
                                                ↓
                                             Wheels

Battery
  ↓
Power Distribution
  ↓
Buck Regulation
  ↓
Pi + Sensors + Electronics
```

This architecture separates perception, decision-making, and actuation
while maintaining feedback between them.

------------------------------------------------------------------------

# Final Hardware Specifications

  System                   Final Component
  ------------------------ --------------------------------------
  Main Controller          Raspberry Pi 4B 4GB
  Camera                   Raspberry Pi Camera Module 3 Wide
  Drive Motor              D360 Brushed DC Motor
  Gearbox                  22:1
  Motor Driver             TB6612FNG
  Steering                 REV Robotics 2000 Series Servo
  IMU                      BNO055
  IR Sensors               4
  Limit Switches           2
  Battery                  7.4 V, 1500 mAh Li-ion
  Main Regulation          5 V 3 A Buck Converter
  Chassis                  LEGO Technic + 3D Printed
  Approx. Weight           650--700 g
  Approx. Base Footprint   22 × 12 cm
  Camera Height            Approx. 26 cm above floor
  Camera Angle             Approx. 10° downward from horizontal

------------------------------------------------------------------------

# Bill of Materials

  Component                             Quantity
  ----------------------------------- ----------
  Raspberry Pi 4B 4GB                          1
  Raspberry Pi Camera Module 3 Wide            1
  D360 Brushed DC Motor                        1
  22:1 Gearbox                                 1
  TB6612FNG Motor Driver                       1
  REV 2000 Series Servo                        1
  GoBILDA Servo Mount                          1
  7.4 V, 1500 mAh Li-ion Battery                    1
  5 V 3 A Buck Converter                       1
  USB Buck Converter                           1
  BNO055 IMU                                   1
  IR Sensors                                   4
  VEX Limit Switches                           2
  LEGO Technic Parts                    Multiple
  3D Printed Parts                        Custom

------------------------------------------------------------------------

# Repository Structure

The repository is organised so that another team can understand both the
final robot and the engineering process.

``` text
BroCode/
│
├── README.md
│
├── Hardware/
│   ├── Hardware Overview.md
│   ├── Wiring/
│   │   ├── Wiring Diagram.png
│   │   └── Pin Mapping.md
│   │
│   ├── CAD/
│   │   ├── Robot CAD/
│   │   ├── STEP/
│   │   └── LEGO Studio/
│   │
│   ├── Robot Assembly Instructions.pdf
│   └── Bill of Materials.xlsx
│
├── Software/
│   ├── Main/
│   ├── Computer Vision/
│   ├── Sensors/
│   ├── Control/
│   ├── Obstacle/
│   ├── Parking/
│   └── README.md
│
├── Testing/
│   ├── Mechanical Testing/
│   ├── Electrical Testing/
│   ├── Sensor Testing/
│   ├── Software Testing/
│   └── Performance/
│
├── Documentation/
│   ├── Engineering Journal.pdf
│   ├── Design Evolution/
│   └── Photos/
│
└── Media/
    ├── Robot Photos/
    └── Driving Videos/
```

------------------------------------------------------------------------

# Hardware and Software Reproducibility

A second team should be able to understand and reproduce the robot using
the documentation provided in this repository.

The documentation covers:

-   Hardware overview
-   Bill of materials
-   CAD files
-   LEGO assembly information
-   Wiring diagram
-   Pin mapping
-   Sensor placement
-   Software source code
-   Software module descriptions
-   Testing workflow
-   Engineering decisions

The mechanical documentation explains how the chassis and custom
components fit together.

The electrical documentation explains how the battery, regulators, motor
driver, controller, and sensors are connected.

The software documentation explains how those electrical components are
controlled by the program.

The exact GPIO and interface mapping should be maintained in the
dedicated wiring and pin-mapping documentation so that hardware changes
do not require rewriting the main README.

------------------------------------------------------------------------

# Software Setup

The software is intended to run on the Raspberry Pi.

The basic setup process is:

``` text
Clone Repository
      ↓
Install Python Dependencies
      ↓
Connect Camera
      ↓
Connect Sensors
      ↓
Verify GPIO / I²C
      ↓
Run Sensor Tests
      ↓
Run Camera Test
      ↓
Run Navigation Program
```

The software is divided into modules so that individual components can
be tested before running the complete autonomous program.

------------------------------------------------------------------------

# Version Control

GitHub is used as part of the engineering process rather than only as a
location for the final code.

Significant development changes should be recorded through meaningful
commits.

Examples of useful commit messages include:

``` text
Initial hardware architecture
Initial autonomous control system
Camera and colour detection added
Steering controller improved
Obstacle recognition added
Parking system added
Sensor calibration update
Final software tuning
Final documentation
```

A useful commit should communicate what changed and, where relevant, why
it changed.

This allows the repository to show the engineering process instead of
only presenting a final code dump.

------------------------------------------------------------------------

# Testing Workflow

Our standard testing workflow is:

``` text
1. Define the problem
2. Create a test
3. Run the current design
4. Record the behaviour
5. Identify the likely cause
6. Change the relevant subsystem
7. Run the same test again
8. Compare the result
9. Keep or revert the change
10. Document the result
```

This prevents random tuning and makes engineering decisions traceable.

------------------------------------------------------------------------

# Evidence-Based Engineering Decisions

Important decisions were based on observed robot behaviour and testing.

### Motor

We selected the D360 + 22:1 gearbox because smaller alternatives did not
provide the required torque, while larger alternatives introduced
unnecessary size and complexity.

### Chassis

We selected LEGO because rapid modification and repair were important
during development.

### Camera

We selected the wide camera because the robot needs to observe the track
and obstacles ahead while driving.

### IMU

We selected the BNO055 because orientation feedback is useful for
steering stability and parking alignment.

### IR Sensors

We used IR sensors for close-range information where camera-based
positioning becomes less reliable.

### White Electronics Cover

We added the white cover after observing that the camera could
incorrectly interpret electronics as environmental features.

These decisions follow the engineering chain:

``` text
Problem
  ↓
Possible Solutions
  ↓
Testing
  ↓
Trade-off
  ↓
Engineering Decision
```

------------------------------------------------------------------------

# Final Performance Validation

**Current Open Challenge reference:** approximately **35 seconds per open-round lap**.

This is the main recorded performance figure currently available to us; other performance metrics are not presented as measured values unless they have been recorded.

The final robot is evaluated across the same major areas used during
development.

### Mechanical

-   Stable chassis
-   Consistent steering
-   Reliable drivetrain
-   Secure component mounting

### Electrical

-   Stable regulated power
-   Reliable motor operation
-   Reliable sensor communication
-   Organised wiring

### Sensors

-   Reliable camera detection
-   Calibrated IMU
-   Functional IR feedback
-   Functional physical switches

### Software

-   Modular architecture
-   Master state machine
-   Computer vision
-   Steering control
-   Obstacle strategy
-   Lap counting
-   Parking logic
-   Recovery handling

### Full System

The final test is performed with all subsystems operating simultaneously
because individual subsystem success does not guarantee full-system
success.

------------------------------------------------------------------------

# Final Robot

Our final robot is the result of repeated mechanical, electrical,
sensor, and software iterations.

The final design combines:

-   A modular LEGO Technic chassis
-   Custom 3D-printed components
-   D360 + 22:1 geared drivetrain
-   REV servo steering
-   Raspberry Pi 4B
-   Raspberry Pi Camera Module 3 Wide
-   BNO055 IMU
-   IR sensors
-   Limit switches
-   Regulated power distribution
-   Modular autonomous software

The most important feature of the design is the interaction between
these systems.

The camera provides information about the environment.

The IMU provides information about robot orientation.

The IR sensors provide close-range feedback.

The software combines these inputs to determine the robot's state.

The control system converts that state into steering and speed commands.

The mechanical system then produces the physical movement.

This creates a closed-loop autonomous vehicle.

------------------------------------------------------------------------

# Engineering Philosophy

The main lesson from developing this robot was that making a robot work
once is different from engineering a robot that works repeatedly.

Our development therefore focused on:

-   Understanding why failures occurred
-   Testing individual subsystems
-   Making changes based on evidence
-   Considering mechanical and software interactions
-   Designing for repairability
-   Reducing single points of failure
-   Documenting decisions
-   Retesting after modifications

Whenever possible, we followed:

**Problem → Analysis → Solution → Test → Result**

rather than simply changing components until the robot appeared to work.

------------------------------------------------------------------------

# Team Responsibilities

## Tanish Kothari

Software and autonomous systems:

-   Software architecture
-   Computer vision
-   OpenCV
-   Colour detection
-   Navigation
-   Steering control
-   Obstacle strategy
-   Lap counting
-   Parking logic
-   IMU software integration
-   Testing
-   Debugging
-   Documentation

## Vihaan Kothari

Hardware and mechanical systems:

-   Chassis
-   LEGO construction
-   Motor mounting
-   Steering mechanism
-   3D-printed components
-   Electronics mounting
-   Wiring
-   Sensor mounting
-   Mechanical testing
-   Hardware iteration

Both members contributed to:

-   Design decisions
-   Testing
-   Problem solving
-   Robot assembly
-   System integration
-   Competition strategy

------------------------------------------------------------------------

# Documentation Checklist

This repository is structured around the five WRO documentation
evaluation criteria.

## 1. Mobility and Mechanical Design

The documentation covers:

-   Chassis design
-   Drive mechanism
-   Steering mechanism
-   Torque and speed reasoning
-   Motor alternatives
-   Mechanical trade-offs
-   Mechanical testing
-   Design evolution
-   CAD and assembly documentation
-   Reproducibility

## 2. Power and Sensor Architecture

The documentation covers:

-   Power architecture
-   Power distribution
-   Voltage regulation
-   Power risks
-   Sensor selection
-   Sensor trade-offs
-   Sensor placement
-   Camera calibration
-   IMU calibration
-   IR sensor usage
-   Wiring
-   Sensor failure handling

## 3. Software Architecture and Obstacle Strategy

The documentation covers:

-   Software architecture
-   Software modules
-   Main control flow
-   Master state machine
-   Computer vision
-   Colour detection
-   Wall / lane following
-   Steering control
-   Speed control
-   Lap counting and debouncing
-   Obstacle recognition
-   Obstacle-side decision logic
-   Obstacle avoidance
-   Recovery
-   Parking
-   Edge cases
-   Testing and tuning
-   Performance metrics

## 4. Systems Thinking and Engineering Decisions

The documentation covers:

-   Engineering constraints
-   Subsystem interactions
-   Motor trade-offs
-   Chassis trade-offs
-   Sensor trade-offs
-   Power decisions
-   Software decisions
-   Failure modes
-   Risk mitigation
-   Design evolution
-   Problems → Solutions → Results
-   Evidence-based decisions

## 5. Reproducibility and GitHub Quality

The repository is being built to contain:

-   README
-   Hardware documentation
-   CAD
-   Wiring information
-   Pin mapping
-   Software source code
-   Testing documentation
-   Assembly information
-   Bill of materials
-   Robot photographs and media
-   Meaningful version history

The README explains the design and engineering process, while the
supporting repository files provide the technical information needed to
reproduce the robot.

------------------------------------------------------------------------

# Conclusion

BroCode's WRO Future Engineers robot was developed as an integrated
engineering system rather than as a collection of individual components.

The mechanical system provides the stability and movement required by
the software.

The electrical system provides controlled and reliable power.

The sensors provide information about both the environment and the
robot.

The software converts that information into decisions.

The control system converts those decisions into physical movement.

Testing connects all of these systems together and allows weaknesses to
be identified and corrected.

Our final design is the result of continuous iteration between
mechanical design, electronics, sensing, software, and control.

The purpose of this repository is to preserve that engineering process
and make the final robot understandable, reproducible, and useful to
anyone who wants to study or build upon the project.

**Built. Tested. Broken. Improved. Rebuilt.**
