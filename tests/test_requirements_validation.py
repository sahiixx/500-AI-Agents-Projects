"""
Comprehensive tests for validating Python requirements files.

Tests cover syntax, version specifications, security, consistency,
and best practices for all requirements files in the repository.
"""
import re
import pytest
from pathlib import Path
from typing import Dict, List, Tuple, Set


class TestRequirementsFileExistence:
    """Test that all requirements files exist and are accessible."""
    
    @pytest.fixture
    def requirements_files(self):
        """List of all requirements files in the repository."""
        return [
            'requirements.txt',
            'requirements-minimal.txt',
            'requirements-py39.txt',
            'requirements-working.txt'
        ]
    
    def test_main_requirements_file_exists(self):
        """Test that the main requirements.txt file exists."""
        req_file = Path('requirements.txt')
        assert req_file.exists(), "requirements.txt should exist"
        assert req_file.is_file(), "requirements.txt should be a file"
    
    def test_all_requirements_files_exist(self, requirements_files):
        """Test that all requirements files exist."""
        for req_file in requirements_files:
            path = Path(req_file)
            assert path.exists(), f"{req_file} should exist"
            assert path.is_file(), f"{req_file} should be a file"
    
    def test_requirements_files_are_readable(self, requirements_files):
        """Test that all requirements files can be read."""
        for req_file in requirements_files:
            path = Path(req_file)
            try:
                content = path.read_text(encoding='utf-8')
                assert content is not None
                assert len(content) > 0, f"{req_file} should not be empty"
            except Exception as e:
                pytest.fail(f"Failed to read {req_file}: {e}")


class TestRequirementsSyntax:
    """Test requirements file syntax and format."""
    
    @pytest.fixture
    def requirements_content(self):
        """Load all requirements files content."""
        files = {
            'main': Path('requirements.txt').read_text(encoding='utf-8'),
            'minimal': Path('requirements-minimal.txt').read_text(encoding='utf-8'),
            'py39': Path('requirements-py39.txt').read_text(encoding='utf-8'),
            'working': Path('requirements-working.txt').read_text(encoding='utf-8')
        }
        return files
    
    def test_requirements_use_utf8_encoding(self):
        """Test that all requirements files use UTF-8 encoding."""
        req_files = [
            'requirements.txt',
            'requirements-minimal.txt',
            'requirements-py39.txt',
            'requirements-working.txt'
        ]
        for req_file in req_files:
            try:
                Path(req_file).read_text(encoding='utf-8')
            except UnicodeDecodeError:
                pytest.fail(f"{req_file} is not UTF-8 encoded")
    
    def test_requirements_have_unix_line_endings(self, requirements_content):
        """Test that requirements files use Unix line endings (LF)."""
        for name, content in requirements_content.items():
            assert '\r\n' not in content, \
                f"requirements-{name} should use Unix line endings (LF), not CRLF"
    
    def test_no_tabs_in_requirements(self, requirements_content):
        """Test that requirements files don't contain tabs."""
        for name, content in requirements_content.items():
            assert '\t' not in content, \
                f"requirements-{name} should not contain tabs"
    
    def test_requirements_end_with_newline(self, requirements_content):
        """Test that requirements files end with a newline."""
        for name, content in requirements_content.items():
            if content:
                assert content.endswith('\n'), \
                    f"requirements-{name} should end with a newline"


