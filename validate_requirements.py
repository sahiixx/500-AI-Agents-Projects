#!/usr/bin/env python3
"""
Utility script to validate requirements files.

This script can be run independently to check requirements files
without running the full test suite.

Usage:
    python validate_requirements.py
    python validate_requirements.py requirements-minimal.txt
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple, Dict


def parse_requirement_line(line: str) -> Tuple[str, str, str]:
    """Parse a requirements line."""
    line = line.strip()
    
    if not line or line.startswith('#'):
        return ('', '', '')
    
    version_pattern = r'^([a-zA-Z0-9\-_\.]+)\s*(==|>=|<=|>|<|!=|~=|===)?\s*([0-9\.]+.*)?$'
    match = re.match(version_pattern, line)
    
    if match:
        package = match.group(1).lower().replace('_', '-')
        operator = match.group(2) or ''
        version = match.group(3) or ''
        return (package, operator, version)
    
    if re.match(r'^[a-zA-Z0-9\-_\.]+$', line):
        return (line.lower().replace('_', '-'), '', '')
    
    return ('', '', '')


def validate_file(file_path: Path) -> Dict[str, List[str]]:
    """Validate a requirements file and return issues."""
    issues = {
        'errors': [],
        'warnings': [],
        'info': []
    }
    
    if not file_path.exists():
        issues['errors'].append(f"File not found: {file_path}")
        return issues
    
    try:
        content = file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        issues['errors'].append("File is not valid UTF-8")
        return issues
    
    lines = content.split('\n')
    packages = []
    
    # Check each line
    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()
        
        # Check for trailing whitespace
        if line and line != line.rstrip():
            issues['warnings'].append(f"Line {line_num}: Trailing whitespace")
        
        # Skip comments and empty lines
        if not stripped or stripped.startswith('#'):
            continue
        
        # Parse requirement
        pkg, op, ver = parse_requirement_line(stripped)
        
        if not pkg:
            issues['errors'].append(f"Line {line_num}: Could not parse requirement: {stripped}")
            continue
        
        packages.append((pkg, op, ver, line_num))
        
        # Check version specifier
        if op and op not in ['==', '>=', '<=', '>', '<', '!=', '~=', '===']:
            issues['errors'].append(f"Line {line_num}: Invalid version operator: {op}")
        
        # Check for wildcards
        if '*' in stripped:
            issues['warnings'].append(f"Line {line_num}: Wildcard version used for {pkg}")
        
        # Check for uppercase
        if any(c.isupper() for c in stripped.split('=')[0].split('>')[0].split('<')[0]):
            issues['warnings'].append(f"Line {line_num}: Package name should be lowercase")
    
    # Check for duplicates
    package_names = [pkg for pkg, _, _, _ in packages]
    duplicates = [pkg for pkg in set(package_names) if package_names.count(pkg) > 1]
    if duplicates:
        issues['errors'].append(f"Duplicate packages found: {', '.join(duplicates)}")
    
    # Check file ending
    if not content.endswith('\n'):
        issues['warnings'].append("File should end with newline")
    
    # Info
    issues['info'].append(f"Total packages: {len(packages)}")
    pinned = sum(1 for _, op, _, _ in packages if op == '==')
    flexible = sum(1 for _, op, _, _ in packages if op in ['>=', '~='])
    issues['info'].append(f"Pinned versions: {pinned}, Flexible versions: {flexible}")
    
    return issues


def print_issues(file_path: Path, issues: Dict[str, List[str]]):
    """Print validation issues."""
    print(f"\n{'='*60}")
    print(f"Validating: {file_path}")
    print(f"{'='*60}")
    
    if issues['errors']:
        print(f"\n❌ ERRORS ({len(issues['errors'])}):")
        for error in issues['errors']:
            print(f"  • {error}")
    
    if issues['warnings']:
        print(f"\n⚠️  WARNINGS ({len(issues['warnings'])}):")
        for warning in issues['warnings']:
            print(f"  • {warning}")
    
    if issues['info']:
        print(f"\n📊 INFO:")
        for info in issues['info']:
            print(f"  • {info}")
    
    if not issues['errors'] and not issues['warnings']:
        print("\n✅ No issues found!")


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        # Validate specific file
        files = [Path(arg) for arg in sys.argv[1:]]
    else:
        # Validate all requirements files
        files = [
            Path('requirements.txt'),
            Path('requirements-minimal.txt'),
            Path('requirements-py39.txt'),
            Path('requirements-working.txt')
        ]
    
    total_errors = 0
    total_warnings = 0
    
    for file_path in files:
        issues = validate_file(file_path)
        print_issues(file_path, issues)
        total_errors += len(issues['errors'])
        total_warnings += len(issues['warnings'])
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Files checked: {len(files)}")
    print(f"Total errors: {total_errors}")
    print(f"Total warnings: {total_warnings}")
    
    if total_errors > 0:
        print("\n❌ Validation failed with errors")
        return 1
    elif total_warnings > 0:
        print("\n⚠️  Validation passed with warnings")
        return 0
    else:
        print("\n✅ All files validated successfully")
        return 0


if __name__ == '__main__':
    sys.exit(main())