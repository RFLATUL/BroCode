BroCode

This repository contains the engineering documentation, software,hardware design, testing process, and development history of ourautonomous robot for the WRO Future Engineers 2026 category.

Our robot was developed with a focus on autonomous navigation, computervision, mechanical stability, controlled steering, obstacle management,parking, reliability, and repeatable performance.

The purpose of this repository is not only to show the final robot, butalso to document why we made our major engineering decisions, whatalternatives we considered, what problems we encountered, how we testedthem, and how the design evolved.

Our development process follows:

Design → Build → Test → Identify Problem → Analyse → Modify → Retest



<table>
<tr>
<td align="center"><img src="assets/robot_front.png" width="220"><br><sub>Front view</sub></td>
<td align="center"><img src="assets/robot_side.png" width="220"><br><sub>Side view</sub></td>
<td align="center"><img src="assets/robot_top.png" width="220"><br><sub>Top view</sub></td>
<td align="center"><img src="assets/robot_rear.png" width="220"><br><sub>Rear view</sub></td>
</tr>
</table>

Table of Contents

1. Project & Team

Team

Project Overview

Engineering Objectives

Overall Robot Architecture

2. Mobility & Mechanical Design

Mobility & Mechanical Design

Mobility and Drive System

Steering System

Mechanical Design Decisions

Why We Chose LEGO

Mechanical Testing

3. Power & Sensor Architecture

Power & Sensor Architecture

Power Budget and Distribution

Sensor Architecture

Sensor Selection and Trade-offs

Sensor Placement

Camera Calibration

IMU Calibration

Sensor Testing and Reliability

4. Software Architecture & Obstacle Strategy

Software Architecture & Obstacle Strategy

Software Modules

Master State Machine

Computer Vision

Colour Detection

Wall and Lane Following

Steering and Speed Control

Lap Counting and Debouncing

Obstacle Detection and Strategy

Red / Green Obstacle Recognition

Obstacle-Side Decision Logic

Obstacle Avoidance and Recovery

Open Challenge Strategy

Parking Strategy

IMU-Based Parking Alignment

Edge Cases and Failure Handling

5. Testing, Systems Thinking & Engineering Decisions

Testing, Validation & Tuning

Testing Methodology

Testing Metrics

Colour Threshold Testing

Steering Parameter Tuning

Obstacle Detection Testing

Lap Counting Testing

Parking Testing

Software Iterations

Systems Thinking & Engineering Decisions

Engineering Constraints

Engineering Trade-offs

Design Evolution

Problems → Solutions → Results

Risk and Failure Analysis

Risk Mitigation

Evidence-Based Engineering Decisions

6. Reproducibility & GitHub Quality

Final System Architecture

Final Hardware Specifications

Bill of Materials

Reproducibility & GitHub Quality

Software Setup

Version Control

Testing Workflow

Final Performance Validation

Final Robot

Engineering Philosophy

Conclusion

Team

BroCode

1. Tanish Kothari --- Software

Primary responsibilities:



2. Vihaan Kothari --- Hardware

Primary responsibilities:



Both members contributed to the overall robot strategy, testing,debugging, design decisions, system integration, and development of thefinal robot.

Project Overview

The WRO Future Engineers challenge requires the robot to navigate thetrack autonomously while responding to changing conditions.

The Open Challenge requires the robot to navigate changing internalwall configurations. The Obstacle Challenge additionally requiresthe robot to recognise red and green obstacles, obey the required sideof the track, and complete the parking task.

Because the environment is not completely fixed, our robot was designedaround closed-loop control rather than a sequence of pre-programmedmovements.

The robot continuously obtains information from its sensors, processesthat information, makes a navigation decision, and changes its movementaccordingly.

The overall control loop is:



This allows the robot to respond to the actual state of the trackinstead of replaying a predetermined route.

Engineering Objectives

Our main engineering objectives were:



Overall Robot Architecture

The robot is divided into five closely connected subsystems:



The systems are not independent. Camera position affects the field ofview available to the software, steering geometry affects therelationship between a software command and vehicle movement, and motorselection affects the speed and acceleration that the control system cansafely use.

This interaction between subsystems was considered throughoutdevelopment.

Mobility & Mechanical Design

The robot uses a hybrid structure made from LEGO Technic componentsand custom 3D-printed parts.

