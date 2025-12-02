import numpy as np
import pandas as pd
from pathlib import Path

def load_vicon_markers(filepath):
    """
    Load Vicon marker data from exported CSV file.
    """
    # Find the row where marker data starts
    with open(filepath, 'r') as f:
        for i, line in enumerate(f):
            if 'Subject 1:D1' in line:
                marker_row = i
                break

    print(f"Found marker row at line: {marker_row}")

    # Read marker data starting from the identified row
    df = pd.read_csv(filepath, skiprows=marker_row, encoding='latin-1')

    # Clean up column names
    df.columns = df.columns.str.strip()

    print(f"Columns found: {list(df.columns)[:10]}")  # First 10 columns
    print(f"DataFrame shape: {df.shape}")

    return df

def extract_marker_trajectories(df):
    """
    Extract marker trajectories from the loaded DataFrame.
    """
    markers = {}

    # Define marker names based on your setup
    marker_names = ['D1', 'D2', 'DC', 'DT', 'F3', 'F1', 'FC', 'F4', 'F2',
                    'T3', 'T1', 'TC', 'T4', 'T2']

    for marker in marker_names:
        col_prefix = f'Subject 1:{marker}'

        # Find the column with the marker name
        marker_cols = [i for i, col in enumerate(df.columns) if col == col_prefix]

        if len(marker_cols) > 0:
            # The marker name column is found, X Y Z data are in the next 3 columns
            marker_col_idx = marker_cols[0]

            # Check if there are at least 3 more columns after the marker column
            if marker_col_idx + 3 <= len(df.columns):
                try:
                    # Extract X, Y, Z from the 3 columns immediately after the marker name
                    x = pd.to_numeric(df.iloc[2:, marker_col_idx], errors='coerce').values
                    y = pd.to_numeric(df.iloc[2:, marker_col_idx + 1], errors='coerce').values
                    z = pd.to_numeric(df.iloc[2:, marker_col_idx + 2], errors='coerce').values

                    # Stack into (N x 3) array
                    markers[marker] = np.column_stack([x, y, z])
                    print(f"  -> Successfully extracted {marker}: {markers[marker].shape}")
                except Exception as e:
                    print(f"  -> Warning: Could not extract marker {marker}: {e}")

    return markers

# Test with the varus bending file
filepath = Path('data/dynamic _trial_bending&varus_motion 1.csv')
print(f"Testing file: {filepath}")
print("="*80)

df = load_vicon_markers(filepath)
markers = extract_marker_trajectories(df)

print("\n" + "="*80)
print(f"Total markers extracted: {len(markers)}")
print(f"Markers: {list(markers.keys())}")
