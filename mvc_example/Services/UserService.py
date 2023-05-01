from mvc_example.Models.User import User
import logging

class UserService:
    users = list()

    @staticmethod
    def GetUser(chat_id):
        for user in UserService.users:
            if user.chat_id == chat_id:
                return user
        return None

    @staticmethod
    def AddUser(user):
        user_found = UserService.GetUser(user.chat_id)

        if user_found == None:
            UserService.users.append(user)
            logging.info("Пользователь добавлен")

    @staticmethod
    def GetOrAddUser(message):
        name = "user"

        try:
            name = message['from']['username']
        except:
            try:
                name = message['from']['first_name']
            except:
                name = message['from']['last_name']

        id = message['chat']['id']

        found_user = UserService.GetUser(id)

        if found_user == None:
            found_user = User(id, name)
            UserService.AddUser(found_user)

        return found_user

