"""
Comprehensive tests for validating Python requirements files.

This test suite validates all requirements files for:
- Proper format and syntax
- Version specifier validity
- Package name conventions
- Consistency across different requirement files
- Security best practices
- Dependency compatibility
"""
import re
import pytest
from pathlib import Path
from typing import List, Tuple, Dict


class TestRequirementsFileStructure:
    """Test the structure and format of requirements files."""
    
    @pytest.fixture
    def requirements_files(self):
        """Provide all requirements file paths."""
        return {
            'main': Path('requirements.txt'),
            'minimal': Path('requirements-minimal.txt'),
            'py39': Path('requirements-py39.txt'),
            'working': Path('requirements-working.txt'),
        }
    
    def test_all_requirements_files_exist(self, requirements_files):
        """Test that all requirements files exist."""
        for name, path in requirements_files.items():
            assert path.exists(), f"Requirements file '{name}' not found: {path}"
    
    def test_requirements_files_not_empty(self, requirements_files):
        """Test that requirements files are not empty."""
        for name, path in requirements_files.items():
            content = path.read_text(encoding='utf-8').strip()
            assert len(content) > 0, f"Requirements file '{name}' is empty"
    
    def test_requirements_files_utf8_encoded(self, requirements_files):
        """Test that requirements files use UTF-8 encoding."""
        for name, path in requirements_files.items():
            try:
                path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                pytest.fail(f"Requirements file '{name}' is not valid UTF-8")
    
    def test_requirements_files_end_with_newline(self, requirements_files):
        """Test that requirements files end with newline."""
        for name, path in requirements_files.items():
            content = path.read_text(encoding='utf-8')
            assert content.endswith('\n'), f"Requirements file '{name}' should end with newline"
    
    def test_no_duplicate_packages(self, requirements_files):
        """Test that no package is listed multiple times in each file."""
        for name, path in requirements_files.items():
            content = path.read_text(encoding='utf-8')
            packages = []
            
            for line in content.split('\n'):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Extract package name
                match = re.match(r'^([a-zA-Z0-9\-_\.]+)', line)
                if match:
                    packages.append(match.group(1).lower())
            
            duplicates = [pkg for pkg in packages if packages.count(pkg) > 1]
            unique_dups = list(set(duplicates))
            
            assert len(unique_dups) == 0, \
                f"Duplicate packages in {name}: {unique_dups}"
    
    def test_no_trailing_whitespace(self, requirements_files):
        """Test that lines don't have trailing whitespace."""
        for name, path in requirements_files.items():
            content = path.read_text(encoding='utf-8')
            lines_with_trailing = []
            
            for i, line in enumerate(content.split('\n'), 1):
                if line and line != line.rstrip():
                    lines_with_trailing.append(i)
            
            assert len(lines_with_trailing) == 0, \
                f"Lines with trailing whitespace in {name}: {lines_with_trailing[:5]}"
    
    def test_consistent_line_endings(self, requirements_files):
        """Test that files use Unix line endings (LF)."""
        for name, path in requirements_files.items():
            content = path.read_bytes()
            assert b'\r\n' not in content, \
                f"File uses Windows line endings (CRLF): {name}"


