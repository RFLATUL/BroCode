#!/usr/bin/env python3
from picamera2 import Picamera2
import cv2
import numpy as np
import time
import board
import adafruit_bno055
import RPi.GPIO as GPIO
import sys

# === I2C & sensors ===
i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)
prev_heading = None
total_heading = 0

# === YOUR hardware ===
MOTOR_PIN_1 = 24
MOTOR_PIN_2 = 23
MOTOR_ENA   = 18
SERVO_PIN   = 25
LEFT_BUMP   = 26
RIGHT_BUMP  = 12

# === Constants ===
X_RESOL, Y_RESOL = 1980, 350
X_MID = X_RESOL / 2

WALL_ROI_Y_START = 100

STEER_CENTER = 118
STEER_LEFT_LIMIT = 190
STEER_RIGHT_LIMIT = 60

SPEED_RUN = 255
SPEED_RUN_SLOW = 255
SPEED_INITIAL = 120
SPEED_OBSTACLE_CLOSE = 150
SPEED_OBSTACLE_FAR = 200
SPEED_OBSTACLE_APPROACH = 180
LAPS_GOAL = 3
EXPOSURE_TIME = 10000

BLACK_LOWER = np.array([0, 118, 118])
BLACK_UPPER = np.array([50, 138, 138])

LEFT_GAP_TARGET_CW  = 600
RIGHT_GAP_TARGET_CW = 600

LEFT_GAP_TARGET  = 250
RIGHT_GAP_TARGET = 780

LEFT_GAP_TARGET_CW  = 250
RIGHT_GAP_TARGET_CW = 780
WALL_GAIN = 0.017

# === Color detection (lap-line colors) ===
ORANGE_LOWER = np.array([60, 135, 140])
ORANGE_UPPER = np.array([255, 220, 255])

BLUE_LOWER = np.array([30, 140, 80])
BLUE_UPPER = np.array([60, 160, 105])

LINE_COOLDOWN = 2.0
last_line_time = 0
line_count = -1

CLOCKWISE = None
direction_confirmed = False
DIRECTION_DETECTION_FRAMES = 10  # Number of frames to confirm direction
direction_detection_counter = 0

# === Color detection (obstacle pillars) ===
OBSTACLE_GREEN_LOWER = np.array([20,   60, 100])
OBSTACLE_GREEN_UPPER = np.array([220, 115, 180])

OBSTACLE_RED_LOWER = np.array([31,  140, 126])
OBSTACLE_RED_UPPER = np.array([61, 170, 156])

# Only look for obstacles in this vertical band
OBSTACLE_ROI_Y_START = WALL_ROI_Y_START

OBSTACLE_AREA_MIN   = 800
OBSTACLE_AREA_CLOSE = 4000
OBSTACLE_AREA_FAR = 2000

# --- Obstacle avoidance ---
OBSTACLE_MIN_OFFSET = 15
OBSTACLE_MAX_OFFSET = 40
OBSTACLE_STEER_SIGN = 1

# Post-obstacle front wall suppression
obstacle_last_seen_time = 0
OBSTACLE_MEMORY_TIME = 2.0
last_obstacle_color = None

def get_obstacle_speed(area):
    """
    Calculate speed based on obstacle proximity (area).
    Larger area = closer obstacle = slower speed
    """
    if area >= OBSTACLE_AREA_CLOSE:
        return SPEED_OBSTACLE_CLOSE
    elif area >= OBSTACLE_AREA_FAR:
        ratio = (area - OBSTACLE_AREA_FAR) / (OBSTACLE_AREA_CLOSE - OBSTACLE_AREA_FAR)
        speed = SPEED_OBSTACLE_FAR - ratio * (SPEED_OBSTACLE_FAR - SPEED_OBSTACLE_CLOSE)
        return int(speed)
    else:
        return SPEED_OBSTACLE_APPROACH

