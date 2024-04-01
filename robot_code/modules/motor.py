import socket
import threading
import keyboard

HOST = '127.0.0.1'
PORT = 65432

class MotorControl:
    def __init__(self):
        self.manual_mode = False
        self.power = 0

    def set_power_based_on_sensor(self, angle, distance):
        if distance < 50:
            self.power = 0
        else:
            self.power = 100
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

    def check_keyboard(self):
        while True:
            try:
                if keyboard.is_pressed('w'):
                    self.manual_mode = True
                    self.power = 100
                    print("Manual: Moving forward")
                elif keyboard.is_pressed('s'):
                    self.manual_mode = True
                    self.power = 0
                    print("Manual: Stopping")
                # Reset manual mode if needed
                # elif keyboard.is_pressed('r'):
                #     self.manual_mode = False
            except RuntimeError:
                pass  # Handle errors due to non-root permissions
            
    def run(self):
        threading.Thread(target=self.receive_data).start()
        self.check_keyboard()

if __name__ == "__main__":
    motor_control = MotorControl()
    motor_control.run()