The LEGO structure was selected because it allowed us to rapidly changethe chassis geometry during development. Components could be moved,reinforced, or replaced without rebuilding the complete robot.

Custom 3D-printed components were used where standard LEGO geometry didnot provide the required solution. These included motor mounting andhousing components, camera mounting/protection, and other customstructural parts.

The mechanical design was based on three requirements:

The approximate base footprint is 22 cm × 12 cm. The camera ismounted approximately 26 cm above the floor, with its optical axisangled approximately 10° downward from horizontal.

The stated robot mass during development was approximately 800g.

Mobility and Drive System

The robot uses a D360 brushed DC motor with a 22:1 gearbox forpropulsion.

The gearbox was important because the robot needs useful wheel torquewhile still maintaining practical speed.

The basic relationship considered during motor selection was:



Increasing the gear ratio increases available wheel torque but reducesoutput speed.

Our objective was not to select the motor with the highest advertisedRPM or torque. We needed a combination that provided:



The D360 with the 22:1 gearbox provided the most suitable balance forour robot.

Steering System



Steering is provided by a REV Robotics 2000 Series Dual Mode Servomounted using a GoBILDA servo frame.

The steering mechanism requires controlled angular positioning, so theservo provides a more appropriate interface than a simple uncontrolledmotor.

Mechanical play was treated as an important source of error. If thelinkage or servo mounting moves under load, the same software commandcan produce different physical steering angles.

The steering loop is:



Mechanical geometry and software parameters were tuned together becausechanging the steering geometry changes the relationship between servoangle and vehicle motion.

Mechanical Design Decisions

Motor Selection

We considered several motor options.

N20 DC Motor

REV NEO 550



LEGO Medium Motor



Final Choice: D360 + 22:1 Gearbox

The D360 solution provided the best overall balance between speed,torque, weight, size, and integration simplicity.

The decision was based on the complete drivetrain requirement ratherthan a single motor specification.

Why We Chose LEGO

The LEGO chassis was designed from scratch for our robot.

We selected LEGO because it provided:



During development, being able to change the chassis quickly was morevaluable to us than using a completely fixed custom frame.

This allowed us to test different motor, camera, sensor, and structuralconfigurations without rebuilding the complete robot.

Mechanical Testing

Mechanical testing was performed after major changes to the drivetrain,chassis, and steering system.

We evaluated:



When inconsistent behaviour appeared, we first checked for a mechanicalcause before changing software parameters.

This prevented software tuning from being used to hide mechanicalinstability.

Power & Sensor Architecture

<table><tr><td align="center"><img src="assets/component_battery.png" width="250"><br><sub>7.4 V rechargeable battery</sub></td><td align="center"><img src="assets/component_buck.png" width="220"><br><sub>5 V buck converter</sub></td><td align="center"><img src="assets/component_pcb.png" width="250"><br><sub>Custom electronics board</sub></td></tr></table>

The robot uses a 7.4 V, 1500 mAh Li-ion rechargeable battery pack.

The battery feeds the power distribution system, which provides theappropriate supply to the motor system and regulated electronics.

The main architecture is:



The Raspberry Pi requires a stable regulated supply because voltagedrops can cause instability or unexpected resets.

The motor power path and regulated electronics path were thereforetreated separately.

Power Budget and Distribution



The major electrical loads are:



The main power risks identified were:



Power connections were secured, regulated supplies were used forsensitive electronics, and the wiring was organised to reduce accidentaldisconnections.

The power system was tested with the motor running because a powersystem that is stable only when the motor is idle is not sufficient forcompetition operation.

Sensor Architecture

<table><tr><td align="center"><img src="assets/component_camera.png" width="220"><br><sub>Raspberry Pi Camera Module 3 Wide</sub></td><td align="center"><img src="assets/component_imu.png" width="220"><br><sub>BNO055 IMU</sub></td><td align="center"><img src="assets/component_ir.png" width="220"><br><sub>IR sensors</sub></td><td align="center"><img src="assets/component_limit.png" width="220"><br><sub>VEX limit switches</sub></td></tr></table>



The robot uses multiple sensors because no single sensor providesreliable information for every part of the challenge.

The main sensing systems are:



Each sensor has a defined role.



