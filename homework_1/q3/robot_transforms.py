import rclpy
from rclpy.node import Node
from turtlesim.srv import TeleportAbsolute

from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster

import math


class RobotTransforms(Node):

    def __init__(self):
        super().__init__('robot_transforms')

        #  publishes our coordinate transformations
        self.tf_broadcaster = TransformBroadcaster(self)

        self.teleport_A = self.create_client(
        TeleportAbsolute,
        '/turtle1/teleport_absolute'
        )

        self.teleport_B = self.create_client(
            TeleportAbsolute,
            '/turtle2/teleport_absolute'
        )
        
        self.start_time = self.get_clock().now()

        # vals from q
        self.R = 5.0
        self.omega = 0.40
        self.T = 8.0

        # robot b amp n vel
        self.amplitude = 1.0
        self.v = 0.4

        # 135 degrees in radians
        self.alpha = 3 * math.pi / 4
        

        # Update positions 20 times per second
        self.timer = self.create_timer(
            0.05,
            self.update_robots
        )

        self.get_logger().info(
            'Robot transform publisher started'
        )


    def update_robots(self):

        now = self.get_clock().now()

        t = (now -self.start_time).nanoseconds / 1e9

        # robot A - CIRCLE
        xA = self.R * math.cos(self.omega * t)
        yA = self.R * math.sin(self.omega * t)
        thetaA = self.omega * t + math.pi / 2

        #transform for robot A
        transform_A = TransformStamped()

        # time of this transform
        transform_A.header.stamp = now.to_msg()

        # world -> robot_A
        transform_A.header.frame_id = 'world'
        transform_A.child_frame_id = 'robot_A'

        # position
        transform_A.transform.translation.x = xA
        transform_A.transform.translation.y = yA
        transform_A.transform.translation.z = 0.0

        # orientation (gotta convert to quanternion)
        transform_A.transform.rotation.x = 0.0
        transform_A.transform.rotation.y = 0.0
        transform_A.transform.rotation.z = math.sin(thetaA / 2)
        transform_A.transform.rotation.w = math.cos(thetaA / 2)

        # publish transform
        self.tf_broadcaster.sendTransform(transform_A)

        #now move it to the left so we can see the full circle
        request_A = TeleportAbsolute.Request()

        request_A.x = float(xA + 5.5)
        request_A.y = float(yA + 5.5)
        request_A.theta = float(thetaA)

        self.teleport_A.call_async(request_A)

    #--------------------------------
        #Robot B -  SIN WAVE
        omega_sine = 2 * math.pi / self.T

        # Sideways sin displacement
        q = self.amplitude * math.sin(
            omega_sine * t
        )

        # position
        xB = (
            self.v * t * math.cos(self.alpha)
            - q * math.sin(self.alpha)
        )

        yB = (
            self.v * t * math.sin(self.alpha)
            + q * math.cos(self.alpha)
        )


        # velocity direction
        dxB = (
            self.v * math.cos(self.alpha)
            - self.amplitude
            * omega_sine
            * math.cos(omega_sine * t)
            * math.sin(self.alpha)
        )

        dyB = (
            self.v * math.sin(self.alpha)
            + self.amplitude
            * omega_sine
            * math.cos(omega_sine * t)
            * math.cos(self.alpha)
        )

        # tangent orientation
        thetaB = math.atan2(dyB, dxB)


        transform_B = TransformStamped()

        transform_B.header.stamp = now.to_msg()

        transform_B.header.frame_id = 'world'
        transform_B.child_frame_id = 'robot_B'

        transform_B.transform.translation.x = xB
        transform_B.transform.translation.y = yB
        transform_B.transform.translation.z = 0.0

        transform_B.transform.rotation.x = 0.0
        transform_B.transform.rotation.y = 0.0
        transform_B.transform.rotation.z = math.sin(thetaB / 2)
        transform_B.transform.rotation.w = math.cos(thetaB / 2)

         # publish transform
        self.tf_broadcaster.sendTransform(transform_B)

        #move to the left so we can see the full sine wave
        request_B = TeleportAbsolute.Request()

        request_B.x = float(xB + 5.5)
        request_B.y = float(yB + 5.5)
        request_B.theta = float(thetaB)

        self.teleport_B.call_async(request_B)


def main(args=None):

    rclpy.init(args=args)

    node = RobotTransforms()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()