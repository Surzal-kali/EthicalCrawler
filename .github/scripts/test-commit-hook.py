#!/usr/bin/env python3
"""
Test script for the commit message validation hook.
Run this to see how different commit messages are validated.
"""

import sys
import os
import re

# Import validation function (inline for simplicity)
# If running as script, import from same directory
# If exec'd, define inline

NARRATIVE_SIGNALS = [
    r'\b(persona|narrator|slip|instability|closeness|quip|theatrical)\b',
    r'\b(mood|voice|character|dialogue|commentary)\b',
    r'\b(stage|act|scene|boot sequence|ritual)\b',
    r'\b(equip|pprint|sudo)\b',
]

TECHNICAL_ONLY_PATTERNS = [
    r'^(fix|add|update|remove|refactor|clean|improve):\s+[a-z]',
    r'^(feat|docs|style|chore|test|build|ci|perf|revert)(\(.+\))?:',
]

EXEMPTION_PATTERNS = [
    r'^\[skip\s+hook\]',
    r'^\[deps\]',
    r'^\[ci\]',
    r'^Merge\s+(branch|pull\s+request)',
    r'^Revert\s+',
]


def validate_commit_message(message):
    """Validate that commit message maintains narrative tone."""
    if not message or not message.strip():
        return True, None
    
    for pattern in EXEMPTION_PATTERNS:
        if re.search(pattern, message, re.IGNORECASE):
            return True, None
    
    has_narrative = any(
        re.search(pattern, message, re.IGNORECASE)
        for pattern in NARRATIVE_SIGNALS
    )
    
    is_technical_only = any(
        re.search(pattern, message, re.IGNORECASE | re.MULTILINE)
        for pattern in TECHNICAL_ONLY_PATTERNS
    )
    
    if is_technical_only and not has_narrative:
        return False, "Commit message appears purely technical."
    
    return True, None


TEST_MESSAGES = [
    # Should pass
    ("Add slip_intensity decay to narrator quips", True),
    ("Fix equip() integration in services stage", True),
    ("Refactor persona evolution logic in theatrics.py", True),
    ("Update boot sequence to include new ritual stage", True),
    ("Improve theatrical instability rendering", True),
    ("[deps] Update psutil to 7.2.2", True),
    ("[skip hook] Update .gitignore", True),
    ("Merge branch 'feature/new-stage'", True),
    
    # Should ask for review
    ("fix: update database schema", False),
    ("feat(db): add migration script", False),
    ("refactor: clean up code", False),
    ("update: improve performance", False),
    ("add: new feature", False),
]


def main():
    """Run test cases."""
    print("Testing Commit Message Validation\n")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for message, expected_valid in TEST_MESSAGES:
        is_valid, reason = validate_commit_message(message)
        
        # Check if result matches expectation
        if is_valid == expected_valid:
            status = "✓ PASS"
            passed += 1
        else:
            status = "✗ FAIL"
            failed += 1
        
        print(f"\n{status}")
        print(f"Message: {message}")
        print(f"Expected: {'Allow' if expected_valid else 'Ask'}")
        print(f"Got: {'Allow' if is_valid else 'Ask'}")
        
        if reason:
            print(f"Reason: {reason[:100]}...")
    
    print("\n" + "=" * 70)
    print(f"\nResults: {passed} passed, {failed} failed out of {len(TEST_MESSAGES)} tests")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
