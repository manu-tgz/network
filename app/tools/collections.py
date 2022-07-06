def get_diferents_by_index_in_list(list, diferent):
    new_list = []
    for i in range(len(list)):
        if i!= diferent and list[i]!=None:
            new_list.append(list[i])
    return new_list

def get_diferent_by_key_in_dict(dic,key):
    new_list = []
    for i in dic:
        if i!=key:
            new_list.append(dic[i])
    return new_list
    
    