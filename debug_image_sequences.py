import os
import glob

# 数据路径配置
data_path = "/root/simlingo/database/simlingo"
route_name = "ConstructionObstacle_Town05_Route68_Weather8"
route_dir = os.path.join(data_path, route_name)

print("=== 调试图像文件序列（修复后） ===")
print(f"样本路线: {route_name}")

# 检查camera目录结构
camera_dir = os.path.join(route_dir, "camera")
if os.path.exists(camera_dir):
    subdirs = [d for d in os.listdir(camera_dir) if os.path.isdir(os.path.join(camera_dir, d))]
    print(f"camera目录下子目录: {subdirs}")
    
    # 查找包含图像的子目录
    image_subdirs = []
    for subdir in subdirs:
        subdir_path = os.path.join(camera_dir, subdir)
        image_files = glob.glob(os.path.join(subdir_path, "*.jpg")) + glob.glob(os.path.join(subdir_path, "*.png"))
        if image_files:
            image_subdirs.append(subdir)
            print(f"  找到图像子目录: {subdir}")
            
            # 检查图像文件
            image_files = sorted([f for f in os.listdir(subdir_path) if f.endswith(('.jpg', '.png', '.jpeg'))])
            print(f"  图像文件总数: {len(image_files)}")
            
            if image_files:
                print(f"  文件命名模式:")
                for i in range(min(10, len(image_files))):
                    print(f"     {image_files[i]}")
                
                # 检查文件编号范围
                numbers = []
                for f in image_files:
                    try:
                        num = int(f.split('.')[0])
                        numbers.append(num)
                    except:
                        pass
                
                if numbers:
                    min_num = min(numbers)
                    max_num = max(numbers)
                    expected_count = max_num - min_num + 1
                    actual_count = len(numbers)
                    
                    print(f"  文件编号范围: {min_num} - {max_num}")
                    print(f"  文件编号连续性: {actual_count} 个文件, 期望 {expected_count} 个文件")
                    
                    # 测试文件路径构建
                    hist_len = 1
                    pred_len = 4
                    skip_first_n_frames = 0
                    num_seq = len(image_files)
                    
                    print(f"  序列范围: {skip_first_n_frames} - {num_seq - pred_len - hist_len - 1}")
                    print(f"  总序列数: {num_seq}")
                    print(f"  历史长度: {hist_len}")
                    print(f"  预测长度: {pred_len}")
                    
                    # 测试几个关键序列的文件路径构建
                    test_sequences = [0, 10, 100, 200]
                    valid_samples = 0
                    
                    print(f"\n  测试文件路径构建（使用5位数字格式）:")
                    for seq in test_sequences:
                        if seq < num_seq - pred_len - hist_len - 1:
                            # 构建5位数字格式的文件名
                            image_filename = f'{(seq):05}'
                            image_path = os.path.join(route_dir, "camera", subdir, image_filename)
                            
                            # 检查文件是否存在
                            exists = False
                            for ext in ['.jpg', '.png', '.jpeg']:
                                if os.path.exists(image_path + ext):
                                    exists = True
                                    break
                            
                            if exists:
                                print(f"  ✓ 序列 {seq}: 文件存在")
                                valid_samples += 1
                            else:
                                print(f"  ✗ 序列 {seq}: 文件不存在")
                                # 显示实际存在的文件
                                actual_files = glob.glob(os.path.join(subdir_path, f"{seq:05}.*"))
                                if actual_files:
                                    print(f"      实际文件: {actual_files[0]}")
                                else:
                                    # 检查相近的文件
                                    similar_files = glob.glob(os.path.join(subdir_path, f"*{seq:04}*"))
                                    if similar_files:
                                        print(f"      相似文件: {similar_files[0]}")
                    
                    print(f"\n  有效样本总数: {valid_samples}")
                    
                    if valid_samples > 0:
                        print("\n  ✓ 调试成功！文件路径构建正确")
                    else:
                        print("\n  ✗ 调试发现问题")
else:
    print("✗ camera目录不存在")