
 # AUTO UPDATE SECTION ::
    
# AUTO UPDATE OF DATA FROM THE INTERNAL STORAGE OF THE "PRATES". THIS INFORMATION IS USED DURING INITIALIZATION 
# OF TEST CASES. AFTER  WE HAVE THE TYPES OF DATA NEEDED TO PERFORM  THE AUTOMATED TEST CASES, WE CAN CARRY OUT
# INTERNAL QUERIES DEDICATED TO THE PRATES STRUCTURE. THIS BEHAVIOR SAVES THE DATA FLOW OF THE DATABASE IN USE!

import operator as ope
import mysql.connector as cnx
from input.ConfigLoader import PratesConfig
from Base import Centralizer as Central, ExternalFile

from utilities.TextFormater import *
from utilities.KeyGenerator import *
from random import randint, randrange
from utilities.ColorText import log, logger6
CtLog = logger6()

class CustomerUpdate:
    MySQLconnection: cnx.MySQLConnection = None #type: ignore
    query_results: object = None
    customers: dict = {}
    cust_codes: list = []

    def __init__(cls) -> None:
        pass

    @classmethod
    def Set_MySQL_Connection(cls, cnn:cnx.MySQLConnection) -> cnx.MySQLConnection:
        """Create an explicit connection mapping to the @property: `MySQLConnection`"""
        cls.MySQLconnection = cnn; return

    @classmethod
    def Create_Customer_Mapping(cls) -> None:
        #\\... LOADING PROJECT SETTINGS ::
        auto_update:bool = bool(PratesConfig.reader().get('auto_update_of_data'))
        custom_sequence:list =PratesConfig.reader().get('sequence_of_customers')
        new_data:bool = bool(PratesConfig.reader().get('set_new_data'))
        get_from_db:bool = bool(PratesConfig.reader().get('get_data_from_db'))
        delimiter:int = PratesConfig.reader().get('limit_for_cust')
        randomize:bool = bool(PratesConfig.reader().get('randomize_choice'))
        print("""🔵\n Project Settings:
        ◽ auto_update: %s
        ◽ custom_sequence: %s
        ◽ new_data: %s
        ◽ get_from_db: %s
        ◽ delimiter: %s
        ◽ randomize: %s"""%(
            auto_update, 
            custom_sequence, 
            new_data, 
            get_from_db, 
            delimiter, 
            randomize))

        #\\... STANDARD CUSTOMER'S MAPPING CREATED AS INITIAL MUTABLE SEQUENCE ::
        cls.customers = dict(
            K0=dict(code_id=1, name='EDSON AZEVEDO', cnpj=None, cpf=None, discount=0, status="ATIVA", record_type='C', is_blocked=False, customer_cred=0, debt_balance=0),
            K1=dict(code_id=3742, name='VISUAL SOFTWARE', cnpj=None, cpf='95022559099', discount=0, status="ATIVA", record_type='C', is_blocked=False, customer_cred=0, debt_balance=0))


        # WHEN THE "PRATES" PROJECT IS RUNNING ON THE scanntech DATABASE, IT IS NOT NECESSARY TO DO ANYTHING
        # MORE THAN DOWNLOADING THE DATA. BUT THIS RESOURCE IS VALID ONLY FOR SCANNTECH DATABASE!
        if((auto_update is True) and (get_from_db is False) and (new_data is False)):
            print('\n\nDownloading Customer Records...')
            CustomerUpdate.Update_Local_Storage_Of_Customers()
            CtLog.info(msg="\n✅ Customer's inner dataschema has been update!")
            CustomerUpdate.Set_Random_CPF()

        # IF THE TESTER WANTS TO USE A SPECIFIC SEQUENCE OF CUSTOMERS FROM DATABASE, THEY MAY USE THIS 
        # STATEMENT AS AN OPTION TO DO SO.
        elif((get_from_db is True) and (new_data is False)):
            cls.customers.clear()
            print('\nDownloading Custom Sequence of Customers Code...'.upper())
            print('------------------------------------------------\n')  
            records = CustomerUpdate.Search_Customers(delimiter, randomize)
            print('\n\n\n📝 TRANSFORMING INTERNAL DICTIONARY OF DATA...')
            print('-------------------------------------------------')  
            for i in range(len(records)):
                new = dict(
                    code_id= records[i][0],
                    name= records[i][1],
                    cnpj= records[i][2],
                    cpf= records[i][3],
                    discount= records[i][4],
                    status= records[i][5],
                    record_type= records[i][6],
                    is_blocked= (False if(records[i][7] in (None, 0)) else True),
                    customer_cred= records[i][8],
                    debt_balance= CustomerUpdate.Customer_Credit(records[i][0]))
                dict_id = create_number_key()
                cls.customers.update([(dict_id, new)])
                print("'index_id': %s\n@property cls.customers in {%s}: %s\n" 
                      %(dict_id, dict_id, cls.customers[dict_id]))              
            CtLog.info(msg="\n✅ Customer's dataschema has been loaded!")
            pass

        # WHEN THE "PRATES" PROJECT IS RUNNING IN ANOTHER DATABASE, IT IS NECESSARY TO VERIFY THE DATA BEFORE
        # DOWNLOADING IT TO THE INTERNAL STRUCTURE.
        elif((new_data is True) and (get_from_db is False) and (ope.ne(custom_sequence, []))):
            cls.customers.clear()
            print('\ncustom_sequence <list>: %s' %custom_sequence)
            print('\n📥 Downloading Custom Sequence of Customers Code...'.upper());
            print('\n💬 REMOVING DUPLICATES FROM custom_sequence <list> WHETER EXISTS...')
            custom_sequence.append(Central.standard_customer_code())
            replace_list = [*set(custom_sequence)]
            custom_sequence.clear(); custom_sequence = replace_list
            create_line(52, break_line=True, to_the_end=True, cmd='print')
            for i in range(len(custom_sequence)):
                new = dict(
                    code_id= custom_sequence[i], 
                    name= 'Faker Client', 
                    cnpj= None, 
                    cpf= None, 
                    discount= 0, 
                    status="NULL", 
                    record_type='Empty', 
                    is_blocked=False, 
                    customer_cred=0, 
                    debt_balance=0)           
                dict_id = create_number_key()
                cls.customers.update([(dict_id, new)])
                print("'index_id': %s\n'self.customers' in {%s}: %s" %(dict_id, dict_id, cls.customers[dict_id]))
            CustomerUpdate.Update_Local_Storage_Of_Customers()
            CtLog.info(msg="\n✅ Cumtom client's dataschema has been loaded!")

        # INTERNAL SECURITY CLAUSE ::
        elif((ope.eq(custom_sequence, []) or (custom_sequence is None) and (new_data is True))):
            log.info('\n', also_console=True)
            log.error('...')
            CtLog.error(f"\nThe 'custom_sequence' variables cannot be EMPTY or NONE!\n".upper())
            raise ValueError()
    
        #\\... FINALLY ::
        # THIS RESOURCE WAS CREATED TO CONTROL THE PROMOTIONS BY CPF CODE IN THE CUSTOMER'S REGISTRATION.
        # SOME  ADVANCED   PROMOTIONS   CAN  ONLY  BE  CARRIED  OUT  IF THE CUSTOMER IN USE HAS NOT BEEN 
        # CONTEMPLATED PREVIOUSLY. ::
        Central.CnpjCpf_on_promotion_list(CustomerUpdate.Get_CPF_CNPJ_From_CustomerDict(), 'set')
        Central.customers(cls.customers, 'set')
        CustomerUpdate.Save_Customers_Data_Sequence()
        return

