import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class DuvarKontrol(Node):

    def __init__(self):
        super().__init__('duvar_kontrol')

        self.pose = None
        self.hedef_aci = None
        self.kacis_modu = False
        self.hiz = 1.0
        self.son_log = 0.0

        self.abone = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        self.yayinci = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self.timer = self.create_timer(0.1, self.kontrol_et)

        self.get_logger().info('Duvar kontrol sistemi baslatildi.')

    def pose_callback(self, mesaj):
        self.pose = mesaj

    def kontrol_et(self):

        if self.pose is None:
            return

        x = self.pose.x
        y = self.pose.y
        aci = self.pose.theta

        mesaj = Twist()

        if self.get_clock().now().nanoseconds - self.son_log >= 1_000_000_000:
            self.get_logger().info(
                f'Konum: x={x:.2f}, y={y:.2f}'
            )
            self.son_log = self.get_clock().now().nanoseconds

        # Guvenli bolgeye girildiginde kacis modunu kapat.
        if self.kacis_modu:
            if 1.5 <= x <= 9.5 and 1.5 <= y <= 9.5:
                self.kacis_modu = False
                self.hedef_aci = None
                self.get_logger().info('Guvenli bolgeye girildi.')

        # Sinira yaklasildiginda merkeze dogru yon belirle.
        if not self.kacis_modu:
            if x < 1.5 or x > 9.5 or y < 1.5 or y > 9.5:
                self.kacis_modu = True
                self.hedef_aci = math.atan2(5.5 - y, 5.5 - x)

                self.get_logger().info(
                    f'Sinira yaklasildi! Yeni yon: {self.hedef_aci:.2f}'
                )

        # Kacis modunda once hedef yone don, sonra ilerle.
        if self.kacis_modu:

            fark = self.hedef_aci - aci
            fark = math.atan2(math.sin(fark), math.cos(fark))

            if abs(fark) > 0.08:
                mesaj.angular.z = 2.0 if fark > 0 else -2.0
            else:
                mesaj.linear.x = self.hiz

        else:
            mesaj.linear.x = self.hiz

        self.yayinci.publish(mesaj)


def main(args=None):

    rclpy.init(args=args)

    dugum = DuvarKontrol()

    try:
        rclpy.spin(dugum)

    except KeyboardInterrupt:
        pass

    finally:
        dugum.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
