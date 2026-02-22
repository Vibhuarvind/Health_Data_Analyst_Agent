from typing import Dict, Any, Optional, Union
import pandas as pd
import numpy as np
from src.data.loader import DataLoader
import traceback

class QueryExecutor:
    """
    Executes the generated pandas code on loaded datasets.
    Handles on-the-fly joining and sandboxed execution.
    
    Attributes:
        df1: Primary health metrics dataset
        df2: Physical activity dataset
    """
    
    def __init__(self) -> None:
        self.df1: pd.DataFrame
        self.df2: pd.DataFrame
        self.df1, self.df2 = DataLoader.load_datasets()
        
    def execute(self, query_code: str) -> Dict[str, Any]:
        """
        Executes the provided python code in a sandboxed environment.
        
        Args:
            query_code: Python/Pandas code string to execute
            
        Returns:
            Dictionary containing:
                - success: Whether execution succeeded
                - result: Query result (DataFrame, Series, or scalar)
                - error: Error message if failed, None otherwise
                - traceback: Full traceback if execution failed
        """
        if not query_code:
            return {"success": False, "result": None, "error": "No query code provided"}
            
        # Define execution namespace
        local_scope = {
            "df1": self.df1,
            "df2": self.df2,
            "pd": pd,
            "np": np,
            "result": None
        }
        
        try:
            # Execute in restricted scope
            exec(query_code, {}, local_scope)
            
            result = local_scope.get("result")
            
            # Post-processing for serialization/display
            processed_result = self._process_result(result)
            
            return {
                "success": True,
                "result": processed_result,
                "error": None
            }
            
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            return {
                "success": False, 
                "result": None, 
                "error": error_msg,
                "traceback": traceback.format_exc()
            }
    
    def _process_result(self, result: Any) -> Union[pd.DataFrame, pd.Series, Any]:
        """
        Helper to format result for downstream consumption.
        
        Args:
            result: Raw execution result
            
        Returns:
            Processed result suitable for display and reasoning
        """
        if isinstance(result, (pd.DataFrame, pd.Series)):
            return result  # Keep as pandas object for display/reasoning
        return result
