"""Network profile builder - create per-worker profiles."""
__all__ = ["build"]

def build(state):
    """
    Build network profiles for each worker thread.
    Assigns DNS resolver, interface, Tailscale exit node per slot.
    Returns next state: "fetch_targets"
    """
    print("  → Building network profiles for worker threads...")
    # TODO: Implement build_profiles(concurrency, resolvers, tailscale_state)
    return "fetch_targets"
