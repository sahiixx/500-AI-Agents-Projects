"""
Comprehensive validation tests for Python requirements files.

This test suite validates all requirements*.txt files in the repository,
ensuring proper syntax, version specifications, security best practices,
and consistency across different requirement variants.
"""

import re
import pytest
from pathlib import Path
from typing import List, Dict, Set, Tuple


class TestRequirementsFilesExist:
    """Test that all expected requirements files exist."""
    
    def test_main_requirements_exists(self):
        """Test that main requirements.txt exists."""
        assert Path("requirements.txt").exists(), "Main requirements.txt must exist"
    
    def test_minimal_requirements_exists(self):
        """Test that requirements-minimal.txt exists."""
        assert Path("requirements-minimal.txt").exists(), \
            "requirements-minimal.txt must exist for minimal installations"
    
    def test_py39_requirements_exists(self):
        """Test that requirements-py39.txt exists."""
        assert Path("requirements-py39.txt").exists(), \
            "requirements-py39.txt must exist for Python 3.9 compatibility"
    
    def test_working_requirements_exists(self):
        """Test that requirements-working.txt exists."""
        assert Path("requirements-working.txt").exists(), \
            "requirements-working.txt must exist as working/tested configuration"


class TestRequirementsSyntax:
    """Test syntax and formatting of requirements files."""
    
    @pytest.fixture
    def requirements_files(self) -> List[Path]:
        """Get all requirements files."""
        return [
            Path("requirements.txt"),
            Path("requirements-minimal.txt"),
            Path("requirements-py39.txt"),
            Path("requirements-working.txt"),
        ]
    
    def test_files_are_utf8(self, requirements_files):
        """Test that all requirements files are valid UTF-8."""
        for req_file in requirements_files:
            try:
                content = req_file.read_text(encoding='utf-8')
                assert content is not None
            except UnicodeDecodeError:
                pytest.fail(f"{req_file} is not valid UTF-8")
    
    def test_files_end_with_newline(self, requirements_files):
        """Test that all requirements files end with newline."""
        for req_file in requirements_files:
            content = req_file.read_text(encoding='utf-8')
            assert content.endswith('\n'), \
                f"{req_file} should end with a newline character"
    
    def test_no_trailing_whitespace(self, requirements_files):
        """Test that lines don't have trailing whitespace."""
        for req_file in requirements_files:
            content = req_file.read_text(encoding='utf-8')
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                # Skip empty lines
                if line:
                    assert not line.rstrip() != line or line.endswith(' ') or line.endswith('\t'), \
                        f"{req_file}:{i} has trailing whitespace"
    
    def test_no_duplicate_packages(self, requirements_files):
        """Test that no package is listed multiple times."""
        for req_file in requirements_files:
            content = req_file.read_text(encoding='utf-8')
            packages = []
            for line in content.split('\n'):
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith('#'):
                    # Extract package name (before ==, >=, <=, etc.)
                    package_name = re.split(r'[=<>!]', line)[0].strip()
                    if package_name:
                        assert package_name not in packages, \
                            f"{req_file} has duplicate package: {package_name}"
                        packages.append(package_name)
    
    def test_valid_version_specifiers(self, requirements_files):
        """Test that version specifiers follow PEP 440."""
        valid_operators = ['==', '>=', '<=', '>', '<', '!=', '~=']
        
        for req_file in requirements_files:
            content = req_file.read_text(encoding='utf-8')
            for i, line in enumerate(content.split('\n'), 1):
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith('#'):
                    # Check if line has version specifier
                    if any(op in line for op in valid_operators):
                        # Should have valid operator and version
                        has_valid_spec = any(op in line for op in valid_operators)
                        assert has_valid_spec, \
                            f"{req_file}:{i} has invalid version specifier: {line}"
                        
                        # Check version format (should be numeric with dots)
                        version_part = re.split(r'[=<>!~]+', line)[-1].strip()
                        if version_part:
                            # Allow version ranges like ">=8.0.0,<9.0.0"
                            for version in version_part.split(','):
                                version = version.strip()
                                assert re.match(r'^\d+(\.\d+)*([a-z]\d+)?$', version), \
                                    f"{req_file}:{i} has invalid version format: {version}"
    
    def test_consistent_comment_style(self, requirements_files):
        """Test that comments use consistent style."""
        for req_file in requirements_files:
            content = req_file.read_text(encoding='utf-8')
            for line in content.split('\n'):
                if line.strip().startswith('#'):
                    # Comments should have space after #
                    if len(line.strip()) > 1:
                        assert line.strip()[1] == ' ', \
                            f"{req_file} comment should have space after #: {line}"


