class Process:
    def __init__(self, time ):
        self.time = time
    def execute(self, network):
        pass
    def __lt__(self, other):
        return True