#=======================================================================================================================================
    # THIS IS A INTERNAL '@method/function' OF THE PRODUCT CUSTOMER MANAGER. ITS FUNCTION IS TO UPDATE THE CUSTOMER 
    # DICTIONARY WITH THE  NEW VALUES AVAILABLE IN THE DATABASE  WHERE THESE DATA ARE DIFFERENT FROM THEMSELVES
    # AND ARE STORED IN THE DICTIONARY.
    
    @classmethod
    def Get_CPF_CNPJ_From_CustomerDict(cls) -> list:
        msg:str = "CREATING THE LIST OF THE CPF CODE SUBSCRIPTED..."
        print("\n%s" %msg)
        create_line(msg.__len__(), cmd='print')
        temp_list: list = list()
        for e in cls.customers.keys():
            elem = cls.customers.get(str(e))
            cpf = remove_punctuation(elem['cpf']) if elem['cpf'] is not None else 'NULL'
            cnpj = remove_punctuation(elem['cnpj']) if elem['cnpj'] is not None else 'NULL'
            if(ope.ne(cpf, 'NULL')): temp_list.append(cpf)
            if(ope.ne(cnpj, 'NULL')):temp_list.append(cnpj)
        print(f"\n@property 'CustomerUpdate.all_cpf_cnpj_on_dict':")
        for i in range(len(temp_list)): 
            print('[%s] ->: %s' %(i, temp_list[i]))
        return temp_list

