import json
from pathlib import Path
import shutil
from arma3_mod_manager.utils import process_mod_name


# Paths
file_path = Path(__file__).resolve().parent
staging_mods_dir = (
    file_path.parent / "mods_staging" / "steamapps" / "workshop" / "content" / "107410"
)
parent_mods_dir = file_path.parent / "mods"
parent_keys_dir = file_path.parent / "keys"
keys_dir = file_path / "keys"
mods_dir = file_path / "mods"

# Load mappings
with open("addons.json") as f:
    addons = json.load(f)
addon_ids = addons.keys()


# Rename folders & files
for addon_id in addon_ids:
    subdir = staging_mods_dir / addon_id
    print(f"Processing {subdir}")
    name = process_mod_name(
        addons[subdir.name] if subdir.name in addons else subdir.name
    )
    for item in subdir.glob("**/*"):
        item.rename(item.parent / item.name.lower())
    # Update mod in overall mods dir & symlink
    target = parent_mods_dir / name
    if target.exists():
        shutil.rmtree(target)
    subdir.rename(target)
    link_target = mods_dir / name
    if not link_target.exists():
        link_target.symlink_to(target)
    # Symlink & add keys
    keys = target.glob("**/*.bikey")
    for key in keys:
        key_location = parent_keys_dir / key.name
        shutil.copy(key, key_location)
        key_link_target = keys_dir / key.name
        if not key_link_target.exists():
            key_link_target.symlink_to(key_location)
