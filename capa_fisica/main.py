from tools.file import get_line, save
from capa_fisica.parser import parser
from capa_fisica.physical import Physical, PhysicalAdmin, Log


def main():
    # if len(argv) < 2 :
    #     raise Exception("Se esperaba la direccion de las instrucciones.")
    
    file_name = "capa_fisica/basic_test.txt" #argv[1]
    with open(file_name, "r") as fd:

        lines = get_line(fd.readlines())
        commands = parser(lines) 
        
        # Create Physical Network
        admin = PhysicalAdmin(Physical())
        admin.add_actions(commands)
        admin.simulate()
        
        print("Saving data...") 
        file_name = file_name[file_name.index("/")+1:]
        for d in admin.network.devices:
            save(d+".txt","solution_to_"+file_name,admin.network.devices[d].log.data)
            # if IMPRIMIR:
            #     print(d,":")
            #     for l in admin.network.devices[d].log.data:
            #         print(" ",l)

        save("all.txt","solution_to_"+file_name,Log.all_data)
        print("Done!")