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
        time.sleep_us(2)
        self.trigger_pin.high()
        time.sleep_us(10)
        self.trigger_pin.low()

        # Measure the duration of the pulse from the echo pin
        while self.echo_pin.value() == 0:
            pulse_start = time.ticks_us()

        while self.echo_pin.value() == 1:
            pulse_end = time.ticks_us()

        pulse_duration = time.ticks_diff(pulse_end, pulse_start)

        # Calculate distance based on the duration of the pulse
        distance = pulse_duration * self.speed_of_sound / (2 * 1000000)  # Convert to meters
        return distance

def test_ultrasonic_sensor():
    # Define trigger and echo pins
    TRIGGER_PIN = "D2"
    ECHO_PIN = "D3"

    # Initialize ultrasonic sensor
    ultrasonic_sensor = UltrasonicSensor(TRIGGER_PIN, ECHO_PIN)

    # Continuously measure distance and print the result
    while True:
        distance = ultrasonic_sensor.measure_distance()
        print("Distance: {:.2f} meters".format(distance))
        time.sleep(1)

if __name__ == "__main__":
    test_ultrasonic_sensor()
