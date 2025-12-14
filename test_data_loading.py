#!/usr/bin/env python3
"""
Test script to verify that the data loading module works correctly
"""

import sys
import os
sys.path.append('/root/simlingo/simlingo_training')

from dataloader.dataset_base import BaseDataset

def test_data_loading():
    """Test the data loading module"""
    
    # Configuration matching the config.yaml
    config = {
        'data_path': '/root/simlingo/database',
        'bucket_path': '/root/simlingo/database/simlingo',
        'bucket_name': 'all',
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
        'split': 'train',
        'skip_first_n_frames': 0,
        'img_augmentation_prob': 0.0
    }
    
    try:
        print("Creating dataset...")
        
        # Set the current working directory to avoid Hydra issues
        original_cwd = os.getcwd()
        os.chdir('/root/simlingo/simlingo_training')
        
        # Manually set the repo_path to avoid Hydra dependency
        import hydra
        from hydra.core.global_hydra import GlobalHydra
        
        # Initialize Hydra if not already initialized
        if not GlobalHydra().is_initialized():
            hydra.initialize(config_path='config', version_base=None)
        
        dataset = BaseDataset(**config)
        
        print(f"Dataset length: {len(dataset)}")
        
        if len(dataset) > 0:
            print("Testing first sample...")
            sample = dataset[0]
            print(f"Sample keys: {list(sample.keys())}")
            print("Data loading successful!")
            
            # Restore original working directory
            os.chdir(original_cwd)
            return True
        else:
            print("Warning: Dataset is empty")
            # Restore original working directory
            os.chdir(original_cwd)
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        
        # Restore original working directory
        os.chdir(original_cwd)
        return False

if __name__ == "__main__":
    success = test_data_loading()
    if success:
        print("\n✅ Data loading test passed!")
    else:
        print("\n❌ Data loading test failed!")
    sys.exit(0 if success else 1)