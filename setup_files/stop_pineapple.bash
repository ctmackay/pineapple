#!/bin/bash

. /opt/ros/kinetic/setup.bash
. /home/ubuntu/code/catkin_ws/install/setup.bash

ps -ef | grep "start_pineapple.bash" | awk '$8 == "/bin/bash" {print $2}' | awk '{print "kill " $1 }' | /bin/bash
