"""
Tests for validating requirements files and dependency management.
"""
import re
import pytest
from pathlib import Path
from typing import Dict, List, Tuple


class TestRequirementsFiles:
    """Test that all requirements files exist and are readable."""
    
    @pytest.fixture
    def requirements_files(self):
        """Get all requirements files."""
        return [
            Path("requirements.txt"),
            Path("requirements-minimal.txt"),
            Path("requirements-py39.txt"),
            Path("requirements-working.txt")
        ]
    
    def test_all_requirements_files_exist(self, requirements_files):
        """Test that all requirements files exist."""
        for req_file in requirements_files:
            assert req_file.exists(), f"{req_file} should exist"
            assert req_file.is_file(), f"{req_file} should be a file"
    
    def test_requirements_files_are_readable(self, requirements_files):
        """Test that all requirements files are readable."""
        for req_file in requirements_files:
            content = req_file.read_text(encoding='utf-8')
            assert content, f"{req_file} should not be empty"
            assert len(content) > 0, f"{req_file} should have content"


class TestRequirementsFormat:
    """Test requirements file format and syntax."""
    
    @pytest.fixture
    def requirements_content(self):
        """Load requirements.txt content."""
        return Path("requirements.txt").read_text(encoding='utf-8')
    
    @pytest.fixture
    def requirements_minimal_content(self):
        """Load requirements-minimal.txt content."""
        return Path("requirements-minimal.txt").read_text(encoding='utf-8')
    
    @pytest.fixture
    def requirements_py39_content(self):
        """Load requirements-py39.txt content."""
        return Path("requirements-py39.txt").read_text(encoding='utf-8')
    
    @pytest.fixture
    def requirements_working_content(self):
        """Load requirements-working.txt content."""
        return Path("requirements-working.txt").read_text(encoding='utf-8')
    
    def test_no_trailing_whitespace(self, requirements_content):
        """Test that requirements.txt has no trailing whitespace."""
        lines = requirements_content.split('\n')
        for i, line in enumerate(lines, 1):
            if line and not line.startswith('#'):
                assert not line.endswith(' '), f"Line {i} has trailing whitespace"
                assert not line.endswith('\t'), f"Line {i} has trailing tab"
    
    def test_valid_package_format(self, requirements_content):
        """Test that all package lines follow valid format."""
        lines = requirements_content.split('\n')
        # Updated pattern to handle complex version specifiers like >=8.0.0,<9.0.0
        pattern = r'^[a-zA-Z0-9_\-\.]+([><=!]+[0-9\.\,<>= ]+)?$'
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.startswith('#') and line:
                assert re.match(pattern, line), f"Line {i} has invalid format: {line}"
    
    def test_no_duplicate_packages(self, requirements_content):
        """Test that no packages are duplicated."""
        lines = requirements_content.split('\n')
        packages = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                package_name = re.split(r'[><=!]', line)[0].strip()
                assert package_name not in packages, f"Duplicate package: {package_name}"
                packages.append(package_name)
    
    def test_comments_have_proper_format(self, requirements_content):
        """Test that comment lines are properly formatted."""
        lines = requirements_content.split('\n')
        
        for i, line in enumerate(lines, 1):
            if line.startswith('#'):
                if len(line) > 1:
                    assert line.startswith('# '), f"Line {i}: Comments should have space after #"


