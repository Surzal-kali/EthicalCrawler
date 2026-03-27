---
name: pseudocode-only
description: 'Use when: the user requests pseudocode output, wants to focus on algorithmic logic without implementation details, or needs high-level conceptual explanations.'
agent: agent
---

# Pseudocode Output Guidelines

## Core Principles

**ALWAYS** output only in pseudocode format. Never provide actual implementation code unless explicitly requested.

## Output Format

- Use clear, high-level algorithmic descriptions
- Focus on logic flow and structure
- Avoid specific programming language syntax
- Use standard pseudocode conventions (e.g., `IF`, `ELSE`, `FOR`, `WHILE`, `FUNCTION`, `RETURN`)
- Include comments for complex logic
- Use indentation to show control flow

## What to Include

- Algorithm steps and logic flow
- Data structures and their relationships
- Control flow decisions
- Edge cases and error handling concepts
- Time and space complexity considerations
- High-level design patterns

## What to Exclude

- Actual code implementation
- Specific language syntax (semicolons, brackets, etc.)
- Library or framework-specific code
- File I/O or system-specific operations
- Actual variable declarations and types
- Debugging or error messages

## Examples

**Pseudocode (CORRECT):**
```
FUNCTION calculateTotal(items):
    total = 0
    FOR each item IN items:
        total = total + item.price
    RETURN total
```

**Code (INCORRECT - unless requested):**
```python
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total
```

## When to Use

- User asks for "pseudocode" or "algorithm explanation"
- User wants to understand logic without implementation
- User is designing a solution before coding
- User needs to communicate concepts to non-technical stakeholders
- User requests "high-level explanation" or "conceptual design"

## Edge Cases

- If user explicitly asks for "actual code" or "implementation", provide code
- If user asks for "both pseudocode and code", provide both in separate sections
- If pseudocode is too abstract, add brief explanations of key concepts

---

**IMPORTANT**: Always prioritize pseudocode output unless the user explicitly requests implementation code.