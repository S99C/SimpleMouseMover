How it Works:
------------
* Just download the latest release of the 'SimpleMouseMover' Zip file, extract it in a folder, and run the executable.
* First time the script is run, it will ask the user to provide "start_delay" and "loop_delay" value.
* If user provides valid input (seconds in number, ex: "120", "3", etc..) it will simply save the values to a config.txt file which will be used by the script from next time onwards. 
* Default values for "start_delay" and "loop_delay" is 3 seconds and 120 seconds, respectively.

Known Limitations:
-----------------
* When paused while "loop_delay" timer is running, pauses immediately but when pressed the key/key-combination for pause while the cursor is moving, it will pause only after completing the loop.
* When "loop_delay" timer is running, keeping the cursor placed on Top Left corner, doesn't stop the script. It only does it after the "delay_loop" is completed.
* "start_delay" and "loop_delay" values don't display on first run if user provides the value, but works as expected.
* User defined 'Hotkey/Key-combnations' for pause/resume will come in future versions.

Libraries Used:
--------------
* PyAutoGui
* volume-control