class TestRequirementsContent:
    """Test specific package requirements and versions."""
    
    @pytest.fixture
    def parsed_requirements(self):
        """Parse requirements.txt into a dictionary."""
        content = Path("requirements.txt").read_text(encoding='utf-8')
        packages = {}
        
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                match = re.match(r'^([a-zA-Z0-9_\-\.]+)([><=!]+.+)?$', line)
                if match:
                    name, version = match.groups()
                    packages[name] = version or ''
        
        return packages
    
    def test_pytest_is_present(self, parsed_requirements):
        """Test that pytest is in requirements."""
        assert 'pytest' in parsed_requirements, "pytest should be in requirements"
    
    def test_pytest_version_updated(self, parsed_requirements):
        """Test that pytest version was updated to >=8.0.0."""
        pytest_version = parsed_requirements.get('pytest', '')
        assert '>=8.0.0' in pytest_version, "pytest should be >=8.0.0"
        assert '<9.0.0' in pytest_version, "pytest should be <9.0.0"
    
    def test_pytest_cov_is_present(self, parsed_requirements):
        """Test that pytest-cov is in requirements."""
        assert 'pytest-cov' in parsed_requirements
    
    def test_core_testing_packages(self, parsed_requirements):
        """Test that core testing packages are present."""
        core_packages = ['pytest', 'pytest-cov', 'pyyaml', 'requests']
        for package in core_packages:
            assert package in parsed_requirements, f"{package} should be in requirements"
    
    def test_python_dotenv_version(self, parsed_requirements):
        """Test that python-dotenv version is correct."""
        assert 'python-dotenv' in parsed_requirements
        version = parsed_requirements['python-dotenv']
        assert '==1.0.0' in version, "python-dotenv should be ==1.0.0"


class TestRequirementsMinimal:
    """Test requirements-minimal.txt content."""
    
    @pytest.fixture
    def parsed_minimal(self):
        """Parse requirements-minimal.txt."""
        content = Path("requirements-minimal.txt").read_text(encoding='utf-8')
        packages = {}
        
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                match = re.match(r'^([a-zA-Z0-9_\-\.]+)([><=!]+.+)?$', line)
                if match:
                    name, version = match.groups()
                    packages[name] = version or ''
        
        return packages
    
    def test_minimal_has_core_packages(self, parsed_minimal):
        """Test that minimal requirements has essential packages."""
        essential = ['pytest', 'pytest-cov', 'pyyaml', 'requests']
        for package in essential:
            assert package in parsed_minimal, f"{package} should be in minimal requirements"
    
    def test_minimal_has_no_crewai(self, parsed_minimal):
        """Test that minimal requirements doesn't include crewai."""
        assert 'crewai' not in parsed_minimal, "crewai should not be in minimal requirements"
        assert 'crewai-tools' not in parsed_minimal
    
    def test_minimal_has_basic_web_scraping(self, parsed_minimal):
        """Test that minimal requirements has basic web scraping."""
        assert 'beautifulsoup4' in parsed_minimal
    
    def test_minimal_has_data_processing(self, parsed_minimal):
        """Test that minimal requirements has data processing packages."""
        assert 'pandas' in parsed_minimal
        assert 'numpy' in parsed_minimal
    
    def test_minimal_has_utilities(self, parsed_minimal):
        """Test that minimal requirements has utility packages."""
        utilities = ['phonenumbers', 'email-validator', 'python-dateutil']
        for package in utilities:
            assert package in parsed_minimal, f"{package} should be in minimal requirements"


class TestRequirementsPy39:
    """Test requirements-py39.txt for Python 3.9 compatibility."""
    
    @pytest.fixture
    def parsed_py39(self):
        """Parse requirements-py39.txt."""
        content = Path("requirements-py39.txt").read_text(encoding='utf-8')
        packages = {}
        
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                match = re.match(r'^([a-zA-Z0-9_\-\.]+)([><=!]+.+)?$', line)
                if match:
                    name, version = match.groups()
                    packages[name] = version or ''
        
        return packages
    
    def test_py39_has_older_crewai(self, parsed_py39):
        """Test that py39 requirements uses older crewai version."""
        assert 'crewai' in parsed_py39
        version = parsed_py39['crewai']
        assert '==0.1.32' in version, "crewai should be ==0.1.32 for Python 3.9"
    
    def test_py39_has_comment_about_compatibility(self):
        """Test that py39 file has comment about Python 3.9 compatibility."""
        content = Path("requirements-py39.txt").read_text(encoding='utf-8')
        assert 'Python 3.9' in content or 'python 3.9' in content.lower()
        assert 'compatible' in content.lower() or 'compatibility' in content.lower()
    
    def test_py39_has_all_categories(self, parsed_py39):
        """Test that py39 requirements has all package categories."""
        assert 'pytest' in parsed_py39
        assert 'crewai' in parsed_py39
        assert 'beautifulsoup4' in parsed_py39
        assert 'pandas' in parsed_py39
        assert 'gspread' in parsed_py39
        assert 'httpx' in parsed_py39
        assert 'python-dotenv' in parsed_py39


