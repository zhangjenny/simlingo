#!/usr/bin/env python3
"""
Simple test script to verify data loading without Hydra dependencies
"""

import sys
import os
sys.path.append('/root/simlingo/simlingo_training')

def test_data_structure():
    """Test the data structure without loading the full dataset"""
    
    # Check if the data directories exist
    data_path = '/root/simlingo/database/simlingo'
    
    if not os.path.exists(data_path):
        print(f"❌ Data path does not exist: {data_path}")
        return False
    
    # List all route directories
    route_dirs = [d for d in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, d)) and 'Town' in d]
    
    print(f"Found {len(route_dirs)} route directories:")
    for route_dir in route_dirs:
        print(f"  - {route_dir}")
    
    if len(route_dirs) == 0:
        print("❌ No route directories found")
        return False
    
    # Check a sample route directory structure
    sample_route = os.path.join(data_path, route_dirs[0])
    print(f"\nChecking sample route: {sample_route}")
    
    # Check for required subdirectories
    subdirs = ['anno', 'camera']
    for subdir in subdirs:
        subdir_path = os.path.join(sample_route, subdir)
        if os.path.exists(subdir_path):
            files = os.listdir(subdir_path)
            print(f"  ✅ {subdir}: {len(files)} files/subdirectories")
            if len(files) > 0:
                print(f"     Sample: {files[:3]}...")
        else:
            print(f"  ❌ {subdir}: missing")
            return False
    
    # Check for JSON files in anno directory
    anno_path = os.path.join(sample_route, 'anno')
    json_files = [f for f in os.listdir(anno_path) if f.endswith('.json.gz')]
    
    if len(json_files) == 0:
        print("❌ No JSON files found in anno directory")
        return False
    
    print(f"  ✅ Found {len(json_files)} JSON files in anno directory")
    
    # Check for image files in camera directory (recursively)
    camera_path = os.path.join(sample_route, 'camera')
    image_files = []
    
    # Recursively search for .jpg files in camera subdirectories
    for root, dirs, files in os.walk(camera_path):
        for file in files:
            if file.endswith('.jpg'):
                image_files.append(os.path.join(root, file))
    
    if len(image_files) == 0:
        print("❌ No image files found in camera directory (including subdirectories)")
        return False
    
    print(f"  ✅ Found {len(image_files)} image files in camera directory")
    
    # Show the structure of camera subdirectories
    camera_subdirs = [d for d in os.listdir(camera_path) if os.path.isdir(os.path.join(camera_path, d))]
    print(f"  Camera subdirectories: {camera_subdirs}")
    
    # Check a sample camera subdirectory
    if camera_subdirs:
        sample_camera_subdir = os.path.join(camera_path, camera_subdirs[0])
        sample_images = [f for f in os.listdir(sample_camera_subdir) if f.endswith('.jpg')][:3]
        print(f"  Sample images from {camera_subdirs[0]}: {sample_images}")
    
    return True

def test_buckets_config():
    """Test the buckets configuration"""
    
    buckets_path = '/root/simlingo/database/simlingo/buckets_paths.pkl'
    
    if not os.path.exists(buckets_path):
        print(f"❌ Buckets configuration not found: {buckets_path}")
        return False
    
    try:
        import pickle
        with open(buckets_path, 'rb') as f:
            buckets_config = pickle.load(f)
        
        print("✅ Buckets configuration loaded successfully")
        print(f"   Available buckets: {list(buckets_config.keys())}")
        
        if 'all' in buckets_config:
            print(f"   Routes in 'all' bucket: {len(buckets_config['all'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading buckets configuration: {e}")
        return False

if __name__ == "__main__":
    print("Testing data structure...")
    data_ok = test_data_structure()
    
    print("\nTesting buckets configuration...")
    buckets_ok = test_buckets_config()
    
    if data_ok and buckets_ok:
        print("\n✅ All tests passed! Data structure looks good.")
        print("\nThe data loading module should now work correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)