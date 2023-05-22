from peewee import *


db = SqliteDatabase('data/data.sqlite')

class BaseModel(Model):
    class Meta:
        database = db

class Role(BaseModel):
    id = PrimaryKeyField(null=False, column_name="RoleID")
    name = TextField(null=False, column_name="Name")
    class Meta:
        table_name = "Roles"

class Client(BaseModel):
    id = PrimaryKeyField(null=False, column_name="ClientID")
    name = TextField(null=False, column_name="Name")
    chatId = IntegerField(null=False, column_name="ChatID")
    username = TextField(null=False, column_name="Username")
    carId = ForeignKeyField(Role, column_name="RoleID", backref="Roles")

    class Meta:
        table_name = "Clients"

if __name__ == "__main__":
    Role.create_table()
    Client.create_table()

    db.close()