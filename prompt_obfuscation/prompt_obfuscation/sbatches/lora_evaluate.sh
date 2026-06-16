#!/bin/bash
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --gres=gpu:1
#SBATCH --constraint=a40|a100|l40
# Load ENV variables
#SBATCH --qos=research-deadline

#SBATCH --output=lora_evaluate.out
#SBATCH --error=lora_evaluate.err

export HTTP_PROXY=http://proxy.utwente.nl:3128
export HTTPS_PROXY=http://proxy.utwente.nl:3128
export TORCH_USE_CUDA_DSA
# Load ENV
source /etc/profile.d/modules.sh
module load nvidia/cuda-11.8

cd /home/simonettos/prompt_stealing/prompt_obfuscation/prompt_obfuscation/
conda activate prompt_obfuscation

python3 evaluate_finetuning.py --results_dir "results/pirate_finetuning" --eval_batch_size 16