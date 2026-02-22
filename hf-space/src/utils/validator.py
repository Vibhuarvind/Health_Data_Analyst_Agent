import re
import ast

class QueryValidator:
    """
    Validates generated Python/Pandas code for safety.
    Prevents execution of dangerous operations using AST analysis and keyword blocking.
    """
    
    BLOCKED_IMPORTS = ['os', 'sys', 'subprocess', 'shutil', 'pickle', 'importlib']
    BLOCKED_CALLS = ['open', 'eval', 'exec', 'compile', 'input', 'exit', 'quit']
    ALLOWED_MODULES = ['pd', 'np', 'pandas', 'numpy']
    
    @staticmethod
    def validate(code: str) -> bool:
        """
        Validates the provided code string.
        Returns: (is_safe: bool, reason: str)
        """
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return False, "Syntax Error in generated code"
            
        for node in ast.walk(tree):
            # Check for imports
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    if alias.name.split('.')[0] in QueryValidator.BLOCKED_IMPORTS:
                        return False, f"Blocked import: {alias.name}"
                        
            # Check for function calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in QueryValidator.BLOCKED_CALLS:
                        return False, f"Blocked function call: {node.func.id}"
                # Check for attribute calls (e.g., os.system)
                elif isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name):
                         if node.func.value.id in QueryValidator.BLOCKED_IMPORTS:
                             return False, f"Blocked attribute call on: {node.func.value.id}"

        return True, "Code is safe"

    @staticmethod
    def clean_code(llm_response: str) -> str:
        """Extracts code from markdown blocks if present"""
        code_match = re.search(r"```python\s*(.*?)```", llm_response, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()
        
        # Fallback: remove python prefix if just ```
        code_match = re.search(r"```\s*(.*?)```", llm_response, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()
            
        return llm_response.strip()
