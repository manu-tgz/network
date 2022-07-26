from sys import argv
from app.network import Network
from app.admin import Admin
from app.tools.file import get_file_name
from app.physical_layer.parser import PhysicalParser
from app.link_layer.parser import LinkParser
from app.net_layer.parser import NetParser


def main():
    if len(argv) < 3 :
        raise Exception("Insert txt address")
    print(argv)
    # Get layer
    layer_number = int(argv[1])
    if layer_number == 1:
        parser = PhysicalParser()
    elif layer_number == 2:
        parser = LinkParser()
    elif layer_number == 3:
        parser = NetParser()
    
    # Get commands from txt 
    file_name = argv[2]
    commands = parser.get_commands_from_txt(file_name)
    
    # Create Physical Network and simulate
    admin = Admin(Network())
    admin.add_actions(commands)
    admin.simulate()
    
    # Save log in txts
    file_name = get_file_name(file_name)
    parser.save_data(file_name, admin.network.devices)

main()