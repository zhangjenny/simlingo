# SimLingo Reproduction Guide - Detailed Steps and Commands

This guide provides comprehensive steps and commands to reproduce the SimLingo project training and evaluation.

## Table of Contents
1. [Environment Setup](#environment-setup)
2. [CARLA Installation](#carla-installation)
3. [Repository Clone](#repository-clone)
4. [Conda Environment Setup](#conda-environment-setup)
5. [Environment Variables](#environment-variables)
6. [Dataset Download](#dataset-download)
7. [Model Training](#model-training)
8. [Model Evaluation](#model-evaluation)
9. [Troubleshooting](#troubleshooting)

---

## Environment Setup

### System Requirements
- **OS**: Linux (Ubuntu 18.04+ recommended)
- **GPU**: NVIDIA GPU (RTX 2080Ti or better recommended)
- **CUDA**: Compatible with PyTorch 2.2.0
- **Python**: 3.8
- **Disk Space**: 
  - Mini dataset: ~4GB
  - Base dataset: ~400GB
  - Full dataset: ~4TB
- **RAM**: At least 32GB

---

## CARLA Installation

### Step 1: Create CARLA directory and download

```bash
# Create CARLA installation directory
mkdir -p ~/software/carla0915
cd ~/software/carla0915

# Download CARLA 0.9.15
wget https://carla-releases.s3.us-east-005.backblazeb2.com/Linux/CARLA_0.9.15.tar.gz

# Extract
tar -xvf CARLA_0.9.15.tar.gz

# Remove archive to save space
rm CARLA_0.9.15.tar.gz
```

### Step 2: Download additional maps

```bash
# Navigate to Import directory
cd Import

# Download additional maps
wget https://carla-releases.s3.us-east-005.backblazeb2.com/Linux/AdditionalMaps_0.9.15.tar.gz

# Return to parent directory and import assets
cd ..
bash ImportAssets.sh
```

### Step 3: Test CARLA installation

```bash
# Start CARLA server (background)
cd ~/software/carla0915
./CarlaUE4.sh -quality-level=Low -RenderOffScreen

# In another terminal, test connection
cd ~/software/carla0915/PythonAPI/examples
python3 spawn_npc.py
```

If vehicles spawn successfully, CARLA is installed correctly. Press `Ctrl+C` to stop the server.

---

## Repository Clone

```bash
# Clone repository
git clone https://github.com/zhangjenny/simlingo.git
cd simlingo

# Or use original repository
# git clone https://github.com/RenzKa/simlingo.git
# cd simlingo
```

---

## Conda Environment Setup

### Step 1: Create base environment

```bash
# Create environment using provided environment.yaml
conda env create -f environment.yaml

# Activate environment
conda activate simlingo
```

### Step 2: Install PyTorch

```bash
# Install PyTorch 2.2.0 (ensure correct CUDA version)
pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0
```

### Step 3: Install Flash Attention

```bash
# Install flash-attn (this may take some time)
pip install flash-attn==2.7.0.post2 --no-build-isolation
```

### Step 4: Verify installation

```bash
# Test PyTorch
python -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"

# Test CARLA Python API
python -c "import carla; print(f'CARLA version: {carla.__version__}')"
```

---

## Environment Variables

### Create environment configuration file

Environment variables need to be set before each use. Create a configuration script:

```bash
# Create configuration script
cat > ~/simlingo_env.sh << 'EOF'
#!/bin/bash

# Set CARLA path
export CARLA_ROOT=~/software/carla0915

# Set work directory
export WORK_DIR=~/simlingo

# Set Python path
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla/dist/carla-0.9.15-py3.8-linux-x86_64.egg
export PYTHONPATH=$PYTHONPATH:${WORK_DIR}

# Set scenario runner paths
export SCENARIO_RUNNER_ROOT=${WORK_DIR}/scenario_runner
export LEADERBOARD_ROOT=${WORK_DIR}/leaderboard
export PYTHONPATH="${CARLA_ROOT}/PythonAPI/carla/":"${SCENARIO_RUNNER_ROOT}":"${LEADERBOARD_ROOT}":${PYTHONPATH}

# Optional: Set HuggingFace mirror for users in China
# export HF_ENDPOINT=https://hf-mirror.com

echo "SimLingo environment variables configured"
EOF

# Make script executable
chmod +x ~/simlingo_env.sh
```

### Use configuration script

```bash
# Run before each use
source ~/simlingo_env.sh
```

---

## Dataset Download

### Option 1: Download Mini dataset (recommended for testing)

```bash
# Create dataset directory
mkdir -p database/simlingo

# Use provided script to download Mini dataset
cd simlingo
bash download_mini.sh
```

### Option 2: Download full dataset from HuggingFace

```bash
# Install Git LFS (if not already installed)
git lfs install

# Clone dataset repository
git clone https://huggingface.co/datasets/RenzKa/simlingo

# Navigate to directory
cd simlingo

# Pull LFS files
git lfs pull
```

### Option 3: Download individual files

```bash
# Download specific file (replace [filename] with actual filename)
wget https://huggingface.co/datasets/RenzKa/simlingo/resolve/main/[filename].tar.gz
```

### Extract dataset

```bash
# Create output directory
mkdir -p database/simlingo

# Extract all .tar.gz files to same directory
for file in *.tar.gz; do
    echo "Extracting $file to database/simlingo/..."
    tar -xzf "$file" -C database/simlingo/
done

echo "Dataset extraction complete"
```

### Verify dataset

```bash
# Check dataset structure
ls -lh database/simlingo/

# Run test script to verify dataset
python test_dataset_loading.py
```

---

## Model Training

### Preparation

1. **Login to Weights & Biases (optional, for training logs)**

```bash
# wandb is already included in environment.yaml
# Login
wandb login
```

2. **Check configuration files**

```bash
# View training configuration
cat simlingo_training/config/experiment/simlingo_seed1.yaml

# Ensure data paths are correct
# Edit data paths in config file
nano simlingo_training/config/experiment/simlingo_seed1.yaml
```

### Train SimLingo-Base model

```bash
# Activate environment and set environment variables
conda activate simlingo
source ~/simlingo_env.sh

# Navigate to training directory
cd simlingo_base_training

# Start training (single GPU)
python train.py

# Multi-GPU training
python train.py gpus=4
```

### Train full SimLingo model

```bash
# Ensure you're in project root
cd ~/simlingo

# Multi-GPU training (e.g., 8 GPUs)
python simlingo_training/train.py \
    experiment=simlingo_seed1 \
    data_module.batch_size=8 \
    gpus=8 \
    name=simlingo_seed1 \
    data_module.base_dataset.data_path=/path/to/database/simlingo
```

### SLURM cluster training (if using cluster)

```bash
# Edit SLURM script
nano train_simlingo_seed1.sh

# Modify the following:
# - Line 7: Set correct output path
# - Line 8: Set correct error log path
# - Line 9: Set correct partition name
# - Line 18: Set correct conda environment path
# - Line 34: Set correct data path

# Submit job
sbatch train_simlingo_seed1.sh
```

### Monitor training

```bash
# View wandb logs (in browser)
# Visit https://wandb.ai to see training progress

# Or view local logs
tail -f results/logs/simlingo_*.out
```

---

## Model Evaluation

### Download pretrained model

```bash
# Download model from HuggingFace
mkdir -p checkpoints
cd checkpoints

# Use git clone
git clone https://huggingface.co/RenzKa/simlingo

# Or use wget to download specific checkpoint
wget https://huggingface.co/RenzKa/simlingo/resolve/main/[checkpoint_name]
```

### Bench2Drive closed-loop driving evaluation

#### Step 1: Prepare evaluation environment

```bash
# Ensure environment variables are set
source ~/simlingo_env.sh

# Check Bench2Drive dataset
ls -l Bench2Drive/
```

#### Step 2: Configure evaluation script

```bash
# Edit evaluation launch script
nano start_eval_simlingo.py

# Configurations to modify (look for TODO markers):
# - carla_root: CARLA installation path
# - repo_root: SimLingo repository path
# - checkpoint: Model checkpoint path
# - agent_file: Agent file path
# - partition_name: SLURM partition name (if using SLURM)
```

#### Step 3: Run evaluation (local single GPU)

```bash
# Set environment variables
export CARLA_ROOT=~/software/carla0915
export WORK_DIR=~/simlingo
export PYTHONPATH=$PYTHONPATH:${WORK_DIR}/Bench2Drive/leaderboard
export PYTHONPATH=$PYTHONPATH:${WORK_DIR}/Bench2Drive/scenario_runner

# Run single route test
cd Bench2Drive

bash leaderboard/scripts/run_evaluation_debug.sh
```

#### Step 4: SLURM cluster parallel evaluation

```bash
# Run evaluation script
python start_eval_simlingo.py

# Script will automatically submit multiple SLURM jobs to evaluate 220 routes in parallel
```

#### Step 5: Merge results and calculate metrics

```bash
# Wait for all evaluations to complete (ensure 220 route results)

# Merge JSON results
python Bench2Drive/tools/merge_route_json.py -f /path/to/results/

# Calculate multi-ability metrics
python Bench2Drive/tools/ability_benchmark.py -r merge.json

# Calculate driving efficiency and smoothness
python Bench2Drive/tools/efficiency_smoothness_benchmark.py -f merge.json -m /path/to/metrics/
```

### Language capability evaluation

#### Step 1: Configure OpenAI API

```bash
# Edit GPT evaluation configuration
nano simlingo_training/utils/gpt_eval.py

# Add your OpenAI API key
# OPENAI_API_KEY = "your-api-key-here"
```

#### Step 2: VQA evaluation

```bash
# Edit evaluation script
nano simlingo_training/eval.py

# Set eval_mode = "QA"

# Run VQA evaluation
cd simlingo_training
python eval.py

# Calculate metrics
python eval_metrics.py
```

#### Step 3: Commentary evaluation

```bash
# Set eval_mode = "commentary"
nano simlingo_training/eval.py

# Run commentary evaluation
python eval.py

# Calculate metrics
python eval_metrics.py
```

#### Step 4: Dreaming evaluation

```bash
# Set eval_mode = "Dreaming"
nano simlingo_training/eval.py

# Run Dreaming evaluation
python eval.py

# Calculate metrics
python eval_metrics.py
```

---

## Troubleshooting

### 1. CARLA won't start

**Issue**: CARLA exits immediately after starting

**Solution**:
```bash
# Check Vulkan
/usr/bin/vulkaninfo | head -n 5

# Reinstall Vulkan tools
sudo apt install vulkan-tools vulkan-utils

# Try downgrading NVIDIA driver to version 470
# Or use offscreen rendering
./CarlaUE4.sh -RenderOffScreen -quality-level=Low
```

### 2. Port conflict

**Issue**: CARLA port is occupied

**Solution**:
```bash
# Check port usage
lsof -i:2000
lsof -i:2001

# Kill occupying process
kill -9 <PID>

# Or use cleanup script
bash Bench2Drive/tools/clean_carla.sh
```

### 3. CUDA out of memory

**Issue**: GPU memory overflow during training

**Solution**:
```bash
# Reduce batch size
python simlingo_training/train.py data_module.batch_size=4

# Use gradient accumulation
python simlingo_training/train.py data_module.batch_size=4 accumulate_grad_batches=2

# Use mixed precision training
python simlingo_training/train.py precision=16
```

### 4. HuggingFace download slow or failing

**Issue**: Cannot access HuggingFace or slow download speed

**Solution**:
```bash
# Use mirror site (for China users)
export HF_ENDPOINT=https://hf-mirror.com

# Use huggingface-cli with resume capability
huggingface-cli download --repo-type dataset --resume-download RenzKa/simlingo --local-dir ./database/simlingo
```

### 5. Dependency issues

**Issue**: Some packages cannot be installed

**Solution**:
```bash
# Install problematic packages separately
pip install <package_name> --no-cache-dir

# Flash-attention compilation fails
# Ensure sufficient RAM (at least 16GB)
pip install flash-attn==2.7.0.post2 --no-build-isolation

# If still failing, can skip (will reduce training speed but won't affect functionality)
# Comment out flash-attn in environment.yaml
```

### 6. Dataset path issues

**Issue**: Cannot find dataset during training

**Solution**:
```bash
# Check dataset structure
ls -l database/simlingo/

# Ensure path is correct
# Edit data_path in config file
nano simlingo_training/config/config.py

# Or specify on command line
python simlingo_training/train.py data_module.base_dataset.data_path=/absolute/path/to/database/simlingo
```

### 7. Evaluation crashes

**Issue**: CARLA crashes during Bench2Drive evaluation

**Solution**:
```bash
# Increase sleep time
# Edit Bench2Drive/leaderboard/leaderboard/leaderboard_evaluator.py
# Increase sleep time on line 207

# Use auto-restart script
# Create infinite loop to restart evaluation until complete
while true; do
    python start_eval_simlingo.py
    if [ $? -eq 0 ]; then
        break
    fi
    sleep 10
done
```

### 8. Clean CARLA processes

**Issue**: Residual CARLA processes

**Solution**:
```bash
# Use provided cleanup script
bash Bench2Drive/tools/clean_carla.sh

# Manual cleanup
ps aux | grep Carla | awk '{print $2}' | xargs kill -9
ps aux | grep carla | awk '{print $2}' | xargs kill -9

# Clean zombie processes
ps aux | grep defunct
```

---

## Quick Start Checklist

- [ ] Install CARLA 0.9.15
- [ ] Clone SimLingo repository
- [ ] Create conda environment
- [ ] Install PyTorch 2.2.0
- [ ] Install flash-attn
- [ ] Set environment variables
- [ ] Download dataset (at least Mini version)
- [ ] Test dataset loading
- [ ] Run one training test
- [ ] Download pretrained model
- [ ] Run one evaluation test

---

## Useful Command Reference

### Check system status

```bash
# Check GPU
nvidia-smi

# Check CUDA version
nvcc --version

# Check disk space
df -h

# Check memory
free -h
```

### Monitor training

```bash
# Monitor GPU usage
watch -n 1 nvidia-smi

# Monitor logs
tail -f results/logs/*.out

# Monitor training process
ps aux | grep python
```

### Dataset management

```bash
# Calculate dataset size
du -sh database/simlingo/

# Find .json.gz files
find database/simlingo/ -name "*.json.gz" | wc -l

# Verify data integrity
python dataset_generation/count_json_gz_files.py
```

---

## Additional Resources

- **Paper**: https://arxiv.org/abs/2503.09594
- **Project Page**: https://www.katrinrenz.de/simlingo/
- **Dataset**: https://huggingface.co/datasets/RenzKa/simlingo
- **Model**: https://huggingface.co/RenzKa/simlingo
- **Video Demo**: https://www.youtube.com/watch?v=Mpbnz2AKaNA
- **GitHub Issues**: https://github.com/RenzKa/simlingo/issues

---

## Citation

If you use this project, please cite:

```bibtex
@InProceedings{Renz2025cvpr,
  title={SimLingo: Vision-Only Closed-Loop Autonomous Driving with Language-Action Alignment},
  author={Renz, Katrin and Chen, Long and Arani, Elahe and Sinavski, Oleg},
  booktitle={Conference on Computer Vision and Pattern Recognition (CVPR)},
  year={2025}
}
```

---

**Last Updated**: 2025-12-28

**Maintainers**: SimLingo Team

For issues, please post on GitHub Issues or refer to the original README.md file.
