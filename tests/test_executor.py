"""Tests for Query Executor module."""
import pytest
import pandas as pd
from src.core.executor import QueryExecutor


class TestQueryExecutor:
    """Test suite for QueryExecutor class."""
    
    @pytest.fixture
    def executor(self):
        """Fixture to create a QueryExecutor instance."""
        return QueryExecutor()
    
    def test_executor_initialization(self, executor):
        """Test that executor initializes with data loaded."""
        assert executor.df1 is not None
        assert executor.df2 is not None
        assert isinstance(executor.df1, pd.DataFrame)
        assert isinstance(executor.df2, pd.DataFrame)
        assert len(executor.df1) > 0
        assert len(executor.df2) > 0
    
    def test_execute_simple_aggregation(self, executor):
        """Test execution of simple aggregation."""
        code = "result = df1['BMI'].mean()"
        result = executor.execute(code)
        assert result["success"] is True
        assert result["error"] is None
        assert isinstance(result["result"], (int, float))
    
    def test_execute_filtering(self, executor):
        """Test execution with filtering."""
        code = "result = df1[df1['Age'] > 50]"
        result = executor.execute(code)
        assert result["success"] is True
        assert isinstance(result["result"], pd.DataFrame)
    
    def test_execute_with_merge(self, executor):
        """Test execution with on-the-fly merge."""
        code = "result = df1.merge(df2, on='Patient_Number')"
        result = executor.execute(code)
        assert result["success"] is True
        assert isinstance(result["result"], pd.DataFrame)
    
    def test_execute_groupby(self, executor):
        """Test execution with groupby operation."""
        code = "result = df1.groupby('Sex')['BMI'].mean()"
        result = executor.execute(code)
        assert result["success"] is True
        assert result["result"] is not None
    
    def test_execute_invalid_code(self, executor):
        """Test handling of syntax error."""
        code = "result = invalid syntax here"
        result = executor.execute(code)
        assert result["success"] is False
        assert result["error"] is not None
    
    def test_execute_empty_code(self, executor):
        """Test handling of empty code."""
        result = executor.execute("")
        assert result["success"] is False
        assert "No query code" in result["error"]
    
    def test_execute_without_result_variable(self, executor):
        """Test handling when result variable not set."""
        code = "x = df1['BMI'].mean()"  # No 'result' variable
        result = executor.execute(code)
        assert result["success"] is True
        # result should be None since no 'result' variable was set
        assert result["result"] is None
    
    def test_execute_returns_dict(self, executor):
        """Test that execute returns properly structured dict."""
        code = "result = 42"
        result = executor.execute(code)
        assert isinstance(result, dict)
        assert "success" in result
        assert "result" in result
        assert "error" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
