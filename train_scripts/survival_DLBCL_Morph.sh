#!/bin/bash
# Training script for DLBCL Morph survival task
# This script can be run directly without SLURM

# ==========================================
# Configuration Variables
# ==========================================
# Task configuration
task_name=DLBCL_Morph
modal=ALL
current_prefix="splits712"

# Path configuration - modify these according to your setup
LOG_DIR="logs"
RESULTS_BASE_DIR="results/experiments/train/splits712"
DATA_ROOT_BASE_DIR="features"

# Create necessary directories
mkdir -p "$LOG_DIR"

# Determine task name with modal suffix
if [ "$modal" == "ALL" ] || [ -z "$modal" ]; then
    task_with_modal="${task_name}_survival"
    data_root_dir="${DATA_ROOT_BASE_DIR}/${task_name}"
    results_dir="${RESULTS_BASE_DIR}/${task_with_modal}"
    root_log="${LOG_DIR}/train_log_${task_name}_"
else
    task_with_modal="${task_name}_survival"
    if [ "$modal" == "HE" ]; then
        data_root_dir="${DATA_ROOT_BASE_DIR}/${task_name}/HE_Only"
    elif [ "$modal" == "IHC" ]; then
        data_root_dir="${DATA_ROOT_BASE_DIR}/${task_name}/IHCs_Only"
    else
        data_root_dir="${DATA_ROOT_BASE_DIR}/${task_name}/Multi_Stain"
    fi
    results_dir="${RESULTS_BASE_DIR}/${task_with_modal}_${modal}"
    root_log="${LOG_DIR}/train_log_${task_name}_${modal}_"
fi

split_dir="$current_prefix/${task_name}_survival_100"

# ==========================================
# Data Preparation
# ==========================================
echo "Preparing survival data splits..."
python re_create_survival_csv.py --task_name $task_name --task_modal $modal
python create_splits_seq.py --test_frac 0.2 --val_frac 0.1 --prefix $current_prefix --k 5 --task "${task_with_modal}" --seed 1024

# ==========================================
# Model Configuration
# ==========================================
backbones="chief conch conch_v1_5 ctranspath gigapath GPFM phikon uni h_optimus_0 virchow virchow2 chief_wsi titan_wsi gigapath_wsi madeleine_wsi"

declare -A in_dim
in_dim["phikon"]=768
in_dim["chief"]=768
in_dim["conch_v1_5"]=768
in_dim["conch"]=512
in_dim["ctranspath"]=768
in_dim["gigapath"]=1536
in_dim["GPFM"]=1024
in_dim["uni"]=1024
in_dim["virchow"]=2560
in_dim["virchow2"]=2560
in_dim["h_optimus_0"]=1536
in_dim["chief_wsi"]=768
in_dim["titan_wsi"]=768
in_dim["gigapath_wsi"]=768
in_dim["madeleine_wsi"]=512

# Training parameters
n_classes=5
seed=1024
preloading="no"
patch_size="512"

# ==========================================
# GPU Configuration
# ==========================================
GPU_ID=${CUDA_VISIBLE_DEVICES:-0}
echo "Using GPU: $GPU_ID"

# ==========================================
# Training Loop
# ==========================================
echo "Starting survival training for backbones: $backbones"

for backbone in $backbones
do
    if [[ $backbone == *"wsi"* ]]; then
        model="wsi_mil"
    else
        model="att_mil"
    fi
    exp=$model"/"$backbone

    echo "Training $exp on GPU: $GPU_ID"

    CUDA_VISIBLE_DEVICES=${GPU_ID} python main.py \
        --seed $seed \
        --split_dir $split_dir \
        --drop_out \
        --task_type survival \
        --data_root_dir $data_root_dir \
        --bag_loss ce_surv \
        --lr 2e-4 \
        --reg 1e-4 \
        --k 5 \
        --k_start 0 \
        --k_end -1 \
        --label_frac 1.0 \
        --max_epochs 30 \
        --exp_code $exp \
        --patch_size $patch_size \
        --weighted_sample \
        --task $task_with_modal \
        --backbone $backbone \
        --results_dir $results_dir \
        --model_type $model \
        --log_data \
        --preloading $preloading \
        --n_classes $n_classes \
        --in_dim ${in_dim[$backbone]} > "${root_log}${model}_${backbone}.log" 2>&1

    echo "Completed $exp"
done

echo "All survival training tasks completed!"