#=======================================================================================================================================
    @classmethod
    def Update_Local_Storage_Of_Customers(cls):
        msg:str = "📑 UPDATING CUSTOMER RECORDS..."
        print('\n%s'%msg)
        create_line(msg.__len__(), cmd=print)
        def trace_func(x:bool) -> bool: 
            return True if x not in (None, 0) else False
        
        for e in cls.customers.keys():
            elem: dict = cls.customers.get(e)
            print(f"\ndebug of '{e}' as `elem` before updating: {elem}")
            elem_keys = list(elem); print(f"debug for elem_keys: {elem_keys}")
            rersults = CustomerUpdate.Customer_Properties(elem['code_id'])
    
            if(rersults is not None):
                debt_balance = CustomerUpdate.Customer_Credit(elem['code_id'])
                for ii in range(len(rersults)):
                    # 3 -> range extension controller...
                    if(ope.ne(elem[str(elem_keys[ii])], rersults[ii]) is True):
                        elem[str(elem_keys[ii])] = (rersults[ii] if(ii != (ope.sub(len(elem_keys), 3)))
                                                    else trace_func(rersults[ope.sub(len(elem_keys), 3)]))
                # Singular customer property. It's out of conventional range of updating...
                elem['debt_balance'] = debt_balance
                print(f"debug of '{e}' after updating: {cls.customers[e]}")
            else:
                print(f"◉ The 'query_results for customer code {elem['code_id']} has returned: '{rersults}'. " +
                      "Because of that, this customer record wiil not be stored in the @property cls.customers")
            create_line(250, '_', cmd='print')
        return
    
#=======================================================================================================================================    
    @classmethod
    def Set_Random_CPF(cls) -> None:
        print('\nAPPLYING THE RANDOM CPF CODE INTO CUSTOMER DICTIONARY...')
        print('--------------------------------------------------------')
        index_id = list(); 
        for i in range(0, 4): x = randint(1, 9); index_id.append(x)
        dict_id = ''.join(map(str, index_id))
        random_cpf = CustomerUpdate.CPF_Generator(area_code=9)
        new = dict(
            code_id=dict_id, 
            name='FAKER CLIENT', 
            cnpj=None, 
            cpf=random_cpf, 
            discount=0, 
            status="NULL")
        cls.customers.update([(str(dict_id), new)])
        print(f"KEY INFO :: dict_key on use: '{dict_id}'")
       
        print('\n📃 NEW DICTIONARY OF CUSTOMERS:')
        print('-----------------------------\n')
        for e in cls.customers.keys():
            print(f"customer dictionary in {e}: {cls.customers[e]}")
        pass

