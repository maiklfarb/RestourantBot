from telebot import TeleBot
from Client import Client
from datetime import datetime
from Procedure import Procedure
from Action import Action
from datetime import datetime
from dbContext import DbContext

app = TeleBot("Restaurant_Bot")
app.config['api_key'] = '5449097213:AAEGC40fY9ccfEPoTF_IIG-wX_Eod1ESl80'
db = DbContext("data")
users = db.clients
menu = [
    {"name": "пицца",'price':200},
    {"name": "бургер",'price':150},
    {"name": "ургре",'price':150},
    {"name": "ургре",'price':150},
    {"name": "ургре",'price':150},
    {"name": "ургре",'price':150},
    {"name": "ургре",'price':150},
    {"name": "ургре",'price':150},
    {"name": "ургре",'price':150},
    {"name": "ургре",'price':150}
]


def log(text):
    print(f"{datetime.now()} -> {text}")

def add_user(id, id_chat, name):
    user = Client(id, id_chat, name)
    users.add_client(user)
    db.SaveChanges()
    log(f'Создан новый пользователь: {user.name} {user.role}')
    return user

def GetUserByContext(dict_message):
    id_chat = dict_message['chat']['id']
    id = dict_message['from']['id']
    name = dict_message['from']['first_name']

    found_user = db.clients.find_client(id)

    if found_user == None:
        found_user = add_user(id, id_chat, name)

    return found_user

def ShowMenu():
    """
    Меню:
    1. Мясо, 1000р
    2. Блюдо, 223р

    ** - жирный в тг
    __ - курсив в тг
    """
    text = "Меню:\n"
    i = 1
    for menuItem in menu:
        text += f"{i}. {menuItem['name']}, {menuItem['price']}р\n"
        i += 1

    return text

@app.route('/help')
def help_handler(dict_message):
    user = GetUserByContext(dict_message)
    app.send_message(user.chat_id, user.Get_Commands())
    log(f'{id} - /help')


@app.route('/menu')
def menu_handler(dict_message):
    user = GetUserByContext(dict_message)

    if user.CheckCommandsPermissions('/menu'):
        app.send_message(user.chat_id, ShowMenu())

    log(f'{id} - /menu')

@app.route('/add admin')
def menu_handler(dict_message):
    user = GetUserByContext(dict_message)

    if user.CheckCommandsPermissions('/add admin'):
        app.send_message(user.chat_id, "команда доступна")
    else:
        app.send_message(user.chat_id, "команда не доступна")

    log(f'{id} - /add admin')

def ask_order_details(chatid):
    app.send_message(chatid, "Перечислите через запятую,что бы вы хотели заказать.")

def ask_addres(chatid):
    app.send_message(chatid, "На какой адрес доставить заказ?")

def ask_time(chatid):
    app.send_message(chatid, "В какое время вы хотите чтобы доставили?")

def IsMenuItem(name):
    for item in menu:
        if item['name'].lower() == name.lower():
            return True
    return False

def order_details_data_handler(order):
    res = []
    order = order.split(',')
    for item in order:
        if IsMenuItem(item) == True:
            res.append(item)
    return res

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

    user = db.clients.find_client(chatid)
    user.order = {'address':address,'details':details,'time':time}
    app.send_message(chatid, f"Процедура оформления заказа окончена, доставка будет доставленна в {time.time()} на адрес: {address}.")

@app.route('/order')
def menu_handler(dict_message):
    user = GetUserByContext(dict_message)

    if user.CheckCommandsPermissions('/order'):
        procedure = Procedure('оформление заказа', user.chat_id,order_procedure_end_handler)
        action1 = Action('детали', ask_order_details, order_details_data_handler)
        action2 = Action('адрес', ask_addres, address_data_handler)
        action3 = Action('время', ask_time, time_data_handler)
        procedure.actions = [action1, action2,action3]
        user.procedure = procedure
        procedure.StartProcedure()
    else:
        app.send_message(user.chat_id, "команда не доступна")

    log(f'{id} - /add admin')

@app.route('/myorder')
def menu_handler(dict_message):
    user = GetUserByContext(dict_message)

    if user.CheckCommandsPermissions('/myorder'):
        if user.order != None:
            app.send_message(user.chat_id, f"Ваш заказ: {user.order}")
        else:
            app.send_message(user.chat_id, "Вы нечего не заказывали.")
    else:
        app.send_message(user.chat_id, "команда не доступна")

@app.route('(?!/).+')
def data_handler(dict_message):
    data = dict_message['text']
    user = GetUserByContext(dict_message)

    if (user.procedure is not None):
        if user.procedure.ContinueProcedure(data) == False:
            user.procedure = None
    else:
        app.send_message(user.chat_id, "Я вас не понимаю")

# Запуск бота
app.poll(debug=True)