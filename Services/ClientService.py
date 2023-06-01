from dbContext import DbContext
from Client import Client
from Services.LogFactory import LogFactory

class ClientService:
    db = DbContext("./data")
    users = db.clients

    @staticmethod
    def AddUser(id, id_chat, name):
        user = Client(id, id_chat, name)
        ClientService.users.add_client(user)
        ClientService.db.SaveChanges()
        LogFactory.logger.info(f'Создан новый пользователь: {user.name} {user.role}')
        return user

    @staticmethod
    def GetUserByContext(dict_message):
        id_chat = dict_message['chat']['id']
        id = dict_message['from']['id']
        name = dict_message['from']['first_name']

        found_user = ClientService.db.clients.find_client(id)

        if found_user == None:
            found_user = ClientService.AddUser(id, id_chat, name)

        return found_user

    @staticmethod
    def AddAdmin(user):
        user.role = "admin"
        ClientService.db.SaveChanges()