#=======================================================================================================================================
    @classmethod
    def Search_Customers(cls, delimiter: int, randomize: bool = False) -> list:
        with cls.MySQLconnection.cursor() as cursor:
            count: int = 0
            if(randomize):
                cls.query_results = CustomerUpdate.Get_From_Database_Range(limit= delimiter)
                print('\n@property cls.query_results: %s' %(cls.query_results,))
                count = len(cls.query_results) 
            else:
                query = """
                SELECT 
                    Codigo, 
                    RazaoSocial, 
                    CNPJ, CPF, 
                    COALESCE(Desconto_Padrao, NULL, 0), 
                    STATUS, 
                    UPPER(Tipo),
                    CreditoCortado,
                    ValorCredito
                    FROM clientes AS c 
                WHERE (CNPJ IS NOT NULL OR CPF IS NOT NULL)
                    AND Ativo <> 0 AND STATUS <> 'INATIVA'
                    AND RazaoSocial IS NOT NULL
                    AND c.DataHoraExclusao IS NULL
                    AND UPPER(Tipo) NOT IN('T', 'F', 'M')
                ORDER BY c.Codigo DESC LIMIT %s"""
            
                cursor.execute(query, (delimiter,))
                cls.query_results = list(cursor.fetchall())
                count = cursor.rowcount; cursor.close()
                print('\n@property cls.query_results: %s' %(cls.query_results,))

            print(f"\n🔍 HAS BBEN FOUND {count} RECORDS FROM <{cls.MySQLconnection.database}> DATABASE:")
            print(f"◾ rows count: {count}\n")

        # IT'S NECESSARY TO ADD THE STANDARD CUSTOMER AND DEFAULT CUSTOMER CODE TO THE CUSTOMERS SEQUENCE ::
        standard_customer = CustomerUpdate.Customer_Properties(cust_code= Central.standard_customer_code())
        default_customer_code = CustomerUpdate.Customer_Properties(cust_code= Central.default_customer_code(gt_log=True))
        
        for i in range(cls.query_results.__len__()): cls.cust_codes.append(cls.query_results[i][0])
        print("\n🙎‍♂️ All customer codes written on @property cls.customers:\n-> %s" %(cls.cust_codes,))
        
        if((standard_customer is not None) and (list(standard_customer).__getitem__(0) not in cls.cust_codes)):
            cls.query_results.append(standard_customer)
            print("\n📝 The sequence: %s has been added in the @propert cls.query_results (Standard Customer)" 
                  %(str(str(standard_customer)[:20] + '...'),))
        else:
            print("\n❌ Default Customer has not been appenned to the customer sequence!" +
                  "\nThat customer code has already been appenned to the @property cls_query_results sequence. " +
                  "Or that one hasn't been found on database records.\nFor more information about it, check for " +
                  "this customer record on database!")
        
        if((default_customer_code is not None) and (list(default_customer_code).__getitem__(0) not in cls.cust_codes)):
            cls.query_results.append(default_customer_code)
            print("\n📝 The sequence: %s has been added in the @propert cls.query_results (Default Customter Code)" 
                  %(str(str(default_customer_code)[:20] + '...'),))

        if((isinstance(cls.query_results, list)) and (ope.ne(cls.query_results, []))):
            for i in range(len(cls.query_results)): print('[%s]: %s' %(i, cls.query_results[i]))
        else: 
            print("\n❗ UNPOSSIBLE TO FIND CUSTOMERS RECORDS ON %s DATABASE!" %cls.MySQLconnection.database)
            print('(InternalError): %s' %(cls.query_results,))
            raise Exception()
        
        return cls.query_results
        
#=======================================================================================================================================
    @classmethod
    def Get_From_Database_Range(cls, limit:int):
        queryA = "SELECT Codigo FROM clientes as p ORDER BY codigo LIMIT 1"
        queryB = "SELECT Codigo FROM clientes as p ORDER BY codigo DESC LIMIT 1"
        range_start: object = None; range_end: object = None

        print('💡 GETTING FOR DATABASE LENGTH...')
        print('----------------------------------')
        with cls.MySQLconnection.cursor() as range_cursor1:
            range_cursor1.execute(queryA)
            range_start = range_cursor1.fetchone()
            print("[%s] database range starts in: %s"
                   %(cls.MySQLconnection.database, range_start))
        pass
        with cls.MySQLconnection.cursor() as range_cursor2:
            range_cursor2.execute(queryB)
            range_end = range_cursor2.fetchone()
            print("[%s] database range ends in: %s" 
                  %(cls.MySQLconnection.database, range_end))
        pass; range_cursor1.close(); range_cursor2.close()
        
        # Internal Method crated like extension of the @property self.my_connection()
        def Execute(client_code:int) -> tuple | None:
            result: object = None
            queryA = """
            SELECT 
                Codigo,
                RazaoSocial, 
                CNPJ, CPF, 
                COALESCE(Desconto_Padrao, NULL, 0),
                STATUS, 
                UPPER(Tipo),
                CreditoCortado, 
                ValorCredito
                FROM clientes AS c 
            WHERE (c.CNPJ IS NOT NULL OR c.CPF IS NOT NULL)
                AND Ativo <> 0 AND STATUS <> 'INATIVA'
                AND RazaoSocial IS NOT NULL
                AND c.DataHoraExclusao IS NULL
                AND UPPER(Tipo) NOT IN('T', 'F', 'M')
                AND c.Codigo = %s"""
            
            with cls.MySQLconnection.cursor() as this_cursor:
                this_cursor.execute(queryA, (client_code,))
                result = this_cursor.fetchone()
                this_cursor.close()
            return result

        # Internal process of Customers Selection according the query results from Execute() method...
        print('\n🔍 SEARCHING CUSTOMERS FROM DATABASE...')
        create_line(42, break_line=True, to_the_end=True, cmd='print') 
        range_list = list(); int_num: int = 0; results = list()
        
        while(len(range_list) < limit):
            int_num = randrange(range_start[0], range_end[0])
            if(ope.eq(range_list, []) or (int_num not in range_list)):
                x = Execute(client_code= int_num)
                if x is not None: 
                    results.append(x); range_list.append(int_num)
                    print('int_num: %s\nx: %s' %(int_num, x))
                    print('query_result: %s\n' %(results[-2:],))
                else:
                    print("🔺 [DataError]: The query result from inner <def>: Execute is `None`")
                    print("Loop defined as continuous...")
                    continue
            else:
                while(True):
                    int_num = randrange(range_start[0], range_end[0])
                    if(int_num not in range_list): 
                        x = Execute(client_code= int_num)  #print('x: %s' %(x,))
                        if(x is not None): 
                            results.append(x); range_list.append(int_num)
                            print('int_num: %s\nx: %s' %(int_num, x))
                            print('query_result[]: %s\n' %(results[-2:],))
                            False; break
                        else:
                            print("🔺 [DataError]: The query result from inner <def>: Execute is `None`")
                            print("Loop defined as continuous...")
                            continue
                    else: continue
        return results
    
