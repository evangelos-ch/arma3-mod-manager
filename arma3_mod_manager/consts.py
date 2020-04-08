from os import environ

STEAMCMD_PATH = environ.get("STEAMCMD_PATH", "../../steamcmd.sh")
MODS_STAGING_DIR = environ.get("MODS_STAGING_DIR", "../../mods_staging")
MODS_REPO_DIR = environ.get("MODS_REPO_DIR", "../../mods")
