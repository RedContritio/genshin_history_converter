from datetime import datetime
import os
import yaml

script_dir = os.path.dirname(os.path.abspath(__file__))
yaml_file_basepath = os.path.join(script_dir, "name_mapping")

def load_yaml(type):
    path = os.path.join(yaml_file_basepath, f"{type}.yaml")
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.load(f, Loader=yaml.FullLoader)
    
common_name_mapping = load_yaml("common")

character_name_mapping = load_yaml("character")
weapon_name_mapping = load_yaml("weapon")

NAME_MAPPING = {**character_name_mapping, **weapon_name_mapping}

assert len(NAME_MAPPING) == len(character_name_mapping) + len(weapon_name_mapping)


wish_type_name_mapping = load_yaml("wish_type")

BANNER_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def banner_dict_to_item(d):
    return {
        "name": d["name"],
        'type': d['type'],
        'start': datetime.strptime(d['time']['start'], BANNER_DATE_FORMAT),
        'end': datetime.strptime(d['time']['end'], BANNER_DATE_FORMAT),
    }
    
banner_dict_list = load_yaml("banner")
banner_list = [banner_dict_to_item(d) for d in banner_dict_list]

banners_data = {}
for b in banner_list:
    if b['type'] not in banners_data:
        banners_data[b['type']] = []
    banners_data[b['type']].append(b)


def check_names(names):
    for n in set(names):
        if n not in NAME_MAPPING:
            print(f"NAME_MAPPING of '{n}' not found.")

def map_name_by_mapping(name, mapping):
    if name in mapping:
        return mapping[name]
    else:
        raise Exception(f"NAME_MAPPING of '{name}' not found.")

def search_banner_name_by_time(wish_type, time: datetime):
    blist = banners_data[wish_type]
    
    for b in blist:
        if b['start'] <= time <= b['end']:
            return b['name']
    return None

def map_common(name):
    return map_name_by_mapping(name, common_name_mapping)

def map_name(name):
    return map_name_by_mapping(name, NAME_MAPPING)