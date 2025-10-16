# Test Suite for 500-AI-Agents-Projects Repository

This directory contains comprehensive validation tests for the repository's documentation,
configuration files, and assets.

## Test Categories

### 1. GitHub Actions Workflow Tests (`test_github_actions_workflow.py`)
- YAML syntax validation
- Required fields verification
- GitHub Actions best practices
- Security checks (no exposed secrets)
- Action version pinning validation
- Proper permissions configuration
- Workflow structure and job dependencies

### 2. Markdown Documentation Tests (`test_markdown_files.py`)
- Existence of required documentation files
- README.md structure and completeness
- CONTRIBUTION.md guidelines validation
- Course documentation quality
- Markdown formatting standards
- Link validation (internal and external)
- Code block formatting
- Consistent heading styles

### 3. LICENSE File Tests (`test_license_file.py`)
- LICENSE file existence and location
- MIT License format validation
- Copyright notice verification
- Required legal disclaimers
- License references in other files
- Compliance with open-source standards

### 4. Image File Tests (`test_images.py`)
- Image file integrity
- Corruption detection
- File size reasonableness
- Dimension validation
- Format correctness
- Duplicate detection
- Usage in documentation
- Link validity

## Running the Tests

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run All Tests
```bash
pytest
```

### Run Specific Test Category
```bash
pytest tests/test_github_actions_workflow.py
pytest tests/test_markdown_files.py
pytest tests/test_license_file.py
pytest tests/test_images.py
```

### Run with Coverage
```bash
pytest --cov=. --cov-report=html
```

### Run with Verbose Output
```bash
pytest -v
```

### Run Specific Test Function
```bash
pytest tests/test_markdown_files.py::TestREADME::test_readme_has_title
```

## Test Markers

Tests are organized with markers for easy filtering:

```bash
# Run only YAML tests
pytest -m yaml

# Run only Markdown tests
pytest -m markdown

# Run only license tests
pytest -m license

# Run only image tests
pytest -m images
```

## CI/CD Integration

These tests can be integrated into GitHub Actions workflow:

```yaml
name: Documentation Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest -v
```

## Test Philosophy

These tests follow the principle that documentation and configuration are just as important
as code. They ensure:

1. **Correctness**: Files are syntactically correct and properly formatted
2. **Completeness**: Required information is present
3. **Quality**: Content meets professional standards
4. **Maintainability**: Structure is consistent and easy to update
5. **Accessibility**: Links work and resources are available

## Contributing

When adding new files to the repository:

1. Update relevant test files to include validation for new content
2. Ensure all tests pass before submitting PR
3. Add new test categories for new file types if needed

## Troubleshooting

### Common Issues

**Import errors**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

**Image tests failing**: Make sure PIL/Pillow is installed:
```bash
pip install Pillow
```

**Path issues**: Tests assume they're run from repository root:
```bash
cd /path/to/repository/root
pytest
```

## Test Coverage Goals

- GitHub Actions: 100% coverage of workflow structure
- Markdown: Validate all .md files in repository
- License: Complete MIT license compliance
- Images: All images validated for integrity

## Future Enhancements

Planned additions to the test suite:
- Link checking for external URLs (with rate limiting)
- Spell checking for documentation
- Accessibility testing for documentation
- Performance benchmarks for large files
- Additional image optimization checks