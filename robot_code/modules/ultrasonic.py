import time
import threading
import sys
import os
import json  # For saving the data in a readable format

# Adjust the sys.path to include the parent directory of robot_code
script_dir = os.path.dirname(__file__)
parent_dir = os.path.join(script_dir, '..', '..')
sys.path.append(os.path.abspath(parent_dir))

from robot_code.utils.pin import Pin
from robot_code.utils.pwm import PWM
from servo import Servo

class UltrasonicServoSensor:
    def __init__(self, trigger_pin, echo_pin, servo_channel, timeout=0.01, servo_offset=0):
        self.trigger_pin = Pin(trigger_pin, Pin.OUT)
        self.echo_pin = Pin(echo_pin, Pin.IN)
        self.servo = Servo(PWM(servo_channel), offset=servo_offset)
        self.timeout = timeout

    def get_distance(self):
        self.trigger_pin.low()
        time.sleep(0.002)  # Shortened sleep to ensure a clean pulse
        self.trigger_pin.high()
        time.sleep(0.00001)
        self.trigger_pin.low()

        start_time = time.time()
        while self.echo_pin.value() == 0:
            pulse_start = time.time()
            if pulse_start - start_time > self.timeout:
                return -1  # Timeout
        while self.echo_pin.value() == 1:
            pulse_end = time.time()
            if pulse_end - start_time > self.timeout:
                return -2  # Timeout

        duration = pulse_end - pulse_start
        distance = (duration * 34300) / 2  # Calculate distance
        return round(distance, 2)

    def scan_270_async(self, callback):
        def scan():
            results = []
            for angle in range(-135, 136, 10):  # 270-degree scan, every 10 degrees
                self.servo.set_angle(angle)
                time.sleep(0.5)  # Slower movement for accuracy
                distance = self.get_distance()
                results.append((angle, distance))
                print(f"Angle: {angle}, Distance: {distance} cm")
            results.sort(key=lambda x: x[0])  # Sort results by angle
            callback(results)

        threading.Thread(target=scan).start()

def print_scan_results(results):
    # Saving the results to a file
    with open('scan_results.json', 'w') as f:
        json.dump(results, f, indent=4)
    for angle, distance in results:
        print(f"Angle: {angle}°, Distance: {distance} cm")

def test_ultrasonic_servo_sensor():
    TRIGGER_PIN = "D2"
    ECHO_PIN = "D3"
    SERVO_CHANNEL = "P0"

    sensor = UltrasonicServoSensor(TRIGGER_PIN, ECHO_PIN, SERVO_CHANNEL)
    sensor.scan_270_async(print_scan_results)

if __name__ == "__main__":
    test_ultrasonic_servo_sensor()
