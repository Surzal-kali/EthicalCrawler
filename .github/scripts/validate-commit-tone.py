#!/usr/bin/env python3
"""
Pre-commit hook to validate that git commit messages maintain LI's narrative/theatrical tone.

Reads hook input from stdin, checks if a git commit is being made, and validates
the commit message against narrative tone guidelines.
"""

import sys
import json
import re


# Narrative tone indicators (positive signals)
NARRATIVE_SIGNALS = [
    # Character/persona language
    r'\b(persona|narrator|slip|instability|closeness|quip|theatrical)\b',
    # Emotional/personality terms
    r'\b(mood|voice|character|dialogue|commentary)\b',
    # Stage/act metaphors
    r'\b(stage|act|scene|boot sequence|ritual)\b',
    # LI-specific concepts
    r'\b(equip|speak|sudo)\b',
]

# Technical-only patterns (warning signals)
TECHNICAL_ONLY_PATTERNS = [
    r'^(fix|add|update|remove|refactor|clean|improve):\s+[a-z]',  # Conventional commits without context
    r'^(feat|docs|style|chore|test|build|ci|perf|revert)(\(.+\))?:',  # Strict conventional commits
]

# Exemptions (these are OK to be technical)
EXEMPTION_PATTERNS = [
    r'^\[skip\s+hook\]',  # Explicit skip
    r'^\[deps\]',  # Dependency updates
    r'^\[ci\]',  # CI configuration
    r'^Merge\s+(branch|pull\s+request)',  # Git merges
    r'^Revert\s+',  # Git reverts
]


def validate_commit_message(message):
    """
    Validate that commit message maintains narrative tone.
    
    Returns:
        tuple: (is_valid: bool, reason: str or None)
    """
    if not message or not message.strip():
        return True, None
    
    # Check exemptions first
    for pattern in EXEMPTION_PATTERNS:
        if re.search(pattern, message, re.IGNORECASE):
            return True, None
    
    # Check for narrative signals
    has_narrative = any(
        re.search(pattern, message, re.IGNORECASE)
        for pattern in NARRATIVE_SIGNALS
    )
    
    # Check for technical-only patterns
    is_technical_only = any(
        re.search(pattern, message, re.IGNORECASE | re.MULTILINE)
        for pattern in TECHNICAL_ONLY_PATTERNS
    )
    
    # If it's purely technical without narrative context, ask for review
    if is_technical_only and not has_narrative:
        return False, (
            "Commit message appears purely technical. Consider adding narrative context:\n"
            "- How does this change affect LI's persona or theatrical elements?\n"
            "- Does it relate to slip mechanics, quip generation, or narrator behavior?\n"
            "- Use [skip hook] prefix to bypass if this is intentionally non-narrative."
        )
    
    return True, None


def main():
    """Hook entry point."""
    try:
        # Read hook input
        hook_input = json.loads(sys.stdin.read())
        
        # Extract tool name and parameters
        tool_name = hook_input.get("tool", {}).get("name", "")
        
        # Only validate git commit commands
        if tool_name not in ["powershell", "bash"]:
            # Not a shell command, allow
            print(json.dumps({"continue": True}))
            return 0
        
        # Get the command being executed
        params = hook_input.get("tool", {}).get("params", {})
        command = params.get("command", "")
        
        # Check if this is a git commit command
        if not re.search(r'\bgit\s+commit\b', command, re.IGNORECASE):
            # Not a git commit, allow
            print(json.dumps({"continue": True}))
            return 0
        
        # Extract commit message from command
        # Try -m flag first
        message_match = re.search(r'-m\s+["\']([^"\']+)["\']', command)
        if not message_match:
            # If no -m flag, this might be opening an editor - allow
            print(json.dumps({"continue": True}))
            return 0
        
        commit_message = message_match.group(1)
        
        # Validate the message
        is_valid, reason = validate_commit_message(commit_message)
        
        if not is_valid:
            # Ask user to review
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "ask",
                    "permissionDecisionReason": reason
                }
            }
            print(json.dumps(output))
            return 0
        
        # Message looks good, allow
        print(json.dumps({"continue": True}))
        return 0
        
    except Exception as e:
        # Don't block on hook errors - just warn
        print(json.dumps({
            "continue": True,
            "systemMessage": f"Pre-commit hook warning: {str(e)}"
        }), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