def steering_for_obstacle(color, cx, area, left_x, right_x):
    """
    Position-based steering with wall awareness for obstacle avoidance.
    """
    centered = 1.0 - min(abs(cx - X_MID) / X_MID, 1.0)
    closeness = min(area / OBSTACLE_AREA_CLOSE, 1.0)
    urgency = max(centered, closeness)
    
    base_magnitude = OBSTACLE_MIN_OFFSET + (OBSTACLE_MAX_OFFSET - OBSTACLE_MIN_OFFSET) * urgency
    
    if color == "GREEN":
        obstacle_steer = STEER_CENTER + OBSTACLE_STEER_SIGN * base_magnitude
    else:  # RED
        obstacle_steer = STEER_CENTER - OBSTACLE_STEER_SIGN * base_magnitude
    
    # Wall awareness during obstacle
    if left_x is not None and right_x is not None:
        gap_center = (left_x + right_x) / 2
        err = gap_center - X_MID
        
        if CLOCKWISE:
            wall_steer = STEER_CENTER - err * 0.3
        else:
            wall_steer = STEER_CENTER + err * 0.3
        
        obstacle_weight = min(1.0, urgency * 1.5)
        wall_weight = 1.0 - obstacle_weight
        
        final_steer = obstacle_steer * obstacle_weight + wall_steer * wall_weight
        
    elif color == "GREEN" and left_x is not None:
        if CLOCKWISE:
            left_error = left_x - LEFT_GAP_TARGET_CW
        else:
            left_error = left_x - LEFT_GAP_TARGET
        
        if left_error < -100:
            final_steer = obstacle_steer * 0.4 + (STEER_CENTER + 10) * 0.6
        else:
            final_steer = obstacle_steer
            
    elif color == "RED" and right_x is not None:
        if CLOCKWISE:
            right_error = right_x - RIGHT_GAP_TARGET_CW
        else:
            right_error = right_x - RIGHT_GAP_TARGET
        
        if right_error > 100:
            final_steer = obstacle_steer * 0.4 + (STEER_CENTER - 10) * 0.6
        else:
            final_steer = obstacle_steer
            
    else:
        final_steer = obstacle_steer
    
    return final_steer

# === GPIO ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PIN_1, GPIO.OUT)
GPIO.setup(MOTOR_PIN_2, GPIO.OUT)
GPIO.setup(MOTOR_ENA, GPIO.OUT)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(LEFT_BUMP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RIGHT_BUMP, GPIO.IN, pull_up_down=GPIO.PUD_UP)

motor_pwm = GPIO.PWM(MOTOR_ENA, 1000)
motor_pwm.start(0)
servo_pwm = GPIO.PWM(SERVO_PIN, 50)
servo_pwm.start(7.5)

# === Camera ===
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": "RGB888", "size": (X_RESOL, Y_RESOL)}))
picam2.preview_configuration.controls.FrameRate = 30
picam2.configure(picam2.preview_configuration)
picam2.set_controls({"AeEnable": False, "ExposureTime": EXPOSURE_TIME, "AnalogueGain": 4.0})
picam2.start()
time.sleep(1)

# === Control ===
def steer(angle):
    angle = max(STEER_RIGHT_LIMIT, min(STEER_LEFT_LIMIT, angle))
    servo_pwm.ChangeDutyCycle(2 + angle / 18)
    return angle

def run(speed):
    GPIO.output(MOTOR_PIN_1, GPIO.HIGH)
    GPIO.output(MOTOR_PIN_2, GPIO.LOW)
    motor_pwm.ChangeDutyCycle(speed / 2.55)

def back(speed):
    GPIO.output(MOTOR_PIN_1, GPIO.LOW)
    GPIO.output(MOTOR_PIN_2, GPIO.HIGH)
    motor_pwm.ChangeDutyCycle(speed / 2.55)

def stop_motors():
    motor_pwm.ChangeDutyCycle(0)
    GPIO.output(MOTOR_PIN_1, GPIO.LOW)
    GPIO.output(MOTOR_PIN_2, GPIO.LOW)

def stop_robot():
    stop_motors()
    steer(STEER_CENTER)

def reset_heading():
    global prev_heading, total_heading
    prev_heading = None
    total_heading = 0

def get_heading():
    global total_heading, prev_heading
    try:
        current_heading = sensor.euler[0]
        if prev_heading is None:
            prev_heading = current_heading
            return 0
        delta = current_heading - prev_heading
        if delta > 180:
            delta -= 360
        elif delta < -180:
            delta += 360
        prev_heading = current_heading
        total_heading += delta
        return delta
    except Exception:
        return 0

