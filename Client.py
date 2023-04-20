class Commands:
    def __init__(self):
        self.clients = {"/help": "получить информацию о командах",
                        "/menu": "просмотр меню",
                        "/order": "сделать заказ",
                        '/myorder': 'посмотреть текущей заказ',
                        '/time': 'указать время доставки'}
        self.courier = {"/order info": "получение информации о заказе"}
        self.manager = {"/order info": "получение информации о заказе"}
        self.admins = {"/add admin": "добавление администратора", "/add manager": "добавление менеджера",
                       "/add courier": "добавление курьера"}
    def get_commands(self, role):
        if role == 'client':
            return self.clients
        elif role == 'courier':
            return self.get_dict_copy(self.courier).update(self.clients) # dict1.update(dict2) - объединяет dict1 с dict2 и сохраняет в dict1
        elif role == 'admin':
            cmds = self.get_dict_copy(self.admins)
            cmds.update(self.clients)
            cmds.update(self.manager)
            cmds.update(self.courier)
            return cmds

    def get_dict_copy(self, dictionary):
        _dict = {}
        for k,v in dictionary.items(): # .items() -> [(k1,v1), (k2,v2)]
            _dict[k] = v
        return _dict


class Client:
    def __init__(self, id, chat_id, name, username=None, role='client'):
        self.id = id
        self.chat_id = chat_id
        self.name = name
        self.username = username
        self.role = role

        self.procedure = None
        self.order = None

    def Get_Commands(self):
        cmds = Commands().get_commands(self.role)

        text = "Доступные команды:\n"

        for k,v in cmds.items():
            text += f"* {k} - {v}.\n"

        return text

    def CheckCommandsPermissions(self, cmd):
        cmds = Commands().get_commands(self.role)
        if cmd in cmds.keys():
            return True
        else:
            return False