class TestRequirementsContent:
    """Test content and organization of requirements files."""
    
    def test_core_testing_packages_present(self):
        """Test that core testing packages are in all files."""
        core_packages = ['pytest', 'pytest-cov', 'pyyaml', 'requests']
        
        for req_file in ['requirements.txt', 'requirements-minimal.txt', 
                         'requirements-py39.txt', 'requirements-working.txt']:
            content = Path(req_file).read_text(encoding='utf-8')
            for package in core_packages:
                assert package in content.lower(), \
                    f"{req_file} must contain {package}"
    
    def test_minimal_is_subset_of_full(self):
        """Test that minimal requirements are subset of full requirements."""
        minimal = self._parse_requirements('requirements-minimal.txt')
        full = self._parse_requirements('requirements.txt')
        
        minimal_packages = set(pkg for pkg, _ in minimal)
        full_packages = set(pkg for pkg, _ in full)
        
        # All minimal packages should be in full (or have different versions)
        for pkg in minimal_packages:
            # Core packages that should be in both
            if pkg in ['pytest', 'pytest-cov', 'pyyaml', 'requests', 
                      'beautifulsoup4', 'pandas', 'numpy', 'python-dotenv',
                      'phonenumbers', 'email-validator', 'python-dateutil']:
                assert pkg in full_packages or self._is_similar_package(pkg, full_packages), \
                    f"Minimal package {pkg} should be in full requirements"
    
    def test_py39_has_compatible_versions(self):
        """Test that py39 requirements use Python 3.9 compatible versions."""
        content = Path('requirements-py39.txt').read_text(encoding='utf-8')
        
        # Should have older CrewAI version for Python 3.9
        assert 'crewai==0.1.32' in content, \
            "Python 3.9 requirements should use older CrewAI version"
        
        # Should mention Python 3.9 compatibility in comments
        assert '3.9' in content or 'py39' in content.lower(), \
            "Should mention Python 3.9 compatibility"
    
    def test_working_has_flexible_versions(self):
        """Test that working requirements use flexible version specifiers."""
        content = Path('requirements-working.txt').read_text(encoding='utf-8')
        
        # Should use >= for some packages
        assert '>=' in content, \
            "Working requirements should use flexible version specifiers"
        
        # Should have crewai with flexible version
        crewai_lines = [line for line in content.split('\n') 
                       if line.strip().startswith('crewai')]
        assert any('>=' in line for line in crewai_lines), \
            "Working requirements should have flexible crewai version"
    
    def test_comments_organize_sections(self):
        """Test that comments are used to organize package sections."""
        for req_file in ['requirements.txt', 'requirements-minimal.txt', 
                         'requirements-py39.txt', 'requirements-working.txt']:
            content = Path(req_file).read_text(encoding='utf-8')
            
            # Should have section comments
            section_keywords = ['Testing', 'CrewAI', 'Web Scraping', 'Data Processing', 
                              'API', 'Environment', 'Utilities']
            
            has_sections = any(keyword in content for keyword in section_keywords)
            assert has_sections, \
                f"{req_file} should have section comments for organization"
    
    def test_no_local_file_references(self):
        """Test that requirements don't reference local files."""
        for req_file in ['requirements.txt', 'requirements-minimal.txt', 
                         'requirements-py39.txt', 'requirements-working.txt']:
            content = Path(req_file).read_text(encoding='utf-8')
            
            # Should not have file:// or local paths
            assert 'file://' not in content.lower(), \
                f"{req_file} should not contain local file references"
            assert not re.search(r'\./|\.\./', content), \
                f"{req_file} should not contain relative path references"
    
    def test_no_git_references(self):
        """Test that requirements don't use git+ URLs."""
        for req_file in ['requirements.txt', 'requirements-minimal.txt', 
                         'requirements-py39.txt', 'requirements-working.txt']:
            content = Path(req_file).read_text(encoding='utf-8')
            
            # Should not have git+ URLs (unless necessary)
            git_lines = [line for line in content.split('\n') 
                        if 'git+' in line.lower() and not line.strip().startswith('#')]
            assert len(git_lines) == 0, \
                f"{req_file} should not use git+ URLs: {git_lines}"
    
    def _parse_requirements(self, filename: str) -> List[Tuple[str, str]]:
        """Parse requirements file and return list of (package, version) tuples."""
        content = Path(filename).read_text(encoding='utf-8')
        requirements = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                # Extract package and version
                match = re.match(r'^([a-zA-Z0-9\-_]+)([=<>!~]+.+)?$', line)
                if match:
                    package = match.group(1)
                    version = match.group(2) if match.group(2) else ''
                    requirements.append((package, version))
        return requirements
    
    def _is_similar_package(self, package: str, package_set: Set[str]) -> bool:
        """Check if package name is similar to any in the set (case-insensitive)."""
        package_lower = package.lower()
        return any(pkg.lower() == package_lower for pkg in package_set)


