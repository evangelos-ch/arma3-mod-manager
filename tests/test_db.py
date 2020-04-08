from arma3_mod_manager.models import Instance, Addon


def test_instances(setup_db):
    instance = Instance.create(name="test", collection_url="test2", folder="test3")
    assert instance.name == "test"
    instance.delete().execute()
    assert len(Instance.select()) == 0


def test_instance_add_addons(setup_db):
    instance = Instance.create(name="test", collection_url="test2", folder="test3")
    instance.add_addons([
        {"name": "test1", "id": "1"},
        {"name": "test2", "id": "2"}
    ])
    assert len(instance.addons) == 2


def test_addons(setup_db):
    addon1 = Addon.create(id="test123", name="test")
    assert addon1.id == "test123"
    addon2 = Addon.create(id="test1234", name="test2")
    instance = Instance.create(name="test", collection_url="test2", folder="test3")
    instance.addons.add([addon1, addon2])
    assert len(instance.addons) == 2
    Addon.delete().execute()
    assert len(Addon.select()) == 0
