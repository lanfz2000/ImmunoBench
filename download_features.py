#!/usr/bin/env python3
"""
Download pre-extracted features from HuggingFace for ImmunoBench.

Usage:
    # Download all features for a specific task
    python download_features.py --task HANCOCK_Chemotherapy_OS --output_dir ./data/features

    # Download features for specific models only
    python download_features.py --task HANCOCK_Chemotherapy_OS --models virchow virchow2 --output_dir ./data/features

    # Download specific modality (HE_Only, IHCs_Only, or Multi_Stain)
    python download_features.py --task HANCOCK_Chemotherapy_OS --modality Multi_Stain --output_dir ./data/features
"""

import argparse
from pathlib import Path
from huggingface_hub import snapshot_download


REPO_ID = "AI4Pathology/ImmunoBench-image-features"

AVAILABLE_TASKS = [
    "HANCOCK_Chemotherapy_DSS",
    "HANCOCK_Chemotherapy_Metastatic",
    "HANCOCK_Chemotherapy_OS",
    "HANCOCK_Chemotherapy_Recurrence",
    "HANCOCK_Radiotherapy_DSS",
    "HANCOCK_Radiotherapy_Metastatic",
    "HANCOCK_Radiotherapy_OS",
    "HANCOCK_Radiotherapy_Recurrence",
    "HANCOCK_Surgery_DSS",
    "HANCOCK_Surgery_Metastatic",
    "HANCOCK_Surgery_OS",
    "HANCOCK_Surgery_Recurrence",
]

AVAILABLE_MODALITIES = ["HE_Only", "IHCs_Only", "Multi_Stain"]

AVAILABLE_MODELS = [
    "chief", "conch", "conch_v1_5", "ctranspath", "gigapath", "GPFM",
    "phikon", "uni", "h_optimus_0", "virchow", "virchow2",
    "chief_wsi", "titan_wsi", "gigapath_wsi", "madeleine_wsi"
]


def download_features(task, output_dir, modality=None, models=None):
    """
    Download features from HuggingFace.

    Args:
        task: Task name (e.g., HANCOCK_Chemotherapy_OS)
        output_dir: Local directory to save features
        modality: Specific modality to download (HE_Only, IHCs_Only, Multi_Stain), or None for all
        models: List of specific models to download, or None for all
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Build pattern for selective download
    patterns = []

    if modality:
        # Download specific modality
        if models:
            # Download specific models within the modality
            for model in models:
                pattern = f"{task}/{modality}/pt_files/{model}/**"
                patterns.append(pattern)
        else:
            # Download all models in the modality
            pattern = f"{task}/{modality}/**"
            patterns.append(pattern)
    else:
        # Download all modalities
        if models:
            # Download specific models across all modalities
            for mod in AVAILABLE_MODALITIES:
                for model in models:
                    pattern = f"{task}/{mod}/pt_files/{model}/**"
                    patterns.append(pattern)
        else:
            # Download everything for the task
            pattern = f"{task}/**"
            patterns.append(pattern)

    print(f"Downloading features for task: {task}")
    print(f"Output directory: {output_path}")
    if modality:
        print(f"Modality: {modality}")
    if models:
        print(f"Models: {', '.join(models)}")
    print(f"Patterns: {patterns}")
    print("-" * 60)

    try:
        snapshot_download(
            repo_id=REPO_ID,
            repo_type="dataset",
            local_dir=str(output_path),
            allow_patterns=patterns,
            resume_download=True,
        )
        print("-" * 60)
        print(f"✓ Successfully downloaded features to: {output_path}")
    except Exception as e:
        print(f"✗ Error downloading features: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Download pre-extracted features from HuggingFace for ImmunoBench"
    )
    parser.add_argument(
        '--task',
        type=str,
        required=True,
        choices=AVAILABLE_TASKS,
        help='Task name to download'
    )
    parser.add_argument(
        '--output_dir',
        type=str,
        default='./data/features',
        help='Output directory for downloaded features (default: ./data/features)'
    )
    parser.add_argument(
        '--modality',
        type=str,
        choices=AVAILABLE_MODALITIES,
        help='Specific modality to download (HE_Only, IHCs_Only, or Multi_Stain). If not specified, downloads all.'
    )
    parser.add_argument(
        '--models',
        type=str,
        nargs='+',
        choices=AVAILABLE_MODELS,
        help='Specific models to download. If not specified, downloads all available models.'
    )

    args = parser.parse_args()

    download_features(
        task=args.task,
        output_dir=args.output_dir,
        modality=args.modality,
        models=args.models
    )


if __name__ == '__main__':
    main()
