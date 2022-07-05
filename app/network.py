class Network:
    def __init__(self,signal_time=10):
        self.devices = {}
        self.signal_time = signal_time 
        
    def add_device(self, device):
        self.devices[device.name] = device