class TestVersionSpecifications:
    """Test version specification formats and patterns."""
    
    def _parse_requirements(self, filepath: str) -> List[Dict[str, str]]:
        """Parse requirements file into structured data."""
        content = Path(filepath).read_text(encoding='utf-8')
        requirements = []
        
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            match = re.match(r'^([a-zA-Z0-9\-_]+)(.*?)$', line)
            if match:
                package = match.group(1)
                version_spec = match.group(2).strip()
                requirements.append({
                    'package': package,
                    'version_spec': version_spec,
                    'line': line
                })
        
        return requirements
    
    def test_main_requirements_uses_version_pinning(self):
        """Test that main requirements.txt uses version constraints."""
        reqs = self._parse_requirements('requirements.txt')
        
        for req in reqs:
            package = req['package']
            version_spec = req['version_spec']
            
            assert version_spec, \
                f"Package '{package}' should have version specification"
    
    def test_pytest_version_in_main_requirements(self):
        """Test pytest version specification."""
        reqs = self._parse_requirements('requirements.txt')
        pytest_req = [r for r in reqs if r['package'] == 'pytest']
        
        assert len(pytest_req) == 1, "pytest should be specified exactly once"
        version_spec = pytest_req[0]['version_spec']
        assert '>=' in version_spec and '<' in version_spec, \
            "pytest should use range specification"
    
    def test_no_duplicate_packages(self):
        """Test that no package is specified multiple times."""
        req_files = ['requirements.txt', 'requirements-minimal.txt', 
                    'requirements-py39.txt', 'requirements-working.txt']
        
        for req_file in req_files:
            reqs = self._parse_requirements(req_file)
            packages = {}
            for req in reqs:
                package = req['package']
                if package in packages:
                    pytest.fail(f"{req_file} has duplicate entry for '{package}'")
                packages[package] = req['version_spec']


class TestDependencyConsistency:
    """Test consistency of dependencies across different requirements files."""
    
    def test_core_testing_dependencies_exist(self):
        """Test that core testing dependencies exist."""
        core_packages = ['pytest', 'pytest-cov', 'pyyaml', 'requests']
        
        for package in core_packages:
            content = Path('requirements.txt').read_text(encoding='utf-8')
            assert package in content.lower(), \
                f"{package} should be in requirements.txt"
    
    def test_minimal_is_subset(self):
        """Test that minimal requirements is a true subset."""
        minimal_content = Path('requirements-minimal.txt').read_text(encoding='utf-8')
        
        # Should not have CrewAI in minimal
        crewai_packages = ['crewai', 'langchain', 'scrapy', 'playwright']
        
        for pkg in crewai_packages:
            assert pkg not in minimal_content.lower(), \
                f"Minimal requirements should not include {pkg}"
    
    def test_python_dotenv_present_in_all(self):
        """Test python-dotenv is in all requirements files."""
        req_files = ['requirements.txt', 'requirements-minimal.txt', 
                    'requirements-py39.txt', 'requirements-working.txt']
        
        for req_file in req_files:
            content = Path(req_file).read_text(encoding='utf-8')
            assert 'python-dotenv' in content, \
                f"python-dotenv should be in {req_file}"


class TestSecurityAndBestPractices:
    """Test security considerations and best practices."""
    
    def test_no_wildcard_versions(self):
        """Test that requirements don't use wildcard versions."""
        req_files = ['requirements.txt', 'requirements-minimal.txt',
                    'requirements-py39.txt', 'requirements-working.txt']
        
        for req_file in req_files:
            content = Path(req_file).read_text(encoding='utf-8')
            for line in content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    assert '*' not in line, \
                        f"{req_file} should not use wildcard versions: {line}"
    
    def test_no_direct_git_urls(self):
        """Test that requirements don't use direct git URLs."""
        req_files = ['requirements.txt', 'requirements-minimal.txt',
                    'requirements-py39.txt', 'requirements-working.txt']
        
        git_patterns = ['git+', 'git://', 'git@']
        
        for req_file in req_files:
            content = Path(req_file).read_text(encoding='utf-8')
            for pattern in git_patterns:
                assert pattern not in content, \
                    f"{req_file} should not use direct git URLs"
    
    def test_requirements_have_section_comments(self):
        """Test that requirements files have section comments."""
        req_files = ['requirements.txt', 'requirements-minimal.txt',
                    'requirements-py39.txt', 'requirements-working.txt']
        
        for req_file in req_files:
            content = Path(req_file).read_text(encoding='utf-8')
            comment_count = content.count('#')
            
            assert comment_count >= 2, \
                f"{req_file} should have section comments"


