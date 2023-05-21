from telebot_router import TeleBot
from Services.ClientService import ClientService
from Services.CommandService import CommandService
from Services.MenuService import MenuService
from Services.ProcedureService import ProcedureService
import logging

# Уровни логирования:
# Debug - логируется только тогда, когда нажимаешь на жучка
# Info - обычная информация
# Warning - предупруждение
# Error - ошибка (в основном в try/except)
# Critical - критическая ошибка

#logging.basicConfig(level=logging.INFO, filename="bot.log",filemode="w",
#                    format="%(asctime)s %(levelname)s %(message)s")

# Создаем объект логгера
logger = logging.getLogger()

# Устанавливаем уровень логирования
logger.setLevel(logging.INFO)

# Создаем обработчик для записи в файл
file_handler = logging.FileHandler("bot.log")
file_handler.setLevel(logging.INFO)

# Создаем обработчик для вывода в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Создаем форматтер для сообщений логгера
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Добавляем форматтер к обоим обработчикам
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Добавляем оба обработчика к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)

app = TeleBot("Restaurant_Bot")
app.config['api_key'] = '6148540855:AAFNaxGTNxK_H332pSG2eCe4rERBSzO2Q44'

ProcedureService.Initialize(app)

@app.route('/help')
def help_handler(dict_message):
    user = ClientService.GetUserByContext(dict_message)
    result = CommandService.get_commands_description(user)
    app.send_message(user.chat_id, result)
    logger.info(f'{user.id} - /help')

@app.route('/menu')
def menu_handler(dict_message):
    user = ClientService.GetUserByContext(dict_message)

    if CommandService.CheckCommandsPermissions('/menu', user):
        result = MenuService.ShowMenu()
        app.send_message(user.chat_id, result)

    logger.info(f'{user.id} - /menu')


@app.route('/myorder')
def my_order_handler(dict_message):
    user = ClientService.GetUserByContext(dict_message)

    if CommandService.CheckCommandsPermissions('/myorder', user):
        if user.order != None:
            app.send_message(user.chat_id, f"Ваш заказ: {user.order}")
        else:
            app.send_message(user.chat_id, "Вы нечего не заказывали.")
    else:
        app.send_message(user.chat_id, "команда не доступна")

@app.route('(?!/).+')
def data_handler(dict_message):
    data = dict_message['text']
    user = ClientService.GetUserByContext(dict_message)

    if not ProcedureService.TryContinueProcedure(data, user):
        app.send_message(user.chat_id, "Я вас не понимаю")

@app.route('/add admin')
def add_admin_handler(dict_message):
    user = ClientService.GetUserByContext(dict_message)

    if CommandService.CheckCommandsPermissions('/add admin', user):
        ProcedureService.StartAddAdminProcedure(user)
    else:
        app.send_message(user.chat_id, "команда не доступна")

    logger.info(f'{user.id} - /addAdmin')

@app.route('/order')
def order_handler(dict_message):
    user = ClientService.GetUserByContext(dict_message)

    if CommandService.CheckCommandsPermissions('/order', user):
        ProcedureService.StartOrderProcedure(user)
    else:
        app.send_message(user.chat_id, "команда не доступна")

    logger.info(f'{user.id} - /addAdmin')

# Запуск бота
app.poll(debug=True)