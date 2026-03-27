"""DNS resolver management - load and apply system DNS."""
__all__ = ["load"]

def load(state):
    """
    Load DNS resolvers from config.
    Returns next state: "load_tailscale"
    """
    print("  → Loading DNS resolvers from config...")
    # TODO: Implement load_resolvers(settings.DNS_PROFILE_FILE)
    return "load_tailscale"
