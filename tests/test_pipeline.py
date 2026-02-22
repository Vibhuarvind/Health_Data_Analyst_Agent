"""Integration tests for the complete pipeline."""
import pytest
from src.core.pipeline import HealthDataPipeline


class TestHealthDataPipeline:
    """Test suite for end-to-end pipeline integration."""
    
    @pytest.fixture
    def pipeline(self):
        """Fixture to create a pipeline instance."""
        return HealthDataPipeline()
    
    def test_pipeline_initialization(self, pipeline):
        """Test that pipeline initializes all components."""
        assert pipeline.planner is not None
        assert pipeline.executor is not None
        assert pipeline.reasoning is not None
    
    def test_pipeline_simple_query(self, pipeline):
        """Test complete pipeline with simple query."""
        result = pipeline.run("What is the average BMI?")
        assert isinstance(result, dict)
        assert result["status"] in ["success", "failed"]
        assert "timings_ms" in result
        assert "py_code" in result
    
    def test_pipeline_complex_query(self, pipeline):
        """Test pipeline with complex multi-condition query."""
        result = pipeline.run(
            "What is the average BMI of patients with chronic kidney disease?"
        )
        assert result["status"] == "success"
        assert result["py_success"] is True
        assert result["final_response"] is not None
    
    def test_pipeline_cross_dataset_query(self, pipeline):
        """Test pipeline with cross-dataset query."""
        result = pipeline.run(
            "Which patients have high stress levels and low physical activity?"
        )
        # Should attempt to join datasets
        assert "py_code" in result
        assert result["py_code"] is not None
    
    def test_pipeline_timing_metrics(self, pipeline):
        """Test that pipeline tracks timing metrics."""
        result = pipeline.run("Count total patients")
        assert "timings_ms" in result
        assert "total" in result["timings_ms"]
        assert isinstance(result["timings_ms"]["total"], (int, float))
    
    def test_pipeline_error_handling(self, pipeline):
        """Test pipeline handles errors gracefully."""
        result = pipeline.run("This is a malformed query that should fail")
        # Even if it fails, should return structured response
        assert isinstance(result, dict)
        assert "status" in result
        assert "error" in result
    
    def test_pipeline_returns_all_fields(self, pipeline):
        """Test that pipeline returns all expected fields."""
        result = pipeline.run("Average BMI")
        expected_fields = {
            "question", "status", "timings_ms", "py_code",
            "py_success", "result", "final_response", "error"
        }
        assert set(result.keys()) == expected_fields


@pytest.mark.parametrize("query,expected_in_code", [
    ("Average BMI", "BMI"),
    ("Patients with high stress", "Level_of_Stress"),
    ("Female patients", "Sex"),
    ("Patients over 50", "Age"),
])
def test_pipeline_query_variations(query, expected_in_code):
    """Test pipeline with various query patterns."""
    pipeline = HealthDataPipeline()
    result = pipeline.run(query)
    if result["py_code"]:
        assert expected_in_code in result["py_code"] or expected_in_code.lower() in result["py_code"].lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
