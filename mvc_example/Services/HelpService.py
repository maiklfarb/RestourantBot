import logging

class HelpService:
    @staticmethod
    def Invoke(user):
        if user.name == "Никита Иванов":
            logging.warning("Пользователь забанен.")
            return f"{user.name} Вы забанены."
        logging.info("OK.")
        return f"{user.name} Ok, команда доступна."

