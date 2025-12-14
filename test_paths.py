#!/usr/bin/env python3
"""
Simple test script to verify data paths without Hydra dependencies
"""

import sys
import os
import glob

def test_data_paths():
    """Test if the data paths are correctly configured"""
    
    # Test the data path from config
    data_path = '/root/simlingo/database/simlingo'
    
    print(f"Testing data path: {data_path}")
    
    if not os.path.exists(data_path):
        print(f"❌ Data path does not exist: {data_path}")
        return False
    
    # Test the glob pattern used in dataset_base.py
    route_dirs = glob.glob(data_path + '/*Town*')
    
    print(f"Found {len(route_dirs)} routes using pattern: {data_path}/*Town*")
    
    if len(route_dirs) == 0:
        print("❌ No route directories found!")
        
        # Let's see what's actually in the directory
        print(f"\nContents of {data_path}:")
        items = os.listdir(data_path)
        for item in items:
            item_path = os.path.join(data_path, item)
            print(f"  - {item} ({'dir' if os.path.isdir(item_path) else 'file'})")
        
        return False
    
    print("✅ Route directories found successfully")
    
    # Show the first few routes
    print("\nFirst 5 route directories:")
    for route_dir in route_dirs[:5]:
        print(f"  - {route_dir}")
    
    # Test if a sample route has the required structure
    sample_route = route_dirs[0]
    print(f"\nTesting sample route structure: {sample_route}")
    
    required_dirs = ['anno', 'camera']
    for req_dir in required_dirs:
        req_path = os.path.join(sample_route, req_dir)
        if os.path.exists(req_path):
            print(f"  ✅ {req_dir}: exists")
        else:
            print(f"  ❌ {req_dir}: missing")
            return False
    
    # Test if there are JSON files in anno
    anno_path = os.path.join(sample_route, 'anno')
    json_files = [f for f in os.listdir(anno_path) if f.endswith('.json.gz')]
    
    if len(json_files) == 0:
        print("❌ No JSON files found in anno directory")
        return False
    
    print(f"  ✅ Found {len(json_files)} JSON files in anno")
    
    # Test if there are image files in camera subdirectories
    camera_path = os.path.join(sample_route, 'camera')
    image_files = []
    
    for root, dirs, files in os.walk(camera_path):
        for file in files:
            if file.endswith('.jpg'):
                image_files.append(os.path.join(root, file))
    
    if len(image_files) == 0:
        print("❌ No image files found in camera directory")
        return False
    
    print(f"  ✅ Found {len(image_files)} image files in camera")
    
    return True

if __name__ == "__main__":
    print("Testing data paths...")
    success = test_data_paths()
    
    if success:
        print("\n✅ All path tests passed! Data paths are correctly configured.")
        sys.exit(0)
    else:
        print("\n❌ Path tests failed!")
        sys.exit(1)