class ArenaAugment:
    def __init__(self,name='',calculations={},data_values={},desc='',icon_url='',tier='',tool_tip='',apply_on_hit=False,on_hit_effectiveness=1):
        self.name = name
        self.calculations = calculations
        self.data_values = data_values
        self.desc = desc
        self.icon_url = icon_url
        self.tier = tier
        self.tool_tip = tool_tip
        self.apply_on_hit = apply_on_hit
        self.on_hit_effectiveness = on_hit_effectiveness #percentage at which extra on_hit is applied