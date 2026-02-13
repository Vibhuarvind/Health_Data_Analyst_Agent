import pandas as pd
from pathlib import Path
from config.settings import DATASET_1_PATH, DATASET_2_PATH
import functools

class DataLoader:
    """Handles loading and validation of health datasets."""
    
    @staticmethod
    @functools.lru_cache(maxsize=1)
    def load_datasets():
        """
        Loads both health datasets with caching.
        Returns: tuple(df1, df2)
        """
        try:
            print(f"Loading datasets from {DATASET_1_PATH} and {DATASET_2_PATH}...")
            
            if not Path(DATASET_1_PATH).exists() or not Path(DATASET_2_PATH).exists():
                raise FileNotFoundError("One or both dataset files are missing.")
                
            df1 = pd.read_csv(DATASET_1_PATH)
            df2 = pd.read_csv(DATASET_2_PATH)
            
            # Basic validation
            DataLoader._validate_structure(df1, df2)
            
            # Feature Engineering (Mandatory 2a)
            df1 = DataLoader._feature_engineering(df1)
            
            print(f"✅ datasets loaded successfully: DF1({len(df1)}), DF2({len(df2)})")
            return df1, df2
            
        except Exception as e:
            print(f"❌ Error loading datasets: {e}")
            raise e

    @staticmethod
    def _feature_engineering(df):
        """Adds derived features to the dataset."""
        if 'BMI' in df.columns:
            # Categorize BMI according to standard ranges
            bins = [0, 18.5, 25, 30, 100]
            labels = ['Underweight', 'Normal', 'Overweight', 'Obese']
            df['BMI_Category'] = pd.cut(df['BMI'], bins=bins, labels=labels)
        return df

    @staticmethod
    def _validate_structure(df1, df2):
        """Validates that necessary columns exist."""
        required_key = "Patient_Number"
        if required_key not in df1.columns:
            raise ValueError(f"Dataset 1 missing required key: {required_key}")
        if required_key not in df2.columns:
            raise ValueError(f"Dataset 2 missing required key: {required_key}")
