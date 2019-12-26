#!/usr/bin/env python

from main_controller.msg import *
import rospy
import smach
import smach_ros
import time

g_remote_output = None

class Sleep(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['waking up', 'stay asleep'])

    def execute(self, userdata):
        time.sleep(3)
        return 'stay asleep'


class Awake(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['go to sleep', 'stay awake'])

    def execute(self, userdata):
        time.sleep(3)
        return 'stay awake'


# def callback(msg):
#     global g_remote_output
#     g_remote_output = msg
#     rospy.loginfo('received action: [%d]' % g_remote_output.action)


def main():
    rospy.init_node('smach_example_state_machine')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['waking up'])

    # Subscribers
#    rospy.Subscriber('/remote', Remote, callback)

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('SLEEP', Sleep(), 
                transitions={'waking up':'AWAKE', 'stay asleep':'SLEEP'})
        smach.StateMachine.add('AWAKE', Awake(), 
                transitions={'go to sleep':'SLEEP', 'stay awake':'AWAKE'})

    # Execute SMACH plan
    outcome = sm.execute()
    rospy.spin()


if __name__ == '__main__':
    main()
