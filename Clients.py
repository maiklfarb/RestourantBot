class Clients:
    def __init__(self):
        self.list = []

    def add_client(self, client):
        if self.find_client(client.id) is None:
            self.list.append(client)

    def find_client(self,id):
        for client in self.list:
            if client.id == id:
                return client
        return None

    def get_client_index(self, id):
        for i in range(len(self.list)):
            if self.list[i].id == id:
                return i
        return -1

    def remove_client(self, id):
        index = self.get_client_index(id)

        if (index != -1):
            del self.list[index]
