import subprocess
import os

# Command to run run.py in the foreground without opening a console window
command_foreground = ["pythonw", "run.py"]

# Command to run background.py in the background without a command prompt window
command_background = ["start", "/B", "pythonw", "background.py"]

# Run run.py in the foreground using pythonw (no console window)
process = subprocess.Popen(command_foreground, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()  # Wait for the process to complete

# Optionally, check for errors in run.py
if stderr:
    print("Error:", stderr.decode())

# After run.py completes, run background.py in the background
subprocess.Popen(command_background, shell=True)

print("Return Code:", process.returncode)
