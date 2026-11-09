# Lidar Robot

Person detection and following with a 2D lidar on a Waveshare JetRacer ROS kit
(Jetson Nano, ROS Melodic, RPLIDAR A1). The lidar detector is trained on labels
generated automatically from the robot's camera.

## Layout

- `scripts/load_scan.py`: load a rosbag with `/scan` and plot one scan from above.
- `scripts/noise_floor.py`: exercise, measure how much each beam wobbles in a still recording.

## Setup (laptop)

```
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows PowerShell
pip install -r requirements.txt
python scripts/load_scan.py path/to/static_01.bag
```

Recordings (`*.bag`) are not stored in git because they are large.
