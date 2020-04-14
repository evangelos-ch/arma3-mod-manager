from typing import Union, Tuple
from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    ManyToManyField,
    ForeignKeyField,
    BooleanField,
)
from arma3_mod_manager.workshop import get_items

db = SqliteDatabase(None)


class Addon(Model):
    id = CharField(primary_key=True, unique=True)
    name = CharField()
    in_repo = BooleanField(default=False)
    keys_in_repo = BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.id}"

    @property
    def processed_name(self) -> str:
        """Utility to process a mod's name to be put into a folder."""
        name = self.name.lower()
        name = name.replace("-", " ")
        name = [substr.strip() for substr in name.split()]
        return "_".join(name)

    class Meta:
        database = db


class Key(Model):
    name = CharField()
    addon = ForeignKeyField(Addon, backref="keys")

    def __str__(self):
        return self.name

    class Meta:
        database = db


class Instance(Model):
    name = CharField(primary_key=True, unique=True)
    collection_url = CharField()
    folder = CharField()
    addons = ManyToManyField(Addon, backref="instances")
    clientside_addons = ManyToManyField(Addon)

    def __str__(self):
        return self.name

    def whitelist_clientside_addon(self, addon: Addon):
        from arma3_mod_manager import filesystem as fs
        if not addon.keys_in_repo:
            fs.add_addon_keys_to_repo(addon)
        fs.add_keys_to_instance(self, addon)
        if addon not in self.clientside_addons:
            self.clientside_addons.add(addon)

    def add_addons(self, addons: dict):
        addons = [
            Addon.get_or_create(id=addon["id"], name=addon["name"])[0]
            for addon in addons
        ]
        self.addons.add(addons)

    def install_addon(self, addon: Addon) -> bool:
        from arma3_mod_manager import filesystem as fs
        # Download addon into general repo
        if not addon.in_repo:
            added = fs.add_addon_to_repo(addon)
            if not added:
                return False
        # Install to instance
        fs.add_addon_to_instance(self, addon)
        # Add keys
        if not addon.keys_in_repo:
            fs.add_addon_keys_to_repo(addon)
        fs.add_keys_to_instance(self, addon)
        if addon not in self.addons:
            self.addons.add(addon)
        return True

    def update_addon(self, addon: Addon) -> bool:
        from arma3_mod_manager import filesystem as fs
        added = fs.add_addon_to_repo(addon)
        return added

    def update_addons(self) -> int:
        updated_count = 0
        for addon in self.addons:
            self.update_addon(addon)
        return updated_count

    def uninstall_addon(self, addon: Addon) -> bool:
        from arma3_mod_manager import filesystem as fs
        fs.remove_addon_from_instance(addon)
        fs.remove_keys_from_instance(addon)
        if addon in self.addons:
            self.addons.remove(addon)
        return True

    def sync_addons(self) -> Union[Tuple[int, int], bool]:
        new_addons_raw = get_items(self.collection_url)
        if new_addons_raw:
            new_addons = [
                Addon.get_or_create(id=addon["id"], name=addon["name"])[0]
                for addon in new_addons_raw
            ]
            # Add new addons
            added_addons = [addon for addon in new_addons if addon not in self.addons]
            removed_addons = [addon for addon in self.addons if addon not in new_addons]
            added_count = 0
            removed_count = 0
            for addon in removed_addons:
                uninstalled = self.uninstall_addon(addon)
                if uninstalled:
                    removed_count += 1
            for addon in added_addons:
                installed = self.install_addon(addon)
                if installed:
                    added_count += 1
            return (len(added_addons), len(removed_addons))
        return False

    class Meta:
        database = db
