

class WishItem:
    def __init__(self, time, name, category, rarity, wish_id):
        self.time = time
        self.name = name
        self.category = category
        self.rarity = rarity
        self.wish_id = wish_id

    def __str__(self):
        return f"时间: {self.time}, 名称: {self.name}, 类别: {self.category}, 星级: {self.rarity}, 祈愿 Id: {self.wish_id}"


class WishHistory:
    def __init__(self, character_event: list[WishItem] = [], weapon_event: list[WishItem] = [], standard: list[WishItem] = [], beginner: list[WishItem] = []) -> None:
        self.character_event = character_event
        self.weapon_event = weapon_event
        self.standard = standard
        self.beginner = beginner
        
    