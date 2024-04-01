import time
import sys
import os

# Add the parent directory of robot_code to sys.path
script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
parent_dir = os.path.join(script_dir, '..', '..')  # Navigate two levels up
sys.path.append(os.path.abspath(parent_dir))

from robot_code.utils.pin import Pin
from robot_code.utils.pwm import PWM
from servo import Servo

class UltrasonicServoSensor:
    def __init__(self, trigger_pin, echo_pin, servo_channel, timeout=0.01, servo_offset=0):
        """
        Initializes the ultrasonic sensor with servo control for 180-degree scans.
        :param trigger_pin: The GPIO pin number used for triggering the sensor.
        :param echo_pin: The GPIO pin number used to read the echo signal.
        :param servo_channel: The PWM channel used by the servo motor.
        :param timeout: Maximum time to wait for echo signal (seconds).
        :param servo_offset: Offset to calibrate the servo's neutral position.
        """
        self.trigger_pin = Pin(trigger_pin, Pin.OUT)
        self.echo_pin = Pin(echo_pin, Pin.IN)
        self.servo = Servo(PWM(servo_channel), offset=servo_offset)
        self.timeout = timeout
        self.angle_distance = []

    def get_distance(self):
        """
        Measures the distance detected by the ultrasonic sensor.
        :return: The distance in centimeters, or -1 if timeout occurred.
        """
        self.trigger_pin.low()
        time.sleep(0.01)  # Ensure clean low pulse
        self.trigger_pin.high()
        time.sleep(0.000015)  # Send out a burst of ultrasonic sound
        self.trigger_pin.low()

        pulse_start_time = time.time()
        while self.echo_pin.value() == 0:
            pulse_start = time.time()
            if pulse_start - pulse_start_time > self.timeout:
                return -1  # Timeout occurred, no echo detected

        while self.echo_pin.value() == 1:
            pulse_end = time.time()
            if pulse_end - pulse_start_time > self.timeout:
                return -2  # Timeout occurred, echo didn't finish

        pulse_duration = pulse_end - pulse_start
        distance_cm = (pulse_duration * 34300) / 2  # Speed of sound: 34300 cm/s, round trip
        return round(distance_cm, 2)

    def scan_180(self):
        """
        Scans across a 180-degree arc, collecting distance measurements.
        :return: A list of (angle, distance) tuples.
        """
        scan_results = []
        for angle in range(-90, 91, 10):  # Adjust step size as needed for your application
            self.servo.set_angle(angle)
            time.sleep(0.5)  # Wait for the servo to reach the set angle
            distance = self.get_distance()
            scan_results.append((angle, distance))
            print(f"Angle: {angle}, Distance: {distance} cm")

        return scan_results

def test_ultrasonic_servo_sensor():
    TRIGGER_PIN = "D2"  # Example pin, replace with actual GPIO number
    ECHO_PIN = "D3"    # Example pin, replace with actual GPIO number
    SERVO_CHANNEL = "P0"  # Example PWM channel, adjust as per your setup

    ultrasonic_servo_sensor = UltrasonicServoSensor(TRIGGER_PIN, ECHO_PIN, SERVO_CHANNEL)

    try:
        scan_results = ultrasonic_servo_sensor.scan_180()
        for angle, distance in scan_results:
            print(f"Angle: {angle}°, Distance: {distance} cm")
    except KeyboardInterrupt:
        print("Scan stopped by user")

if __name__ == "__main__":
    test_ultrasonic_servo_sensor()
