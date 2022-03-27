#!/usr/bin/env python3
# license removed for brevity
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
import math
from time import sleep

def move_arm():
    rospy.init_node('bin_picking',anonymous=True)
    pub_slider = rospy.Publisher('/Slider_position_controller/command',Float64,queue_size=10)
    pub_arm = rospy.Publisher('/arm_joint_position_controller/command',Float64,queue_size=10)
    pub_gripper1 = rospy.Publisher('/gripper1_joint_position_controller/command',Float64,queue_size=10)
    pub_gripper2 = rospy.Publisher('/gripper2_joint_position_controller/command',Float64,queue_size=10)

    while not rospy.is_shutdown():
        pub_slider.publish(0.3)
        sleep(5)
        pub_gripper1.publish(-1.39)
        pub_gripper2.publish(1.39)
        sleep(3)
        pub_arm.publish(2.792)
        sleep(10)
        pub_arm.publish(0)
        sleep(5)
        pub_gripper1.publish(0)
        pub_gripper2.publish(0)
        sleep(5)
        pub_slider.publish(0)
        sleep(2)


if __name__ == '__main__':
    try:
        move_arm()
    except rospy.ROSInterruptException:
        pass