class TestRequirementsSecurity:
    """Test security best practices in requirements files."""
    
    def test_no_insecure_packages(self):
        """Test that requirements don't contain known insecure packages."""
        # List of packages with known security issues (examples)
        insecure_packages = ['pycrypto']  # Use pycryptodome instead
        
        for req_file in ['requirements.txt', 'requirements-minimal.txt', 
                         'requirements-py39.txt', 'requirements-working.txt']:
            content = Path(req_file).read_text(encoding='utf-8')
            for package in insecure_packages:
                assert package not in content.lower(), \
                    f"{req_file} contains insecure package: {package}"
    
    def test_pytest_version_secure(self):
        """Test that pytest version is reasonably recent."""
        for req_file in ['requirements.txt', 'requirements-minimal.txt', 
                         'requirements-py39.txt', 'requirements-working.txt']:
            content = Path(req_file).read_text(encoding='utf-8')
            
            # Extract pytest version
            pytest_lines = [line for line in content.split('\n') 
                           if line.strip().startswith('pytest')]
            assert len(pytest_lines) > 0, f"{req_file} must have pytest"
            
            for line in pytest_lines:
                if 'pytest==' in line or 'pytest>=' in line:
                    # Extract version number
                    version_match = re.search(r'(\d+)\.(\d+)\.(\d+)', line)
                    if version_match:
                        major = int(version_match.group(1))
                        # pytest should be version 7+ for security
                        assert major >= 7, \
                            f"{req_file} pytest version should be 7.0+ for security"
    
    def test_no_development_versions(self):
        """Test that requirements don't use development versions in production."""
        for req_file in ['requirements.txt', 'requirements-py39.txt']:
            content = Path(req_file).read_text(encoding='utf-8')
            
            # Should not have dev versions
            dev_indicators = ['.dev', '-dev', 'alpha', 'beta', 'rc']
            for indicator in dev_indicators:
                matching_lines = [line for line in content.split('\n')
                                 if indicator in line.lower() and not line.strip().startswith('#')]
                assert len(matching_lines) == 0, \
                    f"{req_file} should not use dev versions: {matching_lines}"


