__version__ = "0.1.0"

from .models import db, Instance

db.init("arma3-mod-manager.db")
db.connect()
db.create_tables([Instance])
