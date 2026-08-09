# BroCode

This repository contains the complete engineering documentation, software, hardware design, testing process, and development history of our autonomous self-driving robot for the **WRO Future Engineers 2026** category.

The robot has been designed and developed by **BroCode** with a focus on autonomous navigation, computer vision, mechanical stability, controlled steering, obstacle management, repeatability, and systematic engineering development.

The purpose of this repository is not only to show the final robot, but also to explain **why** the robot was designed in its current form, how the different subsystems interact, what alternatives were considered, how problems were identified, and how testing was used to improve the design.

The development process follows an iterative engineering cycle:

**Design → Build → Test → Identify Problem → Analyse → Modify → Retest**

The repository is intended to provide enough technical information for the robot's design and software architecture to be understood and reproduced.

---

# Table of Contents

1. [Team](#team)
2. [Project Overview](#project-overview)
3. [Engineering Objectives](#engineering-objectives)
4. [Overall Robot Architecture](#overall-robot-architecture)
5. [Mechanical Architecture](#mechanical-architecture)
6. [Mobility and Drive System](#mobility-and-drive-system)
7. [Steering System](#steering-system)
8. [Mechanical Design Decisions](#mechanical-design-decisions)
9. [Mechanical Testing](#mechanical-testing)
10. [Power Architecture](#power-architecture)
11. [Sensor Architecture](#sensor-architecture)
12. [Sensor Selection and Trade-offs](#sensor-selection-and-trade-offs)
13. [Sensor Placement](#sensor-placement)
14. [Sensor Calibration and Reliability](#sensor-calibration-and-reliability)
15. [Software Architecture](#software-architecture)
16. [Software Module Structure](#software-module-structure)
17. [Main Control Flow](#main-control-flow)
18. [Computer Vision](#computer-vision)
19. [Wall and Lane Detection](#wall-and-lane-detection)
20. [Steering Control](#steering-control)
21. [Obstacle Detection and Strategy](#obstacle-detection-and-strategy)
22. [Obstacle State Machine](#obstacle-state-machine)
23. [Parking Strategy](#parking-strategy)
24. [Edge Cases and Failure Handling](#edge-cases-and-failure-handling)
25. [Testing and Tuning](#testing-and-tuning)
26. [Systems Thinking](#systems-thinking)
27. [Engineering Trade-offs](#engineering-trade-offs)
28. [Design Evolution](#design-evolution)
29. [Risk and Failure Mitigation](#risk-and-failure-mitigation)
30. [Repository Structure](#repository-structure)
31. [Software Setup](#software-setup)
32. [Hardware Reproducibility](#hardware-reproducibility)
33. [Version Control](#version-control)
34. [Bill of Materials](#bill-of-materials)
35. [Final Architecture](#final-architecture)
36. [Engineering Philosophy](#engineering-philosophy)
37. [Team Responsibilities](#team-responsibilities)

---

# Team

## BroCode

### 1. Tanish Kothari — Software

Primary responsibilities:

- Software architecture
- Python programming
- Computer vision
- Camera processing
- Colour detection
- Navigation logic
- Steering control
- IMU integration
- Obstacle detection
- Obstacle strategy
- Parking logic
- Software testing and debugging
- GitHub documentation

### 2. Vihaan Kothari — Hardware

Primary responsibilities:

- Mechanical design
- LEGO Technic construction
- Chassis development
- Drive mechanism
- Steering mechanism
- Electronics integration
- Sensor mounting
- Wiring
- Mechanical testing
- Hardware modifications

Both team members contributed to the overall robot strategy, testing, debugging, design decisions, and development of the final autonomous system.

---

# Project Overview

The WRO Future Engineers challenge requires a vehicle to navigate the track autonomously while adapting to changes in the track and, in the Obstacle Challenge, responding to coloured traffic signs.

The 2026 challenge consists of an **Open Challenge** and an **Obstacle Challenge**. In the Open Challenge, the robot must complete three laps with changing internal wall configurations. In the Obstacle Challenge, the robot must complete three laps while responding to randomly positioned red and green traffic signs and subsequently perform parallel parking.

Our robot was therefore designed around the idea that a successful solution cannot depend on one fixed route.

Instead, the robot continuously obtains information from its sensors, processes that information, makes a navigation decision, and then changes its movement accordingly.

The overall control loop is:

```text
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
