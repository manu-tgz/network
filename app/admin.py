from queue import PriorityQueue
      
class Admin:
    def __init__(self, network):
        self.queue = PriorityQueue()
        self.network = network
        self.global_time = 0 
    
    def add_actions(self,list):
        for i in list:
            self.queue.put(i)
            
    def simulate(self):
        while not self.queue.empty():
            t, event = self.queue.get() 
            self.global_time = t 
            more_events = event.execute(self.network)
            if not more_events is None:
                self.add_actions(more_events)     