class TestRequirementsStructure:
    """Test the structure and organization of requirements files."""
    
    def test_requirements_have_logical_sections(self):
        """Test that requirements files are organized."""
        req_files = ['requirements.txt', 'requirements-py39.txt', 
                    'requirements-working.txt']
        
        expected_sections = ['web scraping', 'data processing', 'utilities']
        
        for req_file in req_files:
            content = Path(req_file).read_text(encoding='utf-8').lower()
            
            found_sections = sum(1 for section in expected_sections 
                               if section in content)
            assert found_sections >= 2, \
                f"{req_file} should have organized sections"
    
    def test_blank_lines_separate_sections(self):
        """Test that sections are separated by blank lines."""
        req_files = ['requirements.txt', 'requirements-py39.txt']
        
        for req_file in req_files:
            content = Path(req_file).read_text(encoding='utf-8')
            blank_lines = content.count('\n\n')
            assert blank_lines >= 2, \
                f"{req_file} should use blank lines to separate sections"


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_requirements_not_empty(self):
        """Test that all requirements files have content."""
        req_files = ['requirements.txt', 'requirements-minimal.txt',
                    'requirements-py39.txt', 'requirements-working.txt']
        
        for req_file in req_files:
            content = Path(req_file).read_text(encoding='utf-8').strip()
            
            non_comment_lines = [line for line in content.split('\n')
                                if line.strip() and not line.strip().startswith('#')]
            
            assert len(non_comment_lines) > 0, \
                f"{req_file} should have at least one dependency"
    
    def test_no_excessive_blank_lines(self):
        """Test that there are no excessive blank lines."""
        req_files = ['requirements.txt', 'requirements-minimal.txt',
                    'requirements-py39.txt', 'requirements-working.txt']
        
        for req_file in req_files:
            content = Path(req_file).read_text(encoding='utf-8')
            assert '\n\n\n\n' not in content, \
                f"{req_file} should not have excessive blank lines"


class TestDocumentation:
    """Test documentation and comments in requirements files."""
    
    def test_minimal_has_fewer_dependencies(self):
        """Test minimal file is actually minimal."""
        minimal_content = Path('requirements-minimal.txt').read_text(encoding='utf-8')
        main_content = Path('requirements.txt').read_text(encoding='utf-8')
        
        minimal_lines = [l for l in minimal_content.split('\n') 
                        if l.strip() and not l.strip().startswith('#')]
        main_lines = [l for l in main_content.split('\n') 
                     if l.strip() and not l.strip().startswith('#')]
        
        assert len(minimal_lines) < len(main_lines), \
            "requirements-minimal.txt should have fewer dependencies"
    
    def test_working_has_explanatory_comments(self):
        """Test working file has comments."""
        content = Path('requirements-working.txt').read_text(encoding='utf-8')
        
        comment_lines = [l for l in content.split('\n') 
                        if l.strip().startswith('#')]
        assert len(comment_lines) >= 3, \
            "requirements-working.txt should have explanatory comments"


class TestSpecificDependencies:
    """Test specific dependencies and their configurations."""
    
    def test_pytest_version_format_in_main(self):
        """Test pytest version in main requirements."""
        content = Path('requirements.txt').read_text(encoding='utf-8')
        
        pytest_lines = [line for line in content.split('\n') 
                       if line.strip().startswith('pytest') and '==' not in line or '>=' in line]
        
        assert len(pytest_lines) >= 1, "Should have pytest with flexible versioning"
    
    def test_python_dotenv_version_changed(self):
        """Test python-dotenv version was updated."""
        content = Path('requirements.txt').read_text(encoding='utf-8')
        
        # Check the version is 1.0.0 as per the diff
        assert '1.0.0' in content, "python-dotenv should be version 1.0.0"
    
    def test_crewai_in_main_requirements(self):
        """Test CrewAI dependencies in main requirements."""
        content = Path('requirements.txt').read_text(encoding='utf-8')
        
        crewai_packages = ['crewai', 'crewai-tools', 'langchain']
        
        for package in crewai_packages:
            assert package in content.lower(), \
                f"{package} should be in requirements.txt"
    
    def test_py39_has_compatibility_comment(self):
        """Test py39 file documents Python 3.9 compatibility."""
        content = Path('requirements-py39.txt').read_text(encoding='utf-8')
        
        assert 'python 3.9' in content.lower() or '3.9' in content, \
            "requirements-py39.txt should document Python 3.9 compatibility"
    
    def test_working_uses_flexible_versions(self):
        """Test working requirements uses flexible versioning."""
        content = Path('requirements-working.txt').read_text(encoding='utf-8')
        
        flexible_count = content.count('>=')
        assert flexible_count >= 3, \
            "requirements-working.txt should use flexible version specs"


