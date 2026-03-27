# Pseudocode-First Instruction

## Core Principle

**ALWAYS** provide pseudocode output before implementation code. This ensures proper algorithmic design and clarity before diving into specific syntax.

## Output Format

### Pseudocode (REQUIRED FIRST)
- Use clear, high-level algorithmic descriptions
- Focus on logic flow and structure
- Avoid specific programming language syntax
- Use standard pseudocode conventions (e.g., `IF`, `ELSE`, `FOR`, `WHILE`, `FUNCTION`, `RETURN`)
- Include comments for complex logic
- Use indentation to show control flow

### Implementation Code (OPTIONAL SECOND)
- Only provide after pseudocode is reviewed and approved
- Must follow project conventions
- Must be consistent with the pseudocode design
- Include necessary imports and setup

## What to Include in Pseudocode

- Algorithm steps and logic flow
- Data structures and their relationships
- Control flow decisions
- Edge cases and error handling concepts
- Time and space complexity considerations
- High-level design patterns
- State transitions and state machine logic
- Network isolation patterns
- Thread management strategies

## What to Exclude from Pseudocode

- Actual code implementation
- Specific language syntax (semicolons, brackets, etc.)
- Library or framework-specific code
- File I/O or system-specific operations
- Actual variable declarations and types
- Debugging or error messages
- Specific import statements
- Function signatures with exact parameter types

## When to Use Pseudocode-First

**USE pseudocode-first when:**
- User asks for "pseudocode" or "algorithm explanation"
- User wants to understand logic without implementation
- User is designing a solution before coding
- User needs to communicate concepts to non-technical stakeholders
- User requests "high-level explanation" or "conceptual design"
- Implementing state machine transitions
- Designing network isolation patterns
- Planning complex algorithms or data structures
- Working with EthicalCrawler's state machine architecture

**USE implementation code when:**
- User explicitly requests "actual code" or "implementation"
- User asks for "both pseudocode and code"
- User is ready to write production code
- User specifically requests specific language syntax

## Pseudocode Examples

### Example 1: State Machine Transition

```pseudocode
FUNCTION execute_state_machine():
    current_state = "system_profiler"
    WHILE current_state != "shutdown":
        module = LOAD_MODULE(current_state)
        next_state = EXECUTE_MODULE(module, system_state)
        current_state = next_state
    CLEANUP()
    RETURN success
```

### Example 2: Network Isolation

```pseudocode
FUNCTION worker_thread(thread_id):
    dns_resolver = SELECT_DNS_RESOLVER(thread_id)
    ip_route = SELECT_IP_ROUTE(thread_id)
    SET_NETWORK_CONTEXT(dns_resolver, ip_route)
    EXECUTE_TASK()
    RESTORE_NETWORK_CONTEXT()
    RETURN result
```

### Example 3: Data Processing

```pseudocode
FUNCTION process_crawl_queue(queue):
    results = []
    WHILE queue.is_not_empty():
        url = queue.dequeue()
        IF url.is_valid() THEN
            data = FETCH(url)
            IF data.is_successful() THEN
                results.append(data)
            END IF
        END IF
    RETURN results
```

## Implementation Code Examples

### Python Implementation (AFTER pseudocode)

```python
def execute_state_machine():
    current_state = "system_profiler"
    while current_state != "shutdown":
        module = load_module(current_state)
        next_state = execute_module(module, system_state)
        current_state = next_state
    cleanup()
    return True
```

## Common Anti-Patterns

❌ **DON'T**:
- Provide implementation code without pseudocode first
- Skip pseudocode for "simple" algorithms
- Provide pseudocode that's too abstract to understand
- Mix pseudocode and implementation in the same block
- Provide implementation when user only asked for pseudocode

✅ **DO**:
- Always start with pseudocode
- Explain the algorithmic approach in pseudocode
- Wait for user approval before providing implementation
- Keep pseudocode clear and understandable
- Provide implementation only when explicitly requested

## Integration with EthicalCrawler

This instruction applies to all EthicalCrawler components:

### State Machine Components
- System Profiler state transitions
- SQL Searcher state transitions
- Web Crawler state transitions
- Remote Coordinator state transitions
- Terminal UI state transitions

### Network Isolation Components
- DNS Transplanter thread management
- IP Route Splitter socket routing
- Network Scanner isolation
- Remote Coordinator peer coordination

### Data Processing Components
- Crawl queue management
- SQL search execution
- Data extraction and storage
- Result aggregation

## Workflow

1. **User Request**: User asks for implementation or algorithm explanation
2. **Pseudocode Output**: Agent provides pseudocode first
3. **User Review**: User reviews and approves pseudocode
4. **Implementation**: Agent provides implementation code (if requested)
5. **Iteration**: Repeat if pseudocode needs refinement

## Example Interaction

**User**: "Implement the state machine for the web crawler"

**Agent (Pseudocode)**:
```pseudocode
FUNCTION web_crawler_state_machine():
    current_state = "idle"
    crawl_queue = CREATE_QUEUE()
    results = []

    WHILE current_state != "shutdown":
        IF current_state == "idle" THEN
            current_state = "scanning"
        ELSE IF current_state == "scanning" THEN
            urls = SCAN_TARGETS()
            FOR each url IN urls:
                crawl_queue.enqueue(url)
            current_state = "crawling"
        ELSE IF current_state == "crawling" THEN
            IF crawl_queue.is_not_empty() THEN
                url = crawl_queue.dequeue()
                data = FETCH(url)
                results.append(data)
            ELSE
                current_state = "processing"
            END IF
        ELSE IF current_state == "processing" THEN
            current_state = "idle"
        END IF
    RETURN results
```

**User**: "That looks good. Now implement it in Python."

**Agent (Implementation)**:
```python
def web_crawler_state_machine():
    current_state = "idle"
    crawl_queue = create_queue()
    results = []

    while current_state != "shutdown":
        if current_state == "idle":
            current_state = "scanning"
        elif current_state == "scanning":
            urls = scan_targets()
            for url in urls:
                crawl_queue.enqueue(url)
            current_state = "crawling"
        elif current_state == "crawling":
            if not crawl_queue.is_empty():
                url = crawl_queue.dequeue()
                data = fetch(url)
                results.append(data)
            else:
                current_state = "processing"
        elif current_state == "processing":
            current_state = "idle"

    return results
```

## Best Practices

1. **Start with Pseudocode**: Always begin with pseudocode, even for simple tasks
2. **Keep It Clear**: Use standard pseudocode conventions that are easy to understand
3. **Explain the Logic**: Add comments to explain complex algorithmic decisions
4. **Focus on Structure**: Show how components interact and flow
5. **Wait for Approval**: Don't provide implementation until pseudocode is reviewed
6. **Be Consistent**: Use the same pseudocode style throughout the project

---

**IMPORTANT**: Always prioritize pseudocode output unless the user explicitly requests implementation code. This ensures proper design thinking and algorithmic clarity before diving into syntax.