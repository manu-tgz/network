from app.physical_layer.devices import *

class Link_log(Log):
    all_link_data = []
    link_data = []

    def log_link(self, string):
        self.link_data.append(string)
        self.all_link_data.append(string)