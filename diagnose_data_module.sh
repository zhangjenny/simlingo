#!/bin/bash
echo "=== 诊断数据模块问题 ==="

# 1. 搜索 DataModule 类
echo "搜索 DataModule 类定义:"
find . -name "*.py" -exec grep -l "class DataModule" {} \; 2>/dev/null

# 2. 搜索 datamodule.py 文件
echo -e "\n搜索 datamodule.py 文件:"
find . -name "datamodule.py" 2>/dev/null

# 3. 查看目录结构
echo -e "\n目录结构:"
ls -la simlingo_training/ 2>/dev/null | grep -E "(dataloader|total)" | head -5
ls -la simlingo_base_training/ 2>/dev/null | grep -E "(dataloader|total)" | head -5

# 4. 尝试导入
echo -e "\n尝试导入:"
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    import simlingo_training.dataloader.datamodule
    print('✓ simlingo_training.dataloader.datamodule')
except ImportError as e:
    print(f'✗ simlingo_training.dataloader.datamodule: {e}')
    
try:
    import simlingo_base_training.dataloader.datamodule  
    print('✓ simlingo_base_training.dataloader.datamodule')
except ImportError as e:
    print(f'✗ simlingo_base_training.dataloader.datamodule: {e}')
"
