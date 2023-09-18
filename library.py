import pandas as pd
from datetime import datetime

from wish_history import WishHistory, WishItem
from name_mapper import map_name, map_common, search_banner_name_by_time

class Feixiaoqiu:
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    @staticmethod
    def read(filepath) -> WishHistory:
        return Feixiaoqiu.read_local(filepath)
    
    @staticmethod
    def read_local(filepath) -> WishHistory:
        character = Feixiaoqiu.read_local_tab(filepath, "角色活动祈愿")
        weapon = Feixiaoqiu.read_local_tab(filepath, "武器活动祈愿")
        standard = Feixiaoqiu.read_local_tab(filepath, "常驻祈愿")
        beginner = Feixiaoqiu.read_local_tab(filepath, "新手祈愿")
                
        return WishHistory(character, weapon, standard, beginner)
        
    @staticmethod
    def read_local_tab(filepath, tabname) -> list[WishItem]:
        df = pd.read_excel(filepath, sheet_name=tabname)

        wish_items: list[WishItem] = []
        for _, row in df.iterrows():
            time = datetime.strptime(row['时间'], Feixiaoqiu.DATE_FORMAT)
            name = str(row['名称'])
            category = str(row['类别'])
            rarity = int(row['星级'])
            wish_id = str(row['祈愿 Id'])
            
            wish_item = WishItem(time, map_name(name), map_common(category), rarity, wish_id)
            wish_items.append(wish_item)
            
        return wish_items
    
    
class PaimonWish:
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    COLUMNS = ['Type', 'Name', 'Time', '⭐', 'Pity', '#Roll', 'Group', 'Banner']
    
    @staticmethod
    def write(wish_history: WishHistory, filepath):
        PaimonWish.write_local(wish_history, filepath)
        
    @staticmethod
    def write_local(wish_history: WishHistory, filepath):
        wish_data = {
            'Character Event': wish_history.character_event,
            'Weapon Event': wish_history.weapon_event,
            'Standard': wish_history.standard,
            "Beginners' Wish": wish_history.beginner
        }
        excel_data = dict([(k, PaimonWish.dump_wish_history(v, k)) for k, v in wish_data.items()])
        
        with pd.ExcelWriter(filepath) as writer:
            for sheet_name, df in excel_data.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    @staticmethod
    def dump_wish_history(wish_items: list[WishItem], wish_type) -> pd.DataFrame:
        wish_lines = []
        
        group_id = 0
        rolls = 0
        pity_4 = 0
        pity_5 = 0
        current_banner = None
        prev_time = None
        
        for wish_item in wish_items:
            banner = search_banner_name_by_time(wish_type, wish_item.time)
            if banner != current_banner:
                group_id = 0
                rolls = 0
                current_banner = banner
                
            if wish_item.time != prev_time:
                group_id += 1
            
            rolls += 1
            pity_4 += 1
            pity_5 += 1
            pity = pity_4 if wish_item.rarity == 4 else pity_5
            
            new_row = {
                'Type': wish_item.category,
                'Name': wish_item.name,
                'Time': wish_item.time.strftime(PaimonWish.DATE_FORMAT),
                '⭐': wish_item.rarity,
                'Pity': pity if wish_item.rarity > 3 else 1,
                '#Roll': rolls,
                'Group': group_id,
                'Banner': current_banner
            }
            
            if wish_item.rarity == 4:
                pity_4 = 0
            elif wish_item.rarity == 5:
                pity_5 = 0
            
            prev_time = wish_item.time
            
            wish_lines.append(new_row)
            
        df = pd.DataFrame(wish_lines, columns=PaimonWish.COLUMNS)
            
        return df