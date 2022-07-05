from sys import argv
from app.link_layer.parser import LinkParser
from app.network import Network
from app.admin import Admin
from app.tools.file import get_file_name

def main():
    # if len(argv) < 2 :
    #      raise Exception("Se esperaba la direccion de las instrucciones.")

    # Get commands from txt
    file_name = "network/test.txt" #argv[1]
    parser = LinkParser()
    commands = parser.get_commands_from_txt(file_name)
    
    # Create Physical Network and simulate
    admin = Admin(Network())
    admin.add_actions(commands)
    admin.simulate()
    
    # Save log in txts
    file_name = get_file_name(file_name)
    parser.save_data(file_name, admin.network.devices)

