"""
Example: Download features and run a simple training experiment

This script demonstrates how to:
1. Download features from HuggingFace
2. Update CSV paths
3. Run training programmatically
"""

import os
import subprocess
from pathlib import Path


def download_example_features():
    """Download a small subset of features for quick testing."""
    print("=" * 60)
    print("Step 1: Downloading example features")
    print("=" * 60)

    # Download features for one task and one model
    cmd = [
        "python", "download_features.py",
        "--task", "HANCOCK_Chemotherapy_OS",
        "--modality", "Multi_Stain",
        "--models", "virchow2",
        "--output_dir", "./data/features"
    ]

    subprocess.run(cmd, check=True)
    print("\n✓ Features downloaded successfully!\n")


def update_csv_paths():
    """Update CSV files to point to local feature directory."""
    print("=" * 60)
    print("Step 2: Updating CSV paths")
    print("=" * 60)

    cmd = [
        "python", "utils/update_csv_paths.py",
        "--csv_dir", "dataset_csv",
        "--feature_dir", "./data/features"
    ]

    subprocess.run(cmd, check=True)
    print("\n✓ CSV paths updated successfully!\n")


def run_training():
    """Run a simple training experiment."""
    print("=" * 60)
    print("Step 3: Running training")
    print("=" * 60)

    # Create a minimal training script
    training_script = """#!/bin/bash
# Minimal training script for testing

task_name=HANCOCK_Chemotherapy_OS
modal=ALL
current_prefix="splits712"

LOG_DIR="logs"
RESULTS_BASE_DIR="results/experiments/train/splits712"
DATA_ROOT_BASE_DIR="data/features"

mkdir -p "$LOG_DIR"

task_with_modal="${task_name}_survival"
data_root_dir="${DATA_ROOT_BASE_DIR}/${task_name}"
results_dir="${RESULTS_BASE_DIR}/${task_with_modal}"
split_dir="$current_prefix/${task_name}_survival_100"
root_log="${LOG_DIR}/train_log_${task_name}_"

# Use only virchow2 for quick testing
backbones="virchow2"

declare -A in_dim
in_dim["virchow2"]=2560

n_classes=5
seed=1024
preloading="no"
patch_size="512"
GPU_ID=${CUDA_VISIBLE_DEVICES:-0}

echo "Using GPU: $GPU_ID"
echo "Starting training for: $backbones"

for backbone in $backbones
do
    model="att_mil"
    exp=$model"/"$backbone

    echo "Training $exp on GPU: $GPU_ID"

    CUDA_VISIBLE_DEVICES=${GPU_ID} python main.py \\
        --seed $seed \\
        --split_dir $split_dir \\
        --drop_out \\
        --task_type survival \\
        --data_root_dir $data_root_dir \\
        --bag_loss nll_surv \\
        --lr 2e-4 \\
        --reg 1e-4 \\
        --k 5 \\
        --k_start 0 \\
        --k_end 0 \\
        --label_frac 1.0 \\
        --max_epochs 5 \\
        --exp_code $exp \\
        --patch_size $patch_size \\
        --weighted_sample \\
        --task $task_with_modal \\
        --backbone $backbone \\
        --results_dir $results_dir \\
        --model_type $model \\
        --log_data \\
        --preloading $preloading \\
        --n_classes $n_classes \\
        --in_dim ${in_dim[$backbone]} > "${root_log}${model}_${backbone}.log" 2>&1

    echo "Completed $exp"
done

echo "✓ Training completed!"
"""

    # Save the training script
    script_path = Path("train_scripts/example_quick_test.sh")
    script_path.parent.mkdir(parents=True, exist_ok=True)
    script_path.write_text(training_script)
    script_path.chmod(0o755)

    print(f"Created training script: {script_path}")
    print("Running training (this may take a few minutes)...\n")

    # Run the training script
    subprocess.run(["bash", str(script_path)], check=True)

    print("\n✓ Training completed successfully!\n")


def main():
    """Run the complete example workflow."""
    print("\n" + "=" * 60)
    print("ImmunoBench Quick Start Example")
    print("=" * 60 + "\n")

    print("This script will:")
    print("1. Download example features (virchow2 for HANCOCK_Chemotherapy_OS)")
    print("2. Update CSV paths to point to local features")
    print("3. Run a quick training experiment (1 fold, 5 epochs)")
    print("\nNote: This may take 10-30 minutes depending on your internet speed and GPU.\n")

    response = input("Continue? (y/n): ")
    if response.lower() != 'y':
        print("Aborted.")
        return

    try:
        # Step 1: Download features
        download_example_features()

        # Step 2: Update CSV paths
        update_csv_paths()

        # Step 3: Run training
        run_training()

        print("=" * 60)
        print("Example completed successfully!")
        print("=" * 60)
        print("\nResults saved to:")
        print("  - Logs: logs/train_log_HANCOCK_Chemotherapy_OS_att_mil_virchow2.log")
        print("  - Results: results/experiments/train/splits712/HANCOCK_Chemotherapy_OS_survival/")
        print("\nNext steps:")
        print("  - Check the log file to see training progress")
        print("  - Explore other tasks in train_scripts/")
        print("  - Try different foundation models")
        print("  - See README.md for more details")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nPlease check:")
        print("  1. You have installed all requirements (pip install -r requirements.txt)")
        print("  2. You have a GPU available (or modify the script for CPU)")
        print("  3. You have enough disk space for features (~2-5 GB)")
        raise


if __name__ == '__main__':
    main()
