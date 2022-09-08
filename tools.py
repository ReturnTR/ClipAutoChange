import json
def save_json(data,filename):
    """将数据保存在json文件中"""

    data = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(data)

def get_json(json_file):
    with open(json_file, 'r', encoding='utf-8')as file:
        data=json.loads(file.read())
    return data

def cut_data_ave(data,ave_len=3):
    """
    根据长度平分
    返回的data比原来多一维
    list和str均可
    """
    new_data=[]
    index=0
    while index+ave_len<len(data):
        new_data.append(data[index:index+ave_len])
        index+=ave_len
    new_data.append(data[index:])
    return new_data

def get_module_functions(module):
    return [i for i in dir(module) if i[:2]!="__"]