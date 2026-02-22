"""Pytest configuration and fixtures."""
import pytest
import os
from unittest.mock import Mock, patch


def get_mock_response(prompt):
    """Generate appropriate mock response based on query content."""
    prompt_lower = prompt.lower()
    
    # Check for specific query patterns and return relevant code
    # Order matters - check most specific first
    
    # Check for cross-dataset queries (stress + activity = df1 + df2)
    if ('stress' in prompt_lower and 'activity' in prompt_lower) or \
       ('join' in prompt_lower) or ('merge' in prompt_lower) or \
       ('dataset_2' in prompt) or ('df2' in prompt_lower) or \
       ('both dataset' in prompt_lower) or ('cross' in prompt_lower):
        return """```python
merged = df1.merge(df2, on='Patient_Number')
result = merged[(merged['Level_of_Stress'] > 7) & (merged['Physical_Activity_Level'] < 3)]
```"""
    elif 'average bmi' in prompt_lower or ('bmi' in prompt_lower and 'average' in prompt_lower):
        return """```python
result = df1['BMI'].mean()
```"""
    elif 'stress' in prompt_lower or 'Level_of_Stress' in prompt:
        return """```python
result = df1[df1['Level_of_Stress'] > 7].shape[0]
```"""
    elif 'female' in prompt_lower or 'Sex' in prompt:
        return """```python
result = df1[df1['Sex'] == 'Female']
```"""
    elif 'over 50' in prompt_lower or ('age' in prompt_lower and '50' in prompt):
        return """```python
result = df1[df1['Age'] > 50]
```"""
    elif 'bmi' in prompt_lower:
        return """```python
result = df1['BMI'].mean()
```"""
    elif 'age' in prompt_lower:
        return """```python
result = df1['Age'].mean()
```"""
    else:
        # Default response
        return """```python
result = df1.head()
```"""


@pytest.fixture(autouse=True)
def mock_groq_api():
    """Mock Groq API calls for all tests to avoid real API calls in CI/CD."""
    with patch('src.utils.llm_client.Groq') as mock_groq:
        # Create mock client
        mock_client = Mock()
        
        def create_completion(*args, **kwargs):
            """Dynamic completion based on prompt."""
            # Extract prompt from kwargs
            messages = kwargs.get('messages', [])
            prompt = ''
            for msg in messages:
                if msg.get('role') == 'user':
                    prompt = msg.get('content', '')
                    break
            
            # Generate response based on prompt
            mock_completion = Mock()
            mock_choice = Mock()
            mock_message = Mock()
            mock_message.content = get_mock_response(prompt)
            mock_choice.message = mock_message
            mock_completion.choices = [mock_choice]
            
            return mock_completion
        
        mock_client.chat.completions.create.side_effect = create_completion
        
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
