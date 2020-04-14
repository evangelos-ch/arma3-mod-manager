__version__ = "0.1.0"

from .models import db, Instance, Addon, Key

db.init("arma3-mod-manager.db")
db.connect()
InstanceAddons = Instance.addons.get_through_model()
db.create_tables([Instance, Addon, InstanceAddons, Key])
