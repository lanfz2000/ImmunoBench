# ImmunoBench: A Benchmark for Immunohistochemistry-based Prediction Tasks

\[ [Paper (Coming Soon)]() | [Features on HuggingFace](https://huggingface.co/datasets/AI4Pathology/ImmunoBench-image-features) \]

Welcome to the official GitHub repository of **ImmunoBench**, a comprehensive benchmark for evaluating foundation models on immunohistochemistry (IHC)-based prediction tasks in computational pathology.

<p align="center">
  <img src="figures/Fig1.jpg" alt="ImmunoBench Overview" width="100%">
</p>

<br/>

## What is ImmunoBench?

ImmunoBench provides:
- **Pre-extracted Features**: Ready-to-use image features from 15 foundation models for pathology
- **Multiple Tasks**: Survival prediction, recurrence prediction, and treatment response tasks
- **Multi-Stain Support**: Features from H&E-only, IHC-only, and multi-stain approaches
- **Easy-to-Use Scripts**: Simple training scripts to benchmark models on various clinical prediction tasks

<br/>

## Updates

- **29.04.26**: Initial release of ImmunoBench training scripts and feature access instructions

<br/>

## Dataset Structure

The ImmunoBench features are organized on HuggingFace as follows:

```
ImmunoBench-image-features/
├── HANCOCK_Chemotherapy_DSS/
│   ├── HE_Only/
│   │   └── pt_files/
│   │       ├── virchow/
│   │       ├── virchow2/
│   │       ├── gigapath_wsi/
│   │       └── ...
│   ├── IHCs_Only/
│   │   └── pt_files/
│   │       └── ...
│   └── Multi_Stain/
│       └── pt_files/
│           └── ...
├── HANCOCK_Chemotherapy_OS/
├── HANCOCK_Chemotherapy_Recurrence/
├── HANCOCK_Radiotherapy_DSS/
├── HANCOCK_Radiotherapy_OS/
├── HANCOCK_Radiotherapy_Recurrence/
├── HANCOCK_Surgery_DSS/
├── HANCOCK_Surgery_OS/
└── HANCOCK_Surgery_Recurrence/
```

Each task folder contains three modality subfolders:
- **HE_Only**: Features extracted from H&E stained images only
- **IHCs_Only**: Features extracted from IHC stained images only  
- **Multi_Stain**: Features from both H&E and IHC stains combined

Within each modality, features are organized by foundation model (e.g., `virchow`, `virchow2`, `gigapath_wsi`, `uni`, `conch`, etc.).

**Note:** We provide training scripts and CSV files for all three modalities:
- Files without suffix (e.g., `survival_HANCOCK_Chemotherapy_OS.sh`) use **Multi_Stain** features
- Files with `_HE` suffix use **HE_Only** features
- Files with `_IHC` suffix use **IHCs_Only** features

### Modality Mapping

The file naming convention follows this pattern:

| CSV File Suffix | Modality | HuggingFace Folder | Training Script Suffix |
|----------------|----------|-------------------|----------------------|
| (none) | ALL | `Multi_Stain/` | (none) |
| `_HE` | HE | `HE_Only/` | `_HE` |
| `_IHC` | IHC | `IHCs_Only/` | `_IHC` |

**Examples:**
- `HANCOCK_Chemotherapy_OS_survival.csv` → `Multi_Stain/` → `survival_HANCOCK_Chemotherapy_OS.sh`
- `HANCOCK_Chemotherapy_OS_survival_HE.csv` → `HE_Only/` → `survival_HANCOCK_Chemotherapy_OS_HE.sh`
- `HANCOCK_Chemotherapy_OS_survival_IHC.csv` → `IHCs_Only/` → `survival_HANCOCK_Chemotherapy_OS_IHC.sh`

<br/>

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/immune_bench.git
cd immune_bench
conda create -n "immunobench" python=3.9
conda activate immunobench
pip install -r requirements.txt
```

<br/>

## Quick Start

Here's a complete workflow to get started with ImmunoBench:

### Step 1: Download Features

```python
from huggingface_hub import snapshot_download

# Download all features for a specific task
snapshot_download(
    repo_id="AI4Pathology/ImmunoBench-image-features",
    repo_type="dataset",
    local_dir="./data/features",
    allow_patterns="HANCOCK_Chemotherapy_OS/**"
)
```

Or download specific modality and model:

```python
# Download only Multi_Stain features for virchow2
snapshot_download(
    repo_id="AI4Pathology/ImmunoBench-image-features",
    repo_type="dataset",
    local_dir="./data/features",
    allow_patterns="HANCOCK_Chemotherapy_OS/Multi_Stain/pt_files/virchow2/**"
)

# Download only HE_Only features
snapshot_download(
    repo_id="AI4Pathology/ImmunoBench-image-features",
    repo_type="dataset",
    local_dir="./data/features",
    allow_patterns="HANCOCK_Chemotherapy_OS/HE_Only/**"
)
```

### Step 2: Update CSV Paths

The `update_csv_paths.py` script automatically detects the modality from CSV filenames and maps to the correct folders:

```bash
python utils/update_csv_paths.py \
    --csv_dir dataset_csv \
    --feature_dir ./data/features
```

This will update:
- `HANCOCK_Chemotherapy_OS_survival.csv` → `data/features/HANCOCK_Chemotherapy_OS/Multi_Stain/`
- `HANCOCK_Chemotherapy_OS_survival_HE.csv` → `data/features/HANCOCK_Chemotherapy_OS/HE_Only/`
- `HANCOCK_Chemotherapy_OS_survival_IHC.csv` → `data/features/HANCOCK_Chemotherapy_OS/IHCs_Only/`

### Step 3: Run Training

```bash
cd train_scripts

# Train with Multi_Stain features
bash survival_HANCOCK_Chemotherapy_OS.sh

# Or train with HE Only features
bash survival_HANCOCK_Chemotherapy_OS_HE.sh

# Or train with IHC Only features
bash survival_HANCOCK_Chemotherapy_OS_IHC.sh
```

### Step 4: View Results

Results are saved with modality-specific directories:
```
results/experiments/train/splits712/
├── HANCOCK_Chemotherapy_OS_survival/          # Multi_Stain results
├── HANCOCK_Chemotherapy_OS_survival_HE/       # HE Only results
└── HANCOCK_Chemotherapy_OS_survival_IHC/      # IHC Only results
```

<br/>

## Download Pre-extracted Features

You can download features using the HuggingFace Hub Python API or the command-line tool.

### Method 1: Python API (Recommended)

See the [Quick Start](#quick-start) section above for examples.

### Method 2: Using the Download Script

We provide a helper script for easier downloading:

```bash
# Download all modalities for a specific task
python download_features.py \
    --task HANCOCK_Chemotherapy_OS \
    --output_dir ./data/features

# Download specific modality
python download_features.py \
    --task HANCOCK_Chemotherapy_OS \
    --modality Multi_Stain \
    --output_dir ./data/features

# Download specific models only
python download_features.py \
    --task HANCOCK_Chemotherapy_OS \
    --modality Multi_Stain \
    --models virchow2 uni \
    --output_dir ./data/features
```

<br/>

## Update Dataset CSV Paths

After downloading the features, update the paths in CSV files to point to your local directory.

The `update_csv_paths.py` script automatically:
- Detects modality from CSV filename (no suffix = ALL, `_HE` = HE, `_IHC` = IHC)
- Maps to the correct HuggingFace folder (Multi_Stain, HE_Only, or IHCs_Only)
- Updates all CSV files in batch

```bash
python utils/update_csv_paths.py \
    --csv_dir dataset_csv \
    --feature_dir ./data/features
```

**Manual update example:**

```python
import pandas as pd

# Example: Update paths for survival task
csv_path = "dataset_csv/HANCOCK_Chemotherapy_OS_survival.csv"
df = pd.read_csv(csv_path)

# Replace the old path with your local feature path
old_path = "/tmp/hceph_2_8703562/yanfang/IHC_Benchmarks/data/features_concat/HANCOCK_Chemotherapy_OS"
new_path = "./data/features/HANCOCK_Chemotherapy_OS/Multi_Stain"

df['dir'] = df['dir'].str.replace(old_path, new_path)
df.to_csv(csv_path, index=False)
```

<br/>

## Running Training Scripts

### Example 1: Survival Prediction (HANCOCK Chemotherapy OS)

```bash
cd train_scripts

# Train with Multi_Stain (ALL) features
bash survival_HANCOCK_Chemotherapy_OS.sh

# Or train with HE Only features
bash survival_HANCOCK_Chemotherapy_OS_HE.sh

# Or train with IHC Only features
bash survival_HANCOCK_Chemotherapy_OS_IHC.sh
```

This script will:
1. Prepare data splits (80% train, 20% test, 5-fold cross-validation)
2. Train models using multiple foundation model features
3. Save results to `results/experiments/train/splits712/HANCOCK_Chemotherapy_OS_survival/`
4. Log training progress to `logs/`

### Example 2: Recurrence Prediction (HANCOCK Chemotherapy Recurrence)

```bash
cd train_scripts

# Train with Multi_Stain (ALL) features
bash subtype_HANCOCK_Chemotherapy_Recurrence.sh

# Or train with HE Only features
bash subtype_HANCOCK_Chemotherapy_Recurrence_HE.sh

# Or train with IHC Only features
bash subtype_HANCOCK_Chemotherapy_Recurrence_IHC.sh
```

### Customize Training

You can modify the training scripts to:
- **Change backbones**: Edit the `backbones` variable in the script
  ```bash
  # Train only specific models
  backbones="virchow virchow2"
  
  # Or train all available models
  backbones="chief conch conch_v1_5 ctranspath gigapath GPFM phikon uni h_optimus_0 virchow virchow2"
  ```

- **Change GPU**: Set `CUDA_VISIBLE_DEVICES` before running
  ```bash
  CUDA_VISIBLE_DEVICES=1 bash survival_HANCOCK_Chemotherapy_OS.sh
  ```

- **Modify paths**: Edit configuration variables at the top of each script
  ```bash
  LOG_DIR="logs"
  RESULTS_BASE_DIR="results/experiments/train/splits712"
  DATA_ROOT_BASE_DIR="data/features"
  ```

<br/>

## Available Foundation Models

ImmunoBench includes pre-extracted features from 25+ foundation models:

**Patch-level models:**
- Virchow, Virchow2
- UNI, UNI2-h
- H-Optimus-0, H-Optimus-1
- GigaPath
- CONCH v1, CONCH v1.5
- Phikon, Phikon-v2
- CTransPath
- GPFM
- Chief
- And more...

**WSI-level models:**
- GigaPath-WSI
- Chief-WSI
- Titan-WSI
- Madeleine-WSI

<br/>

## Project Structure

```
immune_bench/
├── train_scripts/              # Training scripts for different tasks
│   ├── survival_HANCOCK_Chemotherapy_OS.sh
│   └── subtype_HANCOCK_Chemotherapy_Recurrence.sh
├── dataset_csv/                # CSV files with data splits and labels
│   ├── HANCOCK_Chemotherapy_OS_survival.csv
│   └── HANCOCK_Chemotherapy_Recurrence_subtyping.csv
├── splits712/                  # Pre-defined train/test splits
├── datasets/                   # Dataset loading utilities
├── mil_models/                 # Multiple Instance Learning model implementations
├── utils/                      # Helper functions
├── main.py                     # Main training script
└── create_splits_seq.py        # Script to create data splits
```

<br/>

## Tasks Overview

ImmunoBench includes multiple clinical prediction tasks:

| Task Type | Task Name | Description | Classes/Bins |
|-----------|-----------|-------------|--------------|
| Survival | HANCOCK_Chemotherapy_OS | Overall survival prediction | 5 bins |
| Survival | HANCOCK_Chemotherapy_DSS | Disease-specific survival | 5 bins |
| Recurrence | HANCOCK_Chemotherapy_Recurrence | Recurrence prediction | Binary |
| Metastasis | HANCOCK_Chemotherapy_Metastatic | Metastasis prediction | Binary |

Similar tasks are available for Radiotherapy and Surgery treatment groups.

<br/>

## Training Arguments

Key arguments for `main.py`:

```bash
--task              # Task name (e.g., HANCOCK_Chemotherapy_OS_survival)
--task_type         # Task type: 'survival' or 'subtyping'
--backbone          # Foundation model name (e.g., virchow2, uni, gigapath)
--model_type        # MIL model: 'att_mil' or 'wsi_mil'
--split_dir         # Directory containing train/test splits
--results_dir       # Output directory for results
--data_root_dir     # Root directory for feature files (survival tasks only)
--n_classes         # Number of classes (2 for binary, 5 for survival)
--in_dim            # Feature dimension (depends on backbone)
--max_epochs        # Maximum training epochs
--lr                # Learning rate
--k                 # Number of folds for cross-validation
--seed              # Random seed for reproducibility
```

<br/>

## Results

Training results will be saved in the specified `results_dir`:

```
results/experiments/train/splits712/HANCOCK_Chemotherapy_OS_survival/
├── att_mil/
│   ├── virchow/
│   │   ├── split_0_results.pkl
│   │   ├── split_1_results.pkl
│   │   └── ...
│   └── virchow2/
└── wsi_mil/
    └── gigapath_wsi/
```

Training logs are saved to the `logs/` directory:
```
logs/
├── train_log_HANCOCK_Chemotherapy_OS_att_mil_virchow.log
├── train_log_HANCOCK_Chemotherapy_OS_att_mil_virchow2.log
└── ...
```

<br/>

## Issues and Support

- For issues related to the code or training scripts, please open a GitHub issue
- For questions about the dataset or features, contact: [your-email@example.com]

<br/>

## License

This project is released under the [LICENSE_TYPE] license.

<br/>

## Acknowledgments

We thank the developers of all foundation models included in this benchmark for making their models publicly available.
