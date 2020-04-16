from os import environ

SERVER_INSTALL_DIR = environ.get("SERVER_INSTALL_DIR", "../../install")
STEAMCMD_PATH = environ.get("STEAMCMD_PATH", "../../steamcmd.sh")
MODS_STAGING_DIR = environ.get("MODS_STAGING_DIR", "../../mods_staging")
MODS_REPO_DIR = environ.get("MODS_REPO_DIR", "../../mods")
KEYS_REPO_DIR = environ.get("KEYS_REPO_DIR", "../../keys")
