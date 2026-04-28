"""Stable test user credential constants shared across test suites.

Credentials are read from environment variables first, with fallback
defaults for local development only. In CI, set TEST_USERNAME and
TEST_PASSWORD as GitHub Actions secrets.
"""
import os

TEST_USERNAME: str = os.getenv("TEST_USERNAME", "13560421999")
TEST_PASSWORD: str = os.getenv("TEST_PASSWORD", "123456")

VALID_USER: dict = {
    "username": TEST_USERNAME,
    "password": TEST_PASSWORD,
}
