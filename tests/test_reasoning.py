"""Tests for Reasoning Engine module."""
import pytest
import pandas as pd
from src.core.reasoning import ReasoningEngine


class TestReasoningEngine:
    """Test suite for ReasoningEngine class."""
    
    @pytest.fixture
    def reasoning(self):
        """Fixture to create a ReasoningEngine instance."""
        return ReasoningEngine()
    
    def test_reasoning_initialization(self, reasoning):
        """Test that reasoning engine initializes correctly."""
        assert reasoning.llm is not None
    
    def test_analyze_result_with_scalar(self, reasoning):
        """Test analysis of scalar result."""
        exec_result = {
            "success": True,
            "result": 25.5,
            "error": None
        }
        result = reasoning.analyze_result(
            "What is the average BMI?",
            exec_result,
            "result = df1['BMI'].mean()"
        )
        assert isinstance(result, dict)
        assert "response" in result
        assert isinstance(result["response"], str)
    
    def test_analyze_result_with_dataframe(self, reasoning):
        """Test analysis of DataFrame result."""
        df = pd.DataFrame({
            "Patient_Number": [1, 2, 3],
            "BMI": [25.0, 30.0, 22.0]
        })
        exec_result = {
            "success": True,
            "result": df,
            "error": None
        }
        result = reasoning.analyze_result(
            "Show patients with BMI > 20",
            exec_result,
            "result = df1[df1['BMI'] > 20]"
        )
        assert "response" in result
        assert isinstance(result["response"], str)
    
    def test_format_result_with_large_dataframe(self, reasoning):
        """Test that large DataFrames are truncated."""
        large_df = pd.DataFrame({
            "col": range(100)
        })
        formatted = reasoning._format_result_for_llm(large_df)
        assert "..." in formatted or "Total" in formatted
    
    def test_format_result_with_empty_dataframe(self, reasoning):
        """Test handling of empty DataFrame."""
        empty_df = pd.DataFrame()
        formatted = reasoning._format_result_for_llm(empty_df)
        assert "Empty" in formatted
    
    def test_format_result_with_series(self, reasoning):
        """Test formatting of pandas Series."""
        series = pd.Series([1, 2, 3, 4, 5])
        formatted = reasoning._format_result_for_llm(series)
        assert isinstance(formatted, str)
    
    def test_analyze_result_returns_dict(self, reasoning):
        """Test that analyze_result returns proper structure."""
        exec_result = {"success": True, "result": 42, "error": None}
        result = reasoning.analyze_result("Test query", exec_result, "result = 42")
        assert isinstance(result, dict)
        assert "response" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