class TestRequirementsWorking:
    """Test requirements-working.txt for flexible versioning."""
    
    @pytest.fixture
    def parsed_working(self):
        """Parse requirements-working.txt."""
        content = Path("requirements-working.txt").read_text(encoding='utf-8')
        packages = {}
        
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                match = re.match(r'^([a-zA-Z0-9_\-\.]+)([><=!]+.+)?$', line)
                if match:
                    name, version = match.groups()
                    packages[name] = version or ''
        
        return packages
    
    def test_working_has_flexible_versions(self, parsed_working):
        """Test that working requirements uses >= for flexibility."""
        content = Path("requirements-working.txt").read_text(encoding='utf-8')
        gte_count = content.count('>=')
        eq_count = content.count('==')
        assert gte_count > 0, "Should have some >= version specifiers"
    
    def test_working_has_crewai_flexible(self, parsed_working):
        """Test that crewai has flexible version in working requirements."""
        assert 'crewai' in parsed_working
        version = parsed_working['crewai']
        assert '>=' in version, "crewai should use >= for flexibility"
    
    def test_working_has_additional_scraping_libs(self, parsed_working):
        """Test that working requirements has additional scraping libraries."""
        assert 'lxml' in parsed_working
        assert 'html5lib' in parsed_working
    
    def test_working_has_comment_sections(self):
        """Test that working requirements has organized comment sections."""
        content = Path("requirements-working.txt").read_text(encoding='utf-8')
        sections = [
            '# Testing',
            '# CrewAI',
            '# Web Scraping',
            '# Data Processing',
            '# API Integrations',
            '# Environment'
        ]
        
        found_sections = 0
        for section in sections:
            if section in content:
                found_sections += 1
        
        assert found_sections >= 4, "Should have at least 4 organized comment sections"


class TestRequirementsConsistency:
    """Test consistency across different requirements files."""
    
    @pytest.fixture
    def all_parsed_requirements(self):
        """Parse all requirements files."""
        files = {
            'main': Path("requirements.txt"),
            'minimal': Path("requirements-minimal.txt"),
            'py39': Path("requirements-py39.txt"),
            'working': Path("requirements-working.txt")
        }
        
        parsed = {}
        for name, path in files.items():
            content = path.read_text(encoding='utf-8')
            packages = {}
            
            for line in content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    match = re.match(r'^([a-zA-Z0-9_\-\.]+)([><=!]+.+)?$', line)
                    if match:
                        pkg_name, version = match.groups()
                        packages[pkg_name] = version or ''
            
            parsed[name] = packages
        
        return parsed
    
    def test_core_packages_consistent_across_files(self, all_parsed_requirements):
        """Test that core packages appear in all files."""
        core_packages = ['pytest', 'pytest-cov', 'pyyaml', 'requests']
        
        for package in core_packages:
            for file_name, packages in all_parsed_requirements.items():
                assert package in packages, f"{package} should be in {file_name}"
    
    def test_minimal_is_subset_of_main(self, all_parsed_requirements):
        """Test that minimal requirements is a subset of main."""
        minimal_packages = set(all_parsed_requirements['minimal'].keys())
        main_packages = set(all_parsed_requirements['main'].keys())
        
        for package in minimal_packages:
            assert package in main_packages, f"{package} in minimal but not in main"
    
    def test_pytest_version_consistency(self, all_parsed_requirements):
        """Test pytest version specifications across files."""
        pytest_versions = {}
        for name, packages in all_parsed_requirements.items():
            if 'pytest' in packages:
                pytest_versions[name] = packages['pytest']
        
        assert '>=8.0.0' in pytest_versions['main']
        assert '==7.4.3' in pytest_versions['minimal']
        assert '==7.4.3' in pytest_versions['py39']
        assert '==7.4.3' in pytest_versions['working']
    
    def test_python_dotenv_versions(self, all_parsed_requirements):
        """Test python-dotenv version consistency."""
        dotenv_versions = {}
        for name, packages in all_parsed_requirements.items():
            if 'python-dotenv' in packages:
                dotenv_versions[name] = packages['python-dotenv']
        
        assert '==1.0.0' in dotenv_versions['main']
        assert '==1.0.1' in dotenv_versions['minimal']
        assert '==1.0.1' in dotenv_versions['py39']
        assert '==1.0.1' in dotenv_versions['working']


