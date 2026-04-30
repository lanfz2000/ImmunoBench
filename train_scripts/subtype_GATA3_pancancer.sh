#!/bin/bash  # 确保使用 Bash（而不是sh）

# process the csv file
python create_splits_seq.py --test_frac 0.2 --prefix splits712 --k 5 --task GATA3_pancancer

# backbones="chief conch conch_v1_5 ctranspath gigapath GPFM phikon uni h_optimus_0 virchow virchow2 chief_wsi titan_wsi gigapath_wsi madeleine_wsi"
backbones="titan_wsi"

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
gpus["att_mil"]=0
gpus["wsi_mil"]=0

n_classes=2 # the class number of dataset
task="GATA3_pancancer" # the name of the dataset, it is defined at `datasets/__init__.py`.
root_log="train_scripts_lanfz/logs/train_log_"$task"_" # log file path
results_dir="/cpfs04/user/yanfang/workspace/IHC_Benchmarks/code/Master/lanfz_results/experiments/train/splits712/"$task # path to save results
split_dir="splits712/GATA3_pancancer_100" # which splits to use
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
            --k 5 \
            --k_start $k_start \
            --k_end $k_end \
            --label_frac 1.0 \
            --max_epochs 100 \
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