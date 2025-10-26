from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd


MARKERS: List[str] = [
    "uFH", "FH", "MC", "uFD", "lFD", "MFEC", "LFEC",
    "LTC", "MTC", "uTD", "lTD", "Heel", "MM", "LM", "Toe",
]


# -------------------------------
# 1) Data Loading: Parsing helpers
# -------------------------------

AXES = ("X", "Y", "Z")


# ---------------------------------
# 2) Preprocessing
# ---------------------------------


# def open_data(path_data):
#     df = pd.read_csv(path_data)
#     return df


df = pd.read_csv("./data/Static_Trial_Bone_Model.csv",header=None)

def markers_point(df):
    df = df.drop(df.index[0:5]).reset_index(drop=True)
    df = df.drop(df.columns[0], axis=1)
    markers_dict = {marker: {"x": [], "y": [], "z": []}for marker in MARKERS}
    for index in range(len(df)):
            row = df.iloc[index]
            col_start = 0

            for marker in MARKERS:
                # get 3 columns (x, y, z)
                x, y, z = map(float, row[col_start: col_start + 3].tolist())
                markers_dict[marker]["x"].append(x)
                markers_dict[marker]["y"].append(y)
                markers_dict[marker]["z"].append(z)

                col_start += 3  # move to the next marker

    return markers_dict  

def average_static_frames(markers_dict):
    """Average XYZ positions over static trial frames to reduce noise.

    Placeholder: compute mean across rows for each (marker, axis). Should return a Series
    with MultiIndex (marker, axis) or a 1-row DataFrame.
    """
    marker_averages = {}
    for marker, axes in markers_dict.items():
        avg_x = np.mean(axes["x"])
        avg_y = np.mean(axes["y"])
        avg_z = np.mean(axes["z"])
        marker_averages[marker] = {"x": avg_x, "y": avg_y, "z": avg_z}
    return marker_averages
    
# markers_data = markers_point(df)
# print(average_static_frames(markers_data))


# ---------------------------------
# 3) Landmark Extraction
# ---------------------------------

def compute_joint_center_femoral_head(*args, **kwargs):
    """Estimate hip joint center (HJC).
    """
    raise NotImplementedError


def compute_knee_center(*args, **kwargs):
    """Compute knee joint center as midpoint of medial/lateral epicondyles."""
    raise NotImplementedError


def compute_ankle_center(*args, **kwargs):
    """Compute ankle joint center as midpoint of malleoli."""
    raise NotImplementedError


# ---------------------------------------------
# 4) Mechanical Axis + 5) Dynamics
# ---------------------------------------------

def compute_mechanical_axis_vector(*args, **kwargs):
    """Compute mechanical axis vector: AnkleCenter - HipCenter."""
    raise NotImplementedError


def compute_axis_angle_relative_to_reference(*args, **kwargs):
    """Angle of axis relative to a reference (e.g., supine static axis)."""
    raise NotImplementedError


def visualize_axis_in_3D(*args, **kwargs):
    """3D visualization of markers and mechanical axis (matplotlib/plotly)."""
    raise NotImplementedError


def track_axis_over_time(*args, **kwargs):
    """Track mechanical axis over frames for dynamic trials."""
    raise NotImplementedError


def compute_axis_variation_metrics(*args, **kwargs):
    """Compute metrics like axis length variance, varus-valgus angle, etc."""
    raise NotImplementedError


def plot_axis_time_series(*args, **kwargs):
    """Plot temporal changes of axis-related angles/metrics."""
    raise NotImplementedError


# ---------------------------------
# 6) Outputs
# ---------------------------------

def export_results_csv(*args, **kwargs):
    """Export computed results to CSV."""
    raise NotImplementedError


def save_visualizations(*args, **kwargs):
    """Save plots/visualizations to disk."""
    raise NotImplementedError


# -------------------------------
# Run main
# -------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