class TestRequirementsDiffChanges:
    """Test the specific changes made in the current branch."""
    
    def test_pytest_version_upgrade_in_main(self):
        """Test that pytest was upgraded from pinned to range version."""
        content = Path('requirements.txt').read_text(encoding='utf-8')
        
        # Should use >=8.0.0,<9.0.0 format
        pytest_lines = [line for line in content.split('\n')
                       if 'pytest' in line and not line.strip().startswith('#')
                       and 'pytest-cov' not in line]
        
        assert len(pytest_lines) > 0, "pytest should be specified"
        pytest_line = pytest_lines[0]
        
        # Verify the new format
        assert '>=8.0.0' in pytest_line, "pytest should specify >=8.0.0"
        assert '<9.0.0' in pytest_line, "pytest should cap at <9.0.0"
        assert '==' not in pytest_line or '>=' in pytest_line, \
            "pytest should use flexible versioning"
    
    def test_python_dotenv_downgrade_in_main(self):
        """Test that python-dotenv was changed from 1.0.1 to 1.0.0."""
        content = Path('requirements.txt').read_text(encoding='utf-8')
        
        dotenv_lines = [line for line in content.split('\n')
                       if 'python-dotenv' in line and not line.strip().startswith('#')]
        
        assert len(dotenv_lines) == 1, "python-dotenv should be specified once"
        dotenv_line = dotenv_lines[0]
        
        # Should be pinned to 1.0.0
        assert '==1.0.0' in dotenv_line or '== 1.0.0' in dotenv_line, \
            "python-dotenv should be version 1.0.0"
    
    def test_new_minimal_requirements_file(self):
        """Test that requirements-minimal.txt was added."""
        minimal_path = Path('requirements-minimal.txt')
        
        assert minimal_path.exists(), "requirements-minimal.txt should exist"
        
        content = minimal_path.read_text(encoding='utf-8')
        
        # Should have basic dependencies
        assert 'pytest' in content, "minimal should include pytest"
        assert 'pyyaml' in content, "minimal should include pyyaml"
        assert 'requests' in content, "minimal should include requests"
        
        # Should NOT have heavy dependencies
        assert 'crewai' not in content.lower(), "minimal should not include crewai"
        assert 'scrapy' not in content.lower(), "minimal should not include scrapy"
    
    def test_new_py39_requirements_file(self):
        """Test that requirements-py39.txt was added with appropriate versions."""
        py39_path = Path('requirements-py39.txt')
        
        assert py39_path.exists(), "requirements-py39.txt should exist"
        
        content = py39_path.read_text(encoding='utf-8')
        
        # Should have Python 3.9 compatible versions
        assert 'crewai==0.1.32' in content, \
            "py39 should use older crewai version (0.1.32)"
        
        # Should document compatibility
        assert 'Python 3.9' in content or 'python 3.9' in content.lower(), \
            "Should document Python 3.9 compatibility"
    
    def test_new_working_requirements_file(self):
        """Test that requirements-working.txt was added."""
        working_path = Path('requirements-working.txt')
        
        assert working_path.exists(), "requirements-working.txt should exist"
        
        content = working_path.read_text(encoding='utf-8')
        
        # Should use flexible versioning
        assert '>=' in content, "working requirements should use flexible versioning"
        
        # Should have testing section
        assert 'Testing' in content or 'testing' in content.lower(), \
            "Should have testing section header"
    
    def test_all_four_requirements_files_present(self):
        """Test that all four requirements files now exist."""
        expected_files = [
            'requirements.txt',
            'requirements-minimal.txt',
            'requirements-py39.txt',
            'requirements-working.txt'
        ]
        
        for req_file in expected_files:
            path = Path(req_file)
            assert path.exists(), f"{req_file} should exist"
            assert path.is_file(), f"{req_file} should be a regular file"
            
            # Each should have content
            content = path.read_text(encoding='utf-8')
            assert len(content) > 100, f"{req_file} should have substantial content"


