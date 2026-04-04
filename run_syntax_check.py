#!/usr/bin/env python
import py_compile
import sys
import os

os.chdir(r'C:\Users\vhols\Documents\GitHub\EthicalCrawler')
files = ['database.py', 'autosave.py', 'theatrics.py', 'services.py', 'enumeration.py', 'chattin.py', 'digestion.py', 'webcrawling.py', 'reportcard.py']

passed = 0
failed = 0
results = []

for file in files:
    try:
        py_compile.compile(file, doraise=True)
        results.append(f'{file} OK')
        passed += 1
    except py_compile.PyCompileError as e:
        error_msg = str(e)
        results.append(f'{file} SYNTAX ERROR - {error_msg}')
        failed += 1

for result in results:
    print(result)

print(f'\n========================================')
print(f'Summary: {passed} passed, {failed} failed')
print(f'========================================')
sys.exit(0 if failed == 0 else 1)
