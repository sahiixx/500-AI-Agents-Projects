# Requirements Files Validation Tests

## Overview

Comprehensive test suite for validating Python requirements files.

**File:** `test_requirements_validation.py`  
**Tests:** 35 test methods across 8 test classes  
**Coverage:** All 4 requirements files

## Quick Start

```bash
# Run all requirements tests
pytest tests/test_requirements_validation.py -v

# Run specific test class
pytest tests/test_requirements_validation.py::TestRequirementsSyntax -v

# Run with verbose output
pytest tests/test_requirements_validation.py -vv
```

## Test Classes

### 1. TestRequirementsFilesExist (4 tests)
Verifies all expected requirements files exist.

### 2. TestRequirementsSyntax (6 tests)
- UTF-8 encoding
- Newline at EOF
- No trailing whitespace
- No duplicate packages
- Valid PEP 440 version specifiers
- Consistent comment style

### 3. TestRequirementsContent (8 tests)
- Core packages present (pytest, pyyaml, requests)
- Minimal is subset of full
- Python 3.9 compatible versions
- Flexible versions in working requirements
- Section organization
- No local file references
- No git URLs

### 4. TestRequirementsSecurity (3 tests)
- No insecure packages (e.g., pycrypto)
- Pytest 7.0+ for security
- No dev/alpha/beta versions

### 5. TestRequirementsVersions (4 tests)
- Appropriate pytest versions per file
- python-dotenv consistency
- CrewAI version compatibility
- Langchain ecosystem consistency

### 6. TestRequirementsDocumentation (4 tests)
- Section headers present
- Python 3.9 compatibility documented
- File purposes clear
- Minimal has fewer packages than full

### 7. TestRequirementsIntegration (3 tests)
- Pip-installable format
- No conflicting versions
- Appropriate package counts

### 8. TestRequirementsEdgeCases (4 tests)
- Files not empty
- No extremely long lines (200 char limit)
- Consistent line endings
- Valid package names

## Files Tested

1. **requirements.txt** - Main requirements with latest versions
2. **requirements-minimal.txt** - Minimal installation (core packages only)
3. **requirements-py39.txt** - Python 3.9 compatible versions
4. **requirements-working.txt** - Working/tested configuration

## Key Validations

✅ **Syntax**: UTF-8, no trailing whitespace, valid version specs  
✅ **Security**: No insecure packages, secure versions  
✅ **Consistency**: Cross-file validation, no duplicates  
✅ **Documentation**: Clear sections, compatibility notes  
✅ **Format**: Pip-installable, valid package names  

## Examples

### Test Core Packages Present
```python
def test_core_testing_packages_present(self):
    """Ensures pytest, pytest-cov, pyyaml, requests in all files."""
```

### Test Python 3.9 Compatibility
```python
def test_py39_has_compatible_versions(self):
    """Validates requirements-py39.txt uses Python 3.9 compatible versions."""
```

### Test Security
```python
def test_no_insecure_packages(self):
    """Blocks known insecure packages like pycrypto."""
```

## Benefits

- **Quality**: Catches errors before installation
- **Security**: Validates secure package versions
- **Consistency**: Enforces formatting standards
- **Maintainability**: Self-documenting test suite
- **CI/CD Ready**: Automated validation

## Integration

Add to CI/CD pipeline:
```yaml
- name: Validate Requirements
  run: pytest tests/test_requirements_validation.py -v
```

## Test Coverage

| Area | Tests | Description |
|------|-------|-------------|
| File Existence | 4 | All requirements files present |
| Syntax | 6 | Format, encoding, style |
| Content | 8 | Package selection, organization |
| Security | 3 | Vulnerable packages, versions |
| Versions | 4 | Compatibility, consistency |
| Documentation | 4 | Comments, sections, clarity |
| Integration | 3 | Cross-file validation |
| Edge Cases | 4 | Uncommon errors |

## Troubleshooting

If tests fail:
1. Check error message for specific file and line number
2. Verify package versions are compatible
3. Ensure no duplicate packages
4. Validate version specifiers follow PEP 440
5. Check for trailing whitespace or encoding issues