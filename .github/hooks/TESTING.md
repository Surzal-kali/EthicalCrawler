# Testing Your Pre-Commit Hook

## Quick Test

Run the test suite to see how different commit messages are validated:

```bash
python .github/scripts/test-commit-hook.py
```

Expected output: **13 passed, 0 failed**

## Manual Testing with Agent

Try these prompts to see the hook in action:

### ✅ Should Allow (Narrative Context Present)

```
@terminal git commit -m "Add slip_intensity decay to narrator quips"
```

Hook allows immediately - message contains "slip_intensity", "narrator", "quips"

```
@terminal git commit -m "Refactor persona evolution in theatrics module"
```

Hook allows immediately - message contains "persona"

### ⚠️ Should Ask for Confirmation (Technical Only)

```
@terminal git commit -m "fix: update database schema"
```

Hook intercepts and asks: "Commit message appears purely technical. Consider adding narrative context..."

```
@terminal git commit -m "feat: add new module"
```

Hook intercepts - no LI-specific terminology present

### Bypass Examples

```
@terminal git commit -m "[skip hook] Update .gitignore"
```

Hook allows with explicit bypass

```
@terminal git commit -m "[deps] Bump faker to 40.11.2"
```

Hook allows - dependency updates are exempt

## How to Respond When Prompted

If the hook asks for confirmation, you have options:

1. **Approve anyway** - The commit proceeds as-is
2. **Revise message** - Add narrative context:
   - ❌ `fix: update database schema`
   - ✅ `Fix session persistence to track persona evolution`

3. **Add bypass** if truly non-narrative:
   - `[skip hook] fix: update database schema`

## Disable Hook Temporarily

If you need to disable the hook for a session:

```bash
# Rename the hook file
mv .github/hooks/pre-commit.json .github/hooks/pre-commit.json.disabled

# Re-enable later
mv .github/hooks/pre-commit.json.disabled .github/hooks/pre-commit.json
```

## Common Questions

**Q: Does this block regular git operations?**  
A: No - the hook only validates when using AI agents with `git commit -m`. Manual terminal commits are unaffected.

**Q: What if I want to adjust the validation rules?**  
A: Edit `.github/scripts/validate-commit-tone.py` and modify the pattern lists:
- `NARRATIVE_SIGNALS` - Add more LI-specific terms
- `TECHNICAL_ONLY_PATTERNS` - Adjust what triggers review
- `EXEMPTION_PATTERNS` - Add more bypass prefixes

**Q: Can I use this in other projects?**  
A: Yes! Just update the narrative signals to match your project's domain language.
