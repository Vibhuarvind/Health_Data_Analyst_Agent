"""Tests for Query Validator module."""
import pytest
from src.utils.validator import QueryValidator


class TestQueryValidator:
    """Test suite for QueryValidator class."""
    
    @pytest.fixture
    def validator(self):
        """Fixture to create a QueryValidator instance."""
        return QueryValidator()
    
    def test_validator_initialization(self, validator):
        """Test that validator initializes correctly."""
        assert validator is not None
    
    def test_validate_safe_code(self, validator):
        """Test validation of safe pandas code."""
        code = "result = df1['BMI'].mean()"
        is_safe, message = validator.validate(code)
        assert is_safe is True
    
    def test_validate_blocks_file_operations(self, validator):
        """Test that file operations are blocked."""
        code = "with open('/etc/passwd', 'r') as f: result = f.read()"
        is_safe, message = validator.validate(code)
        assert is_safe is False
        assert message is not None
    
    def test_validate_blocks_system_calls(self, validator):
        """Test that system calls are blocked."""
        code = "import os; result = os.system('rm -rf /')"
        is_safe, message = validator.validate(code)
        assert is_safe is False
    
    def test_validate_blocks_import(self, validator):
        """Test that dangerous imports are blocked."""
        code = "import subprocess; result = subprocess.call(['ls'])"
        is_safe, message = validator.validate(code)
        assert is_safe is False
    
    def test_validate_allows_pandas(self, validator):
        """Test that pandas operations are allowed."""
        code = "result = df1.merge(df2, on='Patient_Number')"
        is_safe, message = validator.validate(code)
        assert is_safe is True
    
    def test_validate_allows_numpy(self, validator):
        """Test that numpy operations are allowed."""
        code = "result = np.mean(df1['BMI'])"
        is_safe, message = validator.validate(code)
        assert is_safe is True
    
    def test_clean_code_removes_markdown(self, validator):
        """Test that clean_code removes markdown blocks."""
        markdown_code = "```python\nresult = df1['BMI'].mean()\n```"
        cleaned = validator.clean_code(markdown_code)
        assert "```" not in cleaned
        assert "result = df1['BMI'].mean()" in cleaned
    
    def test_clean_code_removes_extra_text(self, validator):
        """Test that clean_code extracts only code."""
        mixed_content = "Here's the code:\n```python\nresult = 42\n```\nThis calculates..."
        cleaned = validator.clean_code(mixed_content)
        assert "Here's" not in cleaned
        assert "calculates" not in cleaned
        assert "result = 42" in cleaned
    
    def test_validate_syntax_error(self, validator):
        """Test handling of syntax errors."""
        code = "result = invalid syntax"
        is_safe, message = validator.validate(code)
        assert is_safe is False
        assert message is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
