#!/usr/bin/env python

#import roslib; roslib.load_manifest('smach_tutorials')
import rospy
import smach
import smach_ros
import time

# define state Sleep 
class Sleep(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['waking up'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state Sleep')
        time.sleep(5)
        return 'waking up'

# define state Awake
class Awake(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['sleeping'])

    def execute(self, userdata):
        rospy.loginfo('Executing state Awake')
        time.sleep(5)
        return 'sleeping'

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
                               transitions={'sleeping':'SLEEP'})

    # Execute SMACH plan
    outcome = sm.execute()


if __name__ == '__main__':
    main()