class TestPackageNameConventions:
    """Test package naming conventions."""
    
    def test_package_names_valid_format(self):
        """Test that package names follow valid format."""
        files = [
            Path('requirements.txt'),
            Path('requirements-minimal.txt'),
            Path('requirements-py39.txt'),
            Path('requirements-working.txt')
        ]
        
        valid_pattern = re.compile(r'^[a-zA-Z0-9\-_\.]+$')
        
        for file_path in files:
            content = file_path.read_text(encoding='utf-8')
            
            for line_num, line in enumerate(content.split('\n'), 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Extract package name
                match = re.match(r'^([a-zA-Z0-9\-_\.]+)', line)
                if match:
                    pkg_name = match.group(1)
                    assert valid_pattern.match(pkg_name), \
                        f"Invalid package name in {file_path.name} line {line_num}: {pkg_name}"


class TestVersionSpecifiers:
    """Test version specifier validity and best practices."""
    
    def test_version_specifiers_are_valid(self):
        """Test that version specifiers follow PEP 440."""
        files = [
            Path('requirements.txt'),
            Path('requirements-minimal.txt'),
            Path('requirements-py39.txt'),
            Path('requirements-working.txt')
        ]
        
        valid_operators = ['==', '>=', '<=', '>', '<', '!=', '~=', '===']
        
        for file_path in files:
            content = file_path.read_text(encoding='utf-8')
            
            for line in content.split('\n'):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Check for version operators
                match = re.match(r'^[a-zA-Z0-9\-_\.]+\s*([=<>!~]+)', line)
                if match:
                    operator = match.group(1)
                    assert operator in valid_operators, \
                        f"Invalid version operator '{operator}' in {file_path.name}: {line}"
    
    def test_versions_follow_semver_pattern(self):
        """Test that version numbers follow semantic versioning."""
        files = [
            Path('requirements.txt'),
            Path('requirements-minimal.txt'),
            Path('requirements-py39.txt'),
            Path('requirements-working.txt')
        ]
        
        # Pattern for semantic versioning
        semver_pattern = re.compile(r'^\d+\.\d+(\.\d+)?')
        
        for file_path in files:
            content = file_path.read_text(encoding='utf-8')
            
            for line in content.split('\n'):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Extract version
                match = re.match(r'^[a-zA-Z0-9\-_\.]+\s*[=<>!~]+\s*(.+)$', line)
                if match:
                    version_spec = match.group(1).strip()
                    
                    # Handle compound specifiers (e.g., >=8.0.0,<9.0.0)
                    for v_part in version_spec.split(','):
                        # Remove operators to get clean version
                        clean_version = re.sub(r'^[<>=!~]+', '', v_part).strip()
                        
                        if clean_version:
                            assert semver_pattern.match(clean_version), \
                                f"Version '{clean_version}' doesn't follow semver in {file_path.name}"
    
    def test_no_wildcard_versions(self):
        """Test that no wildcard versions are used."""
        files = [
            Path('requirements.txt'),
            Path('requirements-minimal.txt'),
            Path('requirements-py39.txt'),
            Path('requirements-working.txt')
        ]
        
        for file_path in files:
            content = file_path.read_text(encoding='utf-8')
            
            for line in content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    assert '*' not in line, \
                        f"Wildcard version found in {file_path.name}: {line}"
    
    def test_pytest_version_updated_in_main(self):
        """Test that main requirements.txt has updated pytest version."""
        content = Path('requirements.txt').read_text(encoding='utf-8')
        
        pytest_lines = [l for l in content.split('\n') if 'pytest' in l and not l.strip().startswith('#')]
        
        assert any('pytest>=' in l for l in pytest_lines), \
            "requirements.txt should use >= for pytest"
        assert any('8.0.0' in l for l in pytest_lines), \
            "requirements.txt should have pytest >= 8.0.0"


class TestRequirementsConsistency:
    """Test consistency across different requirements files."""
    
    def test_core_packages_in_all_files(self):
        """Test that core packages are present in all files."""
        core_packages = {'pytest', 'pytest-cov', 'pyyaml', 'requests'}
        
        files = [
            Path('requirements.txt'),
            Path('requirements-minimal.txt'),
            Path('requirements-py39.txt'),
            Path('requirements-working.txt')
        ]
        
        for file_path in files:
            content = file_path.read_text(encoding='utf-8').lower()
            
            for pkg in core_packages:
                assert pkg in content, \
                    f"Core package '{pkg}' missing from {file_path.name}"
    
    def test_minimal_is_subset_of_main(self):
        """Test that minimal requirements are subset of main."""
        def extract_packages(file_path):
            content = file_path.read_text(encoding='utf-8')
            packages = set()
            for line in content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    match = re.match(r'^([a-zA-Z0-9\-_\.]+)', line)
                    if match:
                        packages.add(match.group(1).lower().replace('_', '-'))
            return packages
        
        main_pkgs = extract_packages(Path('requirements.txt'))
        minimal_pkgs = extract_packages(Path('requirements-minimal.txt'))
        
        # Allow pytest to differ
        minimal_pkgs.discard('pytest')
        main_pkgs.discard('pytest')
        
        missing = minimal_pkgs - main_pkgs
        assert len(missing) == 0, \
            f"Packages in minimal but not in main: {missing}"
    
    def test_py39_has_compatible_versions(self):
        """Test that py39 requirements use older compatible versions."""
        content = Path('requirements-py39.txt').read_text(encoding='utf-8')
        
        # CrewAI should use 0.1.x for Python 3.9
        crewai_lines = [l for l in content.split('\n') if 'crewai==' in l.lower()]
        
        assert len(crewai_lines) > 0, "requirements-py39.txt should have crewai"
        assert any('0.1.' in l for l in crewai_lines), \
            "requirements-py39.txt should use crewai 0.1.x for Python 3.9 compatibility"
    
    def test_working_uses_flexible_versions(self):
        """Test that working requirements use flexible version specifiers."""
        content = Path('requirements-working.txt').read_text(encoding='utf-8')
        
        ge_count = content.count('>=')
        assert ge_count >= 5, \
            f"requirements-working.txt should use >= for flexibility (found {ge_count})"


class TestDependencyGroups:
    """Test that dependencies are properly organized by category."""
    
    def test_dependencies_have_section_comments(self):
        """Test that dependency groups have section comments."""
        # requirements.txt doesn't have a Testing section (pytest is at top)
        files_and_sections = {
            'requirements.txt': ['CrewAI', 'Web Scraping', 'Data Processing', 
                               'API Integrations', 'Environment Management', 'Utilities'],
            'requirements-py39.txt': ['CrewAI', 'Web Scraping', 'Data Processing',
                                     'API Integrations', 'Environment Management', 'Utilities'],
            'requirements-working.txt': ['Testing', 'CrewAI', 'Web Scraping', 'Data Processing',
                                        'API Integrations', 'Environment Management', 'Utilities'],
        }
        
        for file_name, expected_sections in files_and_sections.items():
            content = Path(file_name).read_text(encoding='utf-8')
            
            for section in expected_sections:
                # Look for section in comments
                found = any(section in line for line in content.split('\n') 
                          if line.strip().startswith('#'))
                assert found, f"{file_name} should have '{section}' section comment"
    
    def test_testing_packages_at_top(self):
        """Test that testing packages are at the top of files."""
        for file in ['requirements.txt', 'requirements-minimal.txt']:
            content = Path(file).read_text(encoding='utf-8')
            lines = [l.strip() for l in content.split('\n') 
                    if l.strip() and not l.startswith('#')]
            
            if lines:
                assert 'pytest' in lines[0].lower(), \
                    f"Testing packages should be first in {file}"


class TestSecurityBestPractices:
    """Test security best practices in requirements files."""
    
    def test_no_http_urls(self):
        """Test that no insecure HTTP URLs are used."""
        files = [
            Path('requirements.txt'),
            Path('requirements-minimal.txt'),
            Path('requirements-py39.txt'),
            Path('requirements-working.txt')
        ]
        
        for file_path in files:
            content = file_path.read_text(encoding='utf-8')
            http_urls = re.findall(r'http://[^\s]+', content)
            assert len(http_urls) == 0, \
                f"Found insecure HTTP URLs in {file_path.name}: {http_urls}"
    
    def test_no_hardcoded_credentials(self):
        """Test that no credentials are hardcoded."""
        files = [
            Path('requirements.txt'),
            Path('requirements-minimal.txt'),
            Path('requirements-py39.txt'),
            Path('requirements-working.txt')
        ]
        
        suspicious_patterns = ['password=', 'token=', 'api_key=', 'secret=']
        
        for file_path in files:
            content = file_path.read_text(encoding='utf-8').lower()
            
            found = [p for p in suspicious_patterns if p in content]
            assert len(found) == 0, \
                f"Potential hardcoded credentials in {file_path.name}: {found}"


class TestKnownVulnerablePackages:
    """Test for known vulnerable package versions."""
    
    def test_requests_version_not_vulnerable(self):
        """Test that requests version is not vulnerable."""
        files = [
            Path('requirements.txt'),
            Path('requirements-minimal.txt'),
            Path('requirements-py39.txt'),
            Path('requirements-working.txt')
        ]
        
        for file_path in files:
            content = file_path.read_text(encoding='utf-8')
            
            requests_lines = [l for l in content.split('\n') 
                            if 'requests==' in l.lower() and not l.strip().startswith('#')]
            
            if requests_lines:
                version_match = re.search(r'(\d+)\.(\d+)', requests_lines[0])
                if version_match:
                    major, minor = map(int, version_match.groups())
                    assert (major, minor) >= (2, 31), \
                        f"requests version in {file_path.name} has known vulnerabilities, use >= 2.31.0"


class TestPythonDotenvVersion:
    """Test the specific python-dotenv version changes."""
    
    def test_main_requirements_has_correct_version(self):
        """Test that main requirements.txt has python-dotenv==1.0.0."""
        content = Path('requirements.txt').read_text(encoding='utf-8')
        
        dotenv_lines = [l for l in content.split('\n')
                       if 'python-dotenv' in l and not l.strip().startswith('#')]
        
        assert len(dotenv_lines) > 0, "python-dotenv should be in requirements.txt"
        assert '1.0.0' in dotenv_lines[0], \
            "requirements.txt should have python-dotenv==1.0.0"
    
    def test_other_requirements_have_correct_version(self):
        """Test that other requirements files have python-dotenv==1.0.1."""
        files = ['requirements-minimal.txt', 'requirements-py39.txt', 'requirements-working.txt']
        
        for file_name in files:
            content = Path(file_name).read_text(encoding='utf-8')
            dotenv_lines = [l for l in content.split('\n')
                           if 'python-dotenv' in l and not l.strip().startswith('#')]
            
            assert len(dotenv_lines) > 0, f"python-dotenv should be in {file_name}"
            assert '1.0.1' in dotenv_lines[0], \
                f"{file_name} should have python-dotenv==1.0.1"


class TestFileSpecificRequirements:
    """Test file-specific requirements and their purposes."""
    
    def test_minimal_has_fewer_packages(self):
        """Test that minimal file has fewer packages than main."""
        def count_packages(file_path):
            content = file_path.read_text(encoding='utf-8')
            return len([l for l in content.split('\n')
                       if l.strip() and not l.strip().startswith('#')])
        
        main_count = count_packages(Path('requirements.txt'))
        minimal_count = count_packages(Path('requirements-minimal.txt'))
        
        assert minimal_count < main_count, \
            "requirements-minimal.txt should have fewer packages than requirements.txt"
    
    def test_minimal_excludes_heavy_dependencies(self):
        """Test that minimal requirements exclude AI/ML dependencies."""
        content = Path('requirements-minimal.txt').read_text(encoding='utf-8').lower()
        
        assert 'crewai' not in content, \
            "Minimal requirements should not include crewai"
        assert 'langchain' not in content, \
            "Minimal requirements should not include langchain"
    
    def test_py39_documents_compatibility(self):
        """Test that py39 file documents Python 3.9 compatibility."""
        content = Path('requirements-py39.txt').read_text(encoding='utf-8')
        
        assert '3.9' in content or 'py39' in content.lower(), \
            "requirements-py39.txt should document Python 3.9 compatibility"
    
    def test_main_requirements_uses_recent_pytest(self):
        """Test that main requirements.txt uses recent pytest version."""
        content = Path('requirements.txt').read_text(encoding='utf-8')
        
        pytest_lines = [l for l in content.split('\n') if 'pytest' in l.lower()]
        
        # Should use version 8.x or higher
        has_recent = any('8.' in l or '>=8' in l for l in pytest_lines)
        assert has_recent, \
            "requirements.txt should use recent pytest (8.x)"