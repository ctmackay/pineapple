#!/usr/bin/env python

from main_controller.msg import *
from datetime import datetime
import rospy
import smach
import smach_ros
import time
from std_msgs.msg import String
from random import randint

from sense_hat import SenseHat

g_remote_output = None

def get_time_string():
    time_color = (55, 55, 255)
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    return str(current_time)

class Rest(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['waking up', 'let me rest'])

    def execute(self, userdata):
        SH.show_on_led(SH.get_humidity(), (232, 121, 121))
        SH.show_on_led(get_time_string(), (55, 55, 255))

        time.sleep(3)
        return 'waking up'

class Awake(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['stay awake', 'need to rest'])

    def execute(self, userdata):
        time.sleep(3)
        return 'need to rest'

def callback(msg):
    global g_remote_output
    g_remote_output = msg
    rospy.loginfo('received action: [%d]' % g_remote_output.action)

def main():
    global SH
    from main_controller.SenseHatEnvironment import SenseHatEnvironment
    SH = SenseHatEnvironment()

    rospy.init_node('state_machine')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['waking up'])

    # Subscribers
    rospy.Subscriber('/remote', Remote, callback)

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('REST', Rest(),
                transitions={'waking up':'AWAKE', 'let me rest':'REST'})
        smach.StateMachine.add('AWAKE', Awake(),
                transitions={'need to rest':'REST', 'stay awake':'AWAKE'})

    # Execute SMACH plan
    outcome = sm.execute()
    rospy.spin()

if __name__ == '__main__':
    main()
