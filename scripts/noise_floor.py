"""Measure how much each lidar beam wobbles while nothing moves.

Usage:
    python scripts/noise_floor.py path/to/static_01.bag

Fill in the three TODO lines, then run it.
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from rosbags.highlevel import AnyReader

bag_path = Path(sys.argv[1] if len(sys.argv) > 1 else "static_01.bag")

scans = []
with AnyReader([bag_path]) as reader:
    conns = [c for c in reader.connections if c.topic == "/scan"]
    for conn, timestamp, raw in reader.messages(connections=conns):
        msg = reader.deserialize(raw, conn.msgtype)
        scans.append(np.array(msg.ranges, dtype=float))

# Scans can differ by a beam or two in length, so cut them all to the shortest.
n_beams = min(len(s) for s in scans)
data = np.stack([s[:n_beams] for s in scans])  # shape: (number of scans, number of beams)
print("data shape:", data.shape)

# 'inf' means no echo. Turn it into NaN ("not a number") so numpy can skip it.
data[~np.isfinite(data)] = np.nan

# TODO 1: the average distance of each beam over all scans (one number per beam).
#         Hint: np.nanmean(..., axis=0) averages down each column and skips NaN.
mean_dist = None

# TODO 2: the spread (standard deviation) of each beam over all scans.
#         Hint: same idea, with np.nanstd.
spread = None

# TODO 3: the spread as a percentage of the distance.
spread_pct = None

print(f"median spread: {np.nanmedian(spread) * 100:.1f} cm")
print(f"median spread as % of distance: {np.nanmedian(spread_pct):.2f} %")

plt.scatter(mean_dist, spread * 100, s=3)
plt.xlabel("average distance of the beam (m)")
plt.ylabel("spread over time (cm)")
plt.title("Noise floor: how much a still beam wobbles")
plt.show()
