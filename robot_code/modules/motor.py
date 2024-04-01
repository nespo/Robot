import socket
import threading
from pynput.keyboard import Key, Listener

HOST = '127.0.0.1'
PORT = 65432

class MotorControl:
    def __init__(self):
        # Placeholder for motor setup
        self.manual_mode = False
        self.power = 0

    def set_power_based_on_sensor(self, angle, distance):
        # Example logic to adjust motor power based on sensor data
        if distance < 50:  # Assuming distance is in cm
            self.power = 0  # Stop if obstacle is too close
        else:
            self.power = 100  # Full speed ahead

        print(f"Motor Power: {self.power}")

    def receive_data(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            while True:
                data = s.recv(1024)
                if not data:
                    break
                angle, distance = map(int, data.decode().strip().split(','))
                if not self.manual_mode:
                    self.set_power_based_on_sensor(angle, distance)

    def on_press(self, key):
        # Simple manual control logic
        try:
            if key.char == 'w':  # Forward
                self.power = 100
                self.manual_mode = True
            elif key.char == 's':  # Stop/Reverse?
                self.power = 0
                self.manual_mode = True
        except AttributeError:
            pass

    def on_release(self, key):
        if key == Key.esc:
            # Stop listener
            return False

    def manual_control_listener(self):
        # Collect events until released
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def run(self):
        threading.Thread(target=self.receive_data).start()
        self.manual_control_listener()

# At the end of motor.py
if __name__ == "__main__":
    motor_control = MotorControl()
    motor_control.run()

