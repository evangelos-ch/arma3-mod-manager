def process_mod_name(name: str) -> str:
    """Utility to process a mod's name to be put into a folder."""
    name = name.lower()
    name = name.replace("-", " ")
    name = [substr.strip() for substr in name.split()]
    return "_".join(name)
