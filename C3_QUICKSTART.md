# FAST-LIO2 on the C3 sensor kit — quick start

Pandar40P + Fixposition Vision-RTK 2, ROS 2 Humble.

## 1. Before recording

Laptop clock synced to the Fixposition unit (scripts from the `C3_Sync_Fix` folder):

```bash
./clock_sync_check.sh        # must end with ALL CHECKS PASSED
```

## 2. Build

```bash
mkdir -p ~/fastlio_ws/src && cd ~/fastlio_ws/src
git clone --recursive -b c3-hesai https://github.com/AmirZV/FAST_LIO_ROS2.git
cd .. && source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -y
colcon build --symlink-install
```

## 3. Run

In every terminal:

```bash
source /opt/ros/humble/setup.bash
source <driver workspace>/install/setup.bash
source ~/fastlio_ws/install/setup.bash
```

Live — with the Hesai and Fixposition drivers running (`/lidar_points`, `/fixposition/fpa/rawimu`):

```bash
# terminal 1
python3 ~/fastlio_ws/src/FAST_LIO_ROS2/scripts/c3_fixposition_imu_bridge.py
# terminal 2
ros2 launch fast_lio mapping.launch.py config_file:=hesai_c3.yaml
```

Bag replay:

```bash
# terminal 1
python3 ~/fastlio_ws/src/FAST_LIO_ROS2/scripts/c3_fixposition_imu_bridge.py --ros-args -p use_sim_time:=true
# terminal 2
ros2 launch fast_lio mapping.launch.py config_file:=hesai_c3.yaml use_sim_time:=true
# terminal 3
ros2 bag play <bag> --clock
```

## 4. Map

Saved automatically to `~/fastlio_ws/src/FAST_LIO_ROS2/PCD/scans_N.pcd` (every 600 scans) and `scans.pcd` (rest, on Ctrl+C).
