#!/usr/bin/env python

from main_controller.msg import *
import rospy
import smach
import smach_ros
import time

g_remote_output = None

# define state Sleep 
class Sleep(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['waking up', 'stay asleep'])

    def execute(self, userdata):
        rospy.loginfo('Executing state Sleep')
        time.sleep(3)

        if not g_remote_output == None:
            if g_remote_output.awake:
                rospy.loginfo('Wake up')
                return 'waking up'
            else:
                rospy.loginfo('Stay asleep')
                return 'stay asleep'
        else:
            return 'stay asleep'

# define state Awake
class Awake(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['go to sleep', 'stay awake'])

    def execute(self, userdata):
        global g_remote_output

        rospy.loginfo('Executing state Awake')
        time.sleep(3)

        rospy.loginfo('remote output %s' % g_remote_output)
        if not g_remote_output == None:
            if g_remote_output.sleep:
                rospy.loginfo('Go to sleep')
                return 'go to sleep'
            else:
                rospy.loginfo('Stay awake')
                return 'stay awake'
        else:
            return 'stay awake'

        #rospy.loginfo('g_receive_sleep_command %s' % sleep_command)
        #if sleep_command:
        #    rospy.loginfo('Go to sleep')
        #    return 'sleeping'
        #else:
        #    rospy.loginfo('Stay awake')
        #    return 'stay awake'

def callback(msg):
    global g_remote_output
    g_remote_output = msg

# main
def main():
    rospy.init_node('smach_example_state_machine')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['waking up'])

    rospy.Subscriber('/remote', Remote, callback)

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
