from app.physical_layer.parser import PhysicalParser
from app.tools.file import  save
from devices import Link_log

class LinkParser(PhysicalParser):

    def save_data(file_name, devices):
        print("Saving data...") 
        for d in devices:
            save(d+".txt","output/solution_"+file_name,devices[d].log.data)
            save(d+"_data.txt","output/solution_"+file_name,devices[d].log.link_data)
    
        save("all.txt","output/solution_"+file_name,Link_log.all_data)
        save("data_all.txt","output/solution_"+file_name,Link_log.all_link_data)
        print("OK")