#=======================================================================================================================================
    @classmethod
    def Customer_Properties(cls, cust_code:int) -> tuple|None:
        #temp_internal_custom:object = None; 
        results:object = None
        query =  """
        SELECT 
	        c.Codigo, 
            c.RazaoSocial, 
            c.CNPJ, c.CPF,
            COALESCE(c.Desconto_Padrao, NULL, 0), 
            c.`Status`, 
            UPPER(c.Tipo),
            CreditoCortado, 
            ValorCredito
            FROM clientes AS c
        WHERE c.Codigo = {}""".format(cust_code)

        with cls.MySQLconnection.cursor() as cursor:
            cursor.execute(query)
            #if internal_usage is False: 
            results = cursor.fetchone()
            #else: temp_internal_custom = cursor.fetchone()
            count = cursor.rowcount; cursor.close()
            print("The customer code: {%s} has been updated to: %s" %(cust_code, results))
            print(f"◾ rows count: {count}")
            if(results is None): 
                print("🔺 [DataError]: The query result has returned more than one row or is 'None'")
        return results

#=======================================================================================================================================
    @classmethod
    def Customer_Credit(cls, client_code:int) -> float:
        query =  """
        SELECT 
            ROUND(SUM(ROUND(ValorPendente, 3)), 2)
            FROM contasareceber AS car
        WHERE car.Codigo = %s
            AND Quitado IN (NULL, 0)
            AND DataQuitacao IS NULL"""
    
        new_cursor = cls.MySQLconnection.cursor()
        new_cursor.execute(query, (client_code,))
        result:tuple = new_cursor.fetchone()
        if(result is not None):
            print("► <tuple>:result for customer debt balance has returned the value: %s" 
                  %(result[0] if(ope.ne(result[0], None)) else float(0)))
            return result[0]
        else:
            print("<tuple>:result has returned an invalid value or it's empty!")
            print("► <var>:result ->: %s" %(result,))
            return float(0)

#=======================================================================================================================================        
    @staticmethod
    def Save_Customers_Data_Sequence() -> None:
        ExternalFile.set_file_path(Central.path_local_storage)
        replace = list(); this_content = ExternalFile.read_file(); counter:int = -1
        print("\n🔹📜 STORING DATA SEQUENCE:\n◉ Building Customers Sequence to the Local Storage...")
        create_line(55, cmd='print')

        # Security Clause ::
        if(ope.eq(Central.customers(), {})):
            print("\n❓ There is a problem with @property cls.customers\n" +
                  "in this process step. No elements has been found in both of the classes properties!")
            raise Exception()
        else: pass

        # Execution Statement ::
        for elem in Central.customers().keys():
            counter = ope.iadd(counter, int(1))
            replace.append(Central.customers(gt_log=True, elem_key=elem).__getitem__(elem))
            print("► index <list> replace[%s]:\n💾🙍‍♂️ %s" %(counter, replace[-1]))
            create_line(200, char='_', cmd='print')
        
        ExternalFile.update_file(file= this_content, key= 'customer_sequence', new_value= replace)
        ExternalFile.write_on_file(this_content)
        return