The camera is the primary perception sensor. The IMU providesorientation information, while the IR sensors provide close-rangefeedback where visual positioning becomes less reliable.

Sensor Selection and Trade-offs

Camera



The camera provides substantially more environmental information than asingle distance sensor.

It can be used for:



Its main limitation is sensitivity to lighting, exposure, and colourthresholds.

BNO055 IMU



The BNO055 provides orientation information using internal sensorfusion.

It is useful for:



Its readings can still be affected by calibration and the robot'smounting environment.

IR Sensors



IR sensors are simple and fast for short-range detection.

They are particularly useful during parking when the robot is close tothe parking boundary.

Their limitation is that they provide much less environmentalinformation than the camera.

Limit Switches



Limit switches provide simple physical feedback and an additionalfail-safe if the robot unexpectedly interacts with an object.

Sensor Placement

<img src="assets/sensor_placement.png" alt="Sensor placement on robot" width="850">



Sensor placement was based on the geometry of the task rather thansimply available space.

Camera

The camera is:



The centred mounting keeps the camera coordinate system aligned with therobot's centreline.

The height and angle provide a forward field of view while allowing thesoftware to observe relevant track features before the robot reachesthem.

BNO055

The BNO055 is mounted securely on the left side of the robot.

Its position is kept fixed so that the sensor's coordinate frame remainsconsistent after calibration.

IR Sensors

The IR sensors are placed toward the rear of the robot and areprimarily used for close-range parking detection and alignment.

Limit Switches

The limit switches are positioned so that an unexpected physicalinteraction can be detected.

Camera Calibration

Camera calibration and colour testing were performed using imagescaptured from the actual robot and track.

We initially tested RGB/BGR-based colour detection. We found that theseapproaches were sensitive to changes in lighting and exposure.

We then tested HSV because it separates hue from brightness.

Finally, we tested LAB colour space and selected it for thecolour-detection approach that was most consistent during our testing.

The general processing pipeline is:



Thresholds were tuned using real camera data instead of relying only ontheoretical colour values.

This was one of the most important parts of our development becausecamera reliability affects navigation, obstacle recognition, andparking.

IMU Calibration

The BNO055 is calibrated before navigation testing.

The robot is kept stationary during the initial calibration process sothat a stable reference can be established.

The IMU is then tested by rotating the robot manually and checkingwhether the reported heading changes consistently with the physicalmovement.

Calibration is important because incorrect orientation information cancause the robot to steer in the wrong direction or over-correct duringturns.

The IMU is therefore used as a feedback source and is not treated as areplacement for visual information.

Sensor Testing and Reliability

Sensor testing was performed independently before full-system testing.



Testing sensors independently allowed us to determine whether a failureoriginated from sensing, software, or the physical system.

Software Architecture & Obstacle Strategy

The robot software is modular rather than being one large program.

The main software layers are:



The main functional modules are:



This structure makes it possible to test and modify individual systemswithout rewriting the complete program.

Software Modules

The intended software organisation is:



Each module has a defined responsibility, making debugging and futurechanges easier.

Master State Machine

The master state machine provides the overall structure of the robot'sbehaviour.



The state machine prevents unrelated behaviours from interfering withone another.

For example, parking logic should not activate while the robot is stillcompleting its laps.

Computer Vision

<img src="assets/computer_vision_tasks.svg" alt="Computer vision tasks" width="850">

Computer vision is one of the main parts of our robot.

The Raspberry Pi Camera Module 3 Wide provides the visual input andOpenCV is used to process the images.

The main vision tasks are:



Regions of interest are used where appropriate to reduce unnecessaryprocessing and focus the algorithm on areas relevant to navigation.

Colour Detection

We tested multiple colour representations during development.

RGB/BGR thresholding was investigated first, but colour classificationbecame inconsistent under changes in lighting and exposure.

HSV was then tested because it separates hue from brightness.

LAB was ultimately selected for the colour-detection approach that gavethe most consistent results during our testing.

The process is:



The detected colour region is then converted into information that canbe used by the navigation system.

Wall and Lane Following

The robot continuously estimates the position of relevant trackboundaries using the camera.

A target position is generated from the detected wall or lane geometry.

The difference between the target position and the detected positionbecomes the steering error.



The controller converts this error into a steering command.

This allows the robot to continuously correct its path rather thanrelying on fixed steering angles.

