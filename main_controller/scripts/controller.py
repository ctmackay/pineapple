#!/usr/bin/env python

from main_controller.srv import *
import rospy
import smach
import smach_ros
import time


# define state Sleep 
class Sleep(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['waking up'])

    def execute(self, userdata):
        rospy.loginfo('Executing state Sleep')
        time.sleep(5)
        return 'waking up'

# define state Awake
class Awake(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['go to sleep', 'stay awake'])

    def execute(self, userdata):
        rospy.loginfo('Executing state Awake')
        time.sleep(5)
        return 'go to sleep'

        #rospy.loginfo('g_receive_sleep_command %s' % sleep_command)
        #if sleep_command:
        #    rospy.loginfo('Go to sleep')
        #    return 'sleeping'
        #else:
        #    rospy.loginfo('Stay awake')
        #    return 'stay awake'

# main
def main():
    rospy.init_node('smach_example_state_machine')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['waking up'])

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('SLEEP', Sleep(), 
                               transitions={'waking up':'AWAKE'})
        smach.StateMachine.add('AWAKE', Awake(), 
                               transitions={'go to sleep':'SLEEP',
                               'stay awake':'AWAKE'})

    # Execute SMACH plan
    outcome = sm.execute()


if __name__ == '__main__':
    main()
