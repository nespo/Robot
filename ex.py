import os

# Base directory for the robot code
base_dir = 'robot_code'

# Paths for directories to be created
dirs_to_create = [
    base_dir,
    os.path.join(base_dir, 'modules'),
    os.path.join(base_dir, 'utils'),
    os.path.join(base_dir, 'configs'),
]

# Files to be created with their initial content
files_to_create = {
    os.path.join(base_dir, 'main.py'): '',  # Main script to run the robot
    os.path.join(base_dir, 'modules', '__init__.py'): '',
    os.path.join(base_dir, 'modules', 'motor.py'): '# Control the motors\n',
    os.path.join(base_dir, 'modules', 'photo_interrupter.py'): '# Interact with the photo-interrupter module\n',
    os.path.join(base_dir, 'modules', 'grayscale.py'): '# Interact with the grayscale sensor\n',
    os.path.join(base_dir, 'modules', 'ultrasonic.py'): '# Interact with the ultrasonic sensor\n',
    os.path.join(base_dir, 'utils', '__init__.py'): '',
    os.path.join(base_dir, 'utils', 'pin.py'): '# Pin class provided by the manufacturer\n',
    os.path.join(base_dir, 'configs', '__init__.py'): '',
    os.path.join(base_dir, 'configs', 'pins.py'): '# Define pin mappings and configurations\n',
}

# Creating directories
for directory in dirs_to_create:
    os.makedirs(directory, exist_ok=True)

# Creating files with initial content
for file_path, content in files_to_create.items():
    with open(file_path, 'w') as file:
        file.write(content)

print("Folder structure and files created successfully.")
