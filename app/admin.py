from queue import PriorityQueue
      
class Admin:
    def __init__(self, network):
        self.queue = PriorityQueue()
        self.network = network
        # TODO: This is a synchronous but it would be ideal to use a asynchronous
        # # For more information https://docs.python.org/es/3.8/library/asyncio-queue.html
        
    def add_actions(self,list):
        for i in list:
            self.queue.put(i)
            
    def simulate(self):
        while not self.queue.empty():
            t, event = self.queue.get() 
            
            more_events = event.execute(self.network)
            if not more_events is None:
                self.add_actions(more_events)     