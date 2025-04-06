class Memory:
    def __init__(self):
        self.store = {}

    def save(self, farmer, recommendation):
        self.store[farmer] = recommendation

    def recall(self, farmer):
        return self.store.get(farmer, "No record found.")

memory = Memory()
