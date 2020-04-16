import click
from arma3_mod_manager import steamcmd
from arma3_mod_manager.workshop import get_items, get_item
from arma3_mod_manager.models import Instance, Addon


@click.group()
def main():
    pass


@main.command()
def update_game():
    updated = steamcmd.update_game()
    if updated:
        click.secho("Arma 3 server successfully updated.")
    else:
        click.echo("Update failed. Check logs for more info.")


@main.group()
def instance():
    pass


@instance.command()
@click.argument("instance_name")
@click.argument("collection_url")
@click.argument("folder")
def add(instance_name: str, collection_url: str, folder: str):
    instance = Instance.create(
        name=instance_name, collection_url=collection_url, folder=folder
    )
    click.echo("Created instance!")
    addons = get_items(collection_url)
    if addons:
        instance.add_addons(addons)
        click.echo(f"Added {len(addons)} addons.")
    else:
        click.echo("No items found in collection, probably invalid URL.")


@instance.command()
@click.argument("instance_name")
def delete(instance_name: str):
    if not Instance.filter(name=instance_name).exists():
        click.echo(f"Instance {instance_name} not found.")
        return

    instance = Instance.get(name=instance_name)
    instance.delete().execute()
    click.echo(f"Successfully deleted instance '{instance_name}'!")


@instance.command()
@click.argument("instance_name")
@click.option("--new_name", help="The new name of the instance")
@click.option("--folder", help="The new folder of the instance")
@click.option("--collection_url", help="The new collection URL.")
def update(instance_name: str, new_name: str, folder: str, collection_url: str):
    if not Instance.filter(name=instance_name).exists():
        click.echo(f"Instance {instance_name} not found.")
        return

    instance = Instance.get(name=instance_name)
    if new_name:
        instance.name = new_name
    if folder:
        instance.folder = folder
    if collection_url:
        instance.collection_url = collection_url
        addons = get_items(collection_url)
        if addons:
            instance.add_addons(addons)
    instance.save()
    click.echo(f"Successfully updated instance '{instance_name}'!")


@main.command()
@click.argument("instance_name")
def sync(instance_name: str):
    if not Instance.filter(name=instance_name).exists():
        click.echo(f"Instance {instance_name} not found.")
        return

    instance = Instance.get(name=instance_name)
    sync = instance.sync_addons()
    if sync:
        click.secho(
            f"Sync complete! Installed {sync[0]} new addons, removed {sync[1]} addons."
        )
    else:
        click.echo("Failed to sync mods. Check logs for more errors.")


@main.command()
@click.argument("instance_name")
def update_mods(instance_name):
    if not Instance.filter(name=instance_name).exists():
        click.echo(f"Instance {instance_name} not found.")
        return

    instance = Instance.get(name=instance_name)
    instance.update_addons()
    click.echo("Mods updated!")


@main.command()
@click.argument("instance_name")
def install_mods(instance_name):
    if not Instance.filter(name=instance_name).exists():
        click.echo(f"Instance {instance_name} not found.")
        return

    instance = Instance.get(name=instance_name)
    instance.install_addons()
    click.echo("Mods installed!")


@main.command()
@click.argument("instance_name")
@click.argument("mod_id")
def update_mod(instance_name: str, mod_id: str):
    # Get instance
    if not Instance.filter(name=instance_name).exists():
        click.echo(f"Instance {instance_name} not found.")
        return

    instance = Instance.get(name=instance_name)
    # Get addon
    if not Addon.filter(id=mod_id).exists():
        click.echo(f"Instance {mod_id} not found.")
        return

    addon = Addon.get(id=mod_id)
    instance.update_addon(addon)
    click.echo("Mod updated!")


@main.command()
@click.argument("instance_name")
@click.argument("mod_id")
def whitelist_clientside_addon(instance_name: str, mod_id: str):
    # Get instance
    if not Instance.filter(name=instance_name).exists():
        click.echo(f"Instance {instance_name} not found.")
        return

    instance = Instance.get(name=instance_name)
    # Get addon
    if not Addon.filter(id=mod_id).exists():
        click.echo(f"Instance {mod_id} not found.")
        return

    addon = Addon.get(id=mod_id)
    instance.whitelist_clientside_addon(addon)
    click.echo(f"Addon {addon.name} whitelisted.")


@main.command()
@click.argument("addon_url")
def add_addon(addon_url: str):
    item = get_item(addon_url)
    addon = Addon.get_or_create(id=item["id"], name=item["name"])[0]
    click.echo(f"Added mod {addon} to the registry.")


if __name__ == "__main__":
    main()
