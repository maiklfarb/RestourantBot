from dbContext import DbContext
from Client import Client

class UserService:
    db = DbContext("./data")
    users = db.clients

    @staticmethod
    def add_user(id, id_chat, name):
        user = Client(id, id_chat, name)
        UserService.users.add_client(user)
        UserService.db.SaveChanges()
        #log(f'Создан новый пользователь: {user.name} {user.role}')
        return user

    @staticmethod
    def GetUserByContext(dict_message):
        id_chat = dict_message['chat']['id']
        id = dict_message['from']['id']
        name = dict_message['from']['first_name']

        found_user = UserService.db.clients.find_client(id)

        if found_user == None:
            found_user = UserService.add_user(id, id_chat, name)

        return found_user