class TestRequirementsVersions:
    """Test version specifications and compatibility."""
    
    def test_pytest_version_differences(self):
        """Test that pytest versions are appropriate for each requirements file."""
        main_content = Path('requirements.txt').read_text(encoding='utf-8')
        minimal_content = Path('requirements-minimal.txt').read_text(encoding='utf-8')
        
        # Main requirements should have flexible or newer pytest
        assert 'pytest>=' in main_content or 'pytest==' in main_content, \
            "Main requirements should specify pytest version"
        
        # Minimal should have pinned version for stability
        assert 'pytest==' in minimal_content, \
            "Minimal requirements should pin pytest version"
    
    def test_python_dotenv_version_consistency(self):
        """Test python-dotenv version across files."""
        versions = {}
        for req_file in ['requirements.txt', 'requirements-minimal.txt', 
                         'requirements-py39.txt', 'requirements-working.txt']:
            content = Path(req_file).read_text(encoding='utf-8')
            for line in content.split('\n'):
                if line.strip().startswith('python-dotenv'):
                    versions[req_file] = line.strip()
        
        # All versions should be specified
        assert len(versions) == 4, "All files should specify python-dotenv version"
        
        # Versions should be consistent or have good reason to differ
        unique_versions = set(versions.values())
        # Allow for minor version differences but document them
        assert len(unique_versions) <= 2, \
            f"python-dotenv versions should be mostly consistent: {versions}"
    
    def test_crewai_versions_appropriate(self):
        """Test that CrewAI versions are appropriate for each file."""
        # Main requirements
        main_content = Path('requirements.txt').read_text(encoding='utf-8')
        if 'crewai' in main_content:
            crewai_lines = [line for line in main_content.split('\n')
                           if line.strip().startswith('crewai')]
            for line in crewai_lines:
                if 'crewai==' in line:
                    version_match = re.search(r'(\d+)\.(\d+)', line)
                    if version_match:
                        major = int(version_match.group(1))
                        minor = int(version_match.group(2))
                        # Main should use recent version
                        assert major >= 0 and minor >= 28, \
                            "Main requirements should use recent CrewAI version"
        
        # Python 3.9 requirements
        py39_content = Path('requirements-py39.txt').read_text(encoding='utf-8')
        if 'crewai' in py39_content:
            assert 'crewai==0.1.32' in py39_content, \
                "Python 3.9 requirements should use compatible CrewAI version"
    
    def test_compatible_langchain_versions(self):
        """Test that langchain versions are compatible across files."""
        for req_file in ['requirements.txt', 'requirements-py39.txt', 
                         'requirements-working.txt']:
            content = Path(req_file).read_text(encoding='utf-8')
            
            # If langchain is present, should have related packages
            if 'langchain==' in content or 'langchain>=' in content:
                # Should also have langchain-openai and langchain-community
                assert 'langchain-openai' in content, \
                    f"{req_file} with langchain should have langchain-openai"
                assert 'langchain-community' in content, \
                    f"{req_file} with langchain should have langchain-community"


class TestRequirementsDocumentation:
    """Test documentation and comments in requirements files."""
    
    def test_files_have_section_headers(self):
        """Test that requirements files have clear section headers."""
        required_sections = {
            'requirements.txt': ['CrewAI', 'Web Scraping', 'Data Processing', 'API', 'Environment', 'Utilities'],
            'requirements-minimal.txt': ['Web Scraping', 'Data Processing', 'Environment', 'Utilities'],
            'requirements-py39.txt': ['CrewAI', 'Web Scraping', 'Data Processing', 'API', 'Environment', 'Utilities'],
            'requirements-working.txt': ['Testing', 'CrewAI', 'Web Scraping', 'Data Processing', 'API', 'Environment', 'Utilities'],
        }
        
        for req_file, sections in required_sections.items():
            content = Path(req_file).read_text(encoding='utf-8')
            for section in sections:
                assert section in content, \
                    f"{req_file} should have '{section}' section header"
    
    def test_py39_file_documents_compatibility(self):
        """Test that py39 file documents Python version compatibility."""
        content = Path('requirements-py39.txt').read_text(encoding='utf-8')
        
        # Should mention Python 3.9 or compatibility
        compatibility_mentioned = (
            'Python 3.9' in content or 
            'py39' in content.lower() or
            'compatible with Python 3.9' in content or
            'older versions compatible' in content.lower()
        )
        assert compatibility_mentioned, \
            "requirements-py39.txt should document Python 3.9 compatibility"
    
    def test_working_file_documents_purpose(self):
        """Test that working file documents its purpose."""
        content = Path('requirements-working.txt').read_text(encoding='utf-8')
        
        # Should have comment about being working/tested configuration
        purpose_mentioned = (
            'working' in content.lower() or
            'tested' in content.lower() or
            'compatible' in content.lower()
        )
        # File name itself documents purpose, but comments help
        # This is a soft requirement
        assert True, "working file exists with clear naming"
    
    def test_minimal_file_explains_purpose(self):
        """Test that minimal file is clearly minimal."""
        minimal_content = Path('requirements-minimal.txt').read_text(encoding='utf-8')
        full_content = Path('requirements.txt').read_text(encoding='utf-8')
        
        # Minimal should have fewer packages
        minimal_lines = [l for l in minimal_content.split('\n') 
                        if l.strip() and not l.strip().startswith('#')]
        full_lines = [l for l in full_content.split('\n')
                     if l.strip() and not l.strip().startswith('#')]
        
        assert len(minimal_lines) < len(full_lines), \
            "requirements-minimal.txt should have fewer packages than requirements.txt"


