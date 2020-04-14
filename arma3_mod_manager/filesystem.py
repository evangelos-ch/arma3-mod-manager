from pathlib import Path
import shutil
from arma3_mod_manager.steamcmd import download_addon
from arma3_mod_manager.models import Addon, Instance, Key
from arma3_mod_manager.consts import MODS_STAGING_DIR, MODS_REPO_DIR, KEYS_REPO_DIR


# Static Paths
staging_mods_dir = (
    Path(MODS_STAGING_DIR).resolve() / "steamapps" / "workshop" / "content" / "107410"
)
parent_mods_dir = Path(MODS_REPO_DIR).resolve()
parent_keys_dir = Path(KEYS_REPO_DIR).resolve()


def add_addon_to_repo(addon: Addon) -> bool:
    downloaded = download_addon(addon.id)
    if not downloaded:
        return False
    subdir = staging_mods_dir / addon.id
    target = parent_mods_dir / addon.processed_name
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(subdir, target)
    for item in target.glob("**/*"):
        item.rename(item.parent / item.name.lower())
    keys = target.glob("**/*.bikey")
    addon.keys.clear()
    for key in keys:
        addon.keys.add(Key.get_or_create(name=key.name)[0])
    addon.in_repo = True
    addon.save()
    return True


def remove_addon_from_repo(addon: Addon) -> bool:
    target = parent_mods_dir / addon.processed_name
    shutil.rmtree(target)
    addon.in_repo = False
    addon.save()
    return True


def add_addon_keys_to_repo(addon: Addon) -> bool:
    in_repo = addon.in_repo
    if not in_repo:
        added = add_addon_to_repo(addon)
        if not added:
            return False
    target = parent_mods_dir / addon.processed_name
    keys = target.glob("**/*.bikey")
    for key in keys:
        key_location = parent_keys_dir / key.name
        shutil.copy(key, key_location)
    addon.keys_in_repo = True
    addon.save()
    if not in_repo:
        remove_addon_from_repo(addon)
    return True


def remove_addon_keys_from_repo(addon: Addon) -> bool:
    for key in addon.keys:
        key_location = parent_keys_dir / key.name
        if key_location.exists():
            key_location.unlink()
    return True


def add_addon_to_instance(instance: Instance, addon: Addon) -> bool:
    instance_dir = Path(instance.folder).resolve()
    target = parent_mods_dir / addon.processed_name
    mods_dir = instance_dir / "mods"
    link_target = mods_dir / addon.processed_name
    if not link_target.exists():
        link_target.symlink_to(target)
    return True


def remove_addon_from_instance(instance: Instance, addon: Addon) -> bool:
    instance_dir = Path(instance.folder).resolve()
    mods_dir = instance_dir / "mods"
    link_target = mods_dir / addon.processed_name
    if link_target.exists():
        link_target.rmdir()
    return True


def add_keys_to_instance(instance: Instance, addon: Addon) -> bool:
    instance_dir = Path(instance.folder).resolve()
    keys_dir = instance_dir / "keys"
    for key in addon.keys:
        key_location = parent_keys_dir / key.name
        key_link_target = keys_dir / key.name
        if not key_link_target.exists():
            key_link_target.symlink_to(key_location)
    return True


def remove_keys_from_instance(instance: Instance, addon: Addon) -> bool:
    instance_dir = Path(instance.folder).resolve()
    keys_dir = instance_dir / "keys"
    for key in addon.keys:
        key_link_target = keys_dir / key.name
        if key_link_target.exists():
            key_link_target.unlink()
    return True
