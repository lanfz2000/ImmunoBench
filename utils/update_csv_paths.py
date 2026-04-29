#!/usr/bin/env python3
"""
Update paths in dataset CSV files to point to local feature directories.

Usage:
    python update_csv_paths.py --csv_dir dataset_csv --feature_dir ./data/features
"""

import os
import argparse
import pandas as pd
from pathlib import Path


# Mapping from CSV suffix to HuggingFace modality folder
MODAL_MAPPING = {
    'ALL': 'Multi_Stain',      # No suffix -> Multi_Stain
    'HE': 'HE_Only',            # _HE suffix -> HE_Only
    'IHC': 'IHCs_Only'          # _IHC suffix -> IHCs_Only
}

# Mapping from old path patterns to modal type
OLD_PATH_PATTERNS = {
    'features_concat': 'ALL',
    'features_concat_HE_only': 'HE',
    'features_concat_IHCs_only': 'IHC'
}


def detect_modal_from_path(path):
    """
    Detect modal type from the old path pattern.

    Args:
        path: Old path string

    Returns:
        Modal type ('ALL', 'HE', or 'IHC')
    """
    for pattern, modal in OLD_PATH_PATTERNS.items():
        if pattern in path:
            return modal
    return 'ALL'  # Default to ALL if pattern not found


def detect_modal_from_filename(filename):
    """
    Detect modal type from CSV filename.

    Args:
        filename: CSV filename

    Returns:
        Modal type ('ALL', 'HE', or 'IHC')
    """
    if filename.endswith('_HE.csv'):
        return 'HE'
    elif filename.endswith('_IHC.csv'):
        return 'IHC'
    else:
        return 'ALL'


def update_csv_paths(csv_path, feature_base_dir):
    """
    Update the 'dir' column in a CSV file to point to local feature directory.

    Args:
        csv_path: Path to the CSV file
        feature_base_dir: Base directory where features are stored locally
    """
    print(f"Processing: {csv_path}")

    # Read CSV
    df = pd.read_csv(csv_path)

    if 'dir' not in df.columns:
        print(f"  Warning: No 'dir' column found in {csv_path}, skipping...")
        return

    # Get the first path to extract task name and modal
    sample_path = df['dir'].iloc[0]

    # Detect modal from filename
    filename = os.path.basename(csv_path)
    modal = detect_modal_from_filename(filename)

    # Verify modal matches the path pattern
    path_modal = detect_modal_from_path(sample_path)
    if modal != path_modal:
        print(f"  Warning: Modal mismatch - filename suggests '{modal}' but path suggests '{path_modal}'")
        print(f"  Using modal from filename: {modal}")

    # Extract task name from the old path
    # Example: /tmp/hceph_2_8703562/yanfang/IHC_Benchmarks/data/features_concat/HANCOCK_Chemotherapy_OS
    # We want to extract: HANCOCK_Chemotherapy_OS
    path_parts = sample_path.split('/')
    task_name = path_parts[-1]

    # Get the corresponding HuggingFace modality folder
    hf_modality = MODAL_MAPPING[modal]

    # Construct new path: feature_base_dir/TASK_NAME/MODALITY
    new_base_path = os.path.join(feature_base_dir, task_name, hf_modality)

    # Replace all paths
    old_paths = df['dir'].unique()
    print(f"  Found {len(old_paths)} unique path(s)")
    print(f"  Modal: {modal} -> HuggingFace folder: {hf_modality}")

    for old_path in old_paths:
        df['dir'] = df['dir'].replace(old_path, new_base_path)

    # Save updated CSV
    df.to_csv(csv_path, index=False)
    print(f"  ✓ Updated paths to: {new_base_path}")
    print(f"  ✓ Saved to: {csv_path}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Update paths in dataset CSV files to point to local feature directories"
    )
    parser.add_argument(
        '--csv_dir',
        type=str,
        default='dataset_csv',
        help='Directory containing CSV files (default: dataset_csv)'
    )
    parser.add_argument(
        '--feature_dir',
        type=str,
        default='./data/features',
        help='Base directory where features are stored (default: ./data/features)'
    )
    parser.add_argument(
        '--csv_pattern',
        type=str,
        default='*.csv',
        help='Pattern to match CSV files (default: *.csv)'
    )

    args = parser.parse_args()

    # Convert to absolute paths
    csv_dir = Path(args.csv_dir).resolve()
    feature_dir = Path(args.feature_dir).resolve()

    if not csv_dir.exists():
        print(f"Error: CSV directory not found: {csv_dir}")
        return

    print(f"CSV directory: {csv_dir}")
    print(f"Feature directory: {feature_dir}")
    print("-" * 60)

    # Find all CSV files
    csv_files = list(csv_dir.glob(args.csv_pattern))

    if not csv_files:
        print(f"No CSV files found matching pattern: {args.csv_pattern}")
        return

    print(f"Found {len(csv_files)} CSV file(s)\n")

    # Update each CSV file
    for csv_file in csv_files:
        update_csv_paths(str(csv_file), str(feature_dir))

    print("-" * 60)
    print(f"✓ Successfully updated {len(csv_files)} CSV file(s)")
    print("\nPath mapping:")
    print("  - Files without suffix (ALL) -> Multi_Stain/")
    print("  - Files with _HE suffix (HE) -> HE_Only/")
    print("  - Files with _IHC suffix (IHC) -> IHCs_Only/")


if __name__ == '__main__':
    main()
