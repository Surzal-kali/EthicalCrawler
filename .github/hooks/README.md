# Pre-Commit Hook

Validates that git commit messages maintain LI's narrative/theatrical tone.

## What It Does

Before any `git commit` command executes, this hook checks the commit message for narrative context. It looks for:

✅ **Narrative signals** (good):
- Character/persona language: persona, narrator, slip, instability, closeness, quip, theatrical
- Emotional terms: mood, voice, character, dialogue, commentary  
- Stage metaphors: stage, act, scene, boot sequence, ritual
- LI-specific concepts: equip, pprint, sudo

⚠️ **Technical-only patterns** (triggers review):
- Pure conventional commits: `fix: update database`
- Strict conventional format: `feat(auth): add login`

## Examples

### ✅ Allowed Messages

```
Add slip_intensity decay to narrator quips
```
Contains narrative signal: "slip_intensity", "narrator", "quips"

```
Fix equip() integration in services stage
```
Contains LI-specific concept: "equip"

```
Refactor persona evolution logic in theatrics.py
```
Contains narrative signal: "persona"

```
[deps] Update psutil to 7.2.2
```
Uses exemption prefix

### ⚠️ Will Ask for Review

```
fix: update database schema
```
Purely technical, no narrative context

```
feat(db): add migration script
```
Conventional commit without LI-specific framing

### How to Bypass

Add `[skip hook]` prefix to intentionally non-narrative commits:

```
[skip hook] Update .gitignore
```

## Exemptions

These patterns automatically bypass validation:
- `[skip hook]` - Explicit bypass
- `[deps]` - Dependency updates
- `[ci]` - CI configuration  
- `Merge branch ...` - Git merges
- `Revert ...` - Git reverts

## Testing the Hook

Run the test script to see how different commit messages are validated:

```bash
python .github/scripts/test-commit-hook.py
```

## How It Works

1. Hook intercepts `PreToolUse` events for `powershell`/`bash` tools
2. Checks if command is `git commit -m "message"`
3. Validates message against narrative patterns
4. Returns `permissionDecision: "ask"` if purely technical
5. Returns `continue: true` if narrative context is present

## Hook Configuration

File: `.github/hooks/pre-commit.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "type": "command",
        "command": "python .github/scripts/validate-commit-tone.py",
        "timeout": 10
      }
    ]
  }
}
```

## Related Guidelines

See [Project Guidelines](../copilot-instructions.md) for:
- Narrative CLI style conventions
- Theatrical output patterns
- Project-specific terminology
