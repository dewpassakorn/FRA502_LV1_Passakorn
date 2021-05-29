#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import sys, select, os
if os.name == 'nt':
    import msvcrt
else:
    import tty, termios
from std_msgs.msg import String

MAX_LIN_VEL = 15.0
MAX_ANG_VEL = 20.0

LIN_VEL_STEP_SIZE = 1.5
ANG_VEL_STEP_SIZE = 2.0

msg = """
dew_ros_robot teleop keyboard follwer the key below.
---------------------------
Moving around:
        w
    a   s   d
        x

z/x : increase/decrease linear & angular velocity 

space key, b : force stop

CTRL-C to quit
"""

e = """
Communications Failed
"""

def getkey():
    if os.name == 'nt':
        if sys.version_info[0] >= 3:
            return msvcrt.getch().decode()
        else:
            return msvcrt.getch()

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def vels(target_linear_vel, target_angular_vel):
    return "currently speed set:\tlinear vel %s\t angular vel %s " % (target_linear_vel,target_angular_vel)

def vels_update(control_linear_vel, control_angular_vel):
    return "currently speed:\tlinear vel %s\t angular vel %s " % (control_linear_vel,control_angular_vel)

def constrain(input, low, high,step,ref):
    
    if ref == 'increase':
        output = input + step
        if input >= high:
            output = input
    elif ref == 'decrease':
        output = input - step
        if input <= low:
            output = 0


    return output


if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rospy.init_node('dew_ros_robot_teleop', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    dew_ros_robot = rospy.get_param("model", "dew_ros_robot")

    status = 0
    target_linear_vel   = 1.5
    target_angular_vel  = 2.0
    control_linear_vel  = 0.0
    control_angular_vel = 0.0

    try:
        print(msg)
        while(1):
            key = getkey()
            if key == 'w' :
                control_linear_vel = target_linear_vel
                #print(vels_update(control_linear_vel, control_angular_vel))

            elif key == 's' :
                control_linear_vel = -target_linear_vel
                #print(vels_update(control_linear_vel, control_angular_vel))

            elif key == 'a' :
                control_angular_vel = target_angular_vel
                #print(vels_update(control_linear_vel, control_angular_vel))

            elif key == 'd' :
                control_angular_vel = -target_angular_vel
                #print(vels_update(control_linear_vel, control_angular_vel))
                
            if key == 'z' :
                target_linear_vel = constrain(target_linear_vel, 0, MAX_LIN_VEL, LIN_VEL_STEP_SIZE,'increase')
                target_angular_vel = constrain(target_angular_vel, 0, MAX_ANG_VEL, ANG_VEL_STEP_SIZE,'increase')
                print(vels(target_linear_vel,target_angular_vel))

            elif key == 'x' :
                target_linear_vel = constrain(target_linear_vel, 0, MAX_LIN_VEL, LIN_VEL_STEP_SIZE, 'decrease')
                target_angular_vel = constrain(target_angular_vel, 0, MAX_ANG_VEL, ANG_VEL_STEP_SIZE, 'decrease')               
                print(vels(target_linear_vel,target_angular_vel))

        

            elif key == '' :
                #target_linear_vel   = 0.0
                control_linear_vel  = 0.0
                #target_angular_vel  = 0.0
                control_angular_vel = 0.0
                #print(vels_update(control_linear_vel, control_angular_vel))
            else:
                if (key == '\x03'):
                    break
            

            twist = Twist()

            #control_linear_vel = makeSimpleProfile(control_linear_vel, target_linear_vel, (LIN_VEL_STEP_SIZE/2.0))
            twist.linear.x = control_linear_vel
            twist.linear.y = 0.0
            twist.linear.z = 0.0

            #control_angular_vel = makeSimpleProfile(control_angular_vel, target_angular_vel, (ANG_VEL_STEP_SIZE/2.0))
            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = control_angular_vel
            print(vels_update(control_linear_vel, control_angular_vel))

            pub.publish(twist)

    except:
        print(e)

    finally:
        twist = Twist()
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub.publish(twist)

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
