from Services.LogFactory import LogFactory
class CommandService:
    clients = {"/help": "получить информацию о командах",
                    "/menu": "просмотр меню",
                    "/order": "сделать заказ",
                    '/myorder': 'посмотреть текущей заказ',
                    '/time': 'указать время доставки'}
    courier = {"/order info": "получение информации о заказе"}
    manager = {"/order info": "получение информации о заказе"}
    admins = {"/add admin": "добавление администратора", "/add manager": "добавление менеджера",
                   "/add courier": "добавление курьера"}

    @staticmethod
    def get_commands(role):
        if role == 'client':
            return CommandService.clients
        elif role == 'courier':
            return CommandService.get_dict_copy(CommandService.courier).update(CommandService.clients) # dict1.update(dict2) - объединяет dict1 с dict2 и сохраняет в dict1
        elif role == 'admin':
            cmds = CommandService.get_dict_copy(CommandService.admins)
            cmds.update(CommandService.clients)
            cmds.update(CommandService.manager)
            cmds.update(CommandService.courier)
            return cmds

    @staticmethod
    def get_dict_copy(dictionary):
        _dict = {}
        for k,v in dictionary.items(): # .items() -> [(k1,v1), (k2,v2)]
            _dict[k] = v
        return _dict

    @staticmethod
    def get_commands_description(user):
        commands = CommandService.get_commands(user.role)

        text = "Доступные команды:\n"

        for k, v in commands.items():
            text += f"* {k} - {v}.\n"

        return text

    @staticmethod
    def check_commands_permissions(cmd, user):
        cmds = CommandService.get_commands(user.role)
        if cmd in cmds.keys():
            return True
        else:
            LogFactory.logger.warning(f'{user.chat_id} запрашивает недоступную команду {cmd}')
            return False