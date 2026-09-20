import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

import math


class CosineWave(Node):

    def __init__(self):
        super().__init__('cosine_wave')

        # publisher- sends velocity commands to turtle
        self.publisher_ = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        #subscriber -reads current turtle position
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        self.pose = None

        # starting position of the cos wave
        self.x0 = None
        self.y0 = None

        # cos parameters
        self.amplitude = 1.0
        self.frequency = 1.2

        #vel
        self.speed=1.0

        # controller runs 20/s
        self.timer = self.create_timer(
            0.05,
            self.move_turtle
        )

        self.get_logger().info(
            'Cosine wave controller started'
        )


    def pose_callback(self, msg):

        self.pose = msg

        # save initial pos once
        if self.x0 is None:
            self.x0 = msg.x
            self.y0 = msg.y

            self.get_logger().info(
                f'Starting at x={self.x0:.2f}, y={self.y0:.2f}'
            )


    def move_turtle(self):

        if self.pose is None:
            return

        x= self.pose.x
        y= self.pose.y
        theta = self.pose.theta

        A = self.amplitude
        k = self.frequency


        desired_y = self.y0 + A * (
            math.cos(k * (x - self.x0)) - 1
        )
        
        # slope of cosine curve
        # y =Acos(kx)
        # dy/dx= -A k sin(kx)
      

        slope = -A *k* math.sin(
            k * (x - self.x0)
        )


        # desired direction of turtle
        desired_theta = math.atan(slope)


        # diff between current and desired angle
        angle_error = desired_theta - theta


        # angle bw pi n -pi
        angle_error = math.atan2(
            math.sin(angle_error),
            math.cos(angle_error)
        )


        # diff bw desired y n actual y
        y_error= desired_y - y


        
        # twist command
        

        msg = Twist()
        msg.linear.x = self.speed
        msg.angular.z= (
            3.0 * angle_error
            + 1.5 * y_error
        )


        # stop after finishing a wave
        if x > 10.0: :

            msg.linear.x= 0.0
            msg.angular.z= 0.0

            self.publisher_.publish(msg)

            self.get_logger().info(
                'Finished cosine wave'
            )

            self.timer.cancel()

            return


        self.publisher_.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    node = CosineWave()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()