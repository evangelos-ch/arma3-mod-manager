import pytest
from arma3_mod_manager.models import db, Instance, Addon


@pytest.fixture(autouse=False)
def setup_db():
    db.init(":memory:")
    db.connect()
    InstanceAddons = Instance.addons.get_through_model()
    db.create_tables([Instance, Addon, InstanceAddons])
    yield
    db.close()
