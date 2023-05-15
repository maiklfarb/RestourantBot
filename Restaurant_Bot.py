from telebot_router import TeleBot
from Procedure import Procedure
from Action import Action
from datetime import datetime
from Services.UserService import UserService
from Services.CommandService import CommandService
from Services.MenuService import MenuService
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


@app.route('/help')
def help_handler(dict_message):
    user = UserService.GetUserByContext(dict_message)
    result = CommandService.get_commands_description(user)
    app.send_message(user.chat_id, result)
    logger.info(f'{user.id} - /help')
@app.route('/menu')
def menu_handler(dict_message):
    user = UserService.GetUserByContext(dict_message)

    if CommandService.CheckCommandsPermissions('/menu', user):
        result = MenuService.ShowMenu()
        app.send_message(user.chat_id, result)

    logger.info(f'{user.id} - /menu')

@app.route('/add admin')
def add_admin_handler(dict_message):
    user = UserService.GetUserByContext(dict_message)

    if CommandService.CheckCommandsPermissions('/add admin', user):
        app.send_message(user.chat_id, "команда доступна")
    else:
        app.send_message(user.chat_id, "команда не доступна")

    logger.info(f'{user.id} - /add admin')

def ask_order_details(chatid):
    app.send_message(chatid, "Перечислите через запятую,что бы вы хотели заказать.")

def ask_addres(chatid):
    app.send_message(chatid, "На какой адрес доставить заказ?")

def ask_time(chatid):
    app.send_message(chatid, "В какое время вы хотите чтобы доставили?")





def address_data_handler(address):
    return address

def time_data_handler(textTime):
    # "13:12"
    orderTime = datetime.now()
    orderTime = datetime(year=orderTime.year, hour=orderTime.hour + 1, minute=orderTime.minute, month=orderTime.month,
                         day=orderTime.day)

    try:
        if textTime.lower() == "сейчас":
            raise ValueError()

        nums = textTime.split(':')
        hours = int(nums[0])
        minutes = int(nums[1])

        maybeOrderTime = datetime(year=orderTime.year, hour=hours, minute=minutes, month=orderTime.month,
                                  day=orderTime.day)

        if (orderTime <= maybeOrderTime):
            orderTime = maybeOrderTime
        else:
            raise ValueError()

    except ValueError:
        pass

    return orderTime
def order_procedure_end_handler(actions, chatid):
    details = []
    address = ""
    time = []
    for action in actions:
        if action.name == 'детали':
            details = action.params
        elif action.name == 'адрес':
            address = action.params
        elif action.name == 'время':
            time = action.params

    user = UserService.db.clients.find_client(chatid)
    user.order = {'address':address,'details':details,'time':time}
    app.send_message(chatid, f"Процедура оформления заказа окончена, доставка будет доставленна в {time.time()} на адрес: {address}.")

@app.route('/order')
def order_handler(dict_message):
    user = UserService.GetUserByContext(dict_message)

    if CommandService.CheckCommandsPermissions('/order', user):
        procedure = Procedure('оформление заказа', user.chat_id,order_procedure_end_handler)
        action1 = Action('детали', ask_order_details, MenuService.order_details_data_handler)
        action2 = Action('адрес', ask_addres, address_data_handler)
        action3 = Action('время', ask_time, time_data_handler)
        procedure.actions = [action1, action2,action3]
        user.procedure = procedure
        procedure.StartProcedure()
    else:
        app.send_message(user.chat_id, "команда не доступна")

    logger.info(f'{user.id} - /add admin')

@app.route('/myorder')
def my_order_handler(dict_message):
    user = UserService.GetUserByContext(dict_message)

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
    user = UserService.GetUserByContext(dict_message)

    if (user.procedure is not None):
        if user.procedure.ContinueProcedure(data) == False:
            user.procedure = None
    else:
        app.send_message(user.chat_id, "Я вас не понимаю")

# Запуск бота
app.poll(debug=True)