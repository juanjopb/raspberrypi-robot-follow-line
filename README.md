# Robot Web Control

A Flask-based web application designed to control a robot built with Raspberry Pi 5. This project enables remote control of the robot through a web browser interface, providing basic movement controls and line-following capabilities.

## Features

- Basic robot movement controls (forward, backward, left, right, stop)
- Line following capability
- Real-time log streaming
- Web-based control interface
- Optimized for Raspberry Pi 5 GPIO control
- Remote control through local network

## Hardware Requirements

- Raspberry Pi 5
- Motor Driver Board (L298N or similar)
- DC Motors (2x)
- Wheels
- Line Following Sensors
- Power Supply (5V for Raspberry Pi, separate power for motors)
- Robot Chassis
- Jumper Wires

## Prerequisites

- Raspberry Pi OS (64-bit recommended)
- Python 3.x
- Flask
- RPi.GPIO library
- Robot hardware configured according to robot_config.py specifications

## Installation

1. Clone this repository on your Raspberry Pi:
```bash
git clone [repository-url](https://github.com/juanjopb/raspberrypi-robot-follow-line)
```
2. Install required dependencies:
```bash
pip install flask RPi.GPIO
```

## Hardware Setup
1. GPIO Connections:
    - Motor A: GPIO pins specify pins
    - Motor B: GPIO pins specify pins
    - Line Sensors: GPIO pins specify pins

2. Power Connections:
    - Connect Raspberry Pi to 5V power supply
    - Connect motors to motor driver board
    - Connect motor driver board to appropriate power source

## Usage
1. Start the application on your Raspberry Pi:
```bash
python robot_web_control.py
```
2. Access the control interface through your web browser:
```bash
http://[raspberry-pi-ip-address]:5000
```
## API Endpoints

- `/` - Main control interface
- `/forward` - Move robot forward
- `/backward` - Move robot backward
- `/left` - Turn robot left
- `/right` - Turn robot right
- `/stop` - Stop robot movement
- `/follow` - Activate line following mode
- `/stream_logs` - Stream robot operation logs

## Project Structure

- `robot_web_control.py` - Main Flask application
- `robot_config.py` - Robot configuration and hardware control
- `templates/control.html` - Web interface template

## Safety Considerations
- Always ensure proper voltage levels for components
- Double-check GPIO connections before powering on
- Implement emergency stop functionality
- Monitor motor temperature during extended use
- Ensure proper ventilation for the Raspberry Pi 5

## Error Handling
The application includes basic error handling for:
- Line following operations
- Server shutdown with proper GPIO cleanup
- Motor control failures
- Network connection issues

## Troubleshooting
### Common issues and solutions:
1. Motors not responding:
    - Check GPIO connections
    - Verify power supply connections
    - Ensure motor driver board is properly configured
2. Web interface not accessible:
    - Verify Raspberry Pi is connected to network
    - Check firewall settings
    - Confirm correct IP address and port
3. Line following not working:
    - Check sensor connections
    - Adjust sensor sensitivity
    - Verify sensor positioning

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

