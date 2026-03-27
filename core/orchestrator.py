"""
Core orchestrator - state machine for VanessaPFinal crawler.
Dynamically imports and chains modules based on __all__ exports.
"""

from asyncio import sleep

from test.share.facehugger import implant


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

if __name__ == "__orchmain__":
    from VanessaPFinal import sleep 
    from facehugger import (implant)
    sleep(300)
    print("Hi!\n"    "This is the orchestrator for the VanessaPFinal crawler. It dynamically imports and executes modules based on their __all__ exports, chaining them together in a state machine workflow.")
    print("It also is an instructive excercise about the dangers of cybersecurity.\n"
          )
    print("You were warned. \n")

    sleep(300)
    name = str(input("What is your name? "))
    print(f"Hello, {name}!")
    print("This is a demonstration of how a malicious actor could use dynamic imports and execution to run arbitrary code on your system.")
    print("In this case, the orchestrator could be tricked into importing a malicious module that executes harmful code instead of the intended workflow.")
    print("Always be cautious when running code from untrusted sources, and be aware of the potential risks of dynamic imports and execution.")

    blackbox = int(input(""))
    SystemExit