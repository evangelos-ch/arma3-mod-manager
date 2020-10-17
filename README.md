# Arma 3 Mod Manager

Python package to allow very easily downloading mods from the workshop on a linux server and adding them into an Arma 3 linux server instance.

## Setup

-   Install `poetry`.
-   Run `poetry install`.
-   Set the following env vars:
    -   STEAMCMD_PATH: the path to steamcmd.sh
    -   MODS_STAGING_DIR: the install dir for workshop mods from steam
    -   MODS_REPO_DIR: the dir where the mods can stored
    -   KEYS_REPO_DIR: the dir where keys are stored generally

## Usage

### Add new instance

```sh
arma3-mod-manager instance add <name> <workshop link> <folder>
```

### Update Game

```sh
arma3-mod-manager update-game
```

### Install Addons

```sh
arma3-mod-manager isntall-addons <instance name>
```