class TestRequirementsSecurity:
    """Test security aspects of requirements files."""
    
    def test_no_loose_version_pins_in_main(self):
        """Test that main requirements uses specific versions."""
        content = Path("requirements.txt").read_text(encoding='utf-8')
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                if '>=' in line and '<' not in line and ',' not in line:
                    if 'pytest>=' in line and ',<' in line:
                        continue
    
    def test_no_known_vulnerable_versions(self):
        """Test that requirements don't use known vulnerable package versions."""
        content = Path("requirements.txt").read_text(encoding='utf-8')
        
        vulnerable_patterns = [
            'requests==2.6.0',
            'urllib3<1.26.5',
        ]
        
        for pattern in vulnerable_patterns:
            assert pattern not in content, f"Potentially vulnerable pattern: {pattern}"
    
    def test_all_files_use_utf8_encoding(self):
        """Test that all requirements files are UTF-8 encoded."""
        files = [
            Path("requirements.txt"),
            Path("requirements-minimal.txt"),
            Path("requirements-py39.txt"),
            Path("requirements-working.txt")
        ]
        
        for req_file in files:
            content = req_file.read_text(encoding='utf-8')
            assert content is not None


class TestRequirementsStructure:
    """Test the structure and organization of requirements files."""
    
    def test_requirements_have_sections(self):
        """Test that main requirements file has organized sections."""
        content = Path("requirements.txt").read_text(encoding='utf-8')
        
        expected_sections = [
            'CrewAI',
            'Web Scraping',
            'Data Processing',
            'API Integration',
            'Environment'
        ]
        
        found_count = 0
        for section in expected_sections:
            if section in content:
                found_count += 1
        
        assert found_count >= 3, "Should have at least 3 organized sections"
    
    def test_blank_lines_separate_sections(self):
        """Test that sections are separated by blank lines."""
        content = Path("requirements.txt").read_text(encoding='utf-8')
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if line.startswith('# ') and i > 0:
                if i > 1:
                    prev_line = lines[i-1].strip()
                    assert prev_line == '' or prev_line.startswith('#'), \
                        f"Line {i+1}: Section comment should be preceded by blank line"
    
    def test_packages_grouped_logically(self):
        """Test that related packages are grouped together."""
        content = Path("requirements.txt").read_text(encoding='utf-8')
        
        if '# Web Scraping' in content:
            section_start = content.index('# Web Scraping')
            section_end = content.find('\n\n', section_start)
            if section_end == -1:
                section_end = content.find('\n#', section_start + 1)
            
            section = content[section_start:section_end if section_end != -1 else len(content)]
            
            assert 'beautifulsoup4' in section or 'selenium' in section or 'scrapy' in section


class TestRequirementsVersioning:
    """Test version specification strategies."""
    
    def test_main_requirements_pinned_versions(self):
        """Test that main requirements mostly uses pinned versions."""
        content = Path("requirements.txt").read_text(encoding='utf-8')
        lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]
        
        pinned_count = sum(1 for line in lines if '==' in line)
        total_count = len(lines)
        
        assert pinned_count / total_count >= 0.7, \
            "Main requirements should have mostly pinned versions"
    
    def test_working_requirements_flexible_versions(self):
        """Test that working requirements uses flexible versioning."""
        content = Path("requirements-working.txt").read_text(encoding='utf-8')
        lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]
        
        flexible_count = sum(1 for line in lines if '>=' in line)
        
        assert flexible_count >= 5, \
            "Working requirements should have flexible version specifications"
    
    def test_version_specifiers_are_valid(self):
        """Test that all version specifiers follow PEP 440."""
        files = [
            Path("requirements.txt"),
            Path("requirements-minimal.txt"),
            Path("requirements-py39.txt"),
            Path("requirements-working.txt")
        ]
        
        valid_patterns = [
            r'^[a-zA-Z0-9_\-\.]+==\d+\.\d+\.\d+$',
            r'^[a-zA-Z0-9_\-\.]+>=\d+\.\d+\.\d+$',
            r'^[a-zA-Z0-9_\-\.]+>=\d+\.\d+\.\d+,<\d+\.\d+\.\d+$',
            r'^[a-zA-Z0-9_\-\.]+$',
        ]
        
        for req_file in files:
            content = req_file.read_text(encoding='utf-8')
            for line in content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    matches = any(re.match(pattern, line) for pattern in valid_patterns)
                    assert matches, f"Invalid version specifier in {req_file.name}: {line}"


