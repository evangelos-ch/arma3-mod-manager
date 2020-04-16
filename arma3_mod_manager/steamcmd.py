import subprocess
from arma3_mod_manager.consts import STEAMCMD_PATH, MODS_STAGING_DIR, SERVER_INSTALL_DIR


def download_addon(addon_id: str) -> bool:
    download_cmd = subprocess.run(
        [
            STEAMCMD_PATH,
            "+force_install_dir",
            MODS_STAGING_DIR,
            "+login",
            "anonymous",
            "+workshop_download_item",
            "107410",
            addon_id,
            "validate",
            "+quit",
        ]
    )
    return download_cmd.returncode == 0


def update_game() -> bool:
    update_cmd = subprocess.run(
        [
            STEAMCMD_PATH,
            "+force_install_dir",
            SERVER_INSTALL_DIR,
            "+login",
            "anonymous",
            "+app_update",
            "233780",
            "validate",
            "+quit",
        ]
    )
    return update_cmd == 0
