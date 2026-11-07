"""Load a ROS1 bag with /scan messages and plot one lidar scan.

Usage (from the folder with your .bag file):
    python load_scan.py static_01.bag
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from rosbags.highlevel import AnyReader

bag_path = Path(sys.argv[1] if len(sys.argv) > 1 else "static_01.bag")

# 1. Read every /scan message into a list of range arrays.
scans = []
with AnyReader([bag_path]) as reader:
    conns = [c for c in reader.connections if c.topic == "/scan"]
    for conn, timestamp, raw in reader.messages(connections=conns):
        msg = reader.deserialize(raw, conn.msgtype)
        scans.append(np.array(msg.ranges, dtype=float))
        angle_min, angle_inc = msg.angle_min, msg.angle_increment

print(f"Loaded {len(scans)} scans, {len(scans[0])} beams each")

# 2. Take the first scan and turn (angle, distance) into (x, y).
ranges = scans[0]
angles = angle_min + angle_inc * np.arange(len(ranges))
ok = np.isfinite(ranges)  # drop the 'inf' beams (no echo)
x = ranges[ok] * np.cos(angles[ok])
y = ranges[ok] * np.sin(angles[ok])
print(f"{(~ok).sum()} beams had no echo (inf)")

# 3. Plot it as seen from above. The robot sits at (0, 0).
plt.figure(figsize=(6, 6))
plt.scatter(x, y, s=2)
plt.scatter([0], [0], c="red", marker="x", label="robot")
plt.axis("equal")
plt.xlabel("x (m), forward")
plt.ylabel("y (m), left")
plt.title(f"{bag_path.name}: first scan")
plt.legend()
plt.show()