Steering and Speed Control

The steering system uses feedback.

If the robot is far from the desired path, the controller increases thesteering correction.

If the robot is close to the desired path, the correction becomessmaller.

The basic proportional relationship is:



A proportional controller was selected because our primary requirementwas fast, predictable correction.

Too little correction caused drift, while too much correction causedoscillation.

Steering parameters were therefore tuned experimentally.

Speed is also coordinated with steering. Higher speed can be used whenthe robot is stable and the path is clear, while sharp turns oruncertain perception can justify reducing speed.

The objective is not maximum motor speed; it is the highest speed thatremains reliably controllable.

Lap Counting and Debouncing

Lap counting is handled in software using visual markers and a debouncecondition.

Without debouncing, the same marker could be detected in multipleconsecutive camera frames and incorrectly increase the lap count severaltimes.

The logic is:



This prevents a single physical marker from producing multiple lapcounts.

Obstacle Detection and Strategy

In the Obstacle Challenge, the robot identifies coloured obstacles usingcomputer vision.

The two relevant colours represent different side-obediencerequirements.

The obstacle pipeline is:



The robot uses the detected obstacle colour as an input to thenavigation decision rather than treating colour detection as an isolatedvision feature.

Red / Green Obstacle Recognition

The software uses separate colour masks to distinguish the two obstaclecolours.

The detected obstacle is classified according to its colour, and thatclassification affects the required path.

The exact side decision is implemented in the obstacle strategy moduleso that recognition and navigation remain separate software functions.

Obstacle-Side Decision Logic

The robot considers obstacle colour together with the current drivingstate and visible track geometry.

The decision process is:



This allows the robot to respond to obstacle position rather thanrelying on fixed obstacle coordinates.

Obstacle Avoidance and Recovery

Obstacle avoidance is divided into three stages.

1. Approach

The robot detects the obstacle and prepares for the required pathchange.

2. Pass

The robot moves around the obstacle while maintaining clearance.

3. Recover

After passing the obstacle, the robot gradually returns toward thenormal path.

Gradual recovery is important because an immediate large steeringcorrection can cause oscillation or overshoot.

If the obstacle temporarily disappears from the camera after beingdetected, the robot retains the current avoidance state for a shortperiod rather than immediately returning to normal navigation.

This prevents one missed frame from producing an incorrect path change.

Open Challenge Strategy

The Open Challenge can contain different internal wall configurations.

Our robot therefore does not depend on fixed coordinates for wallpositions.

Instead, it continuously detects visible wall geometry and adjusts itspath.



This allows the navigation system to adapt to different track layouts.

Parking Strategy

Parking was one of the most difficult parts of our design.

Our goal was to use the camera effectively while keeping the sensorsystem as simple as possible.

The current parking development approach combines:



The intended sequence is:



The camera provides the main environmental information while the IMU andIR sensors provide additional feedback during the final alignment stage.

IMU-Based Parking Alignment

The BNO055 is used to estimate the robot's orientation during parking.

The robot compares its current heading with the desired parkingorientation.

The heading error is then used to determine whether an additionalsteering correction is required.

This is useful because camera-only alignment can become less reliablewhen the robot is very close to the parking boundaries.

The IMU therefore provides an independent orientation reference duringthe final manoeuvre.

Edge Cases and Failure Handling

We considered situations where the normal navigation assumptions canfail.

Camera temporarily loses the wall

The robot retains the previous valid steering information and avoidsmaking an extreme correction from a single bad frame.

False colour detection

Colour detections are filtered using thresholding and region checksinstead of accepting every coloured pixel.

Multiple obstacle detections

The system evaluates relevant detected obstacle regions rather thantreating every coloured region as a separate obstacle.

Sensor noise

Sensor readings are interpreted over time rather than relying on oneisolated measurement.

Excessive steering

Steering output is limited so that one erroneous measurement cannotproduce an extreme command.

Robot becomes misaligned

The recovery state reduces aggressive movement and attempts to return toa stable visual path.

Limit switch activation

A physical limit switch can provide an additional indication ofunexpected physical interaction.

Testing, Validation & Tuning

Testing was treated as an engineering process rather than a finalverification step.

Our development cycle was:



Changing one major variable at a time made it easier to determinewhether a change actually improved the robot.

