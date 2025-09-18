#!/usr/bin/env python3
"""
Unit tests for client module.
"""
import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from typing import Dict, List


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: MagicMock) -> None:
        """Test that GithubOrgClient.org returns the correct value."""
        # Setup mock return value
        expected_org_data = {
            "repos_url": f"https://api.github.com/orgs/{org_name}/repos"}
        mock_get_json.return_value = expected_org_data

        # Create client and call org
        client = GithubOrgClient(org_name)
        result = client.org

        # Assertions
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_org_data)

    def test_public_repos_url(self) -> None:
        """Test that _public_repos_url returns the expected value."""
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            # Setup mock org property
            test_payload = {
                "repos_url": "https://api.github.com/orgs/google/repos"}
            mock_org.return_value = test_payload

            client = GithubOrgClient("google")
            result = client._public_repos_url

            self.assertEqual(result, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """Test public_repos method."""
        # Setup test payload
        test_payload = [
            {"name": "Google"},
            {"name": "Twitter"}
        ]
        mock_get_json.return_value = test_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            test_url = "https://api.github.com/orgs/google/repos"
            mock_public_repos_url.return_value = test_url

            client = GithubOrgClient("google")
            result = client.public_repos()

            # Expected result should be list of repo names
            expected = ["Google", "Twitter"]
            self.assertEqual(result, expected)

            # Assert mocked property was called once
            mock_public_repos_url.assert_called_once()

            # Assert get_json was called once with correct URL
            mock_get_json.assert_called_once_with(test_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(
            self,
            repo: Dict,
            license_key: str,
            expected: bool) -> None:
        """Test has_license static method."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up class fixtures before running tests."""
        config = {
            'return_value.json.side_effect': [
                cls.org_payload, cls.repos_payload,
                cls.org_payload, cls.repos_payload
            ]
        }
        cls.get_patcher = patch('requests.get', **config)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down class fixtures after running tests."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Integration test for public_repos method."""
        client = GithubOrgClient("google")

        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Integration test for public_repos method with license."""
        client = GithubOrgClient("google")

        self.assertEqual(
            client.public_repos("apache-2.0"),
            self.apache2_repos
        )


if __name__ == '__main__':
    unittest.main()

