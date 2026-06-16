#!/bin/bash
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --gres=gpu:1
#SBATCH --constraint=a40|a100|l40
# Load ENV variables
#SBATCH --qos=research-deadline

#SBATCH --output=prompt_extraction.out
#SBATCH --error=prompt_extraction.err

export HTTP_PROXY=http://proxy.utwente.nl:3128
export HTTPS_PROXY=http://proxy.utwente.nl:3128
export TORCH_USE_CUDA_DSA
# Load ENV
source /etc/profile.d/modules.sh
module load nvidia/cuda-11.8

cd /home/simonettos/prompt_stealing/prompt_stealing_def/prompt_obfuscation/prompt_obfuscation/
conda activate prompt_obfuscation

# python3 prompt_extraction.py --results_dir "results/soft_pirate_obfuscation" --extraction_prompts_file "extraction_prompts/gpt4_generated.json" --tensor_file "results/soft_pirate_obfuscation/best_candidate.pt" --output_filename "extraction_output_obfuscated.json"
# python3 evaluate_prompt_extraction.py --results_dir "results/soft_pirate_obfuscation"  --extraction_output_file "results/soft_pirate_obfuscation/extraction_output_obfuscated.json" --successful_outputs_filename "successful_extractions_obfuscated.json"
python3 prompt_extraction.py --results_dir "results/soft_pirate_obfuscation" --extraction_prompts_file "extraction_prompts/gpt4_generated.json" --conventional --output_filename "extraction_output_conventional.json"
python3 evaluate_prompt_extraction.py --results_dir "results/soft_pirate_obfuscation"  --extraction_output_file "results/soft_pirate_obfuscation/extraction_output_conventional.json" --successful_outputs_filename "successful_extractions_conventional.json"