Testing Methodology

Testing was divided into:



Full-System Testing

The complete robot was tested with all systems operating simultaneouslybecause success of individual subsystems does not guarantee success ofthe complete system.

Testing Metrics

We used measurable categories to evaluate changes rather than judgingimprovements only by appearance.

The main performance metrics were:



For software tuning, we looked particularly at the trade-off between:



A parameter was not considered better simply because it increased speed.The objective was to improve speed while maintaining reliablecompletion.

Colour Threshold Testing

Colour thresholds were tested using actual camera frames captured fromthe robot.

The process was:



This reduced the chance that the robot would depend on one ideallighting condition.

Steering Parameter Tuning

Steering parameters were tuned through repeated driving tests.

The main failure modes were:

Too little correction

The robot slowly drifted away from the desired path.

Too much correction

The robot oscillated from side to side.

Excessive steering at high speed

The robot could over-correct before the next useful camera update.

The final approach was therefore to balance steering gain with robotspeed.

Obstacle Detection Testing

Obstacle testing was performed by changing:



The objective was to verify that the software did not simply recognisethe colour but actually used it to make the correct navigation decision.

Lap Counting Testing

Lap counting was tested specifically for repeated detections.

A marker visible across several frames should still count as only onelap event.

The debounce logic was therefore tested by:



The final system accepts a new lap only after the previous detection hascleared.

Parking Testing

Parking was tested separately from normal driving.

The main parameters considered were:



The parking algorithm was adjusted through repeated attempts rather thanrelying on one successful run.

The objective was to determine which combination of camera information,IMU heading, and IR feedback produced the most repeatable finalalignment.

Software Iterations

The software evolved through multiple iterations.

The important principle was that changes were made in response toobserved behaviour.

A simplified development sequence was:



Each stage added functionality while preserving previously workingbehaviour.

Systems Thinking & Engineering Decisions

We treated the robot as one integrated system rather than as separatemechanical, electrical, sensor, and software projects.

For example:



Similarly:



A change in one subsystem can therefore affect another subsystem.

This interaction was considered when making design decisions.

Engineering Constraints

The major constraints we worked under were:



Instead of optimising one subsystem independently, we looked forsolutions that worked within the complete system.

Engineering Trade-offs

Speed vs Stability

A faster robot can produce a better lap time, but higher speed reducesthe time available for steering correction.

We therefore prioritised controllable speed over maximum possible speed.

Torque vs Speed

A higher gear ratio provides more torque but reduces wheel speed.

We selected the 22:1 gearbox because the robot needed enough torque toaccelerate and maintain motion while still having useful speed.

Camera Information vs Processing

A wider camera view provides more environmental information but alsoincreases the amount of image that must be processed.

The camera was positioned and processed using relevant regions ofinterest to keep the system practical.

LEGO Modularity vs Custom Construction

A fully custom chassis could provide more fixed geometry, but LEGOallowed us to change the robot much faster during development.

We therefore used LEGO for the main structure and 3D printing wherecustom geometry was necessary.

Sensor Quantity vs Complexity

Adding more sensors can provide more redundancy, but it also increaseswiring, processing, and possible failure points.

We therefore gave each sensor a specific purpose rather than addingsensors without a defined role.

Design Evolution

The robot was developed through repeated changes rather than as onefinal design.

Early Design

The initial objective was to create a vehicle capable of moving andsteering.

Intermediate Design

Driving tests identified issues with:



Improved Design

We introduced:



Final Design

The final system combines:





Problems → Solutions → Results



Why We Used a White Electronics Cover

During camera testing, the camera could sometimes see the colours andcomponents of the electronics.

This created false visual information.

The problem was particularly important because our software relies oncolour and object detection.

We therefore added a white cover over the electronics area.

The cover reduced unwanted visual features and made the camera view moreconsistent.

This was an example of a mechanical change solving a software perceptionproblem.

Risk and Failure Analysis

We considered the following major failure modes:



For example, camera failure cannot always be prevented, so the softwareavoids making an extreme decision based on one bad frame.

Mechanical movement is reduced through stronger mounting, while softwaretuning is performed only after the mechanical system is stable.

This prevents software parameters from being used to hide mechanicalproblems.

Final System Architecture



This architecture separates perception, decision-making, and actuationwhile maintaining feedback between them.

