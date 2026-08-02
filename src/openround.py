import cv2
import numpy as np
import RPi.GPIO as GPIO
from picamera2 import Picamera2
from time import sleep
import time

CLOCKWISE = None
LINE_COOLDOWN = 1.2
blue_detected = False
orange_detected = False
line_count = 0

# --- LAP / LINE CONFIG -----------------------------------------
# LINES_PER_LAP = how many gate detections happen per single lap.
# On most single-gate tracks this is 1 (robot only passes the
# blue/orange marker once per lap). If your track has multiple
# color markers per lap, change LINES_PER_LAP accordingly.
LAPS_TO_COMPLETE = 3
LINES_PER_LAP = 4   # robot crosses the same line 4x before 1 lap counts as done
total_lines = LAPS_TO_COMPLETE * LINES_PER_LAP
# -----------------------------------------------------------------

last_orange_time = 0.0
last_blue_time = 0.0
last_line_time = 0.0
prev_marker_seen = False   # tracks whether the marker was visible last frame

KP = 0.02

# === Pin and hardware config ===
MOTOR_PIN_1 = 24   # direction pin A
MOTOR_PIN_2 = 23   # direction pin B
MOTOR_ENA = 18     # PWM speed (enable) pin
SERVO_PIN = 25

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(MOTOR_PIN_1, GPIO.OUT)
GPIO.setup(MOTOR_PIN_2, GPIO.OUT)
GPIO.setup(MOTOR_ENA, GPIO.OUT)
GPIO.setup(SERVO_PIN, GPIO.OUT)

motor_pwm = GPIO.PWM(MOTOR_ENA, 1000)
motor_pwm.start(0)

servo_pwm = GPIO.PWM(SERVO_PIN, 50)
servo_pwm.start(0)

CENTER = 120 # 98
LEFT = 190 # 70
RIGHT = 60 # 130

last_angle = -1

current_angle = CENTER
last_servo_time = 0
last_valid_angle = CENTER   # holds steering steady while the marker is in view

# === Real-time status, updated every frame for the on-screen overlay ===
current_mode = "IDLE"          # which steering branch fired this frame
current_steer_angle = CENTER   # angle actually sent to steer() this frame


def steer(angle):
    low, high = min(LEFT, RIGHT), max(LEFT, RIGHT)
    angle = max(low, min(high, angle))        # Limit angle, order-independent

    duty = 2.5 + (angle / 180.0) * 10.0
    servo_pwm.ChangeDutyCycle(duty)
    sleep(0.05)
    servo_pwm.ChangeDutyCycle(0)

def forward(speed):
    # If your motor moves backwards, swap which pin gets HIGH vs LOW
    GPIO.output(MOTOR_PIN_1, GPIO.HIGH)
    GPIO.output(MOTOR_PIN_2, GPIO.LOW)
    motor_pwm.ChangeDutyCycle(speed)

def back(speed):
    GPIO.output(MOTOR_PIN_1, GPIO.LOW)
    GPIO.output(MOTOR_PIN_2, GPIO.HIGH)
    motor_pwm.ChangeDutyCycle(speed)

def stop():
    motor_pwm.ChangeDutyCycle(0)
    GPIO.output(MOTOR_PIN_1, GPIO.LOW)
    GPIO.output(MOTOR_PIN_2, GPIO.LOW)


def draw_dashed_vline(img, x, y1, y2, color, dash_len=10, gap_len=6, thickness=1):
    """OpenCV has no built-in dashed line, so this steps down the column
    in dash/gap segments manually."""
    y = y1
    while y < y2:
        y_end = min(y + dash_len, y2)
        cv2.line(img, (x, y), (x, y_end), color, thickness)
        y += dash_len + gap_len


