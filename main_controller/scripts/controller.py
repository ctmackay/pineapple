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

try:
    g_sh = SenseHat()
    g_sh.clear()
    g_sh.low_light = True
except:
    rospy.loginfo('No SenseHat detected')
    g_sh = None

g_remote_output = None

def get_time_string():
    time_color = (55, 55, 255)
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    return str(current_time)

class Sleep(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['waking up', 'stay asleep'])

    def execute(self, userdata):
        SH.show_on_led(SH.get_humidity(), (232, 121, 121))
        SH.show_on_led(get_time_string(), (55, 55, 255))
        SH.show_on_led("Welcome to Charles & Cherry's home!", (153, 255, 153))

        time.sleep(3)
        if not g_remote_output is None:
            if g_remote_output.action == g_remote_output.WAKE:
                return 'waking up'

        return 'stay asleep'


class Awake(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['go to sleep', 'stay awake', 'need to rest'])

    def execute(self, userdata):
        time.sleep(3)
        if not g_remote_output is None:
            if g_remote_output.action == g_remote_output.REST:
                return 'need to rest'

        return 'stay awake'


class Rest(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['go to sleep', 'stop resting', 'need more rest'])

    def execute(self, userdata):
        time.sleep(3)
        return 'need more rest'


def callback(msg):
    global g_remote_output
    g_remote_output = msg
    rospy.loginfo('received action: [%d]' % g_remote_output.action)


def main():
    global SH
    from main_controller.SenseHatEnvironment import Environment
    SH = Environment()

    rospy.init_node('smach_example_state_machine')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['waking up'])

    # Subscribers
    rospy.Subscriber('/remote', Remote, callback)

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('SLEEP', Sleep(),
                transitions={'waking up':'AWAKE', 'stay asleep':'SLEEP'})
        smach.StateMachine.add('AWAKE', Awake(),
                transitions={'go to sleep':'SLEEP', 'stay awake':'AWAKE', 'need to rest':'REST'})
        smach.StateMachine.add('REST', Rest(),
                transitions={'go to sleep':'SLEEP', 'stop resting':'AWAKE', 'need more rest':'REST'})

    # Execute SMACH plan
    outcome = sm.execute()
    rospy.spin()


if __name__ == '__main__':
    main()
