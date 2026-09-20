import rclpy
from rclpy.node import Node
from std_msgs.msg import Char


class CharSubscriber(Node):
    def __init__(self):
        super().__init__('char_subscriber')

        self.subscription = self.create_subscription(
            Char,
            'character_topic',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        character = chr(msg.data)

        self.get_logger().info(
            f'Received: {character}'
        )


def main(args=None):
    rclpy.init(args=args)

    node = CharSubscriber()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()