import RPi.GPIO as GPIO
from time import sleep
import threading
import logging
from datetime import datetime

# Setup logger
logger = logging.getLogger('robot_logger')
logger.setLevel(logging.INFO)
log_messages = []

# Set up GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Motor pins
LEFT_FORWARD = 36
LEFT_BACKWARD = 33
RIGHT_FORWARD = 31
RIGHT_BACKWARD = 40

# Line sensor pins
LEFT_SENSOR = 16
RIGHT_SENSOR = 32

# Threading control
movement_thread = None
stop_event = threading.Event()

def log_movement(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = f"{timestamp} - {message}"
    log_messages.append(log_entry)
    # if len(log_messages) > 1000:  # Keep only last 50 messages
    #     log_messages.pop(0)
    logger.info(message)

# Setup all pins
def setup_robot():
    # Setup motor pins as output
    log_movement("Setup Motor")
    GPIO.setup(LEFT_FORWARD, GPIO.OUT)
    GPIO.setup(LEFT_BACKWARD, GPIO.OUT)
    GPIO.setup(RIGHT_FORWARD, GPIO.OUT)
    GPIO.setup(RIGHT_BACKWARD, GPIO.OUT)
    
    # Setup sensor pins as input
    GPIO.setup(LEFT_SENSOR, GPIO.IN)
    GPIO.setup(RIGHT_SENSOR, GPIO.IN)

# Basic movement functions
def continuous_forward():
    log_movement(" ^ ^ ^ - Moving forward")
    GPIO.output(LEFT_FORWARD, True)
    GPIO.output(RIGHT_FORWARD, True)
    GPIO.output(LEFT_BACKWARD, False)
    GPIO.output(RIGHT_BACKWARD, False)
    sleep(0.1)

def continuous_backward():
    log_movement(" v v v - Moving backward")
    GPIO.output(LEFT_FORWARD, False)
    GPIO.output(RIGHT_FORWARD, False)
    GPIO.output(LEFT_BACKWARD, True)
    GPIO.output(RIGHT_BACKWARD, True)
    sleep(0.1)

def turn_left():
    log_movement(" < < < - Turning left")
    GPIO.output(LEFT_FORWARD, False)
    GPIO.output(RIGHT_FORWARD, True)
    GPIO.output(LEFT_BACKWARD, False)
    GPIO.output(RIGHT_BACKWARD, False)
    

def turn_right():
    log_movement(" > > > - Turning right")
    GPIO.output(LEFT_FORWARD, True)
    GPIO.output(RIGHT_FORWARD, False)
    GPIO.output(LEFT_BACKWARD, False)
    GPIO.output(RIGHT_BACKWARD, False)

def stop():
    stop_event.set()
    if movement_thread and movement_thread.is_alive():
        movement_thread.join()
    log_movement(" . . . - Stopping")
    GPIO.output(LEFT_FORWARD, False)
    GPIO.output(RIGHT_FORWARD, False)
    GPIO.output(LEFT_BACKWARD, False)
    GPIO.output(RIGHT_BACKWARD, False)
    stop_event.clear()

def follow_line():
    while not stop_event.is_set():
        left_sensor = GPIO.input(LEFT_SENSOR)
        right_sensor = GPIO.input(RIGHT_SENSOR)
        if left_sensor == 1 and right_sensor == 1:
            log_movement("Both sensors on the line - Moving Forward")
            continuous_forward()
        elif left_sensor == 0 and right_sensor == 1:
            log_movement("Right sensor on the line - Turn Right")
            turn_right()
        elif left_sensor == 1 and right_sensor == 0:
            log_movement("Left sensor on the line - Turn Left")
            turn_left()
        else:
            log_movement("No sensors on the line - Stopping")
            stop()
        sleep(0.5)

# Control functions to be called from Flask
def start_forward():
    global movement_thread
    stop()  # Stop any existing movement
    stop_event.clear()
    movement_thread = threading.Thread(target=continuous_forward)
    movement_thread.start()

def start_backward():
    global movement_thread
    stop()  # Stop any existing movement
    stop_event.clear()
    movement_thread = threading.Thread(target=continuous_backward)
    movement_thread.start()

def start_follow_line():
    global movement_thread
    stop()  # Stop any existing movement
    stop_event.clear()
    movement_thread = threading.Thread(target=follow_line)
    movement_thread.start()

# Clean up GPIO
def cleanup():
    GPIO.cleanup()