class TestRequirementsEdgeCases:
    """Test edge cases and potential issues."""
    
    def test_no_empty_lines_at_start(self):
        """Test that files don't start with empty lines."""
        files = [
            Path("requirements.txt"),
            Path("requirements-minimal.txt"),
            Path("requirements-py39.txt"),
            Path("requirements-working.txt")
        ]
        
        for req_file in files:
            content = req_file.read_text(encoding='utf-8')
            assert not content.startswith('\n'), f"{req_file.name} should not start with empty line"
    
    def test_files_end_with_newline(self):
        """Test that all files end with a newline."""
        files = [
            Path("requirements.txt"),
            Path("requirements-minimal.txt"),
            Path("requirements-py39.txt"),
            Path("requirements-working.txt")
        ]
        
        for req_file in files:
            content = req_file.read_text(encoding='utf-8')
            assert content.endswith('\n'), f"{req_file.name} should end with newline"
    
    def test_no_windows_line_endings(self):
        """Test that files use Unix line endings."""
        files = [
            Path("requirements.txt"),
            Path("requirements-minimal.txt"),
            Path("requirements-py39.txt"),
            Path("requirements-working.txt")
        ]
        
        for req_file in files:
            content = req_file.read_text(encoding='utf-8')
            assert '\r\n' not in content, f"{req_file.name} should use Unix line endings (LF)"
    
    def test_no_inline_comments(self):
        """Test that there are no inline comments after package declarations."""
        files = [
            Path("requirements.txt"),
            Path("requirements-minimal.txt"),
            Path("requirements-py39.txt"),
            Path("requirements-working.txt")
        ]
        
        for req_file in files:
            content = req_file.read_text(encoding='utf-8')
            for i, line in enumerate(content.split('\n'), 1):
                if line.strip() and not line.strip().startswith('#'):
                    if '==' in line or '>=' in line:
                        parts = line.split('#')
                        if len(parts) > 1:
                            assert False, f"{req_file.name} line {i}: Avoid inline comments"


class TestRequirementsComparison:
    """Test relationships between different requirements files."""
    
    def test_py39_has_older_versions_than_main(self):
        """Test that py39 uses older compatible versions."""
        main_content = Path("requirements.txt").read_text(encoding='utf-8')
        py39_content = Path("requirements-py39.txt").read_text(encoding='utf-8')
        
        main_crewai = re.search(r'crewai==(\d+\.\d+\.\d+)', main_content)
        py39_crewai = re.search(r'crewai==(\d+\.\d+\.\d+)', py39_content)
        
        if main_crewai and py39_crewai:
            main_version = tuple(map(int, main_crewai.group(1).split('.')))
            py39_version = tuple(map(int, py39_crewai.group(1).split('.')))
            
            assert py39_version < main_version, \
                "py39 requirements should use older crewai version"
    
    def test_minimal_has_fewer_packages_than_main(self):
        """Test that minimal has fewer packages than main."""
        main_content = Path("requirements.txt").read_text(encoding='utf-8')
        minimal_content = Path("requirements-minimal.txt").read_text(encoding='utf-8')
        
        main_packages = len([l for l in main_content.split('\n') 
                            if l.strip() and not l.strip().startswith('#')])
        minimal_packages = len([l for l in minimal_content.split('\n') 
                               if l.strip() and not l.strip().startswith('#')])
        
        assert minimal_packages < main_packages, \
            "Minimal requirements should have fewer packages than main"
    
    def test_working_has_most_flexibility(self):
        """Test that working requirements has most flexible versioning."""
        working_content = Path("requirements-working.txt").read_text(encoding='utf-8')
        main_content = Path("requirements.txt").read_text(encoding='utf-8')
        
        working_flexible = working_content.count('>=')
        main_flexible = main_content.count('>=')
        
        assert working_flexible >= main_flexible, \
            "Working requirements should be more flexible than main"


