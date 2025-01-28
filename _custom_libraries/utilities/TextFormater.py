import operator as ope

def remove_punctuation(string_text:str, rplc:str= "", punct:tuple = None, debug:bool=True) -> str:
    # initializing string
    cache = string_text if string_text is not None else 'IS NULL'
    string_text = 'IS NULL' if string_text is None else string_text
    
    punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~''' if(punct is None) else punct
    for c in string_text:
        if c in punctuation:
            string_text = string_text.replace(c, rplc)
        else: continue

    # printing result
    if(debug is True): print("THE CODE: '%s' HAS BEEN REPLACED TO': %s" %(cache, string_text))
    return string_text



def format_fields(
        __max_length:int, 
        /,
        str_fields:tuple[str, ...]|list, 
        separator:str= ' ',
        to_the_end:str= '',
        del_punctuation:bool= False,
        punctuation:tuple = ('$',),
        length_error:bool= True, debug:bool= False,
        split_text:tuple[bool, str] = (False, 'spliter char')) -> tuple:
    
    _copy = list()
    new_field:str = ''

    for i in range(len(str_fields)):
        if(del_punctuation is True):
            new_field = remove_punctuation(str_fields[i], punct=punctuation, debug= debug)
        else: new_field = str_fields[i]

        if(split_text[0] is True):
            new_field = spliter(split_text[1], text= str(new_field), debug= debug)
        else: pass

        letters_count = new_field.__len__()
        if(__max_length > letters_count): calc = ope.sub(__max_length, letters_count)
        else: 
            if(length_error is True): 
                print("❌[FunctionError]¡\n__max_length' must be highligth than 'message' length")
            raise ValueError()
        adjust = list()

        for e in range(calc): adjust.append(separator)
        adjust = ''.join(map(str, adjust))

        if(debug is True): print('adjust: %s' %(adjust.replace('', '.'),))
        formating:str = (new_field + '{}{}'.format(to_the_end, adjust))
        _copy.append(formating)

    if(debug is True): 
        for k in range(len(_copy)): print('\n_copy[%s]: %s' %(k, str(_copy[k]).replace('', '.')))
    return tuple(_copy)



def format_space(__max_length:int, 
                 expression:str, 
                 separator:str=' ',
                 to_the_end:str= ':') -> str:
    
    adjust = list(); calc:int = 0; new_expr:str = ''
    if(__max_length > expression.__len__()):
        calc = ope.sub(__max_length, expression.__len__())
    else: 
        print("❌[FunctionError]¡\n__max_length' must be highligth than 'message' length")
        raise ValueError()
    
    for e in range(calc): adjust.append(separator)
    new_expr = str(expression
                    + (to_the_end if(to_the_end in (':', ';', ' =')) else '')
                    + '{}'.format(''.join(map(str, adjust))))
    return new_expr



def format_keyValues(__max_length:int, /, mapping:dict = {}, separator:str = ' ') -> tuple:
    _copy = list(); 
    for elem in mapping.keys():
        count = len(str(elem))
        if(__max_length > count): calc = ope.sub(__max_length, count)
        else: 
            print("❌[FunctionError]¡\n__max_length' must be highligth than 'message' length")
            raise Exception()
        adjust = list()

        for e in range(calc):
            adjust.append(separator)
        adjust = ''.join(map(str, adjust))

        replc = remove_punctuation(elem, " ", debug= False)
        formating:str = ('{}: {} {}'.format(replc.title(), adjust, mapping[str(elem)]))
        _copy.append(formating)
    return tuple(_copy)



def expand(delimiter:str= ' ', size:int= 8) -> str:
    str_space:list = list()
    for i in range(size): str_space.append(delimiter)
    return ''.join(map(str, str_space))



def create_line(
        space:int, 
        char:str='-', 
        break_line:bool=False, 
        double_break:bool=False, 
        to_the_end:bool=False,
        cmd:str='print | return') -> str|None:
    
    """Create a simple line inside of text body or create a new line like a divisor through it"""
    
    lining:list = list()
    for i in range(space): lining.append(char)
    grouping:str = ''.join(map(str, lining))
    
    #\\... check for method's clauses ::
    if(ope.eq(cmd, 'print')):
        if(to_the_end is False):
            print('%s%s' %(('\n' if(break_line is True) else ('' if(double_break is False) else '\n\n')), grouping))
        else:
            print('%s%s' %(grouping, ('\n' if(break_line is True) else ('' if(double_break is False) else '\n\n'))))
    elif(ope.eq(cmd, 'return')):
        if(to_the_end is False):
            return ('%s%s' %(('\n' if(break_line is True) else ('' if(double_break is False) else '\n\n')), grouping))
        else:
            return ('%s%s' %(grouping, ('\n' if(break_line is True) else ('' if(double_break is False) else '\n\n'))))
    else:
        print('\nInvalid Argumet Type!\n(<def> simple_div(*args))')
        return None



def dlmt_space(seq_length:int=int(), orders:tuple[str, str]= ("",""),) -> str:
    """
    `orders` tuple argument must receives an `int` as a first argument. This
    interger value represent the text length to be constructed. As long as,
    a `str` like second argument that assume the first word to be write in
    the text sequence whose will be ended with the last `str` argument of
    `orders` inside length of the sequence at building. The space alocked
    between both words is an computation has done according to the number
    of the empty places has extract from difference around the words to the
    sequence line to finishing.
    """
    # BASIC SECURITY LAMBDA FUNCTION ::
    msg:str = "\n❓ Invalid value to the mehotd arguments.'"
    check = (
        lambda x , z: 
        True if((int(x) > int())
                and ('', None not in tuple(z)))
             else False)
    
    if(check(seq_length, orders) is False): print(msg); raise ValueError()
    
    init:int = orders[0].__len__()
    ended:int = orders[1].__len__()
    diffe = int(ope.sub(seq_length, (ope.add(init, ended))))
    
    if(ope.le(diffe, int())):
        print("""
            \r❌[FunctionError]¡
            \rUnpossible to perform the string formating. Likely some word in <tuple> 'orders'
            \nis biggest than final text length constructed according to this python function.
            \nCheck for your arguments value and try to format again!""")
        raise ValueError()
    else: pass
    
    #\\... Text Bulding ::
    empty_space = []
    for i in range(diffe): empty_space.append(' ')
    text:str = (orders[0] + ''.join(map(str, empty_space[:])) + orders[1])
    return text


def centralize(space:int, message:str) -> str:
    
    #\\... Security Clauses ::
    if((ope.lt(space, message.__len__())) or (message is None)):
        print("❌[FunctionError]¡\n<def> centralizer ->: @arg(_space, ) cannot be less than <str> message length.")
        raise ValueError()
    else: pass 
    
    remain:int = int(); new_msg:str
    remain = ope.sub(space, message.__len__())
    partial = ope.truediv(remain, 2)
    e = lambda n: expand(size= int(n))
    new_msg=(
              str(e(partial) + message + e(partial + 1)) 
              if( (not isinstance(partial, int)) or (ope.ne(ope.mod(partial, 2), int())) 
                    and (not ope.gt(((partial*2) + remain), space)))
              else str( e(int(partial)) + message + e(int(partial)) ) 
            )
    return new_msg



def spliter(__separator:str='.', __index:int=(-1), /, text=str, debug:bool=True) -> str:
    if(ope.gt(__index, 2) or ope.lt(__index, -2)):
        if(debug is True):
            print("❌[FunctionError]¡\nFuntion positional-only argument `__index` isn't supported.")
    new_text = text.partition(__separator)
    #\\... Unsuccessfull conditional clause :: The 'text' sequence is originally returned.
    if((new_text is None) or ('' in new_text)):
        if(debug is True):
            print("⚠ [FunctionException]¡\nHasn't been found @arg: `__separarator` inside 'text' <str> sequence")
        return text
    return str(new_text[__index])



def element_repalcing(sequence:tuple[str,] | list[str,], to_replacing:dict[str, str]) -> tuple:
    """
    It returns a new building of `sequence` body with their elements for indexers has replaced for the
    same element's name written for `to_replacing` dictionay `_keys`. All of those must be string data types.
    """
    if(((isinstance(sequence, tuple)) and (ope.ne(sequence, ())) and (sequence is not None))
        or (isinstance(sequence, list) and ope.ne(sequence, [])) ):
        _keys = to_replacing.keys()
        for i in range(sequence.__len__()):
            if(sequence[i] in _keys): sequence[i] = to_replacing.__getitem__(sequence[i])
    else:
        print("""
            \r❌[FunctionError]¡
            \rUnpossible to perform the string formating. Likely some keyword in `<to_replacing>` dictionary
            \ror an element existly inside of `sequence` cannot be evaluated like being  a `str` data type.""")
        pass
    return ()
    
