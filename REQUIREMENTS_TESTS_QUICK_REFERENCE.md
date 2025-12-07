# Requirements Tests Quick Reference

## Quick Commands

```bash
# Run all requirements tests
pytest tests/test_requirements_validation.py -v

# Run specific test class  
pytest tests/test_requirements_validation.py::TestVersionSpecifiers -v

# Run with output
pytest tests/test_requirements_validation.py -v -s

# Run validation utility
python validate_requirements.py

# Run validation on specific file
python validate_requirements.py requirements-minimal.txt
```

## Test Structure