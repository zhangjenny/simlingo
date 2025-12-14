#!/usr/bin/env python3
"""
测试脚本：验证图像文件路径构建逻辑
"""

import os
import sys

def test_image_path_construction():
    """测试图像文件路径构建逻辑"""
    
    print("=== 测试图像文件路径构建 ===")
    
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
    
    # 查找包含图像文件的子目录
    image_subdir = None
    for subdir in subdirs:
        subdir_path = os.path.join(camera_path, subdir)
        image_files = [f for f in os.listdir(subdir_path) 
                       if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        if image_files:
            image_subdir = subdir
            print(f"找到包含图像的目录: {image_subdir}")
            print(f"图像文件数量: {len(image_files)}")
            
            # 测试路径构建逻辑
            seq = 0
            idx = 0
            image_filename = f'{(seq + idx):05}'  # 改为5位数字
            
            # 尝试不同的文件扩展名
            for ext in ['.png', '.jpg', '.jpeg']:
                image_path = os.path.join(camera_path, image_subdir, image_filename + ext)
                if os.path.exists(image_path):
                    print(f"✓ 成功构建图像路径: {image_path}")
                    
                    # 测试多个序列
                    test_sequences = [0, 10, 100, 200]
                    for test_seq in test_sequences:
                        test_filename = f'{test_seq:05}'  # 改为5位数字
                        test_path = os.path.join(camera_path, image_subdir, test_filename + ext)
                        if os.path.exists(test_path):
                            print(f"  ✓ 序列 {test_seq}: {test_path}")
                        else:
                            print(f"  ✗ 序列 {test_seq}: 文件不存在")
                    
                    return True
            
            print("✗ 未找到匹配的图像文件")
            return False
    
    print("✗ 未找到包含图像文件的子目录")
    return False

def test_modified_algorithm():
    """测试修改后的图像文件查找算法"""
    
    print("\n=== 测试修改后的图像文件查找算法 ===")
    
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
    
    # 模拟修改后的算法
    rgb_folder = 'camera'
    
    # 检查camera目录是否存在
    if not os.path.exists(route_path + f'/{rgb_folder}'):
        print("✗ camera目录不存在")
        return False
    
    # 检查图像文件在子目录中
    image_files_found = False
    camera_subdirs = [d for d in os.listdir(route_path + f'/{rgb_folder}') 
                    if os.path.isdir(os.path.join(route_path, rgb_folder, d))]
    
    # 尝试在子目录中查找图像文件
    image_subdir = None
    for subdir in camera_subdirs:
        subdir_path = os.path.join(route_path, rgb_folder, subdir)
        # 检查此子目录是否包含图像文件
        image_files = [f for f in os.listdir(subdir_path) if f.endswith(('.jpg', '.png', '.jpeg'))]
        if image_files:
            image_subdir = subdir
            image_files_found = True
            print(f"✓ 找到图像子目录: {image_subdir}")
            print(f"  图像文件数量: {len(image_files)}")
            
            # 显示样本文件
            sample_files = sorted(image_files)[:5]
            print(f"  样本文件: {sample_files}")
            break
    
    if not image_files_found:
        print("✗ 未找到图像文件")
        return False
    
    # 使用找到图像的子目录
    image_dir_path = os.path.join(route_path, rgb_folder, image_subdir)
    image_files = sorted([f for f in os.listdir(image_dir_path) if f.endswith(('.jpg', '.png', '.jpeg'))])
    num_seq = len(image_files)
    
    print(f"序列数量: {num_seq}")
    
    # 测试路径构建
    hist_len = 1
    pred_len = 4
    skip_first_n_frames = 0
    
    valid_samples = 0
    for seq in range(skip_first_n_frames, num_seq - pred_len - hist_len - 1):
        skip = False
        
        # 构建当前和历史帧的路径
        for idx in range(hist_len):
            image_filename = f'{(seq + idx):05}'  # 改为5位数字
            image_path = os.path.join(route_path, rgb_folder, image_subdir, image_filename)
            
            # 尝试不同的文件扩展名
            image_file = None
            for ext in ['.png', '.jpg', '.jpeg']:
                if os.path.exists(image_path + ext):
                    image_file = image_path + ext
                    break
            
            if image_file is None:
                skip = True
                break
        
        if not skip:
            valid_samples += 1
    
    print(f"有效样本数量: {valid_samples}")
    
    if valid_samples > 0:
        print("✓ 算法能够找到有效样本")
        return True
    else:
        print("✗ 算法未能找到有效样本")
        return False

if __name__ == "__main__":
    print("开始测试图像文件路径构建...")
    
    # 测试基本路径构建
    path_ok = test_image_path_construction()
    
    # 测试修改后的算法
    algorithm_ok = test_modified_algorithm()
    
    print("\n=== 测试结果 ===")
    if path_ok and algorithm_ok:
        print("✓ 所有测试通过")
        sys.exit(0)
    else:
        print("✗ 测试失败")
        sys.exit(1)