#!/usr/bin/env python3
# license removed for brevity
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
import math
from time import sleep

wheel_base = 1.312
theta_min,theta_max = -30,30 
track_width = 1.040
gama = 0

def steering_angle(data):
    global gama
    linear_vel = data.linear.x
    angular_vel = data.angular.z
    print(linear_vel,angular_vel)
    #calculating steering angle gamma
    if angular_vel != 0.0 and linear_vel != 0.0:
        turning_radi = linear_vel/angular_vel
        gama = math.atan(wheel_base/turning_radi)
        gama = gama*180/math.pi
        

    del_l = math.atan((wheel_base*math.tan(math.radians(gama))/(wheel_base-(0.5*track_width*math.tan(math.radians(30))))))
    del_r = math.atan((wheel_base*math.tan(math.radians(gama))/(wheel_base+(0.5*track_width*math.tan(math.radians(30))))))
    
    pub_R.publish(del_r)
    pub_L.publish(del_l)
    # count = 0
    # for x in range(1000):
    #     pub_R.publish(del_r)
    #     pub_L.publish(del_l)
    #     count+=1
    #     sleep(0.001)
   
def get_vel():
    global pub_L,pub_R
    rospy.init_node('steering_control_node',anonymous=True)
    pub_R = rospy.Publisher('/right_knuckle_position_controller/command', Float64, queue_size=10)
    pub_L = rospy.Publisher('/left_knuckle_position_controller/command', Float64, queue_size=10)
    rospy.Subscriber('/cmd_vel',Twist,steering_angle) #/robot_base_velocity_controller/cmd_vel
    
    rospy.spin()



if __name__ == '__main__':
    try:
        get_vel()
    except rospy.ROSInterruptException:
        pass