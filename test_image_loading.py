#!/usr/bin/env python3
"""
测试脚本：验证数据加载模块能否正确加载图像文件
"""

import os
import sys

# 添加项目路径
sys.path.insert(0, '/root/simlingo/simlingo_training')

from dataloader.dataset_base import BaseDataset

def test_image_loading():
    """测试图像文件加载功能"""
    
    # 配置参数
    config = {
        'data_path': '/root/simlingo/database/simlingo',
        'bucket_path': '/root/simlingo/database/simlingo',
        'bucket_name': 'all',
        'split': 'train',
        'hist_len': 1,
        'pred_len': 4,
        'skip_first_n_frames': 0,
        'rgb_folder': 'camera',
        'cut_bottom_quarter': False,
        'img_shift_augmentation': False,
        'img_augmentation': False,
        'img_augmentation_prob': 0.0,
        'num_route_points': 10,
        'use_old_towns': False,
        'dreamer': False,
        'dreamer_folder': 'dreamer',
        'evaluation': False
    }
    
    print("=== 测试图像文件加载 ===")
    print(f"数据路径: {config['data_path']}")
    print(f"RGB文件夹: {config['rgb_folder']}")
    
    try:
        # 创建数据集实例
        dataset = BaseDataset(**config)
        
        print(f"数据集长度: {len(dataset)}")
        
        if len(dataset) > 0:
            # 测试加载第一个样本
            sample = dataset[0]
            print("成功加载样本!")
            
            # 检查图像路径
            if hasattr(dataset, 'images') and len(dataset.images) > 0:
                image_path = str(dataset.images[0][0], encoding='utf-8')
                print(f"第一个图像路径: {image_path}")
                
                # 检查文件是否存在
                if os.path.exists(image_path):
                    print("✓ 图像文件存在")
                else:
                    print("✗ 图像文件不存在")
                    
            return True
        else:
            print("✗ 数据集为空")
            return False
            
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_camera_structure():
    """测试camera目录结构"""
    
    print("\n=== 测试camera目录结构 ===")
    
    data_path = '/root/simlingo/database/simlingo'
    
    # 查找路线目录
    route_dirs = [d for d in os.listdir(data_path) if 'Town' in d]
    
    if not route_dirs:
        print("✗ 未找到路线目录")
        return False
    
    sample_route = route_dirs[0]
    route_path = os.path.join(data_path, sample_route)
    camera_path = os.path.join(route_path, 'camera')
    
    print(f"样本路线: {sample_route}")
    print(f"camera路径: {camera_path}")
    
    if not os.path.exists(camera_path):
        print("✗ camera目录不存在")
        return False
    
    # 检查camera子目录
    subdirs = [d for d in os.listdir(camera_path) 
               if os.path.isdir(os.path.join(camera_path, d))]
    
    print(f"camera子目录: {subdirs}")
    
    if not subdirs:
        print("✗ camera目录下没有子目录")
        return False
    
    # 检查每个子目录中的图像文件
    for subdir in subdirs:
        subdir_path = os.path.join(camera_path, subdir)
        image_files = [f for f in os.listdir(subdir_path) 
                       if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        print(f"  {subdir}: {len(image_files)} 个图像文件")
        
        if image_files:
            # 显示前几个文件
            sample_files = image_files[:3]
            print(f"    样本文件: {sample_files}")
    
    return True

if __name__ == "__main__":
    print("开始测试数据加载模块...")
    
    # 测试camera目录结构
    structure_ok = test_camera_structure()
    
    # 测试图像加载
    if structure_ok:
        loading_ok = test_image_loading()
    else:
        loading_ok = False
    
    print("\n=== 测试结果 ===")
    if structure_ok and loading_ok:
        print("✓ 所有测试通过")
        sys.exit(0)
    else:
        print("✗ 测试失败")
        sys.exit(1)