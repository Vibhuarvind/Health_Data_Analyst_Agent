"""Tests for Query Planner module."""
import pytest
from src.core.planner import QueryPlanner


class TestQueryPlanner:
    """Test suite for QueryPlanner class."""
    
    @pytest.fixture
    def planner(self):
        """Fixture to create a QueryPlanner instance."""
        return QueryPlanner()
    
    def test_planner_initialization(self, planner):
        """Test that planner initializes correctly."""
        assert planner.llm is not None
        assert planner.schema is not None
        assert planner.validator is not None
    
    def test_generate_plan_basic_query(self, planner):
        """Test basic query generation."""
        result = planner.generate_plan("What is the average BMI?")
        assert isinstance(result, dict)
        assert "query_code" in result
        assert "explanation" in result
        assert "error" in result
    
    def test_generate_plan_with_filter(self, planner):
        """Test query with filtering conditions."""
        result = planner.generate_plan(
            "What is the average BMI of patients with chronic kidney disease?"
        )
        assert result["error"] is None
        assert "df1" in result["query_code"]
        assert "BMI" in result["query_code"] or "bmi" in result["query_code"].lower()
    
    def test_generate_plan_cross_dataset(self, planner):
        """Test query requiring data from both datasets."""
        result = planner.generate_plan(
            "Which patients have high stress and low physical activity?"
        )
        # Should generate code with merge or require both df1 and df2
        assert result["error"] is None
        code = result["query_code"]
        # Check for either merge or both dataframes mentioned
        has_merge = "merge" in code.lower()
        has_both_dfs = "df1" in code and "df2" in code
        assert has_merge or has_both_dfs
    
    def test_generate_plan_with_health_threshold(self, planner):
        """Test query using health interpretation thresholds."""
        result = planner.generate_plan("Find patients with high stress")
        assert result["error"] is None
        assert "Level_of_Stress" in result["query_code"] or "stress" in result["query_code"].lower()
    
    def test_generate_plan_returns_dict(self, planner):
        """Test that result is properly structured."""
        result = planner.generate_plan("Count patients")
        assert isinstance(result, dict)
        assert set(result.keys()) == {"query_code", "explanation", "error"}
    
    def test_generate_plan_empty_query(self, planner):
        """Test handling of empty query."""
        result = planner.generate_plan("")
        # Should either handle gracefully or return with error
        assert isinstance(result, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