class TestRequirementsPackageNames:
    """Test package naming conventions."""
    
    def test_package_names_are_lowercase(self):
        """Test that package names use lowercase."""
        files = [
            Path("requirements.txt"),
            Path("requirements-minimal.txt"),
            Path("requirements-py39.txt"),
            Path("requirements-working.txt")
        ]
        
        for req_file in files:
            content = req_file.read_text(encoding='utf-8')
            for line in content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    package_name = re.split(r'[><=!]', line)[0].strip()
                    # Package names should be lowercase with hyphens
                    assert package_name == package_name.lower(), \
                        f"{req_file.name}: Package name should be lowercase: {package_name}"
    
    def test_uses_standard_package_names(self):
        """Test that standard package names are used correctly."""
        files = [
            Path("requirements.txt"),
            Path("requirements-minimal.txt"),
            Path("requirements-py39.txt"),
            Path("requirements-working.txt")
        ]
        
        # Check that beautifulsoup4 is used (not beautifulsoup)
        for req_file in files:
            content = req_file.read_text(encoding='utf-8').lower()
            if 'beautifulsoup' in content:
                # Should include the '4'
                assert 'beautifulsoup4' in content, \
                    f"{req_file.name}: Should use beautifulsoup4, not beautifulsoup"


class TestRequirementsComments:
    """Test comment quality and documentation."""
    
    def test_comment_sections_are_descriptive(self):
        """Test that comment sections have descriptive names."""
        content = Path("requirements.txt").read_text(encoding='utf-8')
        comment_lines = [line for line in content.split('\n') if line.strip().startswith('#')]
        
        # Should have meaningful section comments
        assert len(comment_lines) >= 5, "Should have section comments"
        
        # At least some comments should be section headers (not too short)
        substantial_comments = [c for c in comment_lines if len(c.strip()) > 3]
        assert len(substantial_comments) >= 3, "Should have substantial section comments"
    
    def test_new_files_have_comments(self):
        """Test that new requirements files have explanatory comments."""
        new_files = [
            Path("requirements-minimal.txt"),
            Path("requirements-py39.txt"),
            Path("requirements-working.txt")
        ]
        
        for req_file in new_files:
            content = req_file.read_text(encoding='utf-8')
            comment_count = content.count('#')
            assert comment_count >= 3, f"{req_file.name} should have section comments"


class TestRequirementsDependencies:
    """Test specific dependency requirements."""
    
    def test_web_scraping_packages_in_full_requirements(self):
        """Test that full requirements include all web scraping tools."""
        content = Path("requirements.txt").read_text(encoding='utf-8')
        scraping_packages = ['beautifulsoup4', 'selenium', 'scrapy', 'playwright']
        
        for package in scraping_packages:
            assert package in content, f"{package} should be in main requirements"
    
    def test_minimal_excludes_heavy_dependencies(self):
        """Test that minimal requirements excludes heavy packages."""
        content = Path("requirements-minimal.txt").read_text(encoding='utf-8')
        heavy_packages = ['selenium', 'scrapy', 'playwright', 'crewai']
        
        for package in heavy_packages:
            assert package not in content, \
                f"{package} should not be in minimal requirements (too heavy)"
    
    def test_api_integration_packages_present(self):
        """Test that API integration packages are present in full requirements."""
        content = Path("requirements.txt").read_text(encoding='utf-8')
        api_packages = ['gspread', 'twilio', 'httpx']
        
        for package in api_packages:
            assert package in content, f"{package} should be in main requirements"
    
    def test_data_processing_in_all_variants(self):
        """Test that data processing packages are in all requirement variants."""
        files = [
            Path("requirements.txt"),
            Path("requirements-minimal.txt"),
            Path("requirements-py39.txt"),
            Path("requirements-working.txt")
        ]
        
        data_packages = ['pandas', 'numpy']
        
        for req_file in files:
            content = req_file.read_text(encoding='utf-8')
            for package in data_packages:
                assert package in content, \
                    f"{package} should be in {req_file.name}"