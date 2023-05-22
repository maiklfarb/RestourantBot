class MenuService:
    menu = [
        {"name": "пицца", 'price': 200},
        {"name": "бургер", 'price': 150},
        {"name": "ургре", 'price': 150},
        {"name": "ургре", 'price': 150},
        {"name": "ургре", 'price': 150},
        {"name": "ургре", 'price': 150},
        {"name": "ургре", 'price': 150},
        {"name": "ургре", 'price': 150},
        {"name": "ургре", 'price': 150},
        {"name": "ургре", 'price': 150}
    ]
    @staticmethod
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
        for menuItem in MenuService.menu:
            text += f"{i}. {menuItem['name']}, {menuItem['price']}р\n"
            i += 1

        return text
    @staticmethod
    def IsMenuItem(name):
        for item in MenuService.menu:
            if item['name'].lower() == name.lower():
                return True
        return False

    @staticmethod
    def OrderDetailsDataHandler(order):
        res = []
        order = order.split(',')
        for item in order:
            if MenuService.IsMenuItem(item) == True:
                res.append(item)
        return res