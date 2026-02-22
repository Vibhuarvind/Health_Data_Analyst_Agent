from typing import Dict, Any, Union
import pandas as pd
from src.utils.llm_client import GroqClient

class ReasoningEngine:
    """
    Generates natural language insights from query results.
    
    Attributes:
        llm: GroqClient instance for generating insights
    """
    
    def __init__(self) -> None:
        self.llm: GroqClient = GroqClient()
        
    def analyze_result(self, user_query: str, execution_result: Dict[str, Any], generated_code: str) -> Dict[str, str]:
        """
        Generates insights based on the query, code, and result.
        
        Args:
            user_query: Original natural language question
            execution_result: Result from QueryExecutor
            generated_code: Python code that was executed
            
        Returns:
            Dictionary containing:
                - response: Natural language insight/answer
        """
        result_data = execution_result.get("result")
        
        # Format result for prompt
        result_str = self._format_result_for_llm(result_data)
        
        prompt = f"""
        Users asked: "{user_query}"
        
        I executed this pandas code:
        ```python
        {generated_code}
        ```
        
        The result was:
        {result_str}
        
        Please provide:
        1. A clear, natural language answer to the user's question.
        2. Any brief insights or health recommendations relevant to this data (if applicable).
        
        Keep it professional and concise.
        """
        
        response = self.llm.generate(prompt, system_message="You are a helpful Health Data Analyst.")
        
        return {
            "response": response
        }
        
    def _format_result_for_llm(self, result: Any) -> str:
        """
        Optimizes result representation for LLM context window.
        
        Args:
            result: Query execution result
            
        Returns:
            String representation optimized for LLM processing
        """
        if isinstance(result, pd.DataFrame):
            if result.empty:
                return "Empty DataFrame"
            # If too large, send summary
            if len(result) > 20:
                return result.head(10).to_string() + f"\n... (Total {len(result)} rows)"
            return result.to_string()
            
        elif isinstance(result, pd.Series):
             if len(result) > 20:
                return result.head(10).to_string() + f"\n... (Total {len(result)} items)"
             return result.to_string()
             
        return str(result)