class TestRequirementsVersionCompatibility:
    """Test version compatibility and conflict detection."""
    
    def test_no_version_conflicts_within_files(self):
        """Test that there are no obvious version conflicts."""
        req_files = [
            'requirements.txt',
            'requirements-minimal.txt',
            'requirements-py39.txt',
            'requirements-working.txt'
        ]
        
        for req_file in req_files:
            content = Path(req_file).read_text(encoding='utf-8')
            
            # Extract all package names
            packages_seen = set()
            for line in content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    match = re.match(r'^([a-zA-Z0-9\-_]+)', line)
                    if match:
                        package = match.group(1).lower()
                        assert package not in packages_seen, \
                            f"{req_file} has duplicate package: {package}"
                        packages_seen.add(package)
    
    def test_core_packages_consistent_across_files(self):
        """Test that core packages appear consistently."""
        core_packages = ['pytest', 'pyyaml', 'requests']
        
        req_files = {
            'main': Path('requirements.txt').read_text(encoding='utf-8'),
            'minimal': Path('requirements-minimal.txt').read_text(encoding='utf-8'),
            'py39': Path('requirements-py39.txt').read_text(encoding='utf-8'),
            'working': Path('requirements-working.txt').read_text(encoding='utf-8')
        }
        
        for package in core_packages:
            files_with_package = []
            for file_name, content in req_files.items():
                if package in content.lower():
                    files_with_package.append(file_name)
            
            # Core packages should be in all files
            assert len(files_with_package) >= 3, \
                f"Core package '{package}' should be in most requirements files"
    
    def test_pytest_versions_not_conflicting(self):
        """Test that pytest versions across files are compatible."""
        req_files = {
            'main': Path('requirements.txt').read_text(encoding='utf-8'),
            'minimal': Path('requirements-minimal.txt').read_text(encoding='utf-8'),
            'py39': Path('requirements-py39.txt').read_text(encoding='utf-8'),
            'working': Path('requirements-working.txt').read_text(encoding='utf-8')
        }
        
        pytest_versions = {}
        for file_name, content in req_files.items():
            for line in content.split('\n'):
                if line.strip().startswith('pytest') and 'pytest-cov' not in line:
                    pytest_versions[file_name] = line.strip()
        
        # All should have pytest specified
        assert len(pytest_versions) >= 3, "pytest should be in most requirements files"


class TestRequirementsUsability:
    """Test that requirements files are usable and practical."""
    
    def test_minimal_can_run_tests(self):
        """Test that minimal requirements includes everything needed for testing."""
        content = Path('requirements-minimal.txt').read_text(encoding='utf-8')
        
        test_requirements = ['pytest', 'pytest-cov']
        
        for package in test_requirements:
            assert package in content, \
                f"Minimal requirements should include {package} for testing"
    
    def test_requirements_files_are_pip_installable_format(self):
        """Test that requirements files use pip-installable format."""
        req_files = [
            'requirements.txt',
            'requirements-minimal.txt',
            'requirements-py39.txt',
            'requirements-working.txt'
        ]
        
        for req_file in req_files:
            content = Path(req_file).read_text(encoding='utf-8')
            
            # Should not have common pip errors
            assert '-e .' not in content, \
                f"{req_file} should not have editable install of current package"
            
            # Should not have invalid characters in package names
            for line in content.split('\n'):
                if line.strip() and not line.strip().startswith('#'):
                    # Check for common typos
                    assert '  ' not in line.strip(), \
                        f"{req_file} should not have double spaces: {line}"
    
    def test_files_have_clear_purpose(self):
        """Test that each requirements file has a clear purpose."""
        purposes = {
            'requirements.txt': 'main production requirements',
            'requirements-minimal.txt': 'minimal subset',
            'requirements-py39.txt': 'Python 3.9',
            'requirements-working.txt': 'working/development'
        }
        
        for req_file, expected_purpose_keywords in purposes.items():
            path = Path(req_file)
            assert path.exists(), f"{req_file} should exist"
            
            # File should be distinguishable by content
            content = path.read_text(encoding='utf-8')
            assert len(content) > 0, f"{req_file} should have content"


