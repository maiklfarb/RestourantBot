from Clients import Clients
from Client import Client
import os.path

class DbContext:
    def __init__(self, connection):
        self.connection = connection # путь к папке
        self.clients = Clients() # dbSet (отдельная таблица = отдельный dbset)
        self.clientsColumns = {"id": 0, "chat_id": 1, "name": 2, "username": 3, "role": 4, "language_code": 5}
        self.Initialize()


    def SerializeClient(self, client):
        result = f"{client.id},{client.chat_id},{client.name},{client.username},{client.role},{client.language_code}"
        return result

    def DeserializeClient(self, stringClient):
        stringClient = stringClient.split(',')
        client = Client(int(stringClient[self.clientsColumns['id']]),
                        int(stringClient[self.clientsColumns['chat_id']]),
                        stringClient[self.clientsColumns['name']],
                        stringClient[self.clientsColumns['language_code']],
                        stringClient[self.clientsColumns['username']],
                        stringClient[self.clientsColumns['role']])

        return client

    def LoadData(self):
        with open(f"{self.connection}/{Clients.__name__}.csv", 'r') as file:
            data = file.read()
            lines = data.split('\n')
            del lines[0]

            for line in lines:
                client = self.DeserializeClient(line)
                self.clients.add_client(client)

    def SaveChanges(self):
        clients = self.clients.list
        result = self.GetColumnsString() + "\n"

        for client in clients:
            result += self.SerializeClient(client) + "\n"

        result = result.strip('\n')

        with open(f"{self.connection}/{Clients.__name__}.csv", 'w') as file:
            file.write(result)

    def GetColumnsString(self):
        result = ""

        for k in self.clientsColumns.keys():
            result += f"{k},"

        result = result.strip(',')

        return result

    def Initialize(self):
        if not os.path.isfile(f"{self.connection}/{Clients.__name__}.csv"):
            with open(f"{self.connection}/{Clients.__name__}.csv", 'w') as file:
                file.write(self.GetColumnsString())
        else:
            self.LoadData()
