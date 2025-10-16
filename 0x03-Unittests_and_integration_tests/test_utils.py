#!/usr/bin/env python3
"""
Unit test module for utility functions.
"""

import unittest
from unittest.mock import patch, Mock
from typing import Dict, Mapping, Sequence
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test class for util.access_nested_map function"""

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(self, nested_map, path, expected_result):
        """Test that access_nested_map function returns the expected result."""
        self.assertEqual(access_nested_map(nested_map, path), expected_result)

    @parameterized.expand(
        [
            ({}, ("a",), "a"),
            ({"a": 1}, ("a", "b"), "b"),
        ]
    )
    def test_access_nested_map_exception(
        self, nested_map: Mapping, path: Sequence, expected_exception_msg: str
    ):
        """Test that access_nested_map raises KeyError for invalid paths"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)

        # Verify that the exception message matches the expected message
        self.assertEqual(str(context.exception), f"'{expected_exception_msg}'")


class TestGetJson(unittest.TestCase):
    """Test class for util.get_json function"""

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    @patch("utils.requests.get")
    def test_get_json(self, test_url: str, test_payload: Dict, mock_get: Mock):
        """
        Test that get_json returns the expected result and makes proper
        HTTP call
        """
        # Configure the mock to return a response with the test payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the function
        result = get_json(test_url)

        # Assert that requests.get was called exactly once with the test_url
        mock_get.assert_called_with(test_url)

        # Assert that output equals test_payload
        self.assertEqual(result, test_payload)

        # Verify that json() was called on the response
        mock_response.json.assert_called_once()


class TestMemoize(unittest.TestCase):
    """Test class for memoize decorator"""

    def test_memoize(self):
        """
        Test that memoize decorator caches the result and only calls
        the underlying method once
        """

        # Define the test class inside the test method
        class TestClass:
            """
            Test class used to demonstrate memoize decorator functionality.
            """

            def a_method(self):
                """
                Instance method that returns a fixed value.
                """
                return 42

            @memoize
            def a_property(self):
                """
                Memoized property that calls a_method.
                """
                return self.a_method()

        # Mock at class level and create instance within mock context
        with patch.object(TestClass, 'a_method',
                          return_value=42) as mock_a_method:
            test_instance = TestClass()

            # Access the memoized property twice
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            # Both results should be 42
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Assert that a_method was called only once (due to memoization)
            mock_a_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
