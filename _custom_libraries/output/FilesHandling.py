
# -> Built-in Modules, External Resources and Robot Modules ::
import yaml
import operator as ope

# -> Custom Modules has created to the Porject ::
from utilities.AbntRound import round2

class ExternalFilesHandling:
    def __init__(self):
        # Default file to this class startup...
        self.this_path:str = 'default'
        return
    
    @classmethod
    def set_file_path(self, new_path:str, show:bool=True):
        # Ternary Expression with Attribute Building COmpreension ::
        if(show is True): print('\n❕ <def> set_file_path: ' + new_path + '\n')
        self.this_path = new_path
        return
    
    @classmethod
    def read_file(self) -> dict:
        with open(self.this_path, 'r') as read_file:
            attribures = yaml.safe_load(read_file)
            return attribures
    
    @classmethod
    def update_file(self, file:dict, key:str, new_value:object, set:bool= True, add:bool= False):
        # CHECK FOR TYPE AND SET UP THE 'new_value' 
        # AS THEIR OWN DATA TYPE VALUE ::
        if((isinstance(file[key], float)) and (new_value >= int())):
            if(set is True): file[key] = round2(new_value) if(ope.gt(new_value, float(0))) else float(0)
            elif(add is True): calc: float = ope.add(file[key], new_value); file[key] = round2(calc)
        
        elif((isinstance(file[key], float)) and (new_value < int())):
            if(set is True): file[key] = round(round(new_value, 3), 2)
            elif(add is True): calc: float = ope.add(file[key], new_value); file[key] = round(calc, 2)

        elif(isinstance(file[key], int)):
            if(set is True): file[key] = int(new_value)
            elif(add is True): calc: int = ope.add(file[key], int(new_value)); file[key] = calc

        elif(isinstance(file[key], (bool, dict, list))):
            file[key] = new_value
        
        else: print("NO OPTION FOR OUTPUT UPDATING HAS BEEN CONTEMPLATED FOR THE <def>:update_file BOOELAN STATEMENTS!" +
                    "\nCHECK FOR THE PARAMETERS AND THEIR RESPECTLY VALUES HAS PASSED AS ARGUMENTS TO THIS FUNCTION.")
        return

    @classmethod
    def write_on_file(self, contents: object = None):
        with open(self.this_path, 'w') as dump_file:
            yaml.safe_dump(contents, dump_file, line_break=True, 
                           explicit_start=True, explicit_end= True)
        return

    @classmethod
    def print_file(self, contents: dict):
        for elem in contents.keys():
            if(not isinstance(contents[elem], dict)):
                print('%s: %s' %(elem, contents[elem]))
            else:
                sub_elem = list(contents[elem])
                for ee in range(len(sub_elem)):
                    if(ope.eq(ee, int(0))): print('-> %s' %elem)
                    print(' - %s: %s' %(sub_elem[ee], 
                        contents[elem][str(sub_elem[ee])]))
        print('\n')
        return
    
    @classmethod
    def reset_output(self, file:dict):
        # CHECK FOR SETTINGS DATA TYPE -> (float, dict, int) 
        # AND RESET THEIR VALUE ACCORDING TO THEIR DATA TYPE
        for elem in file.keys():
            if(str(elem) not in ('old_cashier_serial_code', 'cashier_serial_code')):
                if(isinstance(file[elem], float)):
                    file[elem] = float(0)
                elif(isinstance(file[elem], dict)):
                    sub_elem = list(file[elem])
                    for ee in range(len(sub_elem)):
                        file[elem][str(sub_elem[ee])] = float(0) 
                elif(isinstance(file[elem], int)): file[elem] = int()
                elif(isinstance(file[elem], list)): file[elem] = [None]
                else: pass # ¡Escape Clause! -> It ignores another data types.
            else: continue
        return