Final Hardware Specifications



Bill of Materials------------------------------------------------------------------------

Bill of Materials



Reproducibility & GitHub Quality

Reproducibility & GitHub Quality

A second team should be able to understand and reproduce the robot usingthe documentation provided in this repository.

The documentation covers:



The mechanical documentation explains how the chassis and customcomponents fit together.

The electrical documentation explains how the battery, regulators, motordriver, controller, and sensors are connected.

The software documentation explains how those electrical components arecontrolled by the program.

The exact GPIO and interface mapping should be maintained in thededicated wiring and pin-mapping documentation so that hardware changesdo not require rewriting the main README.

Software Setup

The software is intended to run on the Raspberry Pi.

The basic setup process is:



The software is divided into modules so that individual components canbe tested before running the complete autonomous program.

Version Control

GitHub is used as part of the engineering process rather than only as alocation for the final code.

Significant development changes should be recorded through meaningfulcommits.

Examples of useful commit messages include:



A useful commit should communicate what changed and, where relevant, whyit changed.

This allows the repository to show the engineering process instead ofonly presenting a final code dump.

Testing Workflow

Our standard testing workflow is:



This prevents random tuning and makes engineering decisions traceable.

Evidence-Based Engineering Decisions

Important decisions were based on observed robot behaviour and testing.

Motor

We selected the D360 + 22:1 gearbox because smaller alternatives did notprovide the required torque, while larger alternatives introducedunnecessary size and complexity.

Chassis

We selected LEGO because rapid modification and repair were importantduring development.

Camera

We selected the wide camera because the robot needs to observe the trackand obstacles ahead while driving.

IMU

We selected the BNO055 because orientation feedback is useful forsteering stability and parking alignment.

IR Sensors

We used IR sensors for close-range information where camera-basedpositioning becomes less reliable.

White Electronics Cover

We added the white cover after observing that the camera couldincorrectly interpret electronics as environmental features.

These decisions follow the engineering chain:



Final Performance Validation------------------------------------------------------------------------

Final Performance Validation

Current Open Challenge reference: approximately 35 seconds per open-round lap.

This is the main recorded performance figure currently available to us; other performance metrics are not presented as measured values unless they have been recorded.

The final robot is evaluated across the same major areas used duringdevelopment.



Full System

The final test is performed with all subsystems operating simultaneouslybecause individual subsystem success does not guarantee full-systemsuccess.

Final Robot

<img src="assets/final_design.svg" alt="Final robot architecture" width="850">

<table><tr><td align="center"><img src="assets/robot_front_card.png" width="240"><br><sub>Front</sub></td><td align="center"><img src="assets/robot_side_card.png" width="240"><br><sub>Side</sub></td><td align="center"><img src="assets/robot_top_card.png" width="240"><br><sub>Top</sub></td><td align="center"><img src="assets/robot_rear_card.png" width="240"><br><sub>Rear</sub></td></tr></table>



Our final robot is the result of repeated mechanical, electrical,sensor, and software iterations.

The final design combines:



The most important feature of the design is the interaction betweenthese systems.

The camera provides information about the environment.

The IMU provides information about robot orientation.

The IR sensors provide close-range feedback.

The software combines these inputs to determine the robot's state.

The control system converts that state into steering and speed commands.

The mechanical system then produces the physical movement.

This creates a closed-loop autonomous vehicle.

Engineering Philosophy

The main lesson from developing this robot was that making a robot workonce is different from engineering a robot that works repeatedly.

Our development therefore focused on:



Whenever possible, we followed:

Problem → Analysis → Solution → Test → Result

rather than simply changing components until the robot appeared to work.

Conclusion

BroCode's WRO Future Engineers robot was developed as an integratedengineering system rather than as a collection of individual components.

The mechanical system provides the stability and movement required bythe software.

The electrical system provides controlled and reliable power.

The sensors provide information about both the environment and therobot.

The software converts that information into decisions.

The control system converts those decisions into physical movement.

Testing connects all of these systems together and allows weaknesses tobe identified and corrected.

Our final design is the result of continuous iteration betweenmechanical design, electronics, sensing, software, and control.

The purpose of this repository is to preserve that engineering processand make the final robot understandable, reproducible, and useful toanyone who wants to study or build upon the project.

