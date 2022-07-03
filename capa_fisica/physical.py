from queue import PriorityQueue


class Log:
    all_data = [] 
    def __init__(self):
        self.data = []
    def log(self, time ,device , action ,data, status):
        s = " ".join([str(time),device,action,str(data), status])
        self.data.append(s)
        self.all_data.append(s)
    
    def __call__(self, time ,device , action ,data, status):
        self.log(time ,device , action ,data, status)

class Process:
    def __init__(self, time ):
        self.time = time
    def execute(self):
        pass

class CreateDevice(Process):
    def __init__(self, time, device, args ):
        super().__init__(time)
        self.device = device
        self.args= args
        
    def execute(self, network):
        device = self.device(*self.args)
        network.add_device(device)
        
class PhysicalAdmin:
    def __init__(self, network):
        self.queue = PriorityQueue()
        self.network = network
        self.global_time = 0 
    
    def add_actions(self,list):
        for i in list:
            self.queue.put(i)
            
    def simulate(self):
        while not self.queue.empty():
            event = self.queue.get() 
            self.global_time = event.time 
            event.execute(self.network)    

class Physical:
    def __init__(self):#, signal_time=10):
        self.devices = {}
        
    def add_device(self, device):
        self.devices[device.name] = device
        
        
  



