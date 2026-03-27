"""Tailscale state management - get exit nodes."""
__all__ = ["get"]

def get(state):
    """
    Get Tailscale state (available exit nodes).
    Returns next state: "build_profiles"
    """
    print("  → Querying Tailscale state...")
    # TODO: Implement get_tailscale_state()
    return "build_profiles"