#=======================================================================================================================================    
    # RECOVER AND RESTORE DATA SEQUENCE...
    @staticmethod
    def Recovery_Data_Sequence() -> None:
        ExternalFile.set_file_path(Central.path_local_storage)    
        build_property = dict()
        content = ExternalFile.read_file()
        data_sequence:list = content['customer_sequence'] 
            
        # Security Clause ::
        if(ope.eq(data_sequence, [])):
            print("\n❓ There was a problem with <list>:data_sequence has created from @property cls.customers" +
                  "appeared in this process step. No elements has been found in both classes properties!")
            raise Exception()
        else: pass
        
        for i in range(len(data_sequence)):
            dict_id = create_number_key()
            build_property.update([(dict_id, data_sequence[i])])
            print("'index_id': %s\n@property cls.customers in [%s]: %s\n" %(dict_id, dict_id, build_property[dict_id]))
        CtLog.info(msg="\n✅ Customer's Local Storage has been successffully recovered!")

        # FINAL SET STATMENT ::
        Central.customers(build_property.copy(), 'set')
        return

#=======================================================================================================================================
    @staticmethod
    def CPF_Generator(area_code: int, cannot_repeat: bool = False) -> str:

        """
        **DOCUMENTATION:** ``FakerClass``
            \n
            This keyword performs the calculation of the verifying digit of the CPF code.
            The digits result is  otained  according to the multiplication of all numbers
            in  the  randomly chosen fot the sequence. See more information at this link: 
            http://clubes.obmep.org.br/blog/a-matematica-nos-documentos-cpf/ \n"""

        # SCOPE VARIABLES:
        CPF_code = []
        calc_list_verifying_digit = []
        calc_digit: int = 10
        cycle: int = 0

        # This next  variable  contains the controll sequence of the random generations code
        # used for 'random.randrange' as 'rr' during the random choices for cpf code. An CPF
        # code  cannot  count  repeated values in your sequence. Therefore a new value is ge-
        # nerated at each cycle of the random choices process. 

        key_control: int = 10 
        # RANDOM CODE GENERATOR:
        print('\n\nGENERATING RANDOM CPF CODE...')
        print('-----------------------------')
        for i in range(cycle, 8):
            this_num = randint(0, 9 ,1)
            # THIS  SEQUENCE  HAS  BEEN  WRITTEN TO CONTROL THE GENERATION OF THE
            # NUMBERS SO THAT IS NOT POSSIBLE TO REPEAT THE INTEGERS SEQUENTIALLY
            if(cannot_repeat != False):
                while(ope.eq(this_num, key_control) == True):
                    this_num = randint(0,9,1)
                    if(ope.ne(this_num, key_control) == True): break
                    else: continue
            key_control = this_num; CPF_code.append(this_num)
            if (len(CPF_code) == 8) : CPF_code.insert(8, area_code)
            else: continue
        print(f"These are the interger list values: {CPF_code}") 

        # CYCLE OF CALCULATIONS ACCORDING THE RULES AT:
        # http://clubes.obmep.org.br/blog/a-matematica-nos-documentos-cpf/

        while cycle < 2:
            for ii in range(cycle, len(CPF_code)): 
                calc_list_verifying_digit.append(ope.mul(CPF_code[ii], calc_digit)); calc_digit -= 1
            print(f"The values given from 'calc_list_verifying_digit' are: {calc_list_verifying_digit}")
            math_reason = (sum(calc_list_verifying_digit, start=cycle) % 11); math_reason = int(math_reason)
            if (ope.eq(cycle, 1)): math_reason -=1
            print(f"The 'math_reason' calculations result is: {math_reason}")
            print(f"The code CPF generated to the {cycle} times is: {CPF_code}")
            if (math_reason <= 0 or math_reason == 1):
                temp_verifying_digits = 0; CPF_code.append(temp_verifying_digits)
                print(f"The value of the 'math_reason' variable has been replaced fo 0")
            else: temp_verifying_digits = ope.sub(11, math_reason); CPF_code.append(temp_verifying_digits)
            print(f"Temp variable of the code calculation: {temp_verifying_digits}")
            print(f"These are the CPF LIST code values: {CPF_code}")
            calc_list_verifying_digit.clear(); calc_digit = 10; temp_verifying_digits = 0; cycle += 1
            print(f"calc_list: {calc_list_verifying_digit}, calc_digit: {calc_digit}, temp_verifyig: " +
                f"{temp_verifying_digits} math_reason: {math_reason}, cycle_times: {cycle}")

        convert_code = str(CPF_code); convert_code = ''.join(map(str, CPF_code))
        print(f"\n🔹 The CPF code is: " + str(convert_code))
        return convert_code
    
#=======================================================================================================================================