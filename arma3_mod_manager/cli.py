import click
from arma3_mod_manager.workshop import get_items
from arma3_mod_manager.models import Instance
from arma3_mod_manager.filesystem import install_addon


@click.group()
def main():
    pass


@main.group()
def instance():
    pass


@instance.command()
@click.argument("name")
@click.argument("collection_url", help="The URL of the Workshop Collection.")
@click.argument("folder", help="Absolute path to the instance folder.")
def add(name, collection_url, folder):
    instance = Instance.create(name=name, collection_url=collection_url, folder=folder)
    click.echo("Created instance!")
    addons = get_items(collection_url)
    if addons:
        instance.add_addons(addons)
        click.echo(f"Added {len(addons)} addons.")
    else:
        click.echo("No items found in collection, probably invalid URL.")


@instance.command()
@click.argument("name")
def delete(name):
    Instance.delete(name=name).execute()
    click.echo(f"Successfully deleted instance '{name}'!")


@instance.command()
@click.argument("name")
@click.option("--new_name", help="The new name of the instance")
@click.option("--folder", help="The new folder of the instance")
@click.option("--collection_url", help="The new collection URL.")
def update(name, new_name, folder, collection_url):
    instance = Instance.get(name=name)
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
    click.echo(f"Successfully updated instance '{name}'!")


@main.command()
@click.argument("instance_name")
def update_mods(instance_name):
    if not Instance.filter(name=instance_name).exists():
        click.echo("No instance found.")
        return

    instance = Instance.get(name=instance_name)
    addons = get_items(instance.collection_url)
    instance.add_addons(addons)
    for addon in instance.addons:
        install_addon(instance.name, addon.id)
    click.echo("Mods updated!")


@main.command()
@click.argument("instance_name")
@click.argument("mod_id")
def update_mod(instance_name, mod_id):
    install_addon(instance_name, mod_id)
    click.echo("Mod updated!")


if __name__ == "__main__":
    main()
