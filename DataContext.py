from peewee import *
db = SqliteDatabase('data.sqlite')

class BaseModel(Model):
    class Meta:
        database = db

class Role(BaseModel):
    id = PrimaryKeyField(null=False, column_name="roleId")
    name = TextField(null=False, column_name="name")
    class Meta:
        table_name = "Roles"

class Client(BaseModel):
    id = PrimaryKeyField(null=False, column_name="clientID")
    name = TextField(null=False, column_name="name")
    chatId = IntegerField(null=False, column_name="ChatId")
    username = TextField(null=False, column_name="username")
    carId = ForeignKeyField(Role, column_name="roleId", backref="Roles")

    class Meta:
        table_name = "Clients"

print(__name__)
if __name__ == "__main__":
    Role.create_table()
    Client.create_table()

    db.close()