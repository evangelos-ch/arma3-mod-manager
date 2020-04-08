from peewee import SqliteDatabase, Model, CharField, ManyToManyField

db = SqliteDatabase(None)


class Addon(Model):
    id = CharField(primary_key=True, unique=True)
    name = CharField()

    class Meta:
        database = db


class Instance(Model):
    name = CharField(primary_key=True, unique=True)
    collection_url = CharField()
    folder = CharField()
    addons = ManyToManyField(Addon, backref="instances")

    def add_addons(self, addons: dict):
        addons = [Addon.get_or_create(id=addon["id"], name=addon["name"])[0] for addon in addons]
        self.addons.add(addons)

    class Meta:
        database = db
