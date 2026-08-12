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

![Evidence-based engineering decision chain](../12_MEDIA/assets/28_decision_chain.svg)

------------------------------------------------------------------------
