from pytest import fixture
from arma3_mod_manager import models, Instance


@fixture
def patch_db(monkeypatch):
    models.db.init(":memory:")
    models.db.connect()
    models.db.create_tables([Instance])


def test_instances(patch_db):
    instance = Instance.create(name="test", collection_url="test2", folder="test3")
    assert instance.name == "test"
    instance.delete().execute()
    assert len(Instance.select()) == 0
