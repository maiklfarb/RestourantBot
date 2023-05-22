from datetime import datetime
from Services.ClientService import ClientService
from Procedure import Procedure
from Action import Action
from Services.MenuService import MenuService

class IProcedure:
    def __init__(self, app):
        self.app = app

class AddAdminProcedure(IProcedure):
    ACTION_NAME_CHATID = 'id'

    def __init__(self, app):
        super(AddAdminProcedure, self).__init__(app)

    def ask_chatid(self, chatid):
        self.app.send_message(chatid, "укажите чат айди пользователя,которого нужно сделать администратором.")

    def chatid_handler(self, text):
        try:
            return int(text)
        except:
            return -1

    def end_handler(self, actions, chatid):
        new_admin_chatid = ""

        for action in actions:
            if action.name == AddAdminProcedure.ACTION_NAME_CHATID:
                new_admin_chatid = action.params

        new_admin = ClientService.db.clients.find_client(new_admin_chatid)

        if new_admin != None:
            ClientService.AddAdmin(new_admin)

            self.app.send_message(chatid,
                                  f"Роль пользователя {new_admin.name} успешно изменена на {new_admin.role}.")

        else:
            self.app.send_message(chatid,
                                  f"Пользователь с chat_id {new_admin_chatid} не найден.")

class OrderProcedure(IProcedure):
    ACTION_NAME_DETAILS = "детали"
    ACTION_NAME_TIME = "время"
    ACTION_NAME_ADDRESS = "адрес"

    def __init__(self, app):
        super(OrderProcedure, self).__init__(app)

    def ask_order_details(self, chatid):
        self.app.send_message(chatid, "Перечислите через запятую,что бы вы хотели заказать.")

    def ask_addres(self,chatid):
        self.app.send_message(chatid, "На какой адрес доставить заказ?")

    def ask_time(self,chatid):
        self.app.send_message(chatid, "В какое время вы хотите чтобы доставили?")

    def order_procedure_end_handler(self,actions, chatid):
        details = []
        address = ""
        time = []
        for action in actions:
            if action.name == OrderProcedure.ACTION_NAME_DETAILS:
                details = action.params
            elif action.name == OrderProcedure.ACTION_NAME_ADDRESS:
                address = action.params
            elif action.name == OrderProcedure.ACTION_NAME_TIME:
                time = action.params

        user = ClientService.db.clients.find_client(chatid)
        user.order = {'address': address, 'details': details, 'time': time}
        self.app.send_message(chatid,
                         f"Процедура оформления заказа окончена, доставка будет доставленна в {time.time()} на адрес: {address}.")

    def time_data_handler(self, textTime):
        # "13:12"
        orderTime = datetime.now()
        orderTime = datetime(year=orderTime.year, hour=orderTime.hour + 1, minute=orderTime.minute,
                             month=orderTime.month,
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

    def address_data_handler(self, address):
        return address

class ProcedureService:
    orderProcedure = None
    addAdminProcedure = None

    @staticmethod
    def Initialize(app):
        ProcedureService.orderProcedure = OrderProcedure(app)
        ProcedureService.addAdminProcedure = AddAdminProcedure(app)

    @staticmethod
    def StartOrderProcedure(user):
        procedure = Procedure('оформление заказа', user.chat_id, ProcedureService.orderProcedure.order_procedure_end_handler)
        action1 = Action(OrderProcedure.ACTION_NAME_DETAILS, ProcedureService.orderProcedure.ask_order_details, MenuService.OrderDetailsDataHandler)
        action2 = Action(OrderProcedure.ACTION_NAME_ADDRESS, ProcedureService.orderProcedure.ask_addres, ProcedureService.orderProcedure.address_data_handler)
        action3 = Action(OrderProcedure.ACTION_NAME_TIME, ProcedureService.orderProcedure.ask_time, ProcedureService.orderProcedure.time_data_handler)
        procedure.actions = [action1, action2, action3]
        user.procedure = procedure
        procedure.StartProcedure()

    @staticmethod
    def StartAddAdminProcedure(user):
        procedure = Procedure('добавление админа', user.chat_id, ProcedureService.addAdminProcedure.end_handler)
        action1 = Action(AddAdminProcedure.ACTION_NAME_CHATID, ProcedureService.addAdminProcedure.ask_chatid, ProcedureService.addAdminProcedure.chatid_handler)
        procedure.actions = [action1]
        user.procedure = procedure
        procedure.StartProcedure()

    @staticmethod
    def TryContinueProcedure(data, user):
        if (user.procedure is not None):
            if user.procedure.ContinueProcedure(data) == False:
                user.procedure = None
            return True
        return False

