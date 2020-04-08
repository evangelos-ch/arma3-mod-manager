from peewee import SqliteDatabase, Model, CharField

db = SqliteDatabase(None)


class Instance(Model):
    name = CharField(primary_key=True, unique=True)
    collection_url = CharField()
    folder = CharField()

    class Meta:
        database = db
