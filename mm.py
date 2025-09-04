import pyautogui as pg
import pyvolume
import time
import keyboard
import os

pg.FAILSAFE = True
print("Keep cursor on top left to STOP script!")

# Global variables to manage state and messages
paused = False
last_message = ""
prev_paused_state = False

# Configuration file name
config_file = "config.txt"

# Default values
default_start_delay = 3
default_delay_seconds = 120

def clear_line():
    """Clears the current line in the terminal."""
    print("\r" + " " * 80 + "\r", end="", flush=True)

def write_config_to_file(start_delay_val, loop_delay_val):
    """Writes the start and loop delay values to the configuration file."""
    try:
        with open(config_file, "w") as f:
            f.write(f"start_delay={start_delay_val}\n")
            f.write(f"loop_delay={loop_delay_val}\n")
        print("Configuration saved.")
    except Exception as e:
        print(f"Error writing to config file: {e}")

def read_config_from_file():
    """Reads start and loop delay values from the configuration file."""
    config = {}
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    config[key] = value
    return config

# Define the hotkey for toggling pause
toggle_key = 'alt+`'

# Function to be called when the hotkey is pressed
def toggle_pause():
    """Toggles the 'paused' state when the hotkey is pressed."""
    global paused
    paused = not paused

# Register the hotkey
keyboard.add_hotkey(toggle_key, toggle_pause)

# --- GET USER INPUT OR READ FROM FILE ---
config_data = read_config_from_file()
should_prompt_user = False

try:
    start_delay = int(config_data.get("start_delay", default_start_delay))
    delay_seconds = int(config_data.get("loop_delay", default_delay_seconds))
    if not config_data:
        should_prompt_user = True
    else:
        print(f"Using saved configuration from '{config_file}'.")
        print(f"Start delay: {start_delay} seconds, Loop delay: {delay_seconds} seconds.")

except (ValueError, FileNotFoundError):
    should_prompt_user = True

if should_prompt_user:
    print(f"Configuration file not found or invalid. Please enter new values.")
    
    # Get start delay
    user_input_start = input(f"Enter the start delay in seconds (default is {default_start_delay}): ")
    try:
        start_delay = int(user_input_start)
    except ValueError:
        print(f"Invalid input. Using default start delay of {default_start_delay} seconds.")
        start_delay = default_start_delay
    
    # Get loop delay
    user_input_loop = input(f"Enter the loop delay in seconds (default is {default_delay_seconds}): ")
    try:
        delay_seconds = int(user_input_loop)
    except ValueError:
        print(f"Invalid input. Using default loop delay of {default_delay_seconds} seconds.")
        delay_seconds = default_delay_seconds
    
    # Write the new configuration to the file
    write_config_to_file(start_delay, delay_seconds)

# Wait for start_delay seconds
for time_remaining in range(start_delay, 0, -1):
    print(f"Starting in {time_remaining} seconds...", end="\r", flush=True)
    time.sleep(1)
print(" " * 50, end="\r", flush=True)

# Set sys vol to n%
pyvolume.custom(percent=100)

# Screen w & h
w = pg.size().width
h = pg.size().height

# Print the static message once at the beginning
print(f"Press '{toggle_key}' to pause/resume.")

while True:
    # Check for state change and print the appropriate message
    if paused and not prev_paused_state:
        clear_line()
        print("Script is paused.", end="", flush=True)
        prev_paused_state = True
        
    elif not paused and prev_paused_state:
        clear_line()
        print("Script resumed.", end="", flush=True)
        prev_paused_state = False
        time.sleep(1)
        clear_line()

    if not paused:
        # Actions when the script is running
        pg.moveTo(w/2, h/2)
        
        pg.PAUSE = 0.25
        pg.dragRel(5, 0, duration=0.15)
        pg.dragRel(0, 5, duration=0.15)
        pg.dragRel(-5, 0, duration=0.15)
        pg.dragRel(0, -5, duration=0.15)
        pg.PAUSE = 0
        
        # Timer messages
        for remaining in range(delay_seconds, 0, -1):
            if not paused:
                new_message = f"Time until next loop: {remaining} seconds"
                print(new_message, end="\r", flush=True)
                time.sleep(1)
            else:
                break
        
        # After the timer, clear the countdown
        print(" " * 50, end="\r", flush=True)
        time.sleep(0.5)
        
    else:
        # Wait a short while to avoid a tight loop when paused
        time.sleep(0.5)