#!/usr/bin/env python3
# license removed for brevity
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
import math
from time import sleep

wheel_base = 1.845 
track_width = 1.242
inner_wheel_lock_angle = 30 
outer_wheel_lock_angle = 23.537
gama = 0  # steering angle for bicycle like model
delta_inner, delta_outer = 0,0
def right_turn(delta_inner,delta_outer):
    delta_inner = -1*min(abs(delta_inner),abs(math.radians(inner_wheel_lock_angle))) # to turn right wheel CW
    delta_outer = -1*min(abs(delta_outer),abs(math.radians(outer_wheel_lock_angle))) # to turn left wheel CW
    pub_R.publish(delta_inner)
    pub_L.publish(delta_outer)

def lef_turn(delta_inner,delta_outer):
    delta_inner = 1*min(abs(delta_inner),abs(math.radians(inner_wheel_lock_angle))) # to turn left wheel CCW
    delta_outer = 1*min(abs(delta_outer),abs(math.radians(outer_wheel_lock_angle))) # to turn right wheel CCW
    pub_R.publish(delta_outer)
    pub_L.publish(delta_inner)

def go_straight(delta_inner=0,delta_outer=0):
    # vehicle need to move straight 
    pub_R.publish(delta_outer)
    pub_L.publish(delta_inner)

def steering_angle(data):
    global gama
    global delta_inner,delta_outer,inner_wheel_lock_angle,outer_wheel_lock_angle
    linear_vel = data.linear.x
    angular_vel = data.angular.z
    
    #calculating steering angle gamma
    if angular_vel != 0.0 and linear_vel != 0.0:
        turning_radi = linear_vel/angular_vel
        gama = math.atan(wheel_base/turning_radi) # gama is in radian
        #delta_inner =  inner wheel turning angle based on ackermann relation
        #delta_outer =  outer wheel turning angle based on ackermann relation
        delta_inner = math.atan((wheel_base*math.tan(gama)/(wheel_base-(0.5*track_width*math.tan(gama))))) 
        delta_outer= math.atan((wheel_base*math.tan(gama)/(wheel_base+(0.5*track_width*math.tan(gama)))))
    if angular_vel ==0 or linear_vel ==0:
        delta_inner,delta_outer = 0,0
    if angular_vel < 0 and linear_vel !=0:
        right_turn(delta_inner,delta_outer)
    if angular_vel > 0 and linear_vel !=0:
        lef_turn(delta_inner,delta_outer)
    if angular_vel == 0 and linear_vel !=0:
        go_straight(delta_inner,delta_outer)

   
def get_vel():
    global pub_L,pub_R
    rospy.init_node('steering_control_node',anonymous=True)
    pub_R = rospy.Publisher('/right_knuckle_position_controller/command', Float64, queue_size=1)
    pub_L = rospy.Publisher('/left_knuckle_position_controller/command', Float64, queue_size=1)
    rospy.Subscriber('/cmd_vel',Twist,steering_angle) 
    rospy.spin()



if __name__ == '__main__':
    try:
        get_vel()
    except rospy.ROSInterruptException:
        pass