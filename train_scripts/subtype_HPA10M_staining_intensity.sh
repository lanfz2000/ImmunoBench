#!/bin/bash  # 确保使用 Bash（而不是sh）

# process the csv file
cd /mnt/petrelfs/yanfang/project/IHC_Benchmarks/code/Master
# python -u create_splits_seq.py --test_frac 0.2 --prefix splits712 --k 1 --task HPA10M_staining_intensity --seed 42

# backbones="chief conch conch_v1_5 ctranspath gigapath GPFM phikon uni h_optimus_0 virchow virchow2 chief_wsi titan_wsi gigapath_wsi madeleine_wsi"
# backbones="chief_wsi gigapath_wsi titan_wsi madeleine_wsi"
backbones="uni"

declare -A in_dim
# patch
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
# wsi
in_dim["chief_wsi"]=768
in_dim["titan_wsi"]=768
in_dim["gigapath_wsi"]=768
in_dim["madeleine_wsi"]=512
# in_dim["chief_wsi"]=768
# in_dim["chief_wsi"]=3072

declare -A gpus
# gpus["ab_mil"]=0
# gpus["clam_sb"]=0
# gpus["trans_mil"]=0
echo "Slurm assigned GPU(s): $CUDA_VISIBLE_DEVICES"
gpus["att_mil"]=$CUDA_VISIBLE_DEVICES
gpus["wsi_mil"]=$CUDA_VISIBLE_DEVICES
# gpus["att_mil"]=3
# gpus["wsi_mil"]=3

n_classes=4 # the class number of dataset
task="HPA10M_staining_intensity" # the name of the dataset, it is defined at `datasets/__init__.py`.
root_log="train_scripts_lanfz/logs/train_log_"$task"_" # log file path
results_dir="/mnt/petrelfs/yanfang/project/IHC_Benchmarks/code/Master/lanfz_results/experiments/train/splits712/"$task # path to save results
split_dir="splits712/"$task"_100" # which splits to use
seed=1024       # random seed
preloading="no"   # load all data into memory and then train the model
patch_size="512"    # the patch size of instances

for backbone in $backbones
do
    if [[ $backbone == *"wsi"* ]]; then
        model="wsi_mil"  # 如果 backbone 包含 "wsi"，就用 wsi_mil
    else
        model="att_mil"  # 否则用 att_mil
    fi
        exp=$model"/"$backbone
        echo $exp", GPU is:"${gpus[$model]}
        export CUDA_VISIBLE_DEVICES=${gpus[$model]}
        # k_start and k_end, only for resuming, default is -1
        k_start=0
        k_end=-1
        nohup python main.py \
            --seed $seed \
            --split_dir $split_dir \
            --drop_out \
            --task_type subtyping \
            --early_stopping \
            --lr 2e-4 \
            --reg 1e-4 \
            --k 1 \
            --k_start $k_start \
            --k_end $k_end \
            --label_frac 1.0 \
            --max_epochs 1 \
            --exp_code $exp \
            --patch_size $patch_size \
            --weighted_sample \
            --task $task \
            --backbone $backbone \
            --results_dir $results_dir \
            --model_type $model \
            --log_data \
            --preloading $preloading \
            --n_classes $n_classes \
            --in_dim ${in_dim[$backbone]} > "$root_log""$model"_"$backbone.log" 2>&1 &
done
wait




# srun -p Medisco --gres=gpu:1 -w SH-IDC1-10-140-37-13 bash train_scripts_lanfz/subtype_lymphoma_RJ.sh 
