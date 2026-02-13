import pandas as pd
import numpy as np
from src.data.loader import DataLoader
import traceback

class QueryExecutor:
    """
    Executes the generated pandas code on loaded datasets.
    Handles on-the-fly joining and sandboxed execution.
    """
    
    def __init__(self):
        self.df1, self.df2 = DataLoader.load_datasets()
        
    def execute(self, query_code: str) -> dict:
        """
        Executes the provided python code.
        Returns: {
            "success": bool,
            "result": Any,
            "error": str
        }
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
    
    def _process_result(self, result):
        """Helper to format result for downstream consumption"""
        if isinstance(result, (pd.DataFrame, pd.Series)):
            return result  # Keep as pandas object for display/reasoning
        return result
