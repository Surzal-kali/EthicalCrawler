#!/usr/bin/env python
"""Run syntax checks on specified Python files."""
import py_compile
import sys

files = [
    'database.py',
    'autosave.py',
    'theatrics.py',
    'services.py',
    'enumeration.py',
    'chattin.py',
    'digestion.py',
    'webcrawling.py',
    'reportcard.py'
]

print("=" * 60)
print("PYTHON SYNTAX CHECK RESULTS")
print("=" * 60)

results = []
for filename in files:
    try:
        py_compile.compile(filename, doraise=True)
        status = "✓ PASS"
        results.append((filename, True))
    except py_compile.PyCompileError as e:
        status = "✗ FAIL"
        results.append((filename, False))
        print(f"\n{filename}: {status}")
        print(f"Error details:\n{str(e)}")
        continue
    
    print(f"{filename}: {status}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
passed = sum(1 for _, result in results if result)
failed = sum(1 for _, result in results if not result)

for filename, result in results:
    status = "PASS" if result else "FAIL"
    print(f"{filename:20} {status}")

print("-" * 60)
print(f"Total: {passed} passed, {failed} failed out of {len(results)} files")
print("=" * 60)
