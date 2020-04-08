from pathlib import Path
import shutil
from arma3_mod_manager.steamcmd import download_addon
from arma3_mod_manager.models import Addon, Instance
from arma3_mod_manager.utils import process_mod_name
from arma3_mod_manager.consts import MODS_STAGING_DIR, MODS_REPO_DIR, KEYS_REPO_DIR


# Static Paths
staging_mods_dir = (
    Path(MODS_STAGING_DIR) / "steamapps" / "workshop" / "content" / "107410"
)
parent_mods_dir = MODS_REPO_DIR
parent_keys_dir = KEYS_REPO_DIR


def install_addon(instance_name: str, addon_id: str) -> bool:
    instance = Instance.get(name=instance_name)
    addon = Addon.get(id=addon_id)
    download_addon(addon_id)
    subdir = staging_mods_dir / addon_id
    name = process_mod_name(addon.name)
    target = parent_mods_dir / name
    if target.exists():
        shutil.rmtree(target)
    subdir.rename(target)
    for item in target.glob("**/*"):
        item.rename(item.parent / item.name.lower())
    instance_dir = Path(instance.folder)
    keys_dir = instance_dir / "keys"
    mods_dir = instance_dir / "mods"
    link_target = mods_dir / name
    if not link_target.exists():
        link_target.symlink_to(target)
    keys = target.glob("**/*.bikey")
    for key in keys:
        key_location = parent_keys_dir / key.name
        shutil.copy(key, key_location)
        key_link_target = keys_dir / key.name
        if not key_link_target.exists():
            key_link_target.symlink_to(key_location)
