from flask import Flask, render_template, Response
import robot_config as robot
import json
from time import sleep

# Create the Flask app
app = Flask(__name__)

# Initialize the robot
robot.setup_robot()

# Main page
@app.route('/')
def home():
    return render_template('control.html')

# Control routes
@app.route('/forward')
def forward():
    robot.start_forward()
    return "Moving Forward"

@app.route('/backward')
def backward():
    robot.start_backward()
    return "Moving Backward"

@app.route('/left')
def left():
    robot.turn_left()
    return "Turning Left"

@app.route('/right')
def right():
    robot.turn_right()
    return "Turning Right"

@app.route('/stop')
def stop():
    robot.stop()
    return "Stopped"

@app.route('/follow')
def follow():
    try:
        robot.start_follow_line()
    except:
        robot.stop()
    return "Following Line"

@app.route('/stream_logs')
def stream_logs():
    def generate():
        last_count = 0
        while True:
            if len(robot.log_messages) > last_count:
                new_logs = robot.log_messages[last_count:]
                last_count = len(robot.log_messages)
                yield f"data: {json.dumps(new_logs)}\n\n"
            sleep(0.2)
    
    return Response(generate(), mimetype='text/event-stream')



# Start the web server
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0',port=8500)
    except:
        robot.cleanup()
