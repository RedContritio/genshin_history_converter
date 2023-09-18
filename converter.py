import pandas as pd
import argparse

from name_mapper import map_name, map_common
from datetime import datetime

from wish_history import WishItem
from library import Feixiaoqiu, PaimonWish

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="输入的 Excel 文件路径")
    parser.add_argument("--format", choices=["feixiaoqiu", "paimon_wish"], default="feixiaoqiu", help="输出格式，默认为 'feixiaoqiu'")

    args = parser.parse_args()

    wish_history = Feixiaoqiu.read(args.input_file)

    if args.format == "feixiaoqiu":
        for wish_item in wish_history.character_event:
            print(wish_item)
            break
    elif args.format == "paimon_wish":
        PaimonWish.write(wish_history, "output.xlsx")
        
