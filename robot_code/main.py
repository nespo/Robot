import subprocess
import threading

def start_ultrasonic():
    # Ensure the path is correctly specified relative to main.py's location
    subprocess.run(["python", "./modules/ultrasonic.py"], check=True)

def start_motor_control():
    # Ensure the path is correctly specified relative to main.py's location
    subprocess.run(["python", "./modules/motor.py"], check=True)

if __name__ == "__main__":
    # Use threading to start both processes simultaneously
    ultrasonic_thread = threading.Thread(target=start_ultrasonic)
    motor_thread = threading.Thread(target=start_motor_control)

    ultrasonic_thread.start()
    motor_thread.start()

    # Wait for both threads to complete
    ultrasonic_thread.join()
    motor_thread.join()