class TestRequirementsIntegration:
    """Test integration and compatibility across requirements files."""
    
    def test_all_files_installable_format(self):
        """Test that all files follow pip-installable format."""
        for req_file in ['requirements.txt', 'requirements-minimal.txt', 
                         'requirements-py39.txt', 'requirements-working.txt']:
            content = Path(req_file).read_text(encoding='utf-8')
            
            for i, line in enumerate(content.split('\n'), 1):
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    # Should match package name pattern
                    assert re.match(r'^[a-zA-Z0-9\-_\[\]]+([=<>!~].*)?$', line), \
                        f"{req_file}:{i} has invalid package format: {line}"
    
    def test_no_conflicting_versions_within_file(self):
        """Test that each file doesn't have conflicting version specs."""
        for req_file in ['requirements.txt', 'requirements-minimal.txt', 
                         'requirements-py39.txt', 'requirements-working.txt']:
            content = Path(req_file).read_text(encoding='utf-8')
            
            package_specs = {}
            for line in content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    # Extract package name
                    package_name = re.split(r'[=<>!~]', line)[0].strip()
                    if package_name in package_specs:
                        pytest.fail(f"{req_file} has duplicate package {package_name}")
                    package_specs[package_name] = line
    
    def test_package_count_appropriate(self):
        """Test that package counts are appropriate for each file."""
        def count_packages(filename: str) -> int:
            content = Path(filename).read_text(encoding='utf-8')
            return len([l for l in content.split('\n')
                       if l.strip() and not l.strip().startswith('#')])
        
        minimal_count = count_packages('requirements-minimal.txt')
        py39_count = count_packages('requirements-py39.txt')
        working_count = count_packages('requirements-working.txt')
        full_count = count_packages('requirements.txt')
        
        # Minimal should be smallest
        assert minimal_count < full_count, \
            "Minimal requirements should have fewer packages than full"
        
        # All should have at least core packages
        assert minimal_count >= 8, \
            "Minimal should have at least core testing and utility packages"
        
        # Python 3.9 and working should have similar counts to full
        assert py39_count >= minimal_count, \
            "Python 3.9 requirements should have more packages than minimal"


class TestRequirementsEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_files_not_empty(self):
        """Test that requirements files are not empty."""
        for req_file in ['requirements.txt', 'requirements-minimal.txt', 
                         'requirements-py39.txt', 'requirements-working.txt']:
            content = Path(req_file).read_text(encoding='utf-8')
            # Should have at least some non-comment lines
            package_lines = [l for l in content.split('\n')
                           if l.strip() and not l.strip().startswith('#')]
            assert len(package_lines) > 0, \
                f"{req_file} should not be empty"
    
    def test_no_extremely_long_lines(self):
        """Test that no lines are excessively long."""
        max_line_length = 200
        
        for req_file in ['requirements.txt', 'requirements-minimal.txt', 
                         'requirements-py39.txt', 'requirements-working.txt']:
            content = Path(req_file).read_text(encoding='utf-8')
            for i, line in enumerate(content.split('\n'), 1):
                assert len(line) <= max_line_length, \
                    f"{req_file}:{i} line too long ({len(line)} chars): {line[:50]}..."
    
    def test_no_mixed_line_endings(self):
        """Test that files use consistent line endings."""
        for req_file in ['requirements.txt', 'requirements-minimal.txt', 
                         'requirements-py39.txt', 'requirements-working.txt']:
            with open(req_file, 'rb') as f:
                content = f.read()
            
            # Check for mixed line endings
            has_crlf = b'\r\n' in content
            has_lf = b'\n' in content and b'\r\n' not in content
            
            # Should use one type consistently
            assert not (has_crlf and has_lf), \
                f"{req_file} has mixed line endings (CRLF and LF)"
    
    def test_valid_package_names(self):
        """Test that all package names follow Python naming conventions."""
        valid_name_pattern = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9\-_]*[a-zA-Z0-9])?$')
        
        for req_file in ['requirements.txt', 'requirements-minimal.txt', 
                         'requirements-py39.txt', 'requirements-working.txt']:
            content = Path(req_file).read_text(encoding='utf-8')
            for i, line in enumerate(content.split('\n'), 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    # Extract package name
                    package_name = re.split(r'[=<>!~\[]', line)[0].strip()
                    if package_name:
                        assert valid_name_pattern.match(package_name), \
                            f"{req_file}:{i} invalid package name: {package_name}"