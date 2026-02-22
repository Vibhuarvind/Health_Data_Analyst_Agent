"""Pytest configuration and fixtures."""
import pytest
import os
from unittest.mock import Mock, patch


@pytest.fixture(autouse=True)
def mock_groq_api():
    """Mock Groq API calls for all tests to avoid real API calls in CI/CD."""
    with patch('src.utils.llm_client.Groq') as mock_groq:
        # Create mock client
        mock_client = Mock()
        mock_completion = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        
        # Set up mock chain
        mock_message.content = """```python
result = df1['BMI'].mean()
```"""
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_completion
        
        # Return mock client when Groq() is called
        mock_groq.return_value = mock_client
        
        yield mock_client


@pytest.fixture(autouse=True)
def set_test_env():
    """Set up test environment variables."""
    # Set a dummy API key if not present
    if not os.getenv('GROQ_API_KEY'):
        os.environ['GROQ_API_KEY'] = 'test_api_key_for_ci'
    
    yield
    
    # Cleanup not needed as it's just for tests
