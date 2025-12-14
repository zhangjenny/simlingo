#!/usr/bin/env python3
"""
Test script to verify the BaseDataset class can load data correctly
"""

import sys
import os
sys.path.append('/root/simlingo/simlingo_training')

def test_dataset_loading():
    """Test the BaseDataset class with actual data loading"""
    
    # Import after path setup
    from dataloader.dataset_base import BaseDataset
    
    # Configuration matching config.yaml
    config = {
        'data_path': '/root/simlingo/database/simlingo',
        'bucket_path': '/root/simlingo/database/simlingo',
        'pred_len': 11,
        'cut_bottom_quarter': True,
        'use_commentary': False,
        'use_qa': False,
        'qa_augmentation': False,
        'img_shift_augmentation': False,
        'hist_len': 1,
        'route_as': 'target_point_command',
        'use_lmdrive_commands': True,
        'use_old_towns': True,
        'use_town13': True,
        'use_safety_flag': False,
        'img_augmentation_prob': 0.0,
        'skip_first_n_frames': 0,
        'split': 'train',
        'bucket_name': 'all'
    }
    
    try:
        print("Creating BaseDataset instance...")
        dataset = BaseDataset(**config)
        
        print(f"Dataset length: {len(dataset)}")
        
        if len(dataset) == 0:
            print("❌ Dataset is empty!")
            return False
        
        print("✅ Dataset created successfully")
        
        # Try to load a sample
        print("\nTesting sample loading...")
        try:
            sample = dataset[0]
            print("✅ Sample loaded successfully")
            print(f"Sample keys: {list(sample.keys())}")
        except Exception as e:
            print(f"❌ Error loading sample: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating dataset: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing BaseDataset data loading...")
    success = test_dataset_loading()
    
    if success:
        print("\n✅ All tests passed! Data loading module is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)