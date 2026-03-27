"""System profile collection - captures environment at startup."""
__all__ = ["collect"]

def collect(state):
    """
    Collect system profile: OS, network, DNS, IP, CPU, memory.
    Saves to CSV and returns next state.
    """
    print("  → Collecting system profile (OS, network, DNS, IP, resources)...")
    # TODO: Implement system profile collection
    # Should create CSV in temp directory
    return "load_dns"
