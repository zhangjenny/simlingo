#!/usr/bin/env python3

import sys
import os

# Add the project root to Python path
sys.path.insert(0, '/root/simlingo')

print("Python path:")
for p in sys.path:
    print(f"  {p}")

print("\nTesting module imports...")

try:
    # Test importing the dataset_driving module
    from simlingo_training.dataloader.dataset_driving import Data_Driving
    print("✓ Successfully imported Data_Driving from dataset_driving")
except ImportError as e:
    print(f"✗ Failed to import Data_Driving: {e}")

try:
    # Test importing the config module
    from simlingo_training.config import TrainConfig
    print("✓ Successfully imported TrainConfig from config")
except ImportError as e:
    print(f"✗ Failed to import TrainConfig: {e}")

print("\nModule import test completed.")

# Test Hydra instantiation in a separate function with proper Hydra context
import hydra
from omegaconf import DictConfig

@hydra.main(config_path=None, version_base="1.1")
def test_hydra_instantiation(cfg: DictConfig):
    try:
        # Create a simple config to test
        config_dict = {
            '_target_': 'simlingo_training.dataloader.dataset_driving.Data_Driving',
            'data_path': '/root/simlingo/database/simlingo',
            'bucket_path': 'data/buckets',
            'bucket_name': 'all',
            'img_augmentation_prob': 0.5,
            'img_shift_augmentation_prob': 0.5,
            'use_commentary': False,
            'use_qa': False,
            'use_lmdrive_commands': False,
            'use_old_towns': False,
            'use_only_old_towns': False,
            'use_town13': False,
            'skip_first_n_frames': 10,
            'pred_len': 11,
            'hist_len': 1,
            'hist_len_commentary': 5,
            'split': 'train'
        }
        
        obj = hydra.utils.instantiate(config_dict)
        print("✓ Successfully instantiated Data_Driving via Hydra")
    except Exception as e:
        print(f"✗ Failed to instantiate via Hydra: {e}")

if __name__ == "__main__":
    # Run the Hydra test
    test_hydra_instantiation()