# EthicalCrawler Workspace Instructions

## Project Overview

EthicalCrawler is an OSINT (Open Source Intelligence) tool designed for ethical, legal, and controlled security testing. The system uses a state machine architecture with network isolation capabilities, allowing each component to operate with its own DNS resolver and IP route.

## Core Principles

1. **Ethical Security First**: Always require explicit written authorization before any security testing activities
2. **Network Isolation**: Each component operates with isolated network identities (DNS resolver + IP route)
3. **State Machine Flow**: Components transition through defined states (system_profiler → sql_searcher → web_crawler → remote_coordinator → terminal_ui → shutdown)
4. **Pseudocode Documentation**: Use pseudocode for high-level algorithmic descriptions before implementation

## Build and Test Commands

**Virtual Environment Setup:**
```bash
# Activate virtual environment
& c:\Users\vhols\Documents\GitHub\EthicalCrawler\test\Scripts\Activate.ps1

# Run main entry point
python VanessaPFinal.py

# Run CLI interface
python cli/main.py

# Run crawler
python crawler.py --mode crawl --start-url https://example.com
```

**No standard build files** (requirements.txt, setup.py, pyproject.toml, Makefile, pytest.ini) exist. Dependencies are installed in the `test/` virtual environment.

## Architecture

### State Machine Flow

```
INIT_SYSTEM
  ↓
system_profiler → sql_searcher → web_crawler → remote_coordinator → terminal_ui → shutdown
```

### Key Components

1. **System Profiler** - Reads and monitors system environment
2. **DNS Transplanter** - Dynamically swaps DNS resolvers per thread
3. **Network Scanner** - Scans local network for devices and ports
4. **IP Route Splitter** - Routes sockets to different DNS resolvers based on threads
5. **SQL Searcher** - Executes web searches and stores results in local database
6. **Web Crawler** - Crawls web for data with network identity isolation
7. **Remote Coordinator** - Coordinates with remote instances via Tailscale
8. **Terminal UI** - Real-time monitoring dashboard

### Directory Structure

- `VanessaPFinal.py` - Main entry point orchestrating all components
- `cli/main.py` - Command-line interface
- `core/` - Core configuration and orchestrator (pseudocode)
- `crawler/` - Web crawler worker module
- `Datamine/` - SQL search functionality
- `test/` - Virtual environment with dependencies

## Project-Specific Conventions

### Pseudocode Output

When requesting algorithmic explanations or high-level design, use pseudocode format:

```pseudocode
FUNCTION process_data(items):
    result = []
    FOR each item IN items:
        IF item.valid THEN
            result.append(item.value)
    RETURN result
```

**Never** provide actual implementation code unless explicitly requested.

### Ethical Framework

All security testing activities must:
- Have explicit written authorization
- Be for educational purposes only
- Respect privacy and data protection regulations
- Document all activities and report findings responsibly

### Network Identity Pattern

Each component operates with isolated network identities:
- Separate DNS resolver per thread
- Separate IP route per thread
- Isolated network context
- Shared local database for results

## Key Files

- [boot.txt](boot.txt) - Boot sequence documentation showing initialization flow
- [github.txt](github.txt) - Usage examples and command-line interface documentation
- [VanessaPFinal.py](VanessaPFinal.py) - Main orchestrator implementation
- [cli/main.py](cli/main.py) - CLI interface implementation
- [core/orchestrator.py](core/orchestrator.py) - State machine orchestrator (pseudocode)
- [crawler/worker.py](crawler/worker.py) - Web crawler pseudocode
- [Datamine/sqlandme.py](Datamine/sqlandme.py) - SQL search pseudocode

## Documentation Links

- [Legal and Ethical Security Testing Guidelines](.github/copilot-instructions.md)
- [Pseudocode Output Guidelines](.github/prompts/pseudocode-only.prompt.md)

## Common Patterns

### State Machine Implementation

```python
# Pseudocode pattern for state transitions
FUNCTION execute_state_machine():
    current_state = "system_profiler"
    WHILE current_state != "shutdown":
        module = LOAD_MODULE(current_state)
        next_state = EXECUTE_MODULE(module, system_state)
        current_state = next_state
    CLEANUP()
```

### Network Isolation Pattern

```python
# Pseudocode pattern for thread isolation
FUNCTION worker_thread(thread_id):
    dns_resolver = SELECT_DNS_RESOLVER(thread_id)
    ip_route = SELECT_IP_ROUTE(thread_id)
    SET_NETWORK_CONTEXT(dns_resolver, ip_route)
    EXECUTE_TASK()
    RESTORE_NETWORK_CONTEXT()
```

## Development Workflow

1. **Design Phase**: Use pseudocode to outline algorithmic logic
2. **Implementation Phase**: Write actual code following project conventions
3. **Testing Phase**: Test with explicit authorization and proper consent
4. **Documentation Phase**: Document all activities in `/consent/` directory

## Potential Pitfalls

- **No standard build system**: Project uses virtual environment directly
- **Pseudocode-only files**: Some files contain pseudocode rather than implementation
- **Ethical compliance**: Always verify authorization before security operations
- **Network isolation**: Ensure proper cleanup of network contexts after operations

## Related Customizations

Consider creating these agent-customizations for specialized workflows:

- `/create-instruction legal-and-ethical-security` - Enforce authorization requirements
- `/create-instruction pseudocode-first` - Require pseudocode before implementation
- `/create-instruction network-isolation` - Guide network identity patterns
- `/create-instruction state-machine` - Enforce state machine architecture