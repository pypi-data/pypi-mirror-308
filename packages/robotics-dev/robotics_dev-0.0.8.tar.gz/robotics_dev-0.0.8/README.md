# ROBOTICS.DEV App Builder

Run AI robotics apps anywhere!

````
pip install robotics-dev
````

Usage:

robotics.connect() - connects to robotics.dev server (optional edge server IPs supported)

robotics.twist(robot_id, linear_x, linear_z)

Example script: 


````
from robotics_dev import robotics
import time

test = robotics.connect() # connects to server
print(test) # returns socket id

robotics.twist("83568ccb-b44f-470f-9429-f5a80294f2a5", 0.3, 0.0) # robot id, linear_x, linear_z
time.sleep(5) #sleeps 5 seconds
robotics.twist("83568ccb-b44f-470f-9429-f5a80294f2a5", 0.0, 0.0) # robot id, linear_x, linear_z
````
