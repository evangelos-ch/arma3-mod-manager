import subprocess
from arma3_mod_manager.consts import STEAMCMD_PATH, MODS_STAGING_DIR


def download_mod(mod_id: str) -> bool:
    download_cmd = subprocess.run(
        [
            STEAMCMD_PATH,
            "+force_install_dir",
            MODS_STAGING_DIR,
            "+login",
            "anonymous",
            "+workshop_install_item",
            "107410",
            mod_id,
            "validate",
            "+quit",
        ]
    )
    return download_cmd.returncode == 0
