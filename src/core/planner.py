from src.utils.llm_client import GroqClient
from src.data.schema import get_schema_info
from src.utils.validator import QueryValidator
import json

class QueryPlanner:
    """
    Generates execution plans (SQL/Python code) from natural language queries.
    """
    
    def __init__(self):
        self.llm = GroqClient()
        self.schema = get_schema_info()
        self.validator = QueryValidator()
        
    def generate_plan(self, user_query: str) -> dict:
        """
        Generates a python code snippet to answer the user query.
        """
        system_prompt = f"""
        You are an expert Python Data Analyst. 
        Your task is to generate Python/Pandas code based on the provided dataset schema.
        
        DATASET SCHEMAS:
        {json.dumps(self.schema, indent=2)}
        
        HEALTH METRIC INTERPRETATION GUIDE:
        - "Perfect/Normal Hemoglobin": Male(13.8-17.2 g/dL), Female(12.1-15.1 g/dL). Use 12-17 as a general filter.
        - "Abnormal Blood Pressure": Use 'Blood_Pressure_Abnormality' == 1.
        - "High Stress": Use 'Level_of_Stress' == 3.
        - "Obese": BMI >= 30.
        - "Smoker": 'Smoking' == 1.
        
        AVAILABLE DATAFRAMES:
        - df1 (Health Metrics)
        - df2 (Physical Activity)
        
        RULES:
        1. Use ONLY pandas/numpy operations.
        2. If you need data from both, join them on 'Patient_Number' (df1.merge(df2, on='Patient_Number')).
        3. Variable 'result' must contain the final answer.
        4. Return ONLY the python code inside markdown blocks.
        
        EXAMPLE: "Find female smokers over 90"
        ```python
        result = df1[(df1['Sex'] == 1) & (df1['Smoking'] == 1) & (df1['Age'] > 90)]
        ```
        """
        
        llm_response = self.llm.generate(user_query, system_message=system_prompt)
        
        # Check for LLM generation failure
        if llm_response.startswith("ERROR_LLM_GEN_FAILED"):
            return {
                "query_code": "",
                "explanation": "LLM Generation failed after all fallbacks.",
                "error": llm_response
            }
        
        # Parse logic
        code = self.validator.clean_code(llm_response)
        
        # Validate logic
        is_safe, message = self.validator.validate(code)
        
        if not is_safe:
            return {
                "query_code": "",
                "explanation": "Query generation failed safety/syntax checks.",
                "error": message
            }
            
        return {
            "query_code": code,
            "explanation": "Generated pandas query based on schema and health thresholds.",
            "error": None
        }
