from telebot_router import TeleBot
from Services.ClientService import ClientService
from Services.CommandService import CommandService
from Services.MenuService import MenuService
from Services.ProcedureService import ProcedureService
from Services.OrderService import OrderService
from Services.LogFactory import LogFactory
from Multilang import TR

app = TeleBot("Restaurant_Bot")
app.config['api_key'] = '6148540855:AAFNaxGTNxK_H332pSG2eCe4rERBSzO2Q44'

LogFactory.Initialize("bot.log")
logger = LogFactory.logger

ProcedureService.Initialize(app)
TR.Initialize("resources/translations.json")

@app.route('/help')
def help_handler(dict_message):
    user = ClientService.GetUserByContext(dict_message)
    result = CommandService.get_commands_description(user)
    app.send_message(user.chat_id, result)
    logger.info(f'{user.id} - /help')

@app.route('/menu')
def menu_handler(dict_message):
    user = ClientService.GetUserByContext(dict_message)

    if CommandService.check_commands_permissions('/menu', user):
        result = MenuService.ShowMenu()
        app.send_message(user.chat_id, result)

    logger.info(f'{user.id} - /menu')


@app.route('/myorder')
def my_order_handler(dict_message):
    user = ClientService.GetUserByContext(dict_message)

    if CommandService.check_commands_permissions('/myorder', user):
        result = OrderService.GetUserOrder(user)

        if result != None:
            app.send_message(user.chat_id, f"{TR.Get('U5A7B','Your order:',user.language_code)} {result}")
        else:
            message = TR.Get("t32qY","You didn't order anything.",user.language_code)
            app.send_message(user.chat_id,message)

    else:
        app.send_message(user.chat_id, TR.Get("9FKKK", "The command is not available.", user.language_code))


    logger.info(f'{user.id} - /myorder')

@app.route('(?!/).+')
def data_handler(dict_message):
    data = dict_message['text']
    user = ClientService.GetUserByContext(dict_message)

    if not ProcedureService.TryContinueProcedure(data, user):
        app.send_message(user.chat_id, TR.Get("KOo7C", "I don't understand you.", user.language_code))

    logger.info(f'{user.id} - send data - {data}')

@app.route('/add admin')
def add_admin_handler(dict_message):
    user = ClientService.GetUserByContext(dict_message)

    if CommandService.check_commands_permissions('/add admin', user):
        ProcedureService.StartAddAdminProcedure(user)
    else:
        app.send_message(user.chat_id, TR.Get("9FKKK", "The command is not available.", user.language_code))  # такого перевода нет - сделать

    logger.info(f'{user.id} - /addAdmin')

@app.route('/order')
def order_handler(dict_message):
    user = ClientService.GetUserByContext(dict_message)

    if CommandService.check_commands_permissions('/order', user):
        ProcedureService.StartOrderProcedure(user)
    else:
        app.send_message(user.chat_id, TR.Get("9FKKK", "The command is not available.", user.language_code))


    logger.info(f'{user.id} - /order')

# Запуск бота
app.poll(debug=True)