#!/usr/bin/env python3
"""Republish Fixposition rawimu (FpaImu) as sensor_msgs/Imu on /fixposition/imu for LIO-SAM.

FpaImu wraps a complete sensor_msgs/Imu in its `data` field; it is published
unchanged, with the device timestamps. Requires the host clock to be synced to
the unit, since the LiDAR is stamped with the host clock.

Uses rawimu: corrimu stays zero without a GNSS fix.

Parameters:
  gyro_bias  [rad/s]  subtracted from angular_velocity (IMU frame)
  accel_bias [m/s^2]  subtracted from linear_acceleration (IMU frame)
"""
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from fixposition_driver_msgs.msg import FpaImu
from sensor_msgs.msg import Imu

INPUT_TOPIC = '/fixposition/fpa/rawimu'
OUTPUT_TOPIC = '/fixposition/imu'

# LiDAR_IMU_Init, 2026-09-30
DEFAULT_GYRO_BIAS = [-0.006683, 0.001984, 0.012579]
DEFAULT_ACCEL_BIAS = [0.013923, -0.010440, 0.004416]


class FixpositionImuBridge(Node):
    def __init__(self):
        super().__init__('fixposition_imu_bridge')
        self.gyro_bias = self.declare_parameter('gyro_bias', DEFAULT_GYRO_BIAS).value
        self.accel_bias = self.declare_parameter('accel_bias', DEFAULT_ACCEL_BIAS).value
        self.pub = self.create_publisher(Imu, OUTPUT_TOPIC, 10)
        # Driver publishes BEST_EFFORT; must match QoS or we get nothing.
        self.sub = self.create_subscription(
            FpaImu, INPUT_TOPIC, self.on_rawimu, qos_profile_sensor_data)
        self.get_logger().info(f'Bridging {INPUT_TOPIC} -> {OUTPUT_TOPIC}')

    def on_rawimu(self, msg: FpaImu):
        imu = msg.data
        imu.angular_velocity.x -= self.gyro_bias[0]
        imu.angular_velocity.y -= self.gyro_bias[1]
        imu.angular_velocity.z -= self.gyro_bias[2]
        imu.linear_acceleration.x -= self.accel_bias[0]
        imu.linear_acceleration.y -= self.accel_bias[1]
        imu.linear_acceleration.z -= self.accel_bias[2]
        self.pub.publish(imu)


def main():
    rclpy.init()
    node = FixpositionImuBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
