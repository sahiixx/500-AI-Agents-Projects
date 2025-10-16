# Test Suite for 500-AI-Agents-Projects

Comprehensive validation tests for repository files, ensuring quality and consistency.

## Test Files

### `test_github_workflow.py`
Tests GitHub Actions workflow configuration:
- YAML syntax validation.
- Required fields and structure.
- Job definitions and dependencies.
- Permissions and triggers.

### `test_markdown_files.py`
Tests Markdown documentation:
- File existence and structure.
- Proper heading hierarchy.
- Code block formatting.
- Content completeness.

### `test_license.py`
Tests LICENSE file:
- MIT License format validation.
- Required clauses.
- Copyright notice.
- Consistency with docs.

### `test_images.py`
Tests image files:
- File existence and readability.
- Valid formats (JPEG/PNG).
- Reasonable dimensions.
- Documentation references.

### `test_integration.py`
Integration tests:
- Repository structure.
- Cross-file consistency.
- Documentation quality.
- Badge and emoji usage.

## Running Tests

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run All Tests
```bash
pytest
```

### Run Specific Test Suite
```bash
pytest tests/test_markdown_files.py -v
```

### Run With Coverage
```bash
pytest --cov=. --cov-report=html
```

### Run Specific Test
```bash
pytest tests/test_license.py::TestLicense::test_license_is_mit -v
```

## Test Coverage

The test suite covers:
- ✅ GitHub Actions workflow configuration.
- ✅ All Markdown documentation files.
- ✅ LICENSE file compliance.
- ✅ Image file validation.
- ✅ Repository structure.
- ✅ Documentation quality metrics.
- ✅ Cross-file consistency.

## Adding New Tests

When adding new files to the repository:
1. Add validation tests to the appropriate test file.
2. Ensure tests check existence, validity, and integration.
3. Run the full test suite before committing.
4. Update this README when adding new test categories.