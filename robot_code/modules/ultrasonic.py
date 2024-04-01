import time
import socket
import os, sys
from threading import Thread

# Adjust the sys.path to include the parent directory of robot_code
script_dir = os.path.dirname(__file__)
parent_dir = os.path.join(script_dir, '..', '..')
sys.path.append(os.path.abspath(parent_dir))

# Assuming these modules are correctly set up in your environment
from robot_code.utils.pin import Pin
from robot_code.utils.pwm import PWM
from servo import Servo

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

class UltrasonicServoSensor:
    def __init__(self, trigger_pin, echo_pin, servo_channel, timeout=0.01, servo_offset=0):
        self.trigger_pin = Pin(trigger_pin, Pin.OUT)
        self.echo_pin = Pin(echo_pin, Pin.IN)
        self.servo = Servo(PWM(servo_channel), offset=servo_offset)
        self.timeout = timeout

    def get_distance(self):
        self.trigger_pin.low()
        time.sleep(0.002)
        self.trigger_pin.high()
        time.sleep(0.00001)
        self.trigger_pin.low()

        start_time = time.time()
        pulse_start, pulse_end = 0, 0
        while self.echo_pin.value() == 0:
            pulse_start = time.time()
            if pulse_start - start_time > self.timeout:
                return -1  # Timeout
        while self.echo_pin.value() == 1:
            pulse_end = time.time()
            if pulse_end - pulse_start > self.timeout:
                return -2  # Timeout

        if pulse_end and pulse_start:
            duration = pulse_end - pulse_start
            distance = (duration * 34300) / 2  # Calculate distance
            return round(distance, 2)
        else:
            return -3  # Failed to capture duration

    def continuous_scan_and_send(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print('Ultrasonic sensor server listening...')
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    for angle in range(-90, 91, 10):  # Adjusted range for front detection
                        self.servo.set_angle(angle)
                        distance = self.get_distance()
                        if distance >= 0:  # Valid distance
                            data = f"{angle},{distance}\n".encode()
                            conn.sendall(data)
                            print(f"Angle: {angle}, Distance: {distance} cm")
                        else:
                            print(f"Error at angle: {angle}")
                        time.sleep(0.4)  # Adjust for servo movement and scanning pace

if __name__ == "__main__":
    sensor = UltrasonicServoSensor("D2", "D3", "P0")
    Thread(target=sensor.continuous_scan_and_send).start()
