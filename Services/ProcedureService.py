from datetime import datetime
from Services.ClientService import ClientService
from Procedure import Procedure
from Action import Action
from Services.MenuService import MenuService
from Services.LogFactory import LogFactory
from Multilang import TR

class IProcedure:
    def __init__(self, app):
        self.app = app

class AddAdminProcedure(IProcedure):
    ACTION_NAME_CHATID = 'id'

    def __init__(self, app):
        super(AddAdminProcedure, self).__init__(app)
        self.logger = LogFactory.logger

    def ask_chatid(self, chatid):   # TODO - сделать так, чтобы в процедурурах передавался пользователь
        user = ClientService.db.clients.find_client(chatid)
        self.app.send_message(chatid, TR.Get("zPJ53", "Specify the chat ID of the user you want to make an administrator.", user.language_code))

    def chatid_handler(self, text):
        try:
            return int(text)
        except:
            self.logger.warning(f"AddAdminProcedure.chatid_handler - invalid data was sent {text}")
            return -1

    def end_handler(self, actions, chatid):
        new_admin_chatid = ""
        user = ClientService.db.clients.find_client(chatid)

        for action in actions:
            if action.name == AddAdminProcedure.ACTION_NAME_CHATID:
                new_admin_chatid = action.params

        new_admin = ClientService.db.clients.find_client(new_admin_chatid)

        if new_admin != None:
            ClientService.AddAdmin(new_admin)

            self.app.send_message(chatid,
                                  f"{TR.Get('5wNWk','User role',user.language_code)} {new_admin.name} {TR.Get('5wNWk','successfully changed to',user.language_code)} {new_admin.role}.")

        else:
            self.app.send_message(chatid,
                                  f"{TR.Get('GAV27','User with chat_id',user.language_code)} {new_admin_chatid} {TR.Get('rl4LA','not found.',user.language_code)}.")

class OrderProcedure(IProcedure):
    ACTION_NAME_DETAILS = "details"
    ACTION_NAME_TIME = "time"
    ACTION_NAME_ADDRESS = "address"

    def __init__(self, app):
        super(OrderProcedure, self).__init__(app)
        self.logger = LogFactory.logger

    def ask_order_details(self, chatid):
        self.app.send_message(chatid, "List, separated by commas, what you would like to order.")

    def ask_addres(self,chatid):
        self.app.send_message(chatid, "To which address should the order be delivered?")

    def ask_time(self,chatid):
        self.app.send_message(chatid, "What time do you want it delivered?")

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
                         f"The order processing procedure is over, the delivery will be delivered to {time.time()} the address: {address}.")
        LogFactory.logger.info(f'{chatid} placed an order, {address}, {details}, {time}')

    def time_data_handler(self, textTime):
        # "13:12"
        orderTime = datetime.now()
        hours = orderTime.hour
        day = orderTime.day

        if (hours >= 23):
            hours = 0
            day += 1

        orderTime = datetime(year=orderTime.year, hour=hours, minute=orderTime.minute,
                             month=orderTime.month,
                             day=day)

        try:
            if textTime.lower() == "now" or textTime.lower() == "сейчас":
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
            self.logger.warning(f"OrderProcedure.time_data_handler - sent the time for which we will not be able to make delivery - {textTime}")
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
        procedure = Procedure('making an order', user.chat_id, ProcedureService.orderProcedure.order_procedure_end_handler)
        action1 = Action(OrderProcedure.ACTION_NAME_DETAILS, ProcedureService.orderProcedure.ask_order_details, MenuService.OrderDetailsDataHandler)
        action2 = Action(OrderProcedure.ACTION_NAME_ADDRESS, ProcedureService.orderProcedure.ask_addres, ProcedureService.orderProcedure.address_data_handler)
        action3 = Action(OrderProcedure.ACTION_NAME_TIME, ProcedureService.orderProcedure.ask_time, ProcedureService.orderProcedure.time_data_handler)
        procedure.actions = [action1, action2, action3]
        user.procedure = procedure
        procedure.StartProcedure()

    @staticmethod
    def StartAddAdminProcedure(user):
        procedure = Procedure('add admin', user.chat_id, ProcedureService.addAdminProcedure.end_handler)
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

