import re
from pathlib import Path

import pytest


@pytest.fixture
def _github_repos():
    """Provide GitHub repository tuples for link validation tests."""
    content = Path("README.md").read_text(encoding="utf-8")
    matches = re.findall(r"https://github\.com/([^/\s\)]+)/([^/\s\)]+)", content)
    return [(owner, repo) for owner, repo in matches]
