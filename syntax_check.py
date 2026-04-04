import py_compile
import sys

files = [
    "database.py",
    "autosave.py",
    "theatrics.py",
    "services.py",
    "enumeration.py",
    "chattin.py",
    "digestion.py",
    "webcrawling.py",
    "reportcard.py"
]

results = []
for file in files:
    try:
        py_compile.compile(file, doraise=True)
        results.append(f"{file} OK")
    except py_compile.PyCompileError as e:
        error_msg = str(e).replace('\n', ' ')
        results.append(f"{file} SYNTAX ERROR - {error_msg}")

for result in results:
    print(result)

# Print summary
passed = sum(1 for r in results if "OK" in r)
failed = sum(1 for r in results if "SYNTAX ERROR" in r)
print(f"\nSummary: {passed} passed, {failed} failed")