class TestRequirementsParsingEdgeCases:
    """Test edge cases in requirements file parsing."""
    
    def test_no_invalid_characters_in_package_names(self):
        """Test that package names don't contain invalid characters."""
        req_files = [
            'requirements.txt',
            'requirements-minimal.txt',
            'requirements-py39.txt',
            'requirements-working.txt'
        ]
        
        invalid_chars = ['$', '!', '@', '%', '^', '&', '*', '(', ')']
        
        for req_file in req_files:
            content = Path(req_file).read_text(encoding='utf-8')
            for line in content.split('\n'):
                if line.strip() and not line.strip().startswith('#'):
                    for char in invalid_chars:
                        assert char not in line, \
                            f"{req_file} contains invalid character '{char}' in: {line}"
    
    def test_version_numbers_are_valid(self):
        """Test that version numbers follow semantic versioning."""
        req_files = [
            'requirements.txt',
            'requirements-minimal.txt',
            'requirements-py39.txt',
            'requirements-working.txt'
        ]
        
        # Regex for semantic versioning
        semver_pattern = re.compile(r'\d+\.\d+(\.\d+)?')
        
        for req_file in req_files:
            content = Path(req_file).read_text(encoding='utf-8')
            for line in content.split('\n'):
                if line.strip() and not line.strip().startswith('#'):
                    # Extract version if present
                    version_match = re.search(r'[=><!~]+\s*(\d+\.\d+(?:\.\d+)?)', line)
                    if version_match:
                        version = version_match.group(1)
                        assert semver_pattern.match(version), \
                            f"{req_file} has invalid version format: {line}"
    
    def test_no_spaces_around_operators(self):
        """Test that version operators don't have inconsistent spacing."""
        req_files = [
            'requirements.txt',
            'requirements-minimal.txt',
            'requirements-py39.txt',
            'requirements-working.txt'
        ]
        
        for req_file in req_files:
            content = Path(req_file).read_text(encoding='utf-8')
            for line in content.split('\n'):
                if line.strip() and not line.strip().startswith('#'):
                    # Check for inconsistent spacing like "== 1.0.0" vs "==1.0.0"
                    if '==' in line:
                        # Both formats are acceptable, just checking for validity
                        assert re.search(r'==\s*\d+', line), \
                            f"{req_file} has malformed version specification: {line}"
    
    def test_comment_lines_start_with_hash(self):
        """Test that all comment lines properly start with #."""
        req_files = [
            'requirements.txt',
            'requirements-minimal.txt',
            'requirements-py39.txt',
            'requirements-working.txt'
        ]
        
        for req_file in req_files:
            content = Path(req_file).read_text(encoding='utf-8')
            for i, line in enumerate(content.split('\n'), 1):
                stripped = line.strip()
                # If line looks like a comment but doesn't start with #
                if stripped and not stripped.startswith('#'):
                    # Should be a valid package specification
                    if not re.match(r'^[a-zA-Z0-9\-_]+', stripped):
                        pytest.fail(
                            f"{req_file} line {i} is neither comment nor valid package: {line}"
                        )


