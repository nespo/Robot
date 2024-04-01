import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

class MotorControl:
    def __init__(self):
        self.manual_mode = False
        self.power = 0

    def set_power_based_on_sensor(self, angle, distance):
        if self.manual_mode:
            print("In manual mode. Sensor data ignored.")
        elif distance < 50:
            self.power = 0
            print(f"Obstacle detected. Stopping. Distance: {distance}cm")
        else:
            self.power = 100
            print(f"Path clear. Moving forward. Distance: {distance}cm")

    def receive_data(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            while True:
                data = s.recv(1024)
                if not data:
                    break
                angle, distance = map(int, data.decode().strip().split(','))
                self.set_power_based_on_sensor(angle, distance)

    def toggle_manual_mode(self):
        while True:
            cmd = input("Enter 'm' to toggle manual mode, 'q' to quit: ").strip()
            if cmd == 'm':
                self.manual_mode = not self.manual_mode
                mode = "Manual" if self.manual_mode else "Automatic"
                print(f"Switched to {mode} mode.")
            elif cmd == 'q':
                print("Exiting.")
                break

    def run(self):
        threading.Thread(target=self.receive_data, daemon=True).start()
        self.toggle_manual_mode()

if __name__ == "__main__":
    motor_control = MotorControl()
    motor_control.run()
