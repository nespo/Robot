import time
import threading
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
                return -1
        while self.echo_pin.value() == 1:
            pulse_end = time.time()
            if pulse_end - start_time > self.timeout:
                return -2

        duration = pulse_end - pulse_start
        distance = (duration * 34300) / 2
        return round(distance, 2)

    def scan_180_async(self, callback):
        def scan():
            results = []
            for angle in range(-90, 91, 5):  # More granular step size
                self.servo.set_angle(angle)
                # Reduced sleep - Assumes servo can move quickly enough
                time.sleep(0.1)
                distance = self.get_distance()
                results.append((angle, distance))
                print(f"Angle: {angle}, Distance: {distance} cm")
            callback(results)

        # Run the scan in a separate thread to avoid blocking
        threading.Thread(target=scan).start()

def print_scan_results(results):
    for angle, distance in results:
        print(f"Angle: {angle}°, Distance: {distance} cm")

def test_ultrasonic_servo_sensor():
    TRIGGER_PIN = "D2"
    ECHO_PIN = "D3"
    SERVO_CHANNEL = "P0"

    sensor = UltrasonicServoSensor(TRIGGER_PIN, ECHO_PIN, SERVO_CHANNEL)
    sensor.scan_180_async(print_scan_results)

if __name__ == "__main__":
    test_ultrasonic_servo_sensor()
