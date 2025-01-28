
import math
import operator as ope

def split_number(number: int | float, debug:bool=False):
    # BROKE THE NUMBER AND SPLIT ITS DECIMAL PLACES ::
    split_number = math.modf(number) if(isinstance(number, float)) else None
    dec_part = split_number[0] if split_number is not None else 0.00
    int_part = split_number[1] if split_number is not None else number
    if(debug is True): 
        print('NUMBER SLICES FROM: %s ↴\n-> int_part: %s\n-> dec_part: %s'    
        %(number, int(int_part), dec_part))
    return (dec_part, int(int_part))
#=====================================================================================================//


def count_decimal_places(dec_part: float | int, int_part: float | int):
    # COUNT HOW MANY DECIMAL PLACES ARE IN THE GIVEN NUMBER AND DIVIDE IT INTO WHOLE PARTS ::
    count_number = str(dec_part).split()
    #print('\ncount_number before anything: %s' %count_number)
    count_number = [''.join(map(str, count_number[0][2:]))]; copy = list()
    for i in count_number[0]: copy.append(int(i))
    #print('ABNT count_number from: -> %s \nplaces copy: %s' %(count_number, copy))
    #print('decimal items in copy: %s' %len(copy))
    return copy
#=====================================================================================================//


def chek_decimal_places(values: list, int_part: int):
    # CONSIDER VALUES IN <object>list() _values[] AND PROCESS ITS VALUES ::    
    
    # -> RESTORE [int(0)] HAS REMOVED FOR THE <calss> math.modf()
    for i in range(2): values.append(int(0))
    #print("'values' after append() method: %s\n" %values)

    if(values[2] > 5 and values[1] < 9):
        values[1] += 1; del(values[2:]); #print('CALUSE: 3_A')
    
    elif(values[2] > 5 and values[1] == 9 and values[0] < 9): 
        values[0] += 1; values[1] = 0; del(values[2:]); #print('CLASUE: 3_B')
    
    elif(values[2] > 5 and values[0] == 9 and values[1] == 9): 
        int_part += 1; values[0] = 0; values[1] = 0; del(values[2:]); #print('CLAUSE: 3_C')

    elif(values[2] < 5): del(values[2:]); #print('CLAUSE: 3_D')
    
    # AS THE NUMBER 5 IS THE DELIMITER BETWEEN THE CLAUSES THAT CONSIDERS THE EVALUATION OF THE NUMBER
    # WITHIN THE DECIMALS, IT'S  NECESSARY  TO APPLY  ZEROS TO THE DECIMAL SO THAT WE CAN EVALUATE ITS 
    # CONDITIONAL CLAUSES. SEE HOW ABNT STANDARDS WORK FOR YOURSELF AT THE LINK:
    # file:///C:/matheus/automations_5.0_Edit/_project_documents/ABNT/REGRA%20DE%20ARREDONDAMENTO%20-%20ABNT%205891.pdf

    elif(values[2] == 5):
 
        if(values[3] != 0 and values[1] < 9): 
            values[1] += 1; del(values[2:]); #print('CLAUSE: 4_A')
        
        elif(values[3] != 0 and values[1] == 9 and values[0] < 9): 
            values[0] += 1; values[1] = 0; del(values[2:]); #print('CLAUSE: 4_B')
        
        elif(values[3] != 0 and values[1] == 9 and values[0] == 9):
            int_part += 1; values[0] = 0; values[1] = 0; del(values[2:]); #print('CLAUSE: 4_C')
        
        elif(values[3] == 0 and (values[1] % 2 == 0)): del(values[2:]); #print('CLAUSE: 4_D')

        elif(values[3] == 0 and (values[1] % 2 != 0) and values[1] < 9):
            values[1] += 1; del(values[2:]); #print('CLAUSE: 4_E')

        elif(values[3] == 0 and (values[1] % 2 != 0) and values[1] == 9 and values[0] < 9):
            values[0] += 1; values[1] = 0; del(values[2:]); #print('CLAUSE: 4_F')
        
        elif(values[3] == 0 and values[1] == 9 and values[0] == 9):
            int_part += 1; values[0] = 0; values[1] = 0; del(values[2:]); #print('CLAUSE: 4_G')

    else: print('The Number given as parameter not correspond the method clauses!'.upper())

    int_part = int(int_part)
    values = ''.join(map(str, values)); values = int(values)
    #print('BEFORE PROCESS:\nint_par: %s && decimals: %s' %(int_part, values))
    new_value = (int_part + (values * 0.01)); new_value = round(new_value, 2)   
    #print(f'AFTER PROCESS -> new_value: {new_value}')
    return new_value
#=====================================================================================================//


def round2(number: float | int, debug:bool=False):
    if(debug is True): 
        print('\n** PERFORMING ROUND ABNT...'+
              '\n----------------------------')
    number_places = split_number(number, debug)
    dec_value = count_decimal_places(number_places[0], number_places[1])
    number = chek_decimal_places(dec_value, number_places[1])
    return number
#=====================================================================================================//
# RESOLUTIONS DEBUG ::

def auto_debug():
    lst_num = [0.342, 0.346, 0.3452, 0.3450, 0.332, 0.336, 0.3352, 
                   0.3350, 0.3050, 0.3150, 0.996, 1.9998, 1.99, 1.0, 2]

    #lst_num = [0.3350, 0.3050, 0.3150, 12.735, 12.737]
    for n in range(len(lst_num)):
        x = round2(lst_num[n])
        print("FINALLY: {:.2f}".format(x))
        print('==========================================')
    input()
#=================================================================================================END//

#AUTO_DEBUG()