# SimLingo - Quick Reference / 快速参考

**[English](#english) | [中文](#中文)**

---

## English

### 📚 Documentation Files

This repository contains comprehensive reproduction guides:

1. **REPRODUCTION_GUIDE.md** - Complete English guide with detailed steps
2. **复现步骤指南.md** - Complete Chinese guide (完整的中文指南)
3. **README.md** - Original project documentation
4. **quick_start.sh** - Automated setup script

### 🚀 Quick Start (3 Steps)

```bash
# Step 1: Clone repository
git clone https://github.com/zhangjenny/simlingo.git
cd simlingo

# Step 2: Run automated setup
bash quick_start.sh

# Step 3: Follow the on-screen instructions
```

### 📖 Manual Setup Summary

```bash
# 1. Install CARLA 0.9.15
mkdir -p ~/software/carla0915
cd ~/software/carla0915
wget https://carla-releases.s3.us-east-005.backblazeb2.com/Linux/CARLA_0.9.15.tar.gz
tar -xzf CARLA_0.9.15.tar.gz
rm CARLA_0.9.15.tar.gz
cd Import && wget https://carla-releases.s3.us-east-005.backblazeb2.com/Linux/AdditionalMaps_0.9.15.tar.gz
cd .. && bash ImportAssets.sh

# 2. Setup conda environment
cd ~/simlingo
conda env create -f environment.yaml
conda activate simlingo
pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0
pip install flash-attn==2.7.0.post2 --no-build-isolation

# 3. Set environment variables (create ~/simlingo_env.sh)
export CARLA_ROOT=~/software/carla0915
export WORK_DIR=~/simlingo
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla/dist/carla-0.9.15-py3.8-linux-x86_64.egg
export PYTHONPATH=$PYTHONPATH:${WORK_DIR}
export SCENARIO_RUNNER_ROOT=${WORK_DIR}/scenario_runner
export LEADERBOARD_ROOT=${WORK_DIR}/leaderboard
export PYTHONPATH="${CARLA_ROOT}/PythonAPI/carla/":"${SCENARIO_RUNNER_ROOT}":"${LEADERBOARD_ROOT}":${PYTHONPATH}

# 4. Download dataset (Mini for testing)
bash download_mini.sh

# 5. Download model
mkdir -p checkpoints && cd checkpoints
git clone https://huggingface.co/RenzKa/simlingo
```

### 🎯 Common Commands

**Before each use:**
```bash
conda activate simlingo
source ~/simlingo_env.sh
```

**Training:**
```bash
# Train SimLingo model
python simlingo_training/train.py \
    experiment=simlingo_seed1 \
    data_module.batch_size=8 \
    gpus=8 \
    name=simlingo_seed1
```

**Evaluation:**
```bash
# Bench2Drive evaluation
python start_eval_simlingo.py

# Language evaluation (VQA/Commentary/Dreaming)
cd simlingo_training
python eval.py  # Edit eval_mode first
python eval_metrics.py
```

### 🔧 Troubleshooting

- **CARLA won't start**: Use `./CarlaUE4.sh -RenderOffScreen -quality-level=Low`
- **Port conflict**: Run `bash Bench2Drive/tools/clean_carla.sh`
- **Out of memory**: Reduce batch size or use gradient accumulation
- **HuggingFace slow**: Use `export HF_ENDPOINT=https://hf-mirror.com` (China users)

### 📝 Resources

- Paper: https://arxiv.org/abs/2503.09594
- Website: https://www.katrinrenz.de/simlingo/
- Dataset: https://huggingface.co/datasets/RenzKa/simlingo
- Model: https://huggingface.co/RenzKa/simlingo

---

## 中文

### 📚 文档文件

本仓库包含完整的复现指南：

1. **复现步骤指南.md** - 完整的中文指南（详细步骤）
2. **REPRODUCTION_GUIDE.md** - Complete English guide
3. **README.md** - 原始项目文档
4. **quick_start.sh** - 自动化安装脚本

### 🚀 快速开始（3步）

```bash
# 步骤 1: 克隆仓库
git clone https://github.com/zhangjenny/simlingo.git
cd simlingo

# 步骤 2: 运行自动化安装脚本
bash quick_start.sh

# 步骤 3: 按照屏幕提示操作
```

### 📖 手动安装摘要

```bash
# 1. 安装 CARLA 0.9.15
mkdir -p ~/software/carla0915
cd ~/software/carla0915
wget https://carla-releases.s3.us-east-005.backblazeb2.com/Linux/CARLA_0.9.15.tar.gz
tar -xzf CARLA_0.9.15.tar.gz
rm CARLA_0.9.15.tar.gz
cd Import && wget https://carla-releases.s3.us-east-005.backblazeb2.com/Linux/AdditionalMaps_0.9.15.tar.gz
cd .. && bash ImportAssets.sh

# 2. 配置 conda 环境
cd ~/simlingo
conda env create -f environment.yaml
conda activate simlingo
pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0
pip install flash-attn==2.7.0.post2 --no-build-isolation

# 3. 设置环境变量 (创建 ~/simlingo_env.sh)
export CARLA_ROOT=~/software/carla0915
export WORK_DIR=~/simlingo
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla/dist/carla-0.9.15-py3.8-linux-x86_64.egg
export PYTHONPATH=$PYTHONPATH:${WORK_DIR}
export SCENARIO_RUNNER_ROOT=${WORK_DIR}/scenario_runner
export LEADERBOARD_ROOT=${WORK_DIR}/leaderboard
export PYTHONPATH="${CARLA_ROOT}/PythonAPI/carla/":"${SCENARIO_RUNNER_ROOT}":"${LEADERBOARD_ROOT}":${PYTHONPATH}

# 设置 HuggingFace 镜像（国内用户）
export HF_ENDPOINT=https://hf-mirror.com

# 4. 下载数据集（Mini版本用于测试）
bash download_mini.sh

# 5. 下载模型
mkdir -p checkpoints && cd checkpoints
git clone https://huggingface.co/RenzKa/simlingo
```

### 🎯 常用命令

**每次使用前：**
```bash
conda activate simlingo
source ~/simlingo_env.sh
```

**训练：**
```bash
# 训练 SimLingo 模型
python simlingo_training/train.py \
    experiment=simlingo_seed1 \
    data_module.batch_size=8 \
    gpus=8 \
    name=simlingo_seed1
```

**评估：**
```bash
# Bench2Drive 评估
python start_eval_simlingo.py

# 语言能力评估 (VQA/Commentary/Dreaming)
cd simlingo_training
python eval.py  # 先编辑 eval_mode
python eval_metrics.py
```

### 🔧 问题解决

- **CARLA 无法启动**: 使用 `./CarlaUE4.sh -RenderOffScreen -quality-level=Low`
- **端口冲突**: 运行 `bash Bench2Drive/tools/clean_carla.sh`
- **内存不足**: 减小 batch size 或使用梯度累积
- **HuggingFace 下载慢**: 使用 `export HF_ENDPOINT=https://hf-mirror.com`

### 📝 资源

- 论文: https://arxiv.org/abs/2503.09594
- 项目主页: https://www.katrinrenz.de/simlingo/
- 数据集: https://huggingface.co/datasets/RenzKa/simlingo
- 模型: https://huggingface.co/RenzKa/simlingo

---

## 📋 Checklist / 检查清单

- [ ] CARLA 0.9.15 installed / 安装 CARLA
- [ ] Repository cloned / 克隆仓库
- [ ] Conda environment created / 创建环境
- [ ] PyTorch installed / 安装 PyTorch
- [ ] Environment variables set / 设置环境变量
- [ ] Dataset downloaded / 下载数据集
- [ ] Model downloaded / 下载模型
- [ ] Test run successful / 测试运行成功

---

## 🆘 Getting Help / 获取帮助

- Read detailed guides / 阅读详细指南:
  - **REPRODUCTION_GUIDE.md** (English)
  - **复现步骤指南.md** (中文)
- Check GitHub Issues: https://github.com/RenzKa/simlingo/issues
- See original README.md for more information

---

**Last Updated / 最后更新**: 2025-12-28
