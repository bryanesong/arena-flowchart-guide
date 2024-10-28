class ArenaChampion:
    def __init__(self,champion_name = '',arena_ability_changes={},original_abilities={},photo_url='',melee=True):
        self.photo_url = photo_url
        self.champion_name = champion_name
        self.arena_ability_changes = arena_ability_changes #dictionary of 'ability name':[list of ability changes']

        self.original_abilities = original_abilities #this is to be left undeveloped for now
    
    def set_name(self,name: str):
        self.champion_name= str(name)

    def add_single_ability_changes(self,ability_name: str,ability_changes: list[str]):
        #if ability name already exists, overwrite with new data
        self.arena_ability_changes[ability_name] = ability_changes
        
        '''
        #below code is incase we want to union join new incoming ability data instead

        if ability_name not in self.arena_ability_changes.keys():
            self.arena_ability_changes[ability_name] = ability_changes
        else:
            self.arena_ability_changes[ability_name] = list(self.arena_ability_changes[ability_name] | ability_changes)
        '''

    def __str__(self)-> str:
        print('# of abilities',len(self.arena_ability_changes))
        res =''
        res+=self.champion_name+'\n'
        for ability, changes in self.arena_ability_changes.items():
            res+=ability+'\n'
            for change in changes:
                res+='\t'+change+'\n'
        print(res)
        return res

    def __dict__(self)->dict:
        #will export as dictionary with the format: {Name : {Ability: Ability_Changes}}
        res = {}
        res[self.champion_name] = self.arena_ability_changes
        return res
        
    

    
