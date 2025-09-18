# Unit Testing and Integration Testing Project Guide

## Overview
This project focuses on creating comprehensive unit tests and integration tests for a GitHub API client. Here's how to approach each task:

## Project Structure
```
0x03-Unittests_and_integration_tests/
├── client.py              # GitHub client class (provided)
├── utils.py               # Utility functions (provided)
├── test_utils.py          # Unit tests for utils
├── test_client.py         # Unit tests for client + integration tests
└── fixtures.py            # Test data fixtures
```

## Key Testing Concepts

### Unit Tests vs Integration Tests
- **Unit Tests**: Test individual functions in isolation, mocking external dependencies
- **Integration Tests**: Test multiple components working together, only mocking external network calls

### Essential Testing Tools
1. **unittest**: Python's built-in testing framework
2. **unittest.mock**: For mocking dependencies
3. **parameterized**: For running same test with different inputs
4. **patch**: For temporarily replacing functions/methods during tests

## Task-by-Task Breakdown

### Task 0: Parameterize a unit test
- Test `access_nested_map` function with different inputs
- Use `@parameterized.expand` decorator
- Keep test method body to 2 lines maximum

### Task 1: Test exceptions  
- Test that `access_nested_map` raises KeyError for invalid paths
- Use `assertRaises` context manager
- Verify exception messages are correct

### Task 2: Mock HTTP calls
- Test `get_json` function without making real HTTP requests
- Use `@patch` to mock `requests.get`
- Parametrize with different URLs and payloads

### Task 3: Test memoization
- Test that `@memoize` decorator caches results
- Mock the underlying method to verify it's called only once
- Test that subsequent calls return cached values

### Task 4: Test GitHub client org method
- Test `GithubOrgClient.org` method
- Mock `get_json` to avoid external calls
- Parametrize with different organization names

### Task 5: Mock properties
- Test `_public_repos_url` property
- Use `PropertyMock` for mocking properties
- Understand difference between methods and properties

### Task 6: More complex mocking
- Test `public_repos` method
- Mock both `get_json` and `_public_repos_url`
- Verify both mocks are called correctly

### Task 7: Parametrize license checking
- Test `has_license` static method
- Parametrize with different license scenarios
- Include expected return values in parameters

### Task 8: Integration tests
- Create integration tests that test end-to-end functionality
- Use `setUpClass` and `tearDownClass` for setup/cleanup
- Mock only external HTTP requests, not internal methods

## Running the Tests

Execute individual test files:
```bash
python -m unittest test_utils.py
python -m unittest test_client.py
```

Run specific test methods:
```bash
python -m unittest test_utils.TestAccessNestedMap.test_access_nested_map
```

Run with verbose output:
```bash
python -m unittest -v test_utils.py
```

## Common Patterns

### Mocking with patch decorator
```python
@patch('module.function_to_mock')
def test_something(self, mock_function):
    mock_function.return_value = "expected_value"
    # ... test code
```

### Mocking as context manager
```python
def test_something(self):
    with patch('module.function_to_mock') as mock_function:
        mock_function.return_value = "expected_value"
        # ... test code
```

### Parameterized tests
```python
@parameterized.expand([
    (input1, expected1),
    (input2, expected2),
])
def test_something(self, input_val, expected):
    result = function_under_test(input_val)
    self.assertEqual(result, expected)
```

### Testing exceptions
```python
def test_exception(self):
    with self.assertRaises(ExceptionType) as context:
        function_that_should_raise()
    self.assertEqual(str(context.exception), "expected message")
```

## Best Practices

1. **Keep tests isolated**: Each test should be independent
2. **Mock external dependencies**: Don't make real HTTP calls or file operations
3. **Test both success and failure cases**: Include edge cases and error conditions
4. **Use descriptive test names**: Test name should describe what it's testing
5. **Follow AAA pattern**: Arrange, Act, Assert
6. **Keep test methods focused**: One assertion per test method when possible

## Important Notes

- Make sure all files are executable (`chmod +x filename`)
- Add proper docstrings to all classes and methods
- Follow PEP 8 style guidelines
- Use type annotations for all function parameters and return values
- Remember the difference between mocking methods vs properties (use PropertyMock for properties)

## Debugging Tips

1. Use `print()` statements to see what values you're getting
2. Run tests with `-v` flag for verbose output
3. Check that your mocks are being called with expected arguments
4. Verify mock return values match what the real function would return
5. Use `mock.assert_called_once_with()` to verify mock calls