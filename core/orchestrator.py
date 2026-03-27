"""
Core orchestrator - state machine for VanessaPFinal crawler.
Dynamically imports and chains modules based on __all__ exports.
"""

def orchestrate(start_state="check_remote"):
    """
    Main orchestration loop.
    Each module's exported function takes state, returns next state.
    """
    state = start_state
    
    while state:
        try:
            # Dynamically import the module
            module_path = _get_module_path(state)
            module = __import__(module_path, fromlist=['__all__'])
            
            # Get the function from __all__
            if not hasattr(module, '__all__') or not module.__all__:
                print(f"[ERROR] Module '{state}' has no __all__ export")
                break
            
            func_name = module.__all__[0]
            if not hasattr(module, func_name):
                print(f"[ERROR] Function '{func_name}' not found in '{state}'")
                break
            
            func = getattr(module, func_name)
            
            # Call the function and get next state
            print(f"[{state.upper()}] Executing...")
            state = func(state)
            
            if state:
                print(f"[ORCHESTRATOR] → Next state: {state}\n")
            else:
                print(f"[ORCHESTRATOR] Workflow complete")
                
        except ImportError as e:
            print(f"[ERROR] Failed to import state '{state}': {e}")
            break
        except Exception as e:
            print(f"[ERROR] Exception in state '{state}': {e}")
            break


def _get_module_path(state):
    """Map state name to module path."""
    mapping = {
        "check_remote": "remote.client",
        "collect_profile": "system_profile.collector",
        "load_dns": "dns.transplant",
        "load_tailscale": "routing.tailscale_manager",
        "build_profiles": "routing.profiles",
        "fetch_targets": "remote.client",
        "schedule_crawl": "crawler.scheduler",
        "gather_records": "storage.db",
        "analytics": "analytics.report",
    }
    return mapping.get(state, f"crawler.{state}")


if __name__ == "__main__":
    orchestrate()