def draw_status_overlay(output, mode, angle, left_target, right_target,
                         blue_detected, orange_detected, clockwise,
                         line_count, total_lines):
    """Draws a live status panel in the top-left corner of the display
    window: current steering mode/angle, which walls and markers are
    detected this frame, direction, and lap progress."""
    h, w = output.shape[:2]

    panel_w, panel_h = 360, 150
    overlay = output.copy()
    cv2.rectangle(overlay, (0, 0), (panel_w, panel_h), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.55, output, 0.45, 0, output)

    MODE_COLORS = {
        "BOTH WALLS": (0, 220, 220),
        "LEFT WALL":  (255, 180, 0),
        "RIGHT WALL": (0, 140, 255),
        "NO WALL":    (0, 0, 255),
        "IDLE":       (150, 150, 150),
    }
    color = MODE_COLORS.get(mode, (255, 255, 255))

    y = 22
    cv2.putText(output, f"MODE: {mode}", (10, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    y += 26
    cv2.putText(output, f"STEER ANGLE: {angle:.1f}", (10, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
    y += 24
    cv2.putText(output,
                f"LEFT WALL: {'YES' if left_target else 'no'}   "
                f"RIGHT WALL: {'YES' if right_target else 'no'}",
                (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    y += 22
    cv2.putText(output,
                f"BLUE: {'YES' if blue_detected else 'no'}   "
                f"ORANGE: {'YES' if orange_detected else 'no'}",
                (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    y += 22
    dir_label = "unknown" if clockwise is None else ("CW / orange" if clockwise else "CCW / blue")
    cv2.putText(output, f"DIRECTION: {dir_label}", (10, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    y += 22
    cv2.putText(output, f"LAPS: line {line_count}/{total_lines}", (10, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)


# ============================================================
# START
# ============================================================

# ==========================================================
# CAMERA SETTINGS
# ==========================================================
WIDTH = 1920
HEIGHT = 680
X_MID = WIDTH // 2

BLACK_LOWER = np.array([0,118,118])
BLACK_UPPER = np.array([75,138,138])

BLUE_LOWER = np.array([0, 120, 80])
BLUE_UPPER = np.array([255, 150, 120])

ORANGE_LOWER = np.array([140, 120, 145])
ORANGE_UPPER = np.array([210, 155, 210])

picam2 = Picamera2()

config = picam2.create_preview_configuration(
    main={"size": (WIDTH, HEIGHT), "format": "RGB888"}
)

picam2.configure(config)

picam2.start()

print("Auto adjusting camera...")
picam2.set_controls({
    "AeEnable": True,
    "AwbEnable": True
})

time.sleep(2)

meta = picam2.capture_metadata()

exp = meta["ExposureTime"]
gain = meta["AnalogueGain"]

picam2.set_controls({
    "AeEnable": False,
    "AwbEnable": False,
    "ExposureTime": exp,
    "AnalogueGain": gain
})

print("Camera locked")
print("Exposure:", exp)
print("Gain:", gain)

clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8,8))
kernel = np.ones((5,5), np.uint8)

fps_time = time.time()

steer(CENTER)
sleep(1)
forward(45) # 60s = 0.02kp

print(f"Robot Started - will stop after {LAPS_TO_COMPLETE} laps ({total_lines} gate crossings)")
#video = cv2.VideoWriter(f"output{timestamp}.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 20, (WIDTH, HEIGHT))
while True:

# Turn PWM off after 30 ms
    if time.time() - last_servo_time > 0.03:
        servo_pwm.ChangeDutyCycle(0)

    frame = picam2.capture_array()
    frame = cv2.GaussianBlur(frame, (5,5), 0)

    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    l,a,b = cv2.split(lab)
    l = clahe.apply(l)
    lab = cv2.merge((l,a,b))

    black_mask = cv2.inRange(lab, BLACK_LOWER, BLACK_UPPER)

    # Build an exclusion mask for the orange marker FIRST, so we can
    # remove those pixels from the black line mask. Keep this tight -
    # only the marker's own pixels, no padding - so we don't eat into
    # real track-line pixels right where a turn might be happening.
    orange_exclude = cv2.inRange(lab, ORANGE_LOWER, ORANGE_UPPER)
    orange_exclude = cv2.morphologyEx(orange_exclude, cv2.MORPH_CLOSE, np.ones((5,5), np.uint8))
    black_mask = cv2.bitwise_and(black_mask, cv2.bitwise_not(orange_exclude))

    black_mask = cv2.morphologyEx(black_mask, cv2.MORPH_OPEN, kernel)
    black_mask = cv2.morphologyEx(black_mask, cv2.MORPH_CLOSE, kernel)
    black_mask = cv2.dilate(black_mask, kernel, iterations=1)
       
    black_contours, _ = cv2.findContours(black_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    output = frame.copy()

    # Debug aid: vertical line at X_MID — makes it easy to see at a glance
    # how far each wall target / marker sits from center while tuning,
    # instead of having to read raw pixel coordinates off the terminal.
    cv2.line(output, (X_MID, 0), (X_MID, HEIGHT), (0, 255, 255), 1)
    cv2.putText(output, "CENTER", (X_MID + 6, HEIGHT - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    # Dashed reference lines at the two single-wall steering targets — the
    # left-wall formula steers to converge only_x toward 200, the
    # right-wall formula toward WIDTH-200. Seeing these columns makes it
    # obvious whether a given angle pushed the wall target toward or away
    # from where it's actually supposed to settle.
    draw_dashed_vline(output, 200, 0, HEIGHT, (255, 180, 0))
    cv2.putText(output, "L TARGET", (206, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 180, 0), 1)
    draw_dashed_vline(output, WIDTH - 200, 0, HEIGHT, (0, 140, 255))
    cv2.putText(output, "R TARGET", (WIDTH - 200 + 6, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 140, 255), 1)
    
    left_target = None
    right_target = None

    left_bottom = -1
    right_bottom = -1

    for cnt in black_contours:
        area = cv2.contourArea(cnt)
        if area < 3000:
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(output, (x, y), (x+w, y+h), (255,255,0), 2)
        cx = x + w//2
        bottom = y + h
        if cx < X_MID:
            if bottom > left_bottom:
                left_bottom = bottom
                left_target = (x+w, bottom)
                cv2.circle(output, left_target, 8, (255,0,0), -1)
        else:
            if bottom > right_bottom:
                right_bottom = bottom
                right_target = (x, bottom)
                cv2.circle(output, right_target, 8, (0,0,255), -1)
                
    blue_detected = False                    
    blue_mask = cv2.inRange(lab, BLUE_LOWER, BLUE_UPPER)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_CLOSE, kernel)
    blue_mask = cv2.dilate(blue_mask, kernel, iterations=1)
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if blue_contours:
        largest = max(blue_contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)
        if area > 800:        
            x, y, w, h = cv2.boundingRect(largest)
            if (x+w) > 300:
                blue_detected = True
            cv2.rectangle(output, (x, y), (x+w, y+h), (255,0,0), 2)
        
    orange_detected = False
    orange_mask = cv2.inRange(lab, ORANGE_LOWER, ORANGE_UPPER)
    orange_mask = cv2.morphologyEx(orange_mask, cv2.MORPH_OPEN, kernel)
    orange_mask = cv2.morphologyEx(
        orange_mask,
        cv2.MORPH_CLOSE,
        np.ones((21,21), np.uint8)
    )
    orange_mask = cv2.dilate(
        orange_mask,
        np.ones((15,15), np.uint8),
        iterations=2
    )
    orange_contours, _ = cv2.findContours(orange_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    all_points = []

    for cnt in orange_contours:
        if cv2.contourArea(cnt) > 50:
            all_points.append(cnt)

    if all_points:
        merged = np.vstack(all_points)
        x, y, w, h = cv2.boundingRect(merged)
        total_area = sum(cv2.contourArea(c) for c in all_points)
        if total_area > 800:
            orange_detected = True
        cv2.rectangle(output, (x, y), (x+w, y+h), (0,165,255), 2)
    
    current_time = time.time()

    if CLOCKWISE is None:
        # Whichever color shows up FIRST wins - that color is used for
        # ALL future counting. The other color is permanently ignored
        # for the rest of the run.
        if orange_detected:
            CLOCKWISE = True
            last_line_time = current_time
            print("First line seen: ORANGE -> counting orange only, blue ignored")

        elif blue_detected:
            CLOCKWISE = False
            last_line_time = current_time
            print("First line seen: BLUE -> counting blue only, orange ignored")

    else:
        if CLOCKWISE:
            marker_seen = orange_detected   # blue is ignored from here on
        else:
            marker_seen = blue_detected     # orange is ignored from here on

        if marker_seen and not prev_marker_seen and current_time - last_line_time > LINE_COOLDOWN:
            line_count += 1
            last_line_time = current_time
            #print("Line :", line_count)
        prev_marker_seen = marker_seen
    if line_count >= total_lines:
        steer(CENTER)
        stop()
        print(f"{LAPS_TO_COMPLETE} laps complete - stopping")
        break
    print(f"Line {line_count} / {total_lines}  (lap {line_count // LINES_PER_LAP} of {LAPS_TO_COMPLETE})")

    if left_target and right_target:

        left_x, left_y = left_target
        right_x, right_y = right_target

        left_distance = left_x
        right_distance = WIDTH - right_x

        error = left_distance - right_distance

        angle = CENTER - error * KP

        steer(angle)
        last_valid_angle = angle
        current_mode = "BOTH WALLS"
        current_steer_angle = angle

    elif left_target:

        only_x, _ = left_target

        angle = CENTER - ((only_x - 200) * KP)

        steer(angle)
        last_valid_angle = angle
        current_mode = "LEFT WALL"
        current_steer_angle = angle

    elif right_target:

        only_x, _ = right_target

        angle = CENTER - ((only_x - (WIDTH - 200)) * KP)

        steer(angle)
        last_valid_angle = angle
        current_mode = "RIGHT WALL"
        current_steer_angle = angle

    else:
        current_mode = "NO WALL"
        if CLOCKWISE:
            steer(CENTER-40)
            current_steer_angle = CENTER-40

        else:
            steer(CENTER+40)
            current_steer_angle = CENTER+40

    # Print the same status to the terminal every frame, and draw it on
    # the display window so it's visible in real time while the robot runs.
    print(f"[{current_mode}] angle={current_steer_angle:.1f}  "
          f"L={'Y' if left_target else 'n'} R={'Y' if right_target else 'n'}  "
          f"blue={'Y' if blue_detected else 'n'} orange={'Y' if orange_detected else 'n'}")

    draw_status_overlay(output, current_mode, current_steer_angle,
                         left_target, right_target,
                         blue_detected, orange_detected, CLOCKWISE,
                         line_count, total_lines)

    cv2.imshow("Original", output)
    #cv2.imshow("Mask", mask)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        steer(CENTER)
        stop()
        #video.release()
        break

cv2.destroyAllWindows()
picam2.stop()
