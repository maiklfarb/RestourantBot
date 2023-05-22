class Client:
    def __init__(self, id, chat_id, name, username=None, role='client'):
        self.id = id
        self.chat_id = chat_id
        self.name = name
        self.username = username
        self.role = role

        self.procedure = None
        self.order = None
