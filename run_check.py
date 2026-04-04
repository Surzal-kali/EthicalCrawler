#!/usr/bin/env python3
"""Run syntax checks and display results"""
import py_compile
import os
import sys

# Change to the script directory
os.chdir(r'C:\Users\vhols\Documents\GitHub\EthicalCrawler')

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

print("=" * 70)
print("PYTHON SYNTAX CHECK RESULTS")
print("=" * 70)

results = []
for filename in files:
    try:
        py_compile.compile(filename, doraise=True)
        status = "✓ PASS"
        results.append((filename, True, None))
        print(f"{filename:25} {status}")
    except py_compile.PyCompileError as e:
        status = "✗ FAIL"
        error_msg = str(e)
        results.append((filename, False, error_msg))
        print(f"{filename:25} {status}")
        print(f"  Error: {error_msg}\n")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
passed = sum(1 for _, result, _ in results if result)
failed = sum(1 for _, result, _ in results if not result)

for filename, result, error in results:
    status = "PASS" if result else "FAIL"
    print(f"{filename:25} {status}")

print("-" * 70)
print(f"Total: {passed} passed, {failed} failed out of {len(results)} files")
print("=" * 70)

sys.exit(0 if failed == 0 else 1)
