import pandas as pd
import numpy as np

CSV = r"c:\Users\sitix\OneDrive - Singapore University of Technology and Design\Desktop\DAI\Capstone\HKA\mechanicalaxiscomputation\data\Static_Trial_Bone_Model.csv"

# Robust loader (same logic as in notebook)

def load_mocap_csv(filepath):
    header_row = None
    marker_name_row = None
    try:
        with open(filepath, 'r', encoding='latin-1') as f:
            lines = [next(f) for _ in range(40)]
    except Exception as e:
        lines = []

    for i, line in enumerate(lines):
        if 'Frame' in line and 'Sub Frame' in line:
            header_row = i
            marker_name_row = i - 1 if i > 0 else None
            break

    try:
        if header_row is not None and marker_name_row is not None:
            df = pd.read_csv(filepath, header=[marker_name_row, header_row], encoding='latin-1')
            if isinstance(df.columns, pd.MultiIndex):
                new_cols = []
                for a, b in df.columns:
                    a_str = '' if pd.isna(a) else str(a).strip()
                    b_str = '' if pd.isna(b) else str(b).strip()
                    if a_str and b_str:
                        new_cols.append(f"{a_str}:{b_str}")
                    else:
                        new_cols.append(a_str or b_str)
                df.columns = new_cols
        else:
            df = pd.read_csv(filepath, encoding='latin-1')
    except Exception as e:
        print('Read failed, error:', e)
        df = pd.read_csv(filepath, encoding='latin-1')

    try:
        if df.shape[0] > 0 and df.iloc[0].astype(str).str.contains('mm|N').any():
            df = df.iloc[1:].reset_index(drop=True)
    except Exception:
        pass

    for col in df.columns:
        if str(col).strip() in ['Frame', 'Sub Frame']:
            continue
        try:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        except Exception:
            pass

    return df


def get_all_markers(df):
    import re
    markers = []
    pattern = re.compile(r"(?:(?:Subject\s*\d+)?:)?(?P<marker>[A-Za-z0-9_]+):[XYZ]$")
    for col in df.columns:
        s = str(col).strip()
        m = pattern.search(s)
        if m:
            candidate = m.group('marker')
            if candidate not in markers and candidate not in ['Frame', 'Sub Frame', 'X', 'Y', 'Z', 'mm']:
                markers.append(candidate)
    return markers

if __name__ == '__main__':
    df = load_mocap_csv(CSV)
    print('Columns (first 50):')
    print(df.columns[:50])
    print('\nNumber of columns:', len(df.columns))
    markers = get_all_markers(df)
    print('\nDetected markers:')
    print(markers)
    print('\nFirst data row:')
    print(df.iloc[0].head(20))
