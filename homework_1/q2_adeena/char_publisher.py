import rclpy
from rclpy.node import Node
from std_msgs.msg import Char


class CharPublisher(Node):
    def __init__(self):
        super().__init__('char_publisher')

        self.publisher_ = self.create_publisher(
            Char,
            'character_topic',
            10
        )

    def run(self):
        while rclpy.ok():
            user_input = input("Enter one character: ")

            if len(user_input) != 1:
                print("Please enter exactly one character.")
                continue

            msg = Char()
            msg.data = ord(user_input)

            self.publisher_.publish(msg)

            self.get_logger().info(
                f'Published: {user_input}'
            )


def main(args=None):
    rclpy.init(args=args)

    node = CharPublisher()
    node.run()

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()