# === Wall detection (with front wall suppression) ===
def detect_walls(lab_frame, display, suppress_front_wall=False):
    # 1. LAB black mask
    black_mask = cv2.inRange(lab_frame, BLACK_LOWER, BLACK_UPPER)

    # 2. Y ROI
    wall_mask = black_mask[WALL_ROI_Y_START:Y_RESOL, :]
    image_width = wall_mask.shape[1]
    mid = image_width // 2

    if image_width < 2:
        return None, None, False

    # 3. Find contours
    kernel = np.ones((15, 15), np.uint8)
    processed = cv2.morphologyEx(wall_mask, cv2.MORPH_CLOSE, kernel)
    processed = cv2.morphologyEx(processed, cv2.MORPH_DILATE, kernel)
    contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 4. Find large front wall (unless suppressed)
    front_wall = False
    if not suppress_front_wall:
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 1000:
                continue

            x, y, w, h = cv2.boundingRect(contour)
            y_display = y + WALL_ROI_Y_START
            width_ratio = w / float(image_width)
            cx = x + w / 2

            if (width_ratio > 0.55 and
                cx > image_width * 0.25 and
                cx < image_width * 0.75):
                front_wall = True
                cv2.rectangle(display, (x, y_display), (x + w, y_display + h), (0, 0, 255), 3)
                cv2.putText(display, "FRONT WALL", (x, max(y_display - 10, 20)),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                break
    else:
        # Still draw detected front walls but don't trigger
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 1000:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            width_ratio = w / float(image_width)
            cx = x + w / 2
            if (width_ratio > 0.55 and
                cx > image_width * 0.25 and
                cx < image_width * 0.75):
                y_display = y + WALL_ROI_Y_START
                cv2.rectangle(display, (x, y_display), (x + w, y_display + h), (128, 128, 128), 3)
                cv2.putText(display, "FRONT (SUPPRESSED)", (x, max(y_display - 10, 20)),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (128, 128, 128), 2)

    # 5. If front wall and not suppressed, return early
    if front_wall:
        return None, None, True

    # 6. Normal side-wall detection
    left_half = processed[:, :mid]
    right_half = processed[:, mid:]

    left_contours, _ = cv2.findContours(left_half, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    right_contours, _ = cv2.findContours(right_half, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    left_x = None
    right_x = None
    max_left_y = 0
    max_right_y = 0

    # LEFT WALL
    for contour in left_contours:
        area = cv2.contourArea(contour)
        if area < 1000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cy = y + h // 2
        if cy > max_left_y:
            max_left_y = cy
            left_x = x + w
            cv2.rectangle(display, (x, y + WALL_ROI_Y_START),
                         (x + w, y + h + WALL_ROI_Y_START), (0, 255, 255), 2)

    # RIGHT WALL
    for contour in right_contours:
        area = cv2.contourArea(contour)
        if area < 1000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        x_full = x + mid
        cy = y + h // 2
        if cy > max_right_y:
            max_right_y = cy
            right_x = x_full
            cv2.rectangle(display, (x_full, y + WALL_ROI_Y_START),
                         (x_full + w, y + h + WALL_ROI_Y_START), (0, 255, 255), 2)

    return left_x, right_x, False

# === Obstacle (pillar) detection ===
def detect_obstacles(lab_frame, display):
    roi = lab_frame[OBSTACLE_ROI_Y_START:Y_RESOL, :]

    green_mask = cv2.inRange(roi, OBSTACLE_GREEN_LOWER, OBSTACLE_GREEN_UPPER)
    red_mask = cv2.inRange(roi, OBSTACLE_RED_LOWER, OBSTACLE_RED_UPPER)

    kernel = np.ones((9, 9), np.uint8)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)

    best_color, best_cx, best_area = None, None, 0

    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in green_contours:
        area = cv2.contourArea(cnt)
        if area > OBSTACLE_AREA_MIN and area > best_area:
            x, y, w, h = cv2.boundingRect(cnt)
            y_display = y + OBSTACLE_ROI_Y_START
            best_area, best_color, best_cx = area, "GREEN", x + w / 2
            cv2.rectangle(display, (x, y_display), (x + w, y_display + h), (0, 255, 0), 3)
            cv2.putText(display, "GREEN - PASS LEFT", (x, max(y_display - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in red_contours:
        area = cv2.contourArea(cnt)
        if area > OBSTACLE_AREA_MIN and area > best_area:
            x, y, w, h = cv2.boundingRect(cnt)
            y_display = y + OBSTACLE_ROI_Y_START
            best_area, best_color, best_cx = area, "RED", x + w / 2
            cv2.rectangle(display, (x, y_display), (x + w, y_display + h), (0, 0, 255), 3)
            cv2.putText(display, "RED - PASS RIGHT", (x, max(y_display - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    return best_color, best_cx, best_area

# === Color line detection with proximity-based direction ===
def detect_color_line(frame, display):
    global last_line_time, line_count, CLOCKWISE, direction_confirmed, direction_detection_counter
    
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    
    # Orange detection
    orange_mask = cv2.inRange(lab, ORANGE_LOWER, ORANGE_UPPER)
    orange_mask = cv2.morphologyEx(orange_mask, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))
    orange_mask = cv2.morphologyEx(orange_mask, cv2.MORPH_CLOSE, np.ones((15,15), np.uint8))
    
    # Blue detection
    blue_mask = cv2.inRange(lab, BLUE_LOWER, BLUE_UPPER)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_CLOSE, np.ones((15,15), np.uint8))
    
    # Find the lowest (closest to robot) contour for each color
    orange_lowest_y = Y_RESOL  # Initialize to bottom of frame
    blue_lowest_y = Y_RESOL
    orange_detected = False
    blue_detected = False
    orange_largest_area = 0
    blue_largest_area = 0
    
    # Check orange - find lowest contour (closest to robot)
    orange_contours, _ = cv2.findContours(orange_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in orange_contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            orange_detected = True
            x, y, w, h = cv2.boundingRect(cnt)
            # The bottom of the contour (y+h) is closest to robot
            bottom_y = y + h
            if bottom_y > orange_lowest_y:  # Lower in frame = closer to robot
                orange_lowest_y = bottom_y
            if area > orange_largest_area:
                orange_largest_area = area
            cv2.rectangle(display, (x, y), (x+w, y+h), (0, 165, 255), 2)
            cv2.putText(display, f"ORANGE (y={bottom_y})", (x, y-5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 1)
    
    # Check blue - find lowest contour (closest to robot)
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in blue_contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            blue_detected = True
            x, y, w, h = cv2.boundingRect(cnt)
            bottom_y = y + h
            if bottom_y > blue_lowest_y:
                blue_lowest_y = bottom_y
            if area > blue_largest_area:
                blue_largest_area = area
            cv2.rectangle(display, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(display, f"BLUE (y={bottom_y})", (x, y-5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    
    current_time = time.time()
    
    # AUTO-DETECT DIRECTION based on which color is closer to robot (lower in frame)
    if CLOCKWISE is None and (orange_detected or blue_detected):
        direction_detection_counter += 1
        
        # Need consistent detection over multiple frames to confirm
        if direction_detection_counter >= DIRECTION_DETECTION_FRAMES:
            # Blue is lower in frame (closer to robot) -> CCW
            # Orange is lower in frame (closer to robot) -> CW
            if blue_detected and orange_detected:
                if blue_lowest_y > orange_lowest_y:
                    # Blue is closer (lower in frame) -> CCW
                    CLOCKWISE = False
                    direction_confirmed = True
                    last_line_time = current_time
                    line_count += 1
                    print("=" * 50)
                    print(f">>> BLUE is closer (y={blue_lowest_y} vs orange y={orange_lowest_y}) <<<")
                    print(">>> Direction: COUNTERCLOCKWISE <<<")
                    print(">>> Running at FULL SPEED now <<<")
                    print("=" * 50)
                elif orange_lowest_y > blue_lowest_y:
                    # Orange is closer (lower in frame) -> CW
                    CLOCKWISE = True
                    direction_confirmed = True
                    last_line_time = current_time
                    line_count += 1
                    print("=" * 50)
                    print(f">>> ORANGE is closer (y={orange_lowest_y} vs blue y={blue_lowest_y}) <<<")
                    print(">>> Direction: CLOCKWISE <<<")
                    print(">>> Running at FULL SPEED now <<<")
                    print("=" * 50)
            elif blue_detected and not orange_detected:
                # Only blue visible -> CCW
                CLOCKWISE = False
                direction_confirmed = True
                last_line_time = current_time
                line_count += 1
                print("=" * 50)
                print(">>> Only BLUE detected! Direction: COUNTERCLOCKWISE <<<")
                print(">>> Running at FULL SPEED now <<<")
                print("=" * 50)
            elif orange_detected and not blue_detected:
                # Only orange visible -> CW
                CLOCKWISE = True
                direction_confirmed = True
                last_line_time = current_time
                line_count += 1
                print("=" * 50)
                print(">>> Only ORANGE detected! Direction: CLOCKWISE <<<")
                print(">>> Running at FULL SPEED now <<<")
                print("=" * 50)
    
    # Count lines after direction confirmed
    elif direction_confirmed:
        if CLOCKWISE:
            # CW mode: only count orange lines
            if orange_detected and current_time - last_line_time > LINE_COOLDOWN:
                line_count += 1
                last_line_time = current_time
                print(f"Line {line_count} (ORANGE) - Lap {line_count // 4}")
        else:
            # CCW mode: only count blue lines
            if blue_detected and current_time - last_line_time > LINE_COOLDOWN:
                line_count += 1
                last_line_time = current_time
                print(f"Line {line_count} (BLUE) - Lap {line_count // 4}")
    
    return orange_detected, blue_detected

# === Should we suppress front wall? ===
def should_suppress_front_wall():
    """
    Suppress front wall detection when:
    - CW mode + RED obstacle recently seen (robot turned right, inner right wall appears as front wall)
    - CCW mode + GREEN obstacle recently seen (robot turned left, inner left wall appears as front wall)
    """
    if time.time() - obstacle_last_seen_time > OBSTACLE_MEMORY_TIME:
        return False
    if last_obstacle_color is None:
        return False
    
    if CLOCKWISE and last_obstacle_color == "RED":
        return True
    elif not CLOCKWISE and last_obstacle_color == "GREEN":
        return True
    
    return False

# === Setup ===
print("=" * 50)
print("WRO Open Challenge - PROXIMITY-BASED DIRECTION")
print("=" * 50)
print("Direction determined by which color appears")
print("CLOSER to robot (lower in frame):")
print("  BLUE closer -> COUNTERCLOCKWISE (counts blue)")
print("  ORANGE closer -> CLOCKWISE (counts orange)")
print("Features:")
print("  - Smart front wall suppression after obstacles")
print("  - Speed control based on obstacle proximity")
print("  - Wall-aware obstacle avoidance")
print("=" * 50)
sys.stdout.flush()

print("\nPress ENTER to start...")
input()

print("Starting in 3 seconds...")
for i in range(3, 0, -1):
    print(i)
    time.sleep(1)
print("GO!")

reset_heading()
laps_completed = 0
start_time = time.time()
last_line_time = time.time()

try:
    while time.time() - start_time < 180:
        frame = picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        lab_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        blur = cv2.GaussianBlur(lab_frame, (5, 5), 0)
        display = frame.copy()

        # Check if we should suppress front wall
        suppress_fw = should_suppress_front_wall()
        
        left_x, right_x, front_wall = detect_walls(blur, display, suppress_front_wall=suppress_fw)
        obstacle_color, obstacle_cx, obstacle_area = detect_obstacles(blur, display)
        orange_seen, blue_seen = detect_color_line(frame, display)
        
        laps_completed = line_count // 4

        # Update obstacle memory
        if obstacle_color is not None:
            obstacle_last_seen_time = time.time()
            last_obstacle_color = obstacle_color

        # --- Choose speed/steering ---
        if obstacle_color is not None:
            # Obstacle avoidance with wall awareness and speed control
            ang = steering_for_obstacle(obstacle_color, obstacle_cx, obstacle_area, left_x, right_x)
            current_speed = get_obstacle_speed(obstacle_area)
            
            side = "LEFT" if obstacle_color == "GREEN" else "RIGHT"
            proximity = "CLOSE" if obstacle_area >= OBSTACLE_AREA_CLOSE else "FAR" if obstacle_area < OBSTACLE_AREA_FAR else "MED"
            mode = f"{obstacle_color} OBSTACLE [{proximity}] - PASS {side} (area={int(obstacle_area)})"
            if left_x is not None or right_x is not None:
                mode += " [WALL-AWARE]"

        elif not direction_confirmed:
            current_speed = SPEED_INITIAL
            ang = STEER_CENTER + 10
            if CLOCKWISE is None and (orange_seen or blue_seen):
                mode = f"DETECTING... Orange(y={Y_RESOL}) Blue(y={Y_RESOL})"
            else:
                mode = "DETECTING DIRECTION..."
        else:
            current_speed = SPEED_RUN if (left_x is not None and right_x is not None) else SPEED_RUN_SLOW
            
            # --- Navigation ---
            if not CLOCKWISE:
                # CCW MODE
                if front_wall:
                    ang = STEER_CENTER + 30
                    mode = "FRONT WALL - TURN RIGHT"
                elif left_x is not None and left_x > 540:
                    ang = STEER_CENTER - 30
                    mode = "LEFT WALL CLOSE - TURN RIGHT"
                elif right_x is not None and right_x < 540:
                    ang = STEER_CENTER + 25
                    mode = "RIGHT WALL CLOSE - TURN LEFT"
                elif left_x is not None and right_x is not None:
                    gap_center = (left_x + right_x) / 2
                    err = gap_center - X_MID
                    ang = STEER_CENTER - err * 0.3
                    mode = "BOTH WALLS - CENTER"
                elif left_x is not None:
                    ang = STEER_CENTER + (left_x - LEFT_GAP_TARGET) * WALL_GAIN
                    mode = "LEFT WALL"
                elif right_x is not None:
                    ang = STEER_CENTER + (right_x - RIGHT_GAP_TARGET) * WALL_GAIN
                    mode = "RIGHT WALL"
                else:
                    ang = STEER_CENTER + 15
                    mode = "NO WALL"
            else:
                # CW MODE
                if front_wall:
                    ang = STEER_CENTER - 30
                    mode = "FRONT WALL - TURN LEFT"
                elif left_x is not None and left_x > 700:
                    ang = STEER_CENTER - 25
                    mode = "LEFT WALL CLOSE - TURN RIGHT"
                elif right_x is not None and right_x < 580:
                    ang = STEER_CENTER + 25
                    mode = "RIGHT WALL CLOSE - TURN LEFT"
                elif left_x is not None and right_x is not None:
                    gap_center = (left_x + right_x) / 2
                    err = gap_center - X_MID
                    ang = STEER_CENTER - err * 0.3
                    mode = "BOTH WALLS - CENTER"
                elif left_x is not None:
                    ang = STEER_CENTER - (left_x - LEFT_GAP_TARGET_CW) * WALL_GAIN
                    mode = "LEFT WALL"
                elif right_x is not None:
                    ang = STEER_CENTER - (right_x - RIGHT_GAP_TARGET_CW) * WALL_GAIN
                    mode = "RIGHT WALL"
                else:
                    ang = STEER_CENTER - 15
                    mode = "NO WALL"

        ang = steer(ang)
        run(current_speed)

        # --- Bump sensors ---
        if GPIO.input(LEFT_BUMP) == GPIO.LOW:
            mode = "BUMP LEFT"
            stop_robot()
            time.sleep(0.2)
            steer(STEER_CENTER + 20)
            back(120)
            time.sleep(0.4)
        elif GPIO.input(RIGHT_BUMP) == GPIO.LOW:
            mode = "BUMP RIGHT"
            stop_robot()
            time.sleep(0.2)
            steer(STEER_CENTER - 20)
            back(120)
            time.sleep(0.4)

        # --- Check lap goal ---
        if laps_completed >= LAPS_GOAL:
            print(f"\n{LAPS_GOAL} laps completed! Stopping...")
            stop_robot()
            break

        # --- Display ---
        if not direction_confirmed:
            if CLOCKWISE is None:
                dir_text = "DETECTING..."
            else:
                dir_text = "CONFIRMING..."
            speed_text = f"SLOW ({SPEED_INITIAL})"
        else:
            dir_text = "CW" if CLOCKWISE else "CCW"
            speed_text = f"{current_speed}"
        
        suppress_text = " [FW SUPPRESSED]" if suppress_fw else ""
        cv2.putText(display, f"Dir: {dir_text} | Speed: {speed_text}{suppress_text}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display, mode, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(display, f"steer={ang} laps={laps_completed} lines={line_count}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(display, f"Orange={orange_seen} Blue={blue_seen}", (10, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        cv2.putText(display, f"Obstacle={obstacle_color} area={int(obstacle_area)}", (10, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        if suppress_fw:
            cv2.putText(display, f"Last obstacle: {last_obstacle_color}", 
                       (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        if obstacle_color is not None:
            if obstacle_area >= OBSTACLE_AREA_CLOSE:
                speed_label = "SLOW"
            elif obstacle_area >= OBSTACLE_AREA_FAR:
                speed_label = "MEDIUM"
            else:
                speed_label = "FAST"
            cv2.putText(display, f"Obstacle speed: {speed_label} ({current_speed})", 
                       (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        cv2.imshow("Camera", display)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_robot()
            break

        time.sleep(0.03)

except KeyboardInterrupt:
    pass

finally:
    stop_robot()
    cv2.destroyAllWindows()
    picam2.stop()
    GPIO.cleanup()

dir_text = "CW" if CLOCKWISE else "CCW" if CLOCKWISE is not None else "UNKNOWN"
print(f"\nRound finished - {laps_completed} laps ({dir_text})")
