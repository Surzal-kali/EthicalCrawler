"""Storage layer - persist crawl records."""
__all__ = ["gather"]

def gather(state):
    """
    Gather crawl records from database.
    Returns next state: "analytics"
    """
    print("  → Gathering crawl records from storage...")
    # TODO: Implement load_crawl_records()
    return "analytics"
