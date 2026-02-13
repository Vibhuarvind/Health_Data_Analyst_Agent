import pandas as pd
from src.utils.llm_client import GroqClient

class ReasoningEngine:
    """
    Generates natural language insights from query results.
    """
    
    def __init__(self):
        self.llm = GroqClient()
        
    def analyze_result(self, user_query: str, execution_result: dict, generated_code: str) -> dict:
        """
        Generates insights based on the query, code, and result.
        Returns: {
            "response": str,
            "insights": str
        }
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
        
    def _format_result_for_llm(self, result):
        """Optimizes result representation for context window"""
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
