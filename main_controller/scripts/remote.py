#!/usr/bin/env python

from main_controller.msg import *
import rospy

def remote_server():
    pub = rospy.Publisher('remote', Remote, queue_size = 10)
    rospy.init_node('remote_server', anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        remote_output = Remote()
        rospy.loginfo('Got command on /remote: %s' % remote_output)
        pub.publish(remote_output)
        rate.sleep()

if __name__ == "__main__":
    try:
        remote_server()
    except rospy.ROSInterruptException:
        pass