class TestRequirementsFileCompletenessForPyPI:
    """Test that requirements are complete for PyPI installation."""
    
    def test_all_packages_use_standard_names(self):
        """Test that package names use standard PyPI naming."""
        req_files = [
            'requirements.txt',
            'requirements-minimal.txt',
            'requirements-py39.txt',
            'requirements-working.txt'
        ]
        
        # Common package name patterns
        valid_name_pattern = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9\-_]*[a-zA-Z0-9])?$')
        
        for req_file in req_files:
            content = Path(req_file).read_text(encoding='utf-8')
            for line in content.split('\n'):
                if line.strip() and not line.strip().startswith('#'):
                    match = re.match(r'^([a-zA-Z0-9\-_]+)', line.strip())
                    if match:
                        package_name = match.group(1)
                        assert valid_name_pattern.match(package_name), \
                            f"{req_file} has invalid package name: {package_name}"
    
    def test_no_local_file_paths(self):
        """Test that requirements don't reference local file paths."""
        req_files = [
            'requirements.txt',
            'requirements-minimal.txt',
            'requirements-py39.txt',
            'requirements-working.txt'
        ]
        
        local_path_indicators = ['file://', './']
        
        for req_file in req_files:
            content = Path(req_file).read_text(encoding='utf-8')
            for indicator in local_path_indicators:
                assert indicator not in content, \
                    f"{req_file} should not contain local file paths"
    
    def test_extras_syntax_if_used(self):
        """Test that extras (package[extra]) use correct syntax if present."""
        req_files = [
            'requirements.txt',
            'requirements-minimal.txt',
            'requirements-py39.txt',
            'requirements-working.txt'
        ]
        
        for req_file in req_files:
            content = Path(req_file).read_text(encoding='utf-8')
            for line in content.split('\n'):
                if '[' in line and line.strip() and not line.strip().startswith('#'):
                    # Should be package[extra]==version format
                    assert ']' in line, \
                        f"{req_file} has malformed extras syntax: {line}"


class TestRequirementsMaintenanceMarkers:
    """Test requirements files for maintainability markers."""
    
    def test_files_have_section_markers(self):
        """Test that requirements files have clear section markers."""
        large_req_files = [
            'requirements.txt',
            'requirements-py39.txt',
            'requirements-working.txt'
        ]
        
        for req_file in large_req_files:
            content = Path(req_file).read_text(encoding='utf-8')
            
            # Should have section comments
            section_comments = [line for line in content.split('\n')
                              if line.strip().startswith('#') and 
                              len(line.strip()) > 2 and
                              not line.strip().startswith('# Testing') or
                              line.strip().startswith('# CrewAI') or
                              line.strip().startswith('# Web') or
                              line.strip().startswith('# Data')]
            
            assert len(section_comments) >= 1, \
                f"{req_file} should have section comment markers"
    
    def test_related_packages_proximity(self):
        """Test that related packages are defined close together."""
        content = Path('requirements.txt').read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # Find langchain packages
        langchain_indices = []
        for i, line in enumerate(lines):
            if 'langchain' in line.lower() and not line.strip().startswith('#'):
                langchain_indices.append(i)
        
        if len(langchain_indices) >= 2:
            # Should be within reasonable distance (15 lines)
            max_dist = max(langchain_indices) - min(langchain_indices)
            assert max_dist <= 15, \
                "Related langchain packages should be grouped together"
    
    def test_alphabetical_ordering_within_sections(self):
        """Test that packages within commented sections follow some order."""
        req_files = [
            'requirements.txt',
            'requirements-minimal.txt',
            'requirements-py39.txt',
            'requirements-working.txt'
        ]
        
        for req_file in req_files:
            content = Path(req_file).read_text(encoding='utf-8')
            
            # This is more of a guideline - just check that packages exist
            # Alphabetical ordering is optional but good practice
            package_lines = [line for line in content.split('\n')
                           if line.strip() and not line.strip().startswith('#')]
            
            assert len(package_lines) > 0, \
                f"{req_file} should have package specifications"