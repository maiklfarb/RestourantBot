from mvc_example.Services.UserService import UserService
from mvc_example.Services.HelpService import HelpService
from telebot_router import TeleBot
import logging

app = TeleBot("Restaurant_Bot")
app.config['api_key'] = '6148540855:AAFNaxGTNxK_H332pSG2eCe4rERBSzO2Q44'
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")

logging.debug("Начало работы программы.")

@app.route('(?!/).+')
def data_handler(dict_message):
    """ Контроллер обработки произвольных сообщений """
    logging.info("Пришли на контроллер.")

    user = UserService.GetOrAddUser(dict_message)
    result = HelpService.Invoke(user)

    logging.info("Контроллер отдал результат.")
    app.send_message(user.chat_id, result)

# Запуск бота
app.poll(debug=True)