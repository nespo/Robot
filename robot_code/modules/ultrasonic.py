import time
import sys
import os

# Add the parent directory of robot_code to sys.path
script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
parent_dir = os.path.join(script_dir, '..', '..')  # Navigate two levels up
sys.path.append(os.path.abspath(parent_dir))

from robot_code.utils.pin import Pin


class UltrasonicSensor:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = Pin(trigger_pin, Pin.OUT)
        self.echo_pin = Pin(echo_pin, Pin.IN)
        self.speed_of_sound = 343.0  # Speed of sound in m/s

    def measure_distance(self):
        # Send a pulse to trigger the ultrasonic sensor
        self.trigger_pin.low()
        time.sleep(0.000002)  # 2 microseconds
        self.trigger_pin.high()
        time.sleep(0.00001)  # 10 microseconds
        self.trigger_pin.low()

        # Measure the duration of the pulse from the echo pin
        pulse_start_time = None
        pulse_end_time = None
        while self.echo_pin.value() == 0:
            pulse_start_time = time.perf_counter()
        while self.echo_pin.value() == 1:
            pulse_end_time = time.perf_counter()

        if pulse_start_time is not None and pulse_end_time is not None:
            pulse_duration = (pulse_end_time - pulse_start_time) * 1_000_000  # Convert duration to microseconds
            # Calculate distance based on the duration of the pulse
            distance = (pulse_duration * self.speed_of_sound) / (2 * 1_000_000)  # Convert to meters
            return distance
        else:
            # Handle the case where a pulse was not detected
            print("Pulse not detected.")
            return None

def test_ultrasonic_sensor():
    # Define trigger and echo pins
    TRIGGER_PIN = "D2"
    ECHO_PIN = "D3"

    # Initialize ultrasonic sensor
    ultrasonic_sensor = UltrasonicSensor(TRIGGER_PIN, ECHO_PIN)

    # Continuously measure distance and print the result
    while True:
        distance = ultrasonic_sensor.measure_distance()
        if distance is not None:
            print("Distance: {:.2f} meters".format(distance))
        else:
            print("Distance measurement failed.")
        time.sleep(1)

if __name__ == "__main__":
    test_ultrasonic_sensor()
