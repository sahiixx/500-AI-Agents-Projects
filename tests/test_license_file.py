"""
Test suite for validating the LICENSE file.

This module contains tests to ensure the LICENSE file is present, properly formatted,
and contains all necessary legal information for the MIT License.
"""

import re
import pytest
from pathlib import Path
from datetime import datetime


class TestLicenseFile:
    """Test suite for LICENSE file validation."""
    
    @pytest.fixture
    def license_content(self):
        """Load LICENSE file content."""
        license_path = Path('LICENSE')
        if not license_path.exists():
            pytest.fail("LICENSE file must exist")
        with open(license_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def test_license_file_exists(self):
        """Test that LICENSE file exists in root directory."""
        license_path = Path('LICENSE')
        assert license_path.exists(), "LICENSE file must exist in repository root"
    
    def test_license_is_mit(self, license_content):
        """Test that the license is MIT License."""
        content_upper = license_content.upper()
        assert 'MIT LICENSE' in content_upper or 'MIT' in content_upper, \
            "LICENSE should be MIT License"
    
    def test_license_has_copyright(self, license_content):
        """Test that license includes copyright notice."""
        content_lower = license_content.lower()
        assert 'copyright' in content_lower, "LICENSE must include copyright notice"
    
    def test_license_has_year(self, license_content):
        """Test that license includes copyright year."""
        # Should have a 4-digit year
        years = re.findall(r'\b(20\d{2})\b', license_content)
        assert len(years) > 0, "LICENSE should include copyright year"
        
        # Year should be reasonable (2020-2030)
        for year in years:
            year_int = int(year)
            assert 2020 <= year_int <= 2030, f"Copyright year {year} seems unusual"
    
    def test_license_has_copyright_holder(self, license_content):
        """Test that license includes copyright holder name."""
        # After "Copyright (c)" or "Copyright" should be a name
        copyright_line = None
        for line in license_content.split('\n'):
            if 'copyright' in line.lower():
                copyright_line = line
                break
        
        assert copyright_line is not None, "Could not find copyright line"
        
        # Should have text after the year (the holder's name)
        has_holder = re.search(r'20\d{2}\s+(\w+)', copyright_line)
        assert has_holder, "COPYRIGHT line should include holder's name"
    
    def test_license_has_permission_grant(self, license_content):
        """Test that license includes permission grant."""
        content_lower = license_content.lower()
        permission_keywords = ['permission', 'granted', 'free of charge']
        
        matches = sum(1 for keyword in permission_keywords if keyword in content_lower)
        assert matches >= 2, "LICENSE should include permission grant language"
    
    def test_license_mentions_software(self, license_content):
        """Test that license mentions 'software'."""
        content_lower = license_content.lower()
        assert 'software' in content_lower, "LICENSE should reference 'software'"
    
    def test_license_has_conditions(self, license_content):
        """Test that license includes standard MIT conditions."""
        content_lower = license_content.lower()
        
        # MIT license should mention these conditions
        required_phrases = [
            'above copyright notice',
            'permission notice',
            'included in all copies',
            'substantial portions'
        ]
        
        matches = sum(1 for phrase in required_phrases if phrase in content_lower)
        assert matches >= 2, "LICENSE should include standard MIT conditions"
    
    def test_license_has_warranty_disclaimer(self, license_content):
        """Test that license includes warranty disclaimer."""
        content_upper = license_content.upper()
        
        warranty_keywords = [
            'WITHOUT WARRANTY',
            'AS IS',
            'NO WARRANTY'
        ]
        
        matches = sum(1 for keyword in warranty_keywords if keyword in content_upper)
        assert matches >= 1, "LICENSE must include warranty disclaimer"
    
    def test_license_has_liability_disclaimer(self, license_content):
        """Test that license includes liability disclaimer."""
        content_upper = license_content.upper()
        
        assert 'LIABILITY' in content_upper, "LICENSE must include liability disclaimer"
        assert 'NO' in content_upper or 'NOT' in content_upper, \
            "LIABILITY disclaimer should disclaim liability"
    
    def test_license_proper_formatting(self, license_content):
        """Test that license has proper formatting."""
        lines = license_content.split('\n')
        
        # Should not be excessively long
        assert len(lines) < 50, "LICENSE seems unusually long for MIT"
        assert len(lines) > 10, "LICENSE seems too short"
        
        # Should have some structure
        assert len(license_content) > 500, "LICENSE should have substantial content"
    
    def test_license_no_extra_restrictions(self, license_content):
        """Test that license doesn't add restrictions beyond standard MIT."""
        content_lower = license_content.lower()
        
        # These phrases would indicate additional restrictions
        restriction_phrases = [
            'you may not',
            'prohibited',
            'forbidden',
            'must not'
        ]
        
        for phrase in restriction_phrases:
            assert phrase not in content_lower, \
                f"LICENSE should not add restrictions: found '{phrase}'"
    
    def test_license_readable_format(self, license_content):
        """Test that license is in readable format."""
        # Should not be all caps (except disclaimer sections)
        lines = license_content.split('\n')
        
        # Count lines that are all uppercase
        all_caps_lines = [line for line in lines if line.strip() and line.strip().isupper()]
        
        # Some caps sections are normal (warranty disclaimer), but not everything
        assert len(all_caps_lines) < len(lines) / 2, \
            "LICENSE should be mostly readable text, not all caps"


class TestLicenseCompliance:
    """Test suite for license compliance and best practices."""
    
    def test_license_encoding(self):
        """Test that LICENSE file uses UTF-8 encoding."""
        license_path = Path('LICENSE')
        
        # Try to read with UTF-8
        try:
            with open(license_path, 'r', encoding='utf-8') as f:
                f.read()
            assert True, "File is UTF-8 encoded"
        except UnicodeDecodeError:
            pytest.fail("LICENSE file should use UTF-8 encoding")
    
    def test_license_file_size(self):
        """Test that LICENSE file is reasonable size."""
        license_path = Path('LICENSE')
        file_size = license_path.stat().st_size
        
        # MIT license is typically 1-2 KB
        assert 500 < file_size < 5000, \
            f"LICENSE file size ({file_size} bytes) seems unusual for MIT license"
    
    def test_license_no_extra_files(self):
        """Test that there's only one LICENSE file."""
        repo_root = Path('.')
        license_files = list(repo_root.glob('LICENSE*'))
        license_files = [f for f in license_files if f.is_file() and '.git' not in str(f)]
        
        # Should have exactly one LICENSE file
        assert len(license_files) == 1, \
            f"Should have exactly one LICENSE file, found: {[f.name for f in license_files]}"
    
    def test_license_matches_repository_metadata(self, license_content):
        """Test that LICENSE content matches expected MIT format."""
        # Verify it follows standard MIT template structure
        sections = [
            'Permission is hereby granted',
            'The above copyright notice',
            'THE SOFTWARE IS PROVIDED "AS IS"',
            'IN NO EVENT SHALL'
        ]
        
        matches = sum(1 for section in sections if section in license_content)
        assert matches >= 3, \
            "LICENSE should follow standard MIT License template structure"


class TestLicenseReferences:
    """Test suite for license references in other files."""
    
    def test_readme_mentions_license(self):
        """Test that README.md mentions the license."""
        readme_path = Path('README.md')
        if not readme_path.exists():
            pytest.skip("README.md not found")
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content_lower = content.lower()
        assert 'license' in content_lower, "README should mention license"
        
        # Should reference LICENSE file
        assert 'LICENSE' in content or '[LICENSE]' in content or 'license' in content_lower, \
            "README should reference LICENSE file"
    
    def test_contribution_guide_mentions_license(self):
        """Test that CONTRIBUTION.md mentions licensing."""
        contrib_path = Path('CONTRIBUTION.md')
        if not contrib_path.exists():
            pytest.skip("CONTRIBUTION.md not found")
        
        with open(contrib_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content_lower = content.lower()
        assert 'license' in content_lower, \
            "CONTRIBUTION.md should mention licensing requirements"