"""Crawl scheduler - spawn worker threads."""
__all__ = ["schedule"]

def schedule(state):
    """
    Schedule crawl: spawn worker threads, each with isolated network profile.
    Returns next state: "gather_records"
    """
    print("  → Scheduling crawl across worker threads...")
    # TODO: Implement schedule_crawl(targets, profiles, settings)
    # Uses ThreadPoolExecutor to spawn workers
    return "gather_records"
