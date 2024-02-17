import rclpy
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile
from std_msgs.msg import Empty
from time import sleep

OMO_R1MINI_MAX_LIN_VEL = 0.50

LIN_VEL_STEP_SIZE = 0.01


def constrain(input_vel, low_bound, high_bound):
    if input_vel < low_bound:
        input_vel = low_bound
    elif input_vel > high_bound:
        input_vel = high_bound
    else:
        input_vel = input_vel

    return input_vel

def main():
    rclpy.init()
    print('START!@!!!!!!')
    qos = QoSProfile(depth=10)
    node = rclpy.create_node('auto_drive_node')
    pub = node.create_publisher(Twist, 'cmd_vel', qos)
    
    status = 0
    target_linear_velocity = 0.1
    control_linear_velocity = 0.0

    try:
        while (1):
            twist = Twist()

            control_linear_velocity = constrain(target_linear_velocity, -OMO_R1MINI_MAX_LIN_VEL, OMO_R1MINI_MAX_LIN_VEL)

            twist.linear.x = control_linear_velocity
            twist.linear.y = 0.0
            twist.linear.z = 0.0

            pub.publish(twist)
            status += 1


            twist = Twist()

    except KeyboardInterrupt:
        print("\nAuto-Driving Stopped")
    except Exception as e:
        print(e)

    finally:
        twist = Twist()
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0

        pub.publish(twist)
        rclpy.shutdown()

if __name__ == '__main__':
    main()

