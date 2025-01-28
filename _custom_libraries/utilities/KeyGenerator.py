
import operator as ope
from random import randrange as rr, randint as rint

def create_number_key(numeric:bool = False) -> str|int:
    dict_id = list()
    for i in range(0, 5):
        _num = rr(1, 9); dict_id.append(_num) #print(f"'index_id': {dict_id}")
        if i >= 1 and dict_id[-2] == _num:
            loop: bool = True
            while loop: _num = rr(1, 9); loop = False if _num != dict_id[-2] else True
            dict_id[-1] = _num
        else: continue
    dict_id = ''.join(map(str, dict_id))
    print('Key generated: %s' %dict_id)
    return dict_id if numeric is False else int(dict_id)


def create_word_key():
    letters:list = ['a', 'b', 'c', 'd', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']
    name = list()
    def Force_Choice(obj:list):
        count:int = 0
        while True:
            choice:str = letters[rint(0, (len(letters)-1))]
            if(choice not in obj): obj.append(choice); count = 0; break
            else: count = ope.iadd(count, int(1))
            # Security clause to the total break up!
            if(ope.eq(count, int(100))): 
                print("The Recursion has been exceeded!"); break
        return obj
    
    while ope.lt(len(name), int(4)):
        choice:str = letters[rint(0, (len(letters)-1))]
        (name.append(choice) if(ope.eq(len(name), int(0))
                                or (choice not in name)) else Force_Choice(name))
        pass
    print("Look at the Final Result for 'name' range: %s" %(name))
    new_name:str = ''.join(map(str, name[:]))
    print("Randomic literal word: '%s'" %new_name)
    return new_name