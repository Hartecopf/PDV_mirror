# SETTINGS
# -> Project Libraries :: MyConnector Propwrties Extension ::
from SystemConfig import PDVConfig
from input.ConfigLoader import PratesConfig

from Base import ExternalFile
from Base import Centralizer as Central
from Base import Payment, Cashier, Storage
from MySQLConnector import MySQLConnector

# -> Built-in Modules, External Resources and Robot Modules ::
import operator as ope
import pyautogui as gui
from random import randrange as rr
from robot.api.deco import library, keyword
from time import strftime as st, localtime as lt

# -> Custom Modules has created to the Porject ::
from utilities.TextFormater import *
from utilities.AbntRound import round2
from utilities.ColorText import log, logger2, logger3, logger6
from utilities.KeyGenerator import create_number_key

from output.Relatory import show_cashier_relatory
from output.Relatory import show_relatory, system_version

DhLog1 = logger6()
DhLog2 = logger3()
DhLog3 = logger2()
PMOTION_DEBUG = True


@library(scope='GLOBAL', version='14.0', auto_keywords=False, doc_format='reST')
class DataHandler:
    def __init__(self):

        #\\ GLOBAL PROJECT FOLDER'S DATA ::
        #\\... Static Data ::
        Central.sales_person_code = int(PratesConfig.reader().get('user_code_id'))
        Central.sales_person_name = str(PratesConfig.reader().get('user_name'))
        Central.machine_name = str(PratesConfig.reader().get('computer_name'))
        Cashier.cashier_code(int(PratesConfig.reader().get('cashier_code')), 'set')
        Cashier.cashier_name(str(PratesConfig.reader().get('cashier_name')), 'set')

        # AUXILIAR @entity ATTRIBUTES IN THIS CLASS ::
        self.qtd_grid_prod_on_sale: int = 0
        self.Kg_product_control: dict = dict()
        self.direct_launch: bool = False
        self.promotion_code_on_use = list()

        # CUSTOMER AND THEIR PROPERTIES ::
        self.customer_property_chosen: object = 'Empty'
        self.registration_status: object = 'Empty'

        # OTHERS:
        self.internal_counters: int = 0


    @keyword(name='Colored Log')
    def colored_log(self, 
            mssg: str = 'message', 
            level: str = 'DEBUG, INFO, WARN, ERROR, NULL'):

        options = ('DEBUG', 'INFO', 'INFO2', 'WARN', 'ERROR', 'NULL')
        level = level.upper()
    
        if(level in options):
            if(ope.eq(level, 'DEBUG')): DhLog1.debug(msg = mssg); return
            elif(ope.eq(level, 'INFO')): DhLog1.info(msg = mssg); return
            elif(ope.eq(level, 'INFO2')): DhLog2.info(msg = mssg); return
            elif(ope.eq(level, 'WARN')): DhLog1.warn(msg = mssg); return
            elif(ope.eq(level, 'ERROR')): DhLog1.error(msg = mssg); return
            else: DhLog1.log(level=50, msg = mssg); return

        else:
            DhLog1.error('Invalid argument!'.upper())
            raise ValueError()
    

    @keyword(name='Console Line')
    def Create_Line(self,
            space: int,
            char: str = '-',
            break_line: bool = False,
            double_break: bool = False,
            to_the_end: bool = False,
            cmd: str = 'print | return', 
            color:str='white', 
            title:bool=False, msg:str='') -> None:
 
        if(title is False):
            (
              DhLog2.debug("{}".format(create_line(space, char, break_line, double_break, to_the_end, cmd))) 
              if ope.eq(color.lower(), 'white') 
              else DhLog2.info("{}".format(create_line(space, char, break_line, double_break, to_the_end, cmd))) 
            )
        else:
            (
              DhLog2.debug("{}".format(create_line(space, char, break_line, double_break, to_the_end, cmd))) 
              if ope.eq(color.lower(), 'white') 
              else DhLog2.info("{}".format(create_line(space, char, break_line, double_break, to_the_end, cmd)))
            )
            DhLog3.info("{}".format(centralize(space, message= msg)))
            (
              DhLog2.debug("{}".format(create_line(space, '-', break_line, double_break, to_the_end, cmd))) 
              if ope.eq(color.lower(), 'white') 
              else DhLog2.info("{}".format(create_line(space, char, break_line, double_break, to_the_end, cmd)))
            )
        return
    
    @keyword(name='Get Master Status')
    def Master_Status(self):
        """
        DOCUMENTATION ``DataHanlder``:

        THIS KEYWORD WAS CREATED TO INFORM WHAT IS THE FINAL STATUS OF THE TEST CASES
        IN EXECUTION. IF ANY TEST CASE FAILS, THE SENTENCE WILL BE ``False`` IF NOT, THE
        SENTENCE WILL BE ``True``. THIS BEHAVIOR DEPENDS ON THE SUCCESS OF THE TEST CASE
        WHICH CAN BE POSITIVE ONLY IF NO ERROR IS FOUND DURING ITS EXECUTION."""
        return Storage.master_status()


    @keyword(name='Set Master Status')
    def Set_Master_Status(self, status:bool):
        Storage.master_status(status, 'set')
        pass


    @keyword(name='Load Storage Path')
    def Set_Storage_Path(self):
        """
        DOCUMENTATION ``DataHanlder``:

        \rLoad the startup input and outpu files from main directory for handling their data
        and create information from those audict. This Automation Project won't wonrk without
        their path files. The argument `main_path` represents the main file where is possible
        to find all of another file's path has write in their inner content.
        """
        print(
            "\n👁‍🗨 <class>:DataCentralizer _properties:" +
            "\n\n📜 %s\n🧾 %s\n💲 %s\n💾 %s\n📓 %s" %(
            Central.path_main_config,
            Central.path_config_bckp, 
            Central.path_cashier_output, 
            Central.path_local_storage, 
            Central.path_pdv_settings))
        print('\n📰 _init_.yaml file: %s' %Central.initial_files_path)
        return

    
    @keyword(name= 'Check For The Project Settings Integrity')
    def Check_Project_Settings_Integrity(self):
        PratesConfig.file_integrity_inspector()
        PratesConfig.file_status_checkup()
        print("\n📑 Config File ::\n".upper())
        PratesConfig.file_printer()
        return

    
    @keyword(name='Initial Info')
    def Current_Time(self, just_log:bool= True, var:bool= False):
        if(just_log is True):
            DhLog1.warn(f"\nTest Case has started at: {st('%H:%M:%S', lt())}")
            system_version(59, 'single')
            return
        elif(var is True): 
            return st('%H:%M:%S', lt())
        else:
            log.info('\n', also_console=True); log.error('...') 
            DhLog1.error('\n❗[ArgumentException]: At least one <def> argument is requiered')
            raise ValueError()


    # This <def> is calling this function from FireBird Connector and loadind the PDV System 
    # Settings to into of Project Data Storagement...											     
    @keyword(name='Load Keyboard Instruction')
    def Get_Keyboard_Shortcut_Mapping(self):
        PDVConfig.Create_And_Call_Keyboard_Query()
        return


    @keyword(name='Load PDV System Settings')
    def Get_PDV_System_Settings(self):
        PDVConfig.Create_And_Call_System_Functions_Quey()
        return
    

    @keyword(name= 'Create Payment Mapping')
    def Build_Payment_Dicionary(self):
        """
        DOCUMENTATION ``DataHanlder``:
        
        Explore the database looking for payment ways and their attributes.
        Therefor, create the `Card Code Mapping` using the card properties
        has found  on  FireBirf  Server Connection on Machine LocalStorage.
        These available cards are products  type credit card or debit card
        recorded as payment options to use the Card Payment Way on PDV.
        """
        MySQLConnector.Download_PaymentWays()
        PDVConfig.Close_System_Settings_Loading()
        return
    
    
    @keyword(name='Create Custommer Mapping')
    def Build_Customer_Mapping(self):
        """
        Library: `DataHandler`
        Create the Customer Data Schema to use for all of `DataHandling`
        `@keywords` or methods and `@classmethods` already writen.
        """
        MySQLConnector.Dowload_Customer_Records()
        return

    
    @keyword(name= 'Create Product Mapping')
    def Build_Products_Mapping(self):
        """
        \nLibrary: ``DataHandling``\n
        \f Create the Product Data Schema to use for all of `DataHandling`
        `@keywords` or methods and `@classmethods` already writen.
        """
        MySQLConnector.Download_Product_Records()
        return


    # CASHIER BLOCK FUNCTION CREATED TO CONTROL THE CASHIER'S BEHAVIOUR ::    
    @keyword(name='Cashier Auto Adjustment')
    def Update_Cashier_Content_Against_Database(self, log:bool= False):
        """
        Update the cashier output file has writen on `yaml` data serialization
        format according  to the  database content for the cashier's event has
        perfomerd for an expecific opening code.
        """
        MySQLConnector.Cashier_Auto_Adjustment(log)
        return
        
    @keyword(name='Reset Cashier Output File')
    def Reset_Cashier_Output_File(self):
        ExternalFile.set_file_path(Central.path_cashier_output)
        yaml_file = ExternalFile.read_file()
        print('Before:\n')
        ExternalFile.print_file(yaml_file)
        if(ope.ne(yaml_file.get('cashier_serial_code'), yaml_file.get('old_cashier_serial_code'))):
            ExternalFile.reset_output(yaml_file)
            print('The file <Outp_Writer>: %s has been truncated!' %(type(ExternalFile)))
            ExternalFile.update_file(yaml_file, 'old_cashier_serial_code', yaml_file['cashier_serial_code'])
            ExternalFile.write_on_file(yaml_file)
            print('\nAfter:\n')
            ExternalFile.print_file(yaml_file)
        pass

    @keyword(name='Load Cashier Contents')
    def Load_Cashier_Contents(self):
        # EXTRACTING FILE ::
        cashier_file = ExternalFile.read_file()
        print('Loading the output data file...\n')
        ExternalFile.print_file(cashier_file)
        
        # ADJUSTING GENERAL CASHIER ::
        Cashier.all_finished_sales(float(cashier_file['all_the_sales_finished']), 'set')
        Cashier.total_on_cashier(float(cashier_file['total_on_cashier']), 'set')
        Cashier.total_sales_value(float(cashier_file['total_sales_value']), 'set')
        Cashier.total_eletronic_payments(float(cashier_file['total_eletronic_payments']), 'set')
        Cashier.qnt_sales(int(cashier_file['sales_quantity']), 'set')
        Cashier.cashiers_event(int(cashier_file['cashiers_event']), 'set')
        Cashier.canceled_sales(int(cashier_file['canceled_sale']), 'set')
        Cashier.uncompleted_sales(int(cashier_file['uncompleted_sale']), 'set')
        Cashier.qnt_sangria(int(cashier_file['sangria_quantity']), 'set')        
        # ADJUSTING CASHIER BREAKDOWN ::
        extract:dict = cashier_file.get('payment_methods')
        Cashier.total_cashback_payments(float(extract['cashback']), 'set')
        Cashier.total_chq_payments(float(extract['check']), 'set')
        Cashier.total_customer_payments(float(extract['customer_payment']), 'set')
        Cashier.total_ticket_payments(float(extract['ticket']), 'set')
        Cashier.total_credit_card_payments(float(extract['credit_card']), 'set')
        Cashier.total_pix_payments(float(extract['pix']), 'set')
        Cashier.total_bank_tranference(float(extract['bank_transfer']), 'set')
        return

 
    @keyword(name='Read System Settings')
    def Read_Keyboard_Shortcut_Key(self, key:str, key_type:str= 'KEYBOARD or FUNCTION'):
        #\\Security internal boolean clause ::
        if(key_type.lower() not in ('keyboard', 'function')):
            log.info('\n', also_console=True); log.error('...') 
            DhLog1.error('\n¡No valid argument has been passed as argument to this @keyword!')
            raise ValueError()
        else: pass
        #\\... read setting's file and its componentes from project folder tree ::
        ExternalFile.set_file_path(Central.path_pdv_settings)
        sysSettings = ExternalFile.read_file()
        print('\n\n...debug -> sys_settings: %s' %(sysSettings,))
        key_values:dict = (
            sysSettings.get('keyboard_keys')
            if(ope.eq((key_type.lower()), 'keyboard'))
            else sysSettings.get('function_keys'))
        print("\n\n...debug -> key_values: %s" %(key_values,))
        #\\... security clause for unknow key-value on settings's file mapping ::
        if(key not in key_values.keys()): 
            log.info('\n', also_console=True); log.error('...') 
            DhLog1.error("\n¡Key '%s' not found in <builtin>:dict_keys from System Settings Dictionary!")
            raise KeyError()
        else:
            print("\n📜 RESULT:\n◈ key_value in [%s]: %s" 
                  %(key, key_values[key],) +"\n\n💬 Reading the code mapping...")
            code_from_map:str = Central.keyboard_keycodes.get(int(key_values[key]))
            print("◉ key_value has found in '%s': %s" %(key_values[key], code_from_map))
            # This function will return the result of the ternary expression bellow ::
            return (
                code_from_map
                if(ope.eq(key_type.lower(), 'keyboard'))
                #\\... keys_values in [key] index for `function` key_value's pottion are all boolean values.
                #\\... As log as, we have something like this:
                else (True 
                    if(ope.ne(key_values[key], int())) 
                    else False))
        

    @keyword(name='Get Card Codes For Payment')
    def Get_Card_Code_Payment(self) -> list:
        """Once the `Card Code Mapping` is created, read it looking for availables card to use."""
        choices:list = list()
        expected_card_info:bool = bool(PratesConfig.reader().get('set_card_info'))
        if(expected_card_info is False):
            print("💰 Available Card Code as Payment Ways:")
            for elem in Payment.card_codes([]).keys():
                print("elem[%s] ->: %s" %(elem, Payment.card_codes([]).get(elem)))
            security_copy:dict = Payment.card_codes([]).copy()
            _range = list(security_copy)
            print("\n💳 Available products as Card Serial Code: %s" %_range)
            dct_key = rr(0, (len(_range) -1)) if(ope.gt(len(_range), 1)) else int(0)
            print("\nDict Key has randomically chosen: %s" %dct_key)
            replace:dict = Payment.card_codes([]).get(_range[dct_key])
            print("replace from <func>:copy() -> %s" %(replace,)); codes:list = replace.get('codes')
            given_code = codes[rr(0, (len(codes) -1))] if(ope.gt(len(codes), 1)) else codes[0]
            choices = [replace['operator'], given_code]
            print("\n👁‍🗨 Look at the list of serial codes chosen from @property <dict> Central.card_codes")
            print("► Serial: %s\n► Code: %s" %(choices[0], choices[1]))
            return choices
        elif(expected_card_info is True):
            elemnts:list = PratesConfig.reader().get('info_card')
            choices = [elemnts[0], elemnts[1]]
            return choices
        else:
            log.info('\n', also_console=True); log.error('...') 
            DhLog1.error('❗[ArgumentException]: At least one <def> argument is requiered!')
            raise ValueError()
        
    
    @keyword(name='CPF Code Generator')
    def CPF_Generator(self, area_code: int, cannot_repeat: bool = False):

        """
        DOCUMENTATION: ``DataHandler``

        \f This keyword performs the calculation of the verifying digit of the CPF code.
        The digits result is  otained  according to the multiplication of all numbers
        in  the  randomly chosen fot the sequence. See more information at this link: 
        http://clubes.obmep.org.br/blog/a-matematica-nos-documentos-cpf/"""

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
        create_line(29, cmd='print')
        for i in range(cycle, 8):
            this_num = rr(0, 9, 1)
            # THIS  SEQUENCE  HAS  BEEN  WRITTEN TO CONTROL THE GENERATION OF THE
            # NUMBERS SO THAT IS NOT POSSIBLE TO REPEAT THE INTEGERS SEQUENTIALLY
            if(cannot_repeat != False):
                while(ope.eq(this_num, key_control) == True):
                    this_num = rr(0,9,1)
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
   

    # CUSTOMER CONTROLLER IS A KEYWORD THAT MANAGES THE CUSTOMER SUBSCRIPTIONS AND THEIR INFORMATION.
    # EACH CUSTOMER CODE HAS ITS OWN  PROPERTIES AND ONE SETTINGS WHICH CAN BE USED DURING THE CASES
    # RUNNING TESTS.  
    @keyword(name='Customer Controller')
    def customer_tasks(self, 
        _key:object= 'empty', _find:bool= False, 
        _get:bool= True, randomize_get:bool= False,
        _id:bool= False,  name:bool= False, 
        cnpj:bool= False, cpf:bool= False, 
        custom_discount:bool= False, status:bool= False, 
        record_type:bool = False, customer_cred:bool= False, 
        is_blocked:bool= False, _all:bool= False, single:bool= True):
        
        """
        **DOCUMENTATION:** ``DataManipulator``
        
        CUSTOMER CONTROLLER IS A KEYWORD THAT MANAGES THE CUSTOMER SUBSCRIPTIONS AND THEIR INFORMATION.
        EACH CUSTOMER CODE HAS ITS OWN PROPERTIES AND  ONE SETTINGS WHICH CAN BE USED DURING THE CASES
        RUNNING TESTS. THESE SETTINGS ARE COMBINATIONS OF THE BOOLEAN KEYS.
        
        FOR EXAMPLE:
        
        :: ``_key`` = **any_value** ( object -> It is obligatory to perform a custom **_get** )
            
        :: ``_get = True`` *(default)*
             
        :: ``_find = False`` *(default)*
        
        THIS EXAMPLE  WILL RETURN THE VALUES OF THE CORRESPONDING KEY PROVIDED BY THE BUILT-IN CUSTOMER
        DICTIONARY. HOWEVER  OTHER COMBINATIONS CAN RETURN ANOTHER VALUES. IF YOU NEED SET UP AN RANDOM
        CHOICE FOR CUSTOMER SUBSCRIPTION  OR TO GET ANOTHER CUSTOMER  PROPERTY JUST INFORM THE SPECIFIC
        COMBINATIONS TO DO THIS.

        POSSIBLE COMBINATIONS FOR THE CUSTOMER PROPERTIES USING:
        
        *( bool _id, bool name, bool cpf & bool custom_discount )*

        ``if( ( _get is True ) and ( _find is not True ) ):``
            It wiil return the customer property in accordance with the **string key** passed
            like a parameter. ``if(_key in self.customers) : return self.customers.get(_key)``

        ``elif( ( _get is not True ) and ( randomize_get is True ) ):``
            It will return the customer property chosen randomly according to the **boolean key**
            passed like a parameter. This settings performing a get of the customers properties
            from the dictionary of customer avaliable in this structue.

        ``elif( ( _get is True ) and ( _find is True ) ):``
            This commands sequence will return the resutlt of the search applied on the dictionary's
            structure  considering  the '_key' value (object) like a comparsion between the element
            and   the boolean  key  like  a return condition. These two arguments must be passes as 
            parameter for this Keyword Method works. This is a searching boolean settings.
        """
        elem: object = 'standard'

        # FIRST BOOLEAN SETTINGS:
        if((_get is True) and (_find is not True)):
            try:
                elem = Central.customers().get(_key)
                print(f"It was chosen the next customer properties: {elem}")   
                print("The Normal Get to select the customers properties was selected in this step!")
            except: 
                print(f"\nValueError() -> '{_key}': was not found in 'self_products")
                log.info('\n', also_console=True); log.error('...')
                DhLog1.error(f"\n-> '{_key}': was not found in 'self_products")
                raise KeyError()

        # SECOND BOOLEAN SETTINGS:
        # This stantment makes the structure of the  dictinonary 'self.customes' be converted to the
        # list  with  acessible indexers  by type, it mean that this list will countain the customer 
        # properties like indexer type string: 
        elif((_get is not True) and (randomize_get is True)):
            print("'self.customers': %s" %(Central.customers().keys(),))
            this_key = list(Central.customers().copy())
            print("\ndebug of: 'this_key': %s" %this_key)
            print("\ndebug of 'this_key' lenght: %s" %len(this_key)) 
            _max = ope.sub(len(this_key), 1); i = rr(0, _max, 1)
            elem = Central.customers().get(str(this_key[i]))
            print(f"It was chosen the next customer properties: {elem}")
            print("The Rancomicaly Get to select the customers properties was was select in this step!")

        # THIRD BOOLEAN SETTINGS: -> THIS PERFORMS A 'get' LOOKUP AND RETURN IT
        # This next  condition checks  if the parameters characterize  a search on the self.customers dictionary. 
        # In  this case, the '_key'  variable  value is not an attribute  but so  an search filter. So that loop
        # to find an  element equal to the  one  passed  like  function's parameter, the loop is stoped and this
        # element is captured from the 'slef.customers' dictinoary and than sends to the initial robot's request. 
        elif((_get is True) and (_find is True)):
            try:
                _all_keys = list(Central.customers().copy())
                for i in range(len(_all_keys)):     
                    elem = Central.customers().get(str(_all_keys[i]))
                    values_in_elem = elem.values()
                    print(f"\n'elem': {elem}\nvalues_in_elem: {values_in_elem}")
                    if(_key in values_in_elem): break 
                    else: continue
            except: log.error('¡%s is not found!' %_key); raise KeyError() 

        else: log.error('\nWas not possible to conclude this process step! There is a problem with the ' + 
        'conditional\nstatements of this structure. Check your bollean settings in this keyword.'); return TypeError()

        # HERE IS  THE  MOMENT  WHERE  WE  WILL APPLY THE CUSTOMER'S REGISTRATION STATUS, IN SUCH WAY THAT SOME
        # CONDITIONS  CAN  ONLY  SEND THE CUSTOMER'S PROPERTY REQUESTED BY THE BOLLEAN SETTINGS OF THIS KEYWORD,
        # IF YOUR REGISTRATION IS ACTIVE.
        self.registration_status = elem['status']
        print(f' self._registration_valid = {self.registration_status}')

        # GET  THE  WISHED  PROPERTY OF  THE  CUSTOMER  IN  ACCORDANCE  WITH THE BOOLEAN SETTINGS AND RETURN IT
        # This is the  setting's  block  of this  function. All the parameters of this fucntion are worked here
        # ... and this method will return the customer's property acoording to these statements ::
        # 🔧⚙
        if(_id is True): print(elem['code_id']); return elem['code_id']     
        
        # 🔧⚙
        elif(name is True): print(elem['name']); return elem['name']

        # 🔧⚙
        elif(cnpj is True):
            force_data = DataHandler.CPF_Generator(self, 9)
            if(elem['cnpj'] is None): 
                DhLog1.info(f"\nTHIS CUSTOMER HAS NOT A CNPJ CODE IN HIS RECORD!")
                return elem['cpf'] if elem['cpf'] is not None else force_data
            else: return elem['cnpj']

        # 🔧⚙
        elif(cpf is True):
            force_data = DataHandler.CPF_Generator(self, 9)
            if(elem['cpf'] is None):
                DhLog1.info(f"\nTHIS CUSTOMER HAS NOT A CPF CODE IN HIS RECORD!")
                return elem['cnpj'] if elem['cnpj'] is not None else force_data
            else: print(elem['cpf']); return elem['cpf']  

        # 🔧⚙
        elif(custom_discount is True):
            if((self.registration_status != 'INATIVA') and (self.registration_status != 'NULL')):
                print(elem['discount']); return elem['discount']
            else: print('_prperty = 0.00'); return 0 

        # 🔧⚙
        elif(status is True): print(elem['status']); return elem['status']

        # 🔧⚙
        elif(record_type is True): print(elem['record_type']); return elem['record_type']

        # 🔧⚙
        elif(customer_cred is True): print(elem['customer_cred']); return elem['cred_value']

        # 🔧⚙
        elif(is_blocked is True): print(elem['is_blocked']); return elem['is_blocked']

        # 🔧⚙
        elif((_all is True) and (single is False)): print(elem); return ','.join(map(str, elem))

        # 🔧⚙
        else: log.error('No element valid has given as dict _key to the dictionary!'); return ValueError()


    # ESCAPE KEYWORDS ::
    @keyword(name='Get The Customer Record Status')
    def Show_Customer_Record_Status(self):
        if(ope.ne(self.registration_status, 'ATIVA')): 
            return False
        else: return True


    @keyword(name='Store The Customer Code Or CPF/CNPJ')
    def Store_The_Customer_Code(self, code_id: int = 0, cpf_cnpj: object = 'Empty', is_random: bool = False):
        """
        DOCUMENTATION: `DataHandler`

        WHENEVER  THIS  KEYWORD  IS CALLED FOR ANY COMPONENT OF THE MODULE,
        IT STORE THE VALUE PASSED AS AN ARGUMENT OF THE VARIABLE ``code_id``
        AND ``cpf_cnpj``  TO   THE  CLASS   PROPERTIES.  ITS  MEANS  THESE
        VARIABLES WILL  APPLY A DIFFERENT VALUE FOR THE 'self.customer_code'
        AND ``self.customer_cpf_cnpj`` ARGUMENTS FOR EACH CALL IN RUNTIME.
        FURTHERMORE,  THIS  KEYWORD  HAS THE FUNCTION OF CALLING THE OFFER 
        CONTROLLER WHENEVER THERE IS AN OFFER AVAILABLE FOR USE DURING THE 
        TEST CASE ESPECIALLY IF THIS OFFER HAS A CPF/CNPJ CONTROL ACTIVATED.
        """
        
        # This clausule bellow assegures that the randomic selection for code type CPF or CNPJ
        # receives the number one (<int>  1) as a defualt value for Customer Code. Its likelly
        # that a CPF/CNPJ has randomically generated haven't an internal client code storage in
        # the database in usage. Because of that reson, It is necessary to set a pattern value to. 
        Storage.last_customer_code(1, 'set') if(is_random is True) else Storage.last_customer_code(code_id, 'set')

        if (ope.ne(code_id, 0)): 
            Central.customer_code(code_id, 'set')
            Storage.last_customer_code(code_id, 'set')
            print("📑 The <int>:code_id %s has been storage\n" %(Storage.last_customer_code().__getitem__(-1)))
        if(ope.ne(cpf_cnpj, 'Empty')):
            rplc = None if((ope.eq(code_id, 1)) and (ope.eq(cpf_cnpj, 'SET'))) else remove_punctuation(cpf_cnpj)
            Central.current_cpf_cnpj(rplc, 'set')
            print("❕ The <object>:cpf_cnpj %s serial code has been stored." %Central.current_cpf_cnpj())
        if ((ope.eq(code_id, 0)) and (ope.eq(cpf_cnpj, None))):
            log.info('\n', also_console=True); log.error('...')
            DhLog1.error('\nAt least one parameter is required for this keyword!', html=True)
            raise ValueError()
        return

    @keyword(name='Get The Customer Identification')
    def Get_Customer_Code(self, cpf_cnpj: bool = False, code_id: bool = True):
        if(cpf_cnpj is True):
            return Central.current_cpf_cnpj()
        elif(code_id is True):
            return Central.customer_code()
        else: print('\nNo valid argument has given!'); raise ValueError()


    @keyword(name='Store The Customer Discount')
    def Store_The_Customer_Discount(self, discount: object|int|float = None):
        """
        **DOCUMENTATION:** ``DataManipulator``

        WHENEVER  THIS  KEYWORD  IS CALLED FOR ANY COMPONENT OF THE MODULE,
        IT STORE THE VALUE PASSED AS AN ARGUMENT OF THE VARIABLE ``discount``
        TO  THE CLASS PROPERTY ``self.customer.discount``. ITS  MEANS  THIS 
        VARIABLE  WILL  APPLY A DIFFERENT VALUE FOR THE 'discount' ARGUMENT
        FOR EACH CALL IN RUNTIME"""
        Central.customer_discount(discount if(discount is not None) else float(0), 'set')
        return

    # KEYWORDS OF CONTROL FOR THIS CLASSES PROPERTIES AND CUSTOMER'S PROPERTY MANAGEMENT ::
    @keyword(name='Get The Customer Discount')
    def Show_The_Customer_Discount(self):
        """
        **DOCUMENTATION:** ``DataManipulator``
        
        AS LONG AS THE CUSTOMER DISCOUNT IS GREATER THAN 0, IT WILL BE APPLIED TO THE
        CURRENT SALE. THIS  KEYWORD  IS CALLED TO CAPTURE THE VALUE OF THE CUSTOMER'S
        DISCOUNT AND UPLOAD IT IN THE RESPECTIVE PROCESS OF THE SYSTEM THAT REQUESTED IT"""
        return(Central.customer_discount())


    # PRODUCTS CONTROLLER IS A KEYWORD THAT MANAGES THE PROPERTIES OF THE PRODUCTS AND SENDS THESE
    # INFORMATION TO THE ROBOT'F INTERNAL PROCESS IN RUNNNING.
    # EACH PRODUCT CODE HAS ITS OWN PROPERTIES WHICH CAN BE USED AND WILL BE USED DURING THE CASES
    # RUNNING TESTS. THE CHOICE  OF  PRODUCTS  IS  MADE BY ROBOT IN THE MODULE 'various_products'.
    # ON THE  OTHER HAND, THIS KEYWORD  IS WHAT CONTROLS AND MANAGES THE PROPERTIES OF THE PRODUCT 
    # IN A WAY THAT IT SENDS AND STORE ANY AND ALL INFORMATION MOVED INSIDE IT.
    @keyword(name='Product Controller')
    def products_tasks(self,
            _key:object = 'inform',  _get:bool = True,
            _find:bool = False, randomize_get:bool = False,
            _id:bool = False, barcode:bool = False, 
            reference:bool = False, description:bool = False,
            price_T1:bool = False, _all:bool = False, 
            single:bool = True, is_grid:bool = False, 
            build_sale:bool= True, attr_logger:bool= True):

        """DOCUMENTATION: ``FakerClass``
        
        THIS KEYWORD STORE  THE  PRODUCTS PROPERTIES AS LOCAL STORAGE PERFORMING A DATA STRUCTURE
        CAN BE  USED  FOR  ROBOT  DURING THE SALE RUNNING PROCESS. THE PRODUCTS OF THE DICTINOARY 
        HAVE AN INTERNAL CODE, A DESCRIPTION, A REFERENCE STRING OR NUMERIC DATA TYPE AND A PRICE.
        ALL  THESE  PRODUCTS  PROPERTIES BELONG TO THE STRUCTURE OF THE 'products' DICTIONARY AND
        CAN BE ACCESSED  BY THIS KEYWORD IN ACCORDANCE WITH  THE BOOLEAN SETTINGS HAS PASSED LIKE
        PARAMETERS.
        
        FOR EXAMPLE:
        
        :: ``_key`` = **any_value** (object -> It is obligatory)
            
        :: ``_get = True`` *(default)*
             
        :: ``_find = False`` *(default)*
        
        THIS EXAMPLE WILL RETURN THE VALUES OF THE CORRESPONDING KEY PROVIDED BY THE BUILT-IN PRODUCT
        DICTIONARY. HOWEVER OTHER COMBINATIONS CAN RETURN ANOTHER VALUES. IF YOU NEED SET UP AN RANDOM
        CHOICE FOR PRODUCTS SUBSCRIPTION OR TO GET ANOTHER PRODUCT PROPERTY, JUST INFORM THE  SPECIFIC
        COMBINATIONS TO DO THIS.
        
        LOOK AT THIS STATEMENTS BELOW FOR THE VARIABLES:
        \r*( bool _id, bool refference, bool description & bool price )*

        ``if( ( _get is True ) and ( _find is not True ) ):``
            -> It wiil return the product property in accordance with the **string _key** passed
            like a parameter. ``if(_key in self.products) : return self.products.get(_key)``

        ``elif( ( _get is not True ) and ( randomize_get is True ) ):``
            -> This settings will return the product property  chosen randomly according to the 
            **boolean args** passed like a parameter. This option performs a _get_ of the product's 
            properties from the dictionary of products avaliable in this structure retunrning the 
            property has passed like a parameter for serching. This parameter of searching is one of 
            the varibles type ``bool`` available in this Keyword.

        ``elif( ( _get is True ) and ( _find is True ) ):``
            -> This commands sequence will return the  resutlt of the search  applied on the dictionary's
            structure  considering  the  '_key'  value  (object) as a comparsion between  the element
            and the ``boolean var`` provided  like  a return condition. These  two  arguments must be
            passed  as  parameter for this Keyword Method works. This is a searching boolean settings.
         """
   
        elem:object = 'standard'

        if((_get is True) and (_find is not True)):
            try:
                elem = Central.products().get(_key)
                print(f"It was chosen the next product properties: {elem}")   
                print("The Normal Get to select the product properties was selected in this step!")
            except: 
                log.info('\n', also_console=True); log.error('...')
                DhLog1.error("-> ('_key'): was not found in 'self_products")
                raise KeyError()

        # SECOND BOOLEAN SETTINGS ::
        # This stantment makes the structure of the  dictinonary 'self.products' be converted to the
        # list with  acessible indexers by type, it  mean that this list  will countain the products 
        # properties like indexer type string:
        elif((_get is not True) and (randomize_get is True)):
            _key = list(Central.products().copy())
            i = rr(0, (len(_key)-1), 1) 
            elem = Central.products().get(str(_key[i]))
            print(f"It was chosen the next customer properties: {elem}")    
            print("The Rancomicaly Get to select the customers properties was was select in this step!")

        
        # THIRD BOOLEAN SETTINGS: -> THIS PERFORMS A 'get' AS LOOKUP AND RETURN IT ::
        # This next condition checks if the parameters characterize  a search on the 'self.products dictionary'.
        # In this case,  the '_key' variable  value  is not  an attribute but so an search filter. So that loop
        # to find an element equal to the one passed like function's  parameter,  the  loop  is stoped and this
        # element is captured from the 'slef.products' dictinoary and than sends to the initial robot's request. 
        elif((_get is True) and (_find is True)):
            log.info('A look up has been initiated in the products internal data dictionary...')
            try:
                print(f"debug of '_key' on use for look up: {_key}\n")
                _all_keys = list(Central.products().copy())
                for i in range(len(_all_keys)):
                    elem:dict = Central.products().get(str(_all_keys[i]))
                    values_in_elem = elem.values()
                    if(_key in values_in_elem):
                        print(f"'elem': {elem}\nvalues_in_elem: {values_in_elem}"); break
                    else: continue
            except: 
                log.info(msg='\n', also_console=True); log.error(msg='...')
                DhLog1.error(msg="\n¡%s is not found!' %_key"); raise KeyError() 
          
        else: 
            log.info(msg='\n', also_console=True); 
            log.error('Was not possible to conclude this process step! There is a' +
            '\nproblem with the conditional\nstatements of this structure. Check your' +
            '\nbollean settings on this keyword.')
            raise ValueError()

        #--------------------------------------------------------------------------------------------------------------------+
        # STATEMENTS OF METHODS RETURN...                                                                                    |
        #--------------------------------------------------------------------------------------------------------------------+
        # 🔧⚙ PROD. ID:
        if(_id is True): print('product id: %s' %elem['code_id']); return elem['code_id']

        # ▶ PROD. BARCODE:
        elif(barcode is True): 
            print('\nProduct Barcode: %s' %elem['bar_code'])
            if(ope.eq(str(elem['bar_code'][0]), str(2))):
                print('\nThis product as as serial code equivalet to the by [Kg] control!'.upper())
                DataHandler.Launch_Produto_Kg(self, elem['code_id'], elem['bar_code'], elem['descrpt'])
            return elem['bar_code']

        # 🔧⚙ PROD. REFERENCE:
        elif(reference is True): 
            print('product reference: %s' %elem['reference'])
            if(elem['reference'] is None):
                (DhLog1.info(msg=f"\n[{elem['code_id']}]This product has no reference in your record!".upper())
                 if(attr_logger is True) else None); return elem['descrpt']
            else: return elem['reference']

        # 🔧⚙ PROD. DESCRIPTION:
        elif(description is True): print('product description: %s' %elem['descrpt']); return elem['descrpt']

        # 🔧⚙ PROD. PRICE FOR SALE:
        elif(price_T1 is True):
            print(f"\n@product:\n-> price_T1: {elem['price_T1']}\n-> promotion: {elem['promotion']}\n-> offer: {elem['offer']}")
            # internal delimiters and settings ::
            value: float = 0; dsct_status: bool = True
            #--------------------------------------------------------------------------------------------------------------//
            # WHENEVER IS FOUND A PRODUCT ON OFFER, THIS @classmethod WILL CALL THE OFFERS' CONTROLLER TO VERIFY IF THE
            # PROMOTIONAL  PRICE  OF THE PRODUCT SHOULD BE APPLIED TO THE CURRENT SALE OR NOT. THERE IS AN NUMERIC
            # COUNTER WHO CONTROLS THIS  CONDITIONAL  STATEMENT  IN SUCH WAY THAT THIS PRODUCT WILL BE RELEASED AT
            # ITS PROMOTIONAL PRICE ONLY IN ACCORDANCE WITH THESE CONDITIONS ::

            # OBS: The local variable <bool>: 'build_sale' has declared in this function <products_tasks> and it must be
            # (True) for the clauses and statements bellow correctly works. That settings has been created as an internal
            # control to this function behaviour against to the another depencences of this <object> class DataManipulator.py.
            # Wheter that varible is (False), this method don't will build the sales process but will respctly return the
            # product attribtute according to the boolean settings has passed as paramenter to the current function/method.
            #--------------------------------------------------------------------------------------------------------------\\
            # 🔖💰 OFFER ::
            if((elem['offer'] is not None) and (ope.ne(elem['offer'], int()))):
                # HERE WE EXTRACT THE CONTENT FROM 'offer' KEY :: 
                offer = elem['offer']; this_value: float = offer[0]; minm: int = offer[1]
                if(minm <= 1):
                    print('\nthis product is on offer by direct launching!'.upper())
                    print("'offer' key properties -> value: %s, minimun: %s" %(this_value, minm))
                    # UPDATE VALUES IN 'offer' KEY...
                    value = this_value
                    dsct_status = False if (Central.block_discount_for_promotion() is True) else True
                    # ANNOUNCEMENT ↴
                    if(attr_logger is True): DhLog1.debug(msg=f"This product is on offer for: {value}")
                elif((minm > 1) and (build_sale is True)):
                    # IN THIS CASE, THE PRODUCT IN USE IN THE CURRENT PROCESS WILL BE REPLACED AFTER THE SUBTOTAL OF THE SALE.
                    print('\nthis Product is on offer!'.upper())
                    offer = Central.prod_on_offer_controller(gt_log=True).get(str(elem['code_id']))
                    this_value: float = offer['price']; minm: int = offer['minimum']; counter: int = offer['counter']
                    print("'offer' key properties -> value: %s, minimun: %s, counter: %s" %(this_value, minm, counter))
                    DataHandler.Offers_Launcher_Controller(self, elem['code_id'], debug_logger= attr_logger)
                    value = elem['price_T1']
                
            # 💲💰 PROMOTION ::
            elif((elem['promotion'] > 0) and (build_sale is True)):
                normal_controllers:dict = Central.prod_on_promotion_controller(gt_log=True).get(str(elem['code_id']))
                paymnt_controllers:dict = Central.payment_controllers(gt_log=True).get(str(normal_controllers['prom_code']))
                print(f"\ndebug of normal controllers for this product on promotion: {normal_controllers}")
                print(f"debug of payment controllers for this product on promotion: {paymnt_controllers}")
                
                # ANNOUNCEMENT ↴ 
                if(attr_logger is True):
                    DhLog1.log(level=40, msg=f"This product is on promotion for: {elem['promotion']}")
               
                # TRATEMENTS ↴                                                                       
                if(normal_controllers['cpf'] is False):
                    DataHandler.Promotions_Launcher_Controller(self, elem['code_id'], elem['promotion'])
                    value = elem['price_T1']
                else:
                    if(attr_logger is True):
                        DhLog1.info("This promtion is controlled by the customer's cpf code.".upper())
                    DataHandler.Promotions_Launcher_Controller(self, elem['code_id'], elem['promotion'])
                    value = elem['price_T1']

                if(paymnt_controllers['paymnt_method'] is not None):
                    if(attr_logger is True):
                        DhLog1.info(f"available only for payments type: {paymnt_controllers['paymnt_method']}".upper())

                if(elem['code_id'] not in self.promotion_code_on_use):
                    self.promotion_code_on_use.append(elem['code_id'])
                    print(f"PROMOTIONS: debug of promotion on use: {self.promotion_code_on_use}")

            else: value = elem['price_T1']

            if(attr_logger is True): DhLog1.warn(msg=f"Product Price: {value}")
            print('\nGENERATING DICTIONARY KEY...')
            create_line(28, cmd='print')

            if(build_sale is True):
                dict_id = create_number_key()
                Central.products_for_sale(
                    [(str(dict_id), 
                        {'prod_code':elem['code_id'], 
                         'prod_price':value, 
                         'dsct_status':dsct_status})], 'set')
                #--------------------------------------------------------------------------------------------------------------//
                # This local storage property serves to store the products posted for sale in progress and their properties, as 
                # well as their price and percentage discount status. Whenever it is necessary to replace the main dict of sale
                # properties, we will do this task using this storage!
                #--------------------------------------------------------------------------------------------------------------\\
                Storage.restore_sale_properties(
                    [(str(dict_id), 
                        {'prod_code':elem['code_id'], 
                         'prod_price':value, 
                         'dsct_status':dsct_status})], 'set')
                
                print('\nCREATING DICTIONARY OF THE PRODUCT FOR SALE...'); create_line(50, cmd='print')
                print(f"debug of @property <dict> Centralizer.product_for_sale:")
                for elem in Central.products_for_sale().keys(): 
                    print(f"[{elem}]: {Central.products_for_sale().get(elem)}")
            return value
        
        # 🔧⚙ PROD. GRID CODE:
        elif(is_grid is True):
            #--------------------------------------------------------------------------------------------------------------//
            # OBS: The local variable <bool>: 'build_sale' has declared in this function <products_tasks> must be
            # (True) for the clauses and statements bellow correctly works. That method setting has been created
            # as an internal control to this function behaviour against to the another depencences of this <object>
            # class DataManipulator.py. Wheter that varible is (False), this method don't will build the sales process
            # but will return the repctly product attribtute according to the boolean settings has passed as paramenter
            # to the current function/method.
            #--------------------------------------------------------------------------------------------------------------\\

            print(f"is_grid = {elem['is_grid']}")
            if((elem['is_grid'] is True) and (build_sale is True)): 
                self.qtd_grid_prod_on_sale += 1; return elem['is_grid']
            else: return elem['is_grid']

        # 🔧⚙ PROD. ALL RRODUCT PROPERTIES:
        elif((_all is True) and (single is False)):
            print(elem); return elem
        
        # 🔧⚙ INVALID ARGUMENT ECEPTION!
        else:
            log.info('\n', also_console=True); log.error(msg='...')
            DhLog1.error('\nNo element valid has given as dict _key to the dictionary!')
            raise ValueError()

    
    # 🔧💰
    def Offers_Launcher_Controller(self, prod_code: int, debug_logger:bool= True):
        # THIS STEP OF OUR CODE IS WHERE WE EXTRACT PROMOTION CONTROLLERS...
        print('\nOFFER CONTROL:'); create_line(15, cmd='print')
        print('LOOK AT THIS @property BEFORE IT IS CALLED: %s' 
              %(Central.prod_on_offer_controller(gt_log=True).get(str(prod_code)),))
        controllers:dict = Central.prod_on_offer_controller().get(str(prod_code))
        vlr = controllers['price']
        mnm = controllers['minimum']
        cnt = (controllers['counter'] + 1)
        if(debug_logger is True):
            DhLog1.log(level= 40, msg="This product is on offer for: %s" %vlr)
            DhLog1.info(msg="MINIMUM QUANTITY: %s" %mnm)     
        Central.prod_on_offer_controller(
            [(str(prod_code), 
                {'price':vlr, 
                 'minimum':mnm, 
                 'counter':cnt})], 'set')
        print("debug of <dict> controllers after updated: [%s]: %s"
               %(prod_code, Central.prod_on_offer_controller(gt_log=True).get(str(prod_code))))
        return
        

    # 🔧💲
    def Promotions_Launcher_Controller(self, prod_code: int, promotion_value: float):
        # THIS STEP OF OUR CODE IS WHERE WE EXTRACT PROMOTION CONTROLLERS...
        print('\n🔖 LOOK AT THIS @property BEFORE IT IS CALLED:')
        controllers:dict = Central.prod_on_promotion_controller().get(str(prod_code))
        mn = controllers['min']
        prcd = controllers['prom_code']
        mx = controllers['max']
        repeat = controllers['repeat']
        mx_prm = controllers['max_promo']
        cpf = controllers['cpf']
        cnt = controllers['counter']
        cnt += 1 

        #--------------------------------------------------------------------------------------------------------------//
        # PAY ATTENTION!!
        # There is an difference between the 'cnt' variable written inside of the _property dict: 
        # Central.prod_on_promotion_contoller and the 'counter' of the products' launcher for sale. This {cnt} variable
        # lets us to know if this product can  be  considered  in  their promotion. This  {cnt}  variable stored inside
        # of dictionary is an promotions delimiter and the 'counter' variable controls the product launching during the
        # replacement of products for sale.
            
        # WHETER THERE'S NOT A PRODUCT DICITONARI FOR THE PRODUCT ON (var):'prod_conde' A NEW DICT
        # OF PRODUCTS FOR SALE WILL BE CREATED ONCE THIS FUNCTION IS CALLED. THIS DICT.py CONTAINS THE PRICES ON 
        # PROMOTION FOR EACH PRODUCT STORED IN ITS ACESS KEYS. IT IS CLEAR THAT THIS FEATURE IS ACCORDING TO PROMOTION
        # CONTROLLERS AS THEIR NUMERICAL COUNTERS, FOR EXAMPLE.
        #--------------------------------------------------------------------------------------------------------------\\
        
        print('\n💡 PROMOTION CONTROL:'); create_line(20, cmd='print')
        if(str(prod_code) not in Central.product_on_promotion_subdict().keys()):
            Central.product_on_promotion_subdict(
                [(str(prod_code), 
                    {'prod_code':prod_code, 
                     'prom_code':prcd, 
                     'promotion_value':promotion_value})], 'set')
            print("debug of @entity <dict> Centralizer.product_on_promotion_subdict':")
            for _key in Central.product_on_promotion_subdict().keys():
                print("🔑[%s]: %s" %(_key, Central.product_on_promotion_subdict(gt_log=True).get(_key)))
        Central.prod_on_promotion_controller(
            [(str(prod_code), 
                {'prom_code':prcd, 
                 'min':mn, 'max':mx, 
                 'cpf':cpf, 'max_promo':mx_prm, 
                 'repeat':repeat, 'counter':cnt})], 'set')                     
        print("\n🔧⚙ <var>'controllers' after updated:")
        for _key in Central.prod_on_promotion_controller().keys():
            print("🔑[%s]: %s" %(_key, Central.prod_on_promotion_controller(gt_log=True).get(_key)))
        return
    

    # 🔧🔁
    def Reset_Offer_Controll(self):
        print('\n🔄✨ OFFERS REFRESH!'); create_line(20, cmd='print')
        Central.prod_on_offer_controller('clear')
        #print("🗝 Central.prod_on_offer_controller().keys() %s"
        #      %(Central.prod_on_offer_controller().keys(),))
        #\\... ReSTORING...
        if(Central.offer_controllers_storage() not in (None, {})):
            Central.prod_on_offer_controller(Central.offer_controllers_storage(), 'set')
            print("@entity: Central._prod_on_offer_controller has been updated to:")
            for e in Central.prod_on_offer_controller().keys():
                print("🗝 [%s]: %s" %(e, Central.prod_on_offer_controller(gt_log=True).__getitem__(e)))
        else:
            print("❕ There isn't offers to restore from storage.")
        return

    # 🔧🔁
    def Reset_Promotion_Controll(self):
        print('\n🔄✨ PROMOTION REFRESH!'); create_line(25, cmd='print')
        self.promotion_code_on_use.clear()
        Central.prod_on_promotion_controller('clear')
        Central.product_on_promotion_subdict('clear')
        #print("🗝 Central.prod_on_promotion_controller().keys(): %s" 
        #      %(Central.prod_on_promotion_controller().keys(),))
        #\\... ReSTORING...
        if(Central.promotion_controller_storage() not in (None, {})):
            Central.prod_on_promotion_controller(Central.promotion_controller_storage(), 'set')
            print("@entity: Central.prod_on_promotion_controller has been updated to:")   
            for e in Central.prod_on_promotion_controller().keys():
                print("🗝 [%s]: %s" %(e, Central.prod_on_promotion_controller(gt_log=True).__getitem__(e)))
        else:
            print("❕ There isn't promotion to restore from storage.")
        return


    @keyword(name='Interpreter Of Sequences')
    def Sequence_Parser(self, 
            sequence:list|tuple, 
            is_list:bool= True) -> list|tuple:
        
        #/// START REPLACEMENT ::
        replace:list =  list()
        for i in range(len(sequence)):
            print('📝 sequence in [%s]: %s ⇒ type(%s)'
                   %(i, sequence[i], type(sequence[i])))
            #/// THEN ::
            if(isinstance(sequence[i], int)): 
                replace.append(sequence[i])
            else:
                if((isinstance(sequence[i], (list, tuple)))
                    and (isinstance(sequence[i][1], int,))):
                    for e in range(sequence[i][1]): replace.append(sequence[i][0])
                
                elif((isinstance(sequence[i]), (list, tuple))
                     and isinstance(sequence[i][1], float)): 
                    #/// APEND TO AUXILIAR 'Kg' PRODUCT CONTROL ::
                    if(sequence[i][0] not in replace):
                        self.Kg_product_control.update(
                            [(sequence[i][0], {'code':sequence[i][0], 'kg':sequence[i][1]})])
                        replace.append(sequence[i][0])
                    else:
                        #/// EXTRACT VALUE FROM @property sel.Kg_product_control AND APPLY IT ::
                        add = ope.add(
                            self.Kg_product_control.get(sequence[i][0]['kg']), sequence[i][1])
                        self.Kg_product_control.update(
                            [(sequence[i][0], {'code':sequence[i][0], 'kg':round(add, 4)})])
                else:
                    print("\n❌ Invalid Data Type or Expression in sequence[%s]" %i)
                    raise ValueError()
            print('append ⇨ %s\n' %(replace[i],))
        
        #/// FINISH PROCESS ::
        print("\n• List length: %s" %len(replace))
        for t in range(len(replace)): print(' ◾ [%s] => %s' %(t, replace[t]))
        
        print("\n• 'Kg Products' List length:")
        for j in range(len(self.Kg_product_control)): 
            print(" ⚖ [%s] => %s" %(j, self.Kg_product_control[j]))
        return replace if(is_list is True) else tuple(replace)


    @keyword(name='Set Group Products For Sale')
    def Items_Grouping(self):
        prod_for_sale:dict = Central.products_for_sale().copy()
        new_dict = dict()
        
        def Get_Product_Barcode(_key:object) -> str:
            print("\nSEARCHING FOR [%s] IN THE _property <dict> self.products..." %_key)
            _all_keys = list(Central.products().copy())
            for i in range(len(_all_keys)):
                try:
                    elem:dict = Central.products().get(str(_all_keys[i]))
                    inner_key_values = elem.values()
                    if(_key in inner_key_values): 
                        print(f"'elem': {elem}\nvalues_in_elem: {inner_key_values}")
                        return elem['bar_code']; break
                    else: continue
                except: 
                    log.info(msg='\n', also_console=True); log.error(msg='...')
                    DhLog1.error(msg='\n¡%s is not found!' %_key); raise KeyError()
        
        def Check_For_Kg_Product(pcode:int) -> float:
            keys = list(self.Kg_product_control.copy())
            if(pcode in keys):
                extract:dict = self.Kg_product_control.get(pcode)
                create_line(40, cmd='prirnt')
                print("⚖ Has been found an element inside <dict>"
                      " self.Kg_product_control like %s"%pcode)
                create_line(40, break_line=True, to_the_end=True, cmd='prirnt')
                return extract['kg']
            else: return float(0)

        print("\nCREATING A NEW MAPPING OF PRODUCTS FOR SALES BUILDING...")
        #--------------------------------------------------------------------------------------------------||
        #                                       MAPPING STRUCTURE 
        #--------------------------------------------------------------------------------------------------||
        # <int>: [Master_Key]               -> <dict> main_indexer: {elem['prod_code']} as _key()
        #   ↳ <str>: [access_key]           -> <dict> key_value: 'barcode'  => <str>
        #       ↳ <str>: [access_key]       -> <dict> key_value: 'quantity' => <int>
        #           ↳ <str>: [access_key]   -> <dict> key_value: 'total'    => <float>
        #--------------------------------------------------------------------------------------------------||
        for elem in prod_for_sale.keys():
            barcode:str = Get_Product_Barcode(prod_for_sale[elem]['prod_code']); print("◈ 'barcode': %s" %barcode)
            prod_code:object = prod_for_sale[elem]['prod_code']; print("◈ 'prod_code': %s" %prod_code)
            prod_price:float = prod_for_sale[elem]['prod_price']; print("◈ 'prod_price': %s" %prod_price)
            prod_status:bool = prod_for_sale[elem]['dsct_status']; print("◈ 'dsct_status': %s" %prod_status)
            prod_kg = Check_For_Kg_Product(prod_for_sale[elem]['prod_code']); print("⚖ 'prod_kg': %s" %prod_kg)                                                            

            if((ope.eq(new_dict, {})) or (prod_for_sale[elem]['prod_code'] not in new_dict.keys())):
                print("Building a <dict>: 'new_dict' of products group for sale...")
                new_dict.update(
                    [(prod_code, 
                        {'barcode':barcode, 
                         'quantity':(int(1) if(ope.le(prod_kg, float(0))) else prod_kg), 
                         'total':prod_price if(ope.le(prod_kg, float(0))) else round2(ope.mul(prod_price, prod_kg)),
                         'mod_status':prod_status})])
                print("<dict>: new_dict has received a new element in their access keys: '%s'"
                    %(prod_for_sale[elem]['prod_code'],)); print(f"► [{prod_code}]: {new_dict.get(prod_code)}")
            else:
                qnt_sum:int= ope.add(new_dict[prod_code]['quantity'], 1)
                # This _sum process is make from @property <dict>: Centralizer.products_for_sale attributes whose
                # are captured and stored in the _local_object <dict>: 'new_dict' until the current loop is ended.
                price_sum:float = round2(ope.add(prod_price, new_dict[prod_code]['total']))
                new_dict.update(
                    [(prod_code, 
                        {'barcode':barcode, 
                         'quantity':qnt_sum, 
                         'total':price_sum, 
                         'mod_status':prod_status})])
                print("\nOne or more than element into of the <dict> 'new_dict' were updated to the new value!")
                print(f"► [{prod_code}]: {new_dict.get(prod_code)}")
        #\\... THEN ::
        print("\n✔ <dict>: 'new_dict' has been created!\n► The @property <dict>: " +
              "Centralizer.group_prod_for_sale was updated to copy from <new_dict> access_keys")
        print("👁‍🗨 Look at the body of the <object>(dict): 'new_dict':")
        for i in new_dict.keys():
            print("🔑 [%s]: 🛒 %s" %(i, new_dict.get(i)))

        Central.group_prod_for_sale(new_dict, 'set'); dict_length:int = len(list(new_dict))
        print("\n-> The new dictionary of products for sale countains %s items!" %dict_length)
        return dict_length


    @keyword(name='Get Group of Products For Sale')
    def Get_The_Group(self, indexer:int) -> tuple:
        elements = list(Central.group_prod_for_sale().copy())
        print("There are %s elements in @entity Centralizer.group_prod_for_sale" %(len(elements)))
        if(indexer <= len(elements)):
            print("Handling indexer number: [%s]" %indexer)
            product:dict = Central.group_prod_for_sale().get(elements[indexer])
            print("Element in [%s] -> '%s'" %(indexer, elements[indexer]))
        else: 
            print("<var> 'indexer' is out of the range in the <list>: 'elements'" +
                "generated from @entity <dict>: Centralizer.group_prod_for_sale ")
            raise Exception()
        
        prod_attr:tuple = (
            product['quantity'], 
            elements[indexer], 
            product['barcode'], 
            product['total'], 
            product['mod_status'])
        
        print("\nLook at the products attributes has generated from @propertry <dict>: " +
              "Centralizer.group_prod_for_sale in the indexer [%s] in elem '%s': %s" 
              %(indexer, elements[indexer], Central.group_prod_for_sale().get(elements[indexer])))
        return prod_attr


    # ¡Uncompleted function!
    def Launch_Produto_Kg(self, prod_code: int, prod_barcode: str, prod_name:str):
        print("LAUNCHING THE PRODUCT KG...")
        print('---------------------------')
        rplc: dict = {'prod_code':prod_code, 'prod_barcode':prod_barcode, 'description':prod_name}
        _dict_key = create_number_key()
        Central.produto_pesavel([(str(_dict_key), rplc)], 'set')
        print("@property Centralizer.produto_pesal has been updated to: \n%s" %(Central.produto_pesavel(),))
        # Continue....
        pass


    @keyword(name='Remove Product From Sale')    
    def Remove_Product_From_Dict(self, last_prod:bool= True, code:int= 0):
        itm = dict()
        print("\n📑 Items in <dict> Ce.products_for_sale before remotions from itself:")
        for _key in Central.products_for_sale().keys(): 
            print("[%s]: %s" %(_key, Central.products_for_sale().get(_key)))
        
        # Internal resources for this method ::
        # /// Look Up and Count for products code has found in the sequence ::
        def looking_for(i_code:int) -> tuple: 
            print("\n🔍 Searching for [%s] inside of <dict> Ce.products_for_sale searching ..." %code)
            i_add = list()
            for elem in Central.products_for_sale().keys():
                itm:dict = Central.products_for_sale().get(elem)
                if(ope.eq(i_code, itm.get('prod_code'))): i_add.append(elem)
                else: continue
            print("\n🔧 <def>: looking_for -> tuple: %s" %(tuple(i_add),))
            return tuple(i_add)
        # /// Search for products has stored on @property <dict> self.products and return it.
        def searching_element(prod_code:int) -> dict:
            items_in_k = dict()
            for k in Central.products().keys():
                items_in_k:dict = Central.products().get(k)
                if(ope.eq(prod_code, items_in_k.get('code_id'))):
                    break 
                else: continue
            print("\n🔧 <def>: searching_element -> dict:\n► %s" %(items_in_k,))
            return items_in_k
        
        # 📝 LAST ITEM HAS INDEXED AS dict_key IN Ce.products_for_sale ::
        if((last_prod is True) and (ope.eq(code, int(0)))):
            # This statements performs an extraction of the last item in the dict_keys range.
            # The last boolean clause handling this resource. To keep the Ce.products_for_sale 
            # integrity, that proccess has done using a copy from main products dictionary. 
            copy:dict = Central.products_for_sale().copy(); elements:list = list(copy)
            itm:dict = Central.products_for_sale().get(elements[-1])
            print("\n❌📝 Removing last item [%s] of the product code %s from Ce.products_for_sale dictionary"
                   %(elements[-1], itm.get('prod_code')))
            Central.products_for_sale().pop(elements[-1])
        
        # 🔍 LOKKING FOR EXPECIFIC ITEM FROM DICTIONARY KEYS ::
        elif((ope.ne(code, int(0))) and (last_prod is False)):
            results:tuple = looking_for(code)
            for e in range(len(results)):
                print("\n❌ Removing item [%s] of the product code %s from Ce.products_for_sale dictionary"
                   %(results[e], Central.products_for_sale().get(results[e])))
                if(results[e] in Central.products_for_sale().keys()):
                    Central.products_for_sale().pop(results[e])
        
        # ❓ EXCEPTION SETTINGS TRATEMENT
        else:
            log.info('\n', also_console=True); log.error('[Argument Exception]')
            DhLog1.error('\nInvalid argument settings has entered in this keyword!')
            raise ValueError()

        # Simple Function type: Find and Get ::
        prod_proprt:dict = (
            searching_element(itm['prod_code'])
            if((last_prod is True) and ope.eq(code, 0)) 
            else searching_element(code))
        
        log.info("", also_console=True); log.error('...')
        DhLog2.debug("%s" %(create_line(59, char='=', break_line=True, cmd='return'),))
        DhLog1.error("This product code [%s] has been removed from the sequence" %prod_proprt.get('code_id'))
        DhLog1.warning("Check for the Product Record against database [%s]." %MySQLConnector.Get_Database_Name())
        mssg = format_keyValues(22, prod_proprt)
        DhLog2.debug("%s" %(create_line(59, cmd='return'),))
        # Console output...
        for i in range(len(mssg)): DhLog1.critical(str(mssg[i]))
        DhLog2.debug("%s" %(create_line(59, cmd='return'),))

        print("\n\n📑👌 New dictionary of products for sale: <dict> Ce.products_for_sale:")
        for _key in Central.products_for_sale().keys(): print("[%s]: %s" %(_key, Central.products_for_sale().get(_key)))
        return
    
   
    @keyword(name='Set Payment Way')
    def Set_Payment_Way(self, paymnt_way:str= 'DIN, CHQ, CRE, CRT, TEF, PIX, BNC, VLE'):
        """
        DOCUMENTATION:
        
        \rTHIS  KEYWORD  IS  RESPONSIBLE FOR NOTICE TO THE SYSTEM ABOUT THE PAYMENT METHOD ON USE
        DURING THE TEST AT RUNTIME. SOME PAYMENT METHODS CAN CHANGE THE OFFER CONTROL PERFORMED
        IN THE MOMENT OF THE SALE FINALIZATION."""
        
        #-> The 'key_code' variable is the keyboard [key_code] represented by an interger sequence base 10 type Shift.
        # This interger represents a serial letter in the computer keyboard and it's used to enter the payment method
        # to be used in the sale in running.
        key_code: str= 'Empty' 
        
        if(paymnt_way not in ('DIN', 'CHQ', 'CRE', 'CRT', 'TEF', 'PIX', 'BNC', 'VLE')):
            log.info(msg='\n', also_console=True) 
            log.error(msg='...')
            DhLog1.error('\nThis method requieres a valid payment method reference!')
            DhLog1.warn('Check your Payment Method on usage according to their value' +
                        '\nVerifier the possibilities on Prates Documentation and')
            raise ValueError()
        else:
            for elem in Payment.payment_ways().keys():
                paymnt_attr:dict = Payment.payment_ways().get(elem)
                if(ope.eq(paymnt_way, paymnt_attr['unq_key'])): 
                    Payment.current_paymnt_on_use(paymnt_way, 'set')
                    key_code = 'KEY.' + paymnt_attr['key_code']
                    break
                else: continue
        return key_code

    
    @keyword(name='Replace Products On Offer')
    def Replace_Products_On_Offer(self):
    
        print("\nREPLACING PRODUCTS ON OFFER AVAILABLE IN THE PRODUCTS FOR SALE...")
        #\\... lambda function writen to extract dictionary key-values ::
        extract = (
            lambda x, y: x.get(y) 
                if((isinstance(x, dict)) and (isinstance(y, (str, int))) and (x.__contains__(y))) else None)
        #\\... extracting dictionary key-vallues ::
        pdv_settgs:dict = extract(PDVConfig.Read_System_Config(), 'function_keys')
        if ope.eq(pdv_settgs, None): 
            print("❗❓ [FunctionError]: 'extract' <lambda> function has is empty or None!")
            raise ValueError()
        else: pass

        print("@entity: Central.prod_on_offer_controller ↴")
        extraction = list(Central.prod_on_offer_controller()) if ope.ne(Central.prod_on_offer_controller(), {}) else None
        for e in Central.prod_on_offer_controller().keys():
            print("[%s]: %s" %(e, Central.prod_on_offer_controller().__getitem__(e)))

        def find(ref:str|int):
            for _id in Central.products().keys():
                elem = extract(Central.products(gt_log=True, elem_key=_id).__getitem__(_id), 'code_id')
                if((ope.ne(elem, None)) and (ope.eq(elem, ref))):
                    break
                else: continue
            return _id
        
        # CHECK FOR PAYMENT RESTRICTION ::
        if(ope.eq(Payment.current_paymnt_on_use(), 'CRE') and (bool(pdv_settgs.get('NAOPROMOCAOVENDAPRAZO')) is True)):
            print("\n❕❗ The settings of the ERP System is applying a payment control to the customer payment method!" +
                    "No Offer and Promotion are available for this payment method on use."
                    "\nCheck for the PDV System Settings on 'C://Visual Software/MyComemrce/PDV/Manutencao.exe'" +
                    "\nto apply the payment delimiters to this promotional controller according their attibutes!")
            #\\... CONSOLE LOG ::
            DhLog2.debug('%s' %(create_line(59, cmd='return'),))
            DhLog2.warning('%s' %(dlmt_space(59, ('[ WARN ]', 'Restricted Payment Way'.upper())),))
            DhLog2.debug('%s' %(create_line(59, cmd='return'),))
            DhLog1.warning("No Offer or Promotion is available to this payment method".upper())
            DhLog1.warning("There is a restriction actived on ERP System. Check it out.".upper())
            DhLog2.debug('%s' %(create_line(59, break_line=True, to_the_end=True, cmd='return'),))
            #\\... ADUJSTMENT ::
            for _key in Central.products_for_sale().keys():
                pcode = extract(Central.products_for_sale(gt_log=True, elem_key=_key).__getitem__(_key), 'prod_code')
                _id = find(pcode)
                replace:dict = {
                    'prod_code':pcode,
                    'prod_price':extract(Central.products(gt_log=True, elem_key=str(_id)).__getitem__(_id), 'price_T1'), 
                    'dsct_status':False}
                Central.products_for_sale([(str(_key), replace)], 'set')
            return #\\... ESCAPE
        else: pass

        # REPLACEMENT ::
        for _key in Central.products_for_sale().keys():
            values = Central.products_for_sale().__getitem__(_key)
            print("key [%s] -> values: %s" %(_key, values,))
            if((extraction is not None) and (str(values['prod_code']) in extraction)):
                create_line(120, char='_', cmd='print')
                prod_offer:dict = Central.prod_on_offer_controller().__getitem__(str(values['prod_code']))
                print("\n@property: self.prod_on_offer_controller [%s] -> %s" %(values['prod_code'], prod_offer))
                minimum = prod_offer['minimum']; counter = prod_offer['counter']; offer_value = prod_offer['price']
                print('Extraction Elements ↴\n-> Min: %s,\n-> Counter: %s,\n-> Price: %s' %(minimum, counter, offer_value))
                print("{prod_offer}: %s" %(prod_offer,))
                if(counter >= minimum):
                    replace: dict = {'prod_code':values['prod_code'], 'prod_price':offer_value, 'dsct_status':False}
                    Central.products_for_sale([(str(_key), replace)], 'set')
                    print("\n@property Centralizer.products_for_sale has updated to:\n%s"
                        %(Central.products_for_sale(gt_log=True).get(_key),))
                elif(minimum <= 1): print("\nThis Product has been released directly with its promotional value.!")
                else: print("\nMinimun quantity has not been contemplated in this sale!")
                create_line(120, char='_', break_line=True, to_the_end=True, cmd='print')
        return


    @keyword(name='Replace Products On Promotion')
    def Replace_Products_On_Promotion(self):
        # WHENEVER THERE IS AN AVALIABLE PROMOTIONS IN EXECUTION, THIS KEYWORD WILL CHECK IF
        # THE PROMOTIONAL PRICES CAN BE APPLIED FOR SALE OR NOT. THE OFFER CONTROL PROPERTIES CAN BE FOUND ON
        # <class> DataManipulator.py AND SOMETHING OF ITS PROPERTIES ARE WRITTEN AT <calss> DataManager.py.

        prm_cd: int = 0
        for i in range(len(self.promotion_code_on_use)):
            print('\n\n\n💠 PROMOTION CODE STATUS VERIFICATION FOR AVAILABLE OFFER...'); create_line(61, cmd='print')
            print(f"✨🎉 Available Promotions in the dictionary: {self.promotion_code_on_use}")
            controllers:dict = Central.prod_on_promotion_controller().__getitem__(str(self.promotion_code_on_use[i]))
            # HTML OUTUPUT ::
            print('\nDebug of @entity Central.prod_on_promotion_controller:')
            for n in Central.prod_on_promotion_controller().keys(): 
                print('🗝 [%s]: %s' %(n, Central.prod_on_promotion_controller(gt_log=True).get(n)))
            print('\n⚙ Controllers to be used in this process: 🔧 %s' %(controllers,))
            
            # MAIN CONTROLLERS OF THE PROMOTION IN RUNNING...
            mn_qnt = controllers.get('min')
            max_qnt = controllers.get('max')
            prm_cd = controllers.get('prom_code')
            repeat = controllers.get('repeat')
            cnt = controllers.get('counter')
            promo_max = controllers.get('max_promo')
            
            # ANOTHER CONTROLLERS OF THIS PROMOTION, IF ANY...
            # LAMBDA EXPRESSION WRITEN TO EVALUATE A DICTIONARY COMPREENSION ::
            extract = (
                lambda x, y: x.__getitem__(y) 
                if((isinstance(x, dict)) 
                   and (isinstance(y, (str, int))) 
                   and (x.__contains__(y) is True)) 
                else None)
            
            print('\n\nCHECKING FOR PAYMENT CONTROLLERS:%s' %create_line(33, break_line=True, cmd='return'))
            print('💡 Promotional Code On Usage: [%s]' %prm_cd)
            print('◉ All Available Payments Controllers: ↴')
            for e in Central.payment_controllers().keys(): print("  🗝 [%s]: %s" %(e, Central.payment_controllers().get(e)))
            print('\n◉ Payment Controllers in this promotion: ↴\n%s' %Central.payment_controllers().__getitem__(str(prm_cd)))
            paymnt = Payment.current_paymnt_on_use(); print("💲 Payment Code on Usage: %s" %paymnt)
            pay_methods:list = extract(Central.payment_controllers().__getitem__(str(prm_cd)), 'paymnt_method')
            modifier_config:bool = Central.block_discount_for_promotion()
            print("🤔 BLock discount to this promotion: %s" %modifier_config)
            pdv_settgs:dict = extract(PDVConfig.Read_System_Config(), 'function_keys')
            
            # IN THIS STEP, WE EXTRACTS THE ELEMENT 'unq_key' FROM <dict> Centralizer.payment_ways AND COMPARE
            # IT TO THE PAYMENT CODE ON USAGE AND RECORDED AS <dict> PROPERTIES INDEXED FOR ITS [access_key]'s.
            # LOOKING FOR PAYMENT WAY WHERE ITS CODE AND UNIQUE KEY BE EQUAL TO THE CURRENT PRODUCT'S PROMOTION CODE ::
            pay_checking:bool = False
            if(bool(pdv_settgs.get('OPCOES_PROMOFINALIZADORAS')) is True):
                for _key in Payment.payment_ways().keys():
                    print("Checking Payment Code '%s' in Central.payment_ways.keys() ⇨ " %(_key,) +
                        "💰 Payment Unique Key in [%s]: '%s'" %(_key, (extract(Payment.payment_ways().get(_key), 'unq_key'))))
                    if(
                        #\\... 0n CLAUSE ::
                        (ope.eq(pay_methods, None) is True)
                        
                        #\\... 1ª CLAUSE ::
                        or ((
                            (ope.ne(paymnt, 'CRE'))
                            and (ope.eq(pay_methods, None))
                            ) is True
                           )
                        #\\... 2ª CLAUSE ::
                        or ((
                            (ope.ne(pay_methods, None))
                            and (int(_key) in pay_methods)
                            and (ope.eq(paymnt, extract(Payment.payment_ways().get(_key), 'unq_key')))
                            and (ope.ne(extract(Payment.payment_ways().get(_key), 'unq_key'), 'CRE')) 
                             ) is True
                            )
                        #\\... 3 CLAUSE ::							
                        or ((
                            (ope.ne(pay_methods, None))
                            and (int(_key) in pay_methods)
                            and (ope.eq(paymnt, extract(Payment.payment_ways().get(_key), 'unq_key')))
                            and (ope.eq(extract(Payment.payment_ways().get(_key), 'unq_key'), 'CRE')
                                and (bool(pdv_settgs.get('NAOPROMOCAOVENDAPRAZO')) is False))
                             ) is True
                            )
                        ): #\\... END IF
                        
                        msg:str ="💰🎉 THIS PAYMENT WAY IS AVAILABLE ON PROMOTION!"
                        print("\n%s%s" %(msg, create_line(msg.__len__() + 3, break_line=True, cmd='return')))
                        pay_checking = True; break
                    else: continue
            else:
                if(ope.ne(paymnt, 'CRE') 
                   or (ope.eq(paymnt, 'CRE')
                       and (bool(pdv_settgs.get('NAOPROMOCAOVENDAPRAZO')) is False))):
                    pay_checking = True 
                else: pass
                print("\n❕❗ The settings of the PDV System aren't applying a promotional payment control!" +
                      "\nCheck for the PDV System Settings on 'C://Visual Software/MyComemrce/PDV/Manutencao.exe'" +
                      "\nto apply the payment delimiters to this promotional controller according their attibutes!")
    
            prod_cd = str(self.promotion_code_on_use[i])
            print(f"\n🔧🔖 Look at controllers of '{self.promotion_code_on_use[i]}': {controllers}")
            print(f"🔍 checking the promotion code [{prm_cd}] of the product '{prod_cd}' " +
                  f" of the available product promotion: {self.promotion_code_on_use}...")
    
            if(pay_checking is False):
                print('❌ This promotion is unvailable for this payment method!'.upper())
                DhLog1.info('%s' %(create_line(59, cmd='return'),))
                DhLog1.info('%s' %(dlmt_space(59, ('[ INFO ]', f'Promotion Code: {self.promotion_code_on_use[i]}')),))
                DhLog1.info('%s' %(create_line(59, cmd='return'),))
                DhLog2.debug("This promotion is unvailable for this payment method!".upper())
                DhLog1.info('%s' %(create_line(59, break_line=True, to_the_end=True, cmd='return'),))

            elif((pay_checking is True) and (controllers['cpf'] is True)):
                print('\n❕ THIS PRODUCT PROMOTION IS CONTROLED FOR THE CPF OR CNPJ CODE!')
                # <class> ``Centralizer`` PROPERTIES OF CONTROL BY CPF CODE ::
                # AT THE FIRST WE REMOVE THE PUNCTUATION FROM CPF/CNPJ STRING USING THE STRING.FORMAT RESOURCE!
                # UNDESEJABLE  CHARACTERS: '''!()-[]{};:'"\,<>./?@#$%^&*_~'''. AFTER THIS PROCESS, WE CHECK FOR
                # CPF/CNPJ CODE IN THE @property: Centralizer.store_cpf_code_for_promotion_control TO  SET
                # THE PROMOTION OR NOT. CASE  THE @property IS EMPTY, IT MEANS THIS PROMOTION CODE HAS BEEN NOT
                # USED YET BEFORE THIS PRESENT MOMENT...
                cpf_cnpj = Central.current_cpf_cnpj()
                cpf_cnpj = remove_punctuation(string_text= cpf_cnpj)  
                serial_control:dict = Central.cpf_controller_storage().__getitem__(str(prod_cd))
                dict_cpf_code:dict = serial_control.__getitem__('cpf_code')

                # -> hltm.log OUTPUT ::
                print('\n\nPEFORMING CPF/CNPJ CHECKING... 🔍')
                create_line(32, cmd='print')
                print(f"-> Centralizer.customer_cpf_cnpj: {cpf_cnpj}")
                print(f"-> Centralizer.cpf_controller_storage in key: [{prod_cd}]")
                for t_key in serial_control.keys():
                    if(not isinstance(serial_control[t_key], dict)):
                        print('  - %s: %s' %(t_key, serial_control.get(t_key))) 
                    else: 
                        elements:dict = serial_control.get(t_key)
                        for n_key in elements.keys(): print('   - %s: %s' %(n_key, elements[n_key]))
                
                print("👁‍🗨 Look at keys in <dict> [dict_cpf_code]:")
                for k_key in dict_cpf_code.keys(): print('  - %s: %s' %(k_key, dict_cpf_code[k_key]))

                # ** THIS STATEMENT CONSIDERS THE POSSIBILTY OF BE IN USAGE THE CLIENT CODE NUMBER '1'.
                # WHENEVER THE NEXT STATEMENT MAKE THE LAUNCHING OF THE CLIENT 'cpf_cnpj' CODE INSIDE THE 
                # @property Centralizer.cpf_controller_storage. 
                if((cpf_cnpj is not None) and (ope.ne(cpf_cnpj.lower(), 'is null'))):
                    replacement:dict = dict_cpf_code.copy()
                    if(cpf_cnpj not in dict_cpf_code.keys()):
                        print('📝 INSERTING CPF/CNPJ %s IN THE Centralizer.cpf_controller_storage <-' %(cpf_cnpj))
                        replacement.update([(str(cpf_cnpj), {'cpf_cnpj':cpf_cnpj, 'counter_used':int(0)})])
                        dict_cpf_code.update(replacement); serial_control['cpf_code'] = dict_cpf_code

                        # -> hltm.log OUTPUT ::
                        print('\n❕ <dict> [serial_control] after update itself:')
                        for t_key in serial_control.keys():
                            if(not isinstance(serial_control[t_key], dict)):
                                print(' 🗝 %s: 📩 %s' %(t_key, serial_control[t_key]))
                            else: 
                                elements: dict = serial_control[t_key]
                                for n_key in elements.keys(): print('    🗝 %s: 📩 %s' %(n_key, elements[n_key]))

                    print('\n\n📑 REPLACING THE PRICE OF THE PRODUCTS ON SALE ACCORDING TO THE PROMOTION NUMBER: [%s]' %prod_cd)
                    create_line(84, cmd='print')
                    print(f"🧿 ALL Products ON SALE:")
                    for i_key in Central.products_for_sale().keys():
                        print(Central.products_for_sale().get(i_key))

                    print(f"\n✨🎉 Products ON PROMOTION:")
                    for e_key in Central.product_on_promotion_subdict().keys():
                        print("▸ [%s]: %s" %(e_key, Central.product_on_promotion_subdict().__getitem__(e_key)))

                    print(f"\nKeys from dictinaries:\n'elem_1': {Central.products_for_sale().keys()}"+
                        f"\n'elem_2': {Central.product_on_promotion_subdict().keys()}\n")


                    # EXTRACTION HIERARCHY ::
                    #   |__. [prod_code]         -> <dict> master_key
                    #       |__. [cpf_cnpj]      -> <dict> access_key
                    #           ↳.  [element]    -> <dict> desidered data
                    
                    # IN THE FIRST TIME IT'S NECESSARY TO VERIFY HOW MANY PRODUCTS ON PROMOTION THERE ARE FOR EACH AVALIABLE PROMOTION
                    # PERFORMED  BY  THIS  FUNCTION. IT'S  IMPORTAT REMEMBER THAT THERE ARE NO MORE PRODUCTS IN THE  DICTIONARY OF 
                    # PROMOTIONAL PRODUCTS THAN THE MAXIMUM QUANTITY ALLOWED BY THEIR CONTROLLERS ::
                    counter: int = 0
                    promotion:float = extract(Central.product_on_promotion_subdict().__getitem__(str(prod_cd)), 'promotion_value')
                    extracting:dict = extract(Central.cpf_controller_storage().__getitem__(str(prod_cd)), 'cpf_code')
                    extracting.get(str(cpf_cnpj))
                    promo_counter = extracting.get('counter_used')  # <- element wished

                    print(f"\n📑 PERFORMING REPLACEMENT IN ACCORDANCE WITH THEIR SETTINGS...")
                    create_line(62, cmd='print')
                    if(cnt >= mn_qnt):
                        for e in Central.products_for_sale().keys():
                            elem = Central.products_for_sale().get(str(e))
                            print("\n🔍 CHECKING PRODUCT: ``%s``" %elem['prod_code'])
                            print(f"debug of 'Manager.product_for_sale' as 'elem' in {e}: {elem}")
                            
                            if(ope.eq(str(elem['prod_code']), prod_cd) and (counter < max_qnt) and (promo_counter < promo_max)):    
                                print('✅ This products is on promotion!'.upper())
                                elem['prod_price'] = promotion
                                elem['dsct_status'] = (False if((elem['dsct_status'] is True) and (modifier_config is True)) else True)
                                print(f"◉ UPDATING: debug of the <builtin>:dict_key {e} as 'elem_2' after updated: {elem}")
                                counter += 1; promo_counter += 1; 
                                print(f"► 'counter': {counter} for LIMIT: {max_qnt} and Promo. Max. {promo_max}")
                                print('CONTINUING...')
                            create_line(136, char='_', cmd='print')   

                        DhLog1.info('%s' %(create_line(59, cmd='return'),))
                        DhLog1.info('%s' %(dlmt_space(59, ('[ INFO ]', f'Promotion Code: {self.promotion_code_on_use[i]}')),))
                        DhLog1.info('%s' %(create_line(59, cmd='return'),))
                        DhLog1.debug('This Customer have been contemplated by this promotion!'.upper())
                        DhLog1.info('%s' %(create_line(59, break_line=True, to_the_end=True, cmd='return'),))

                        # UPDATING CONTROLLERS RECORD ::
                        replacement.update([(str(cpf_cnpj), {'cpf_cnpj':cpf_cnpj, 'counter_used':int(counter)})])
                        dict_cpf_code.update(replacement); serial_control['cpf_code'] = dict_cpf_code
                    else:
                        print('❌ The minimum quantity of products for this promotion has not been reached!'.upper())
                        DhLog1.info('%s' %(create_line(59, cmd='return'),))
                        DhLog1.info('%s' %(dlmt_space(59, ('[ INFO ]', f'Promotion Code: {self.promotion_code_on_use[i]}')),))
                        DhLog1.info('%s' %(create_line(59, cmd='return'),))
                        DhLog2.debug("      the minimum quantity of products for this".upper())
                        DhLog2.debug("           promotion has not been reached!".upper())
                        DhLog1.info('%s' %(create_line(59, break_line=True, to_the_end=True, cmd='return'),))

                else:
                    DhLog1.info('%s' %(create_line(59, cmd='return'),))
                    DhLog1.info('%s' %(dlmt_space(59, ('[ INFO ]', f'Promotion Code: {self.promotion_code_on_use[i]}')),))
                    DhLog1.info('%s' %(create_line(59, cmd='return'),))
                    DhLog2.debug('NO CUSTOMER CPF CODE HAS BEEN NOTICED OR THIS CPF/CNPJ')
                    DhLog2.debug('has already been contemplated in this promotion!'.upper())
                    DhLog1.info('%s' %(create_line(59, break_line=True, to_the_end=True, cmd='return'),))
                    print('❌ THIS CPF/CNPJ CODE HAVE ALREADY BEEN CONTEMPLATED!!\n\n')
            
            elif((pay_checking is True) and (controllers['cpf'] is False)):
                print('\n\n📑 REPLACING THE PRICE OF PRODUCTS FOR SALE ACCORDING PROMOTION AVALIABLE [%s]...' %prm_cd)
                create_line(83, cmd='print')
                print(f"🧿 ALL Products ON SALE:")
                for t_key in Central.products_for_sale().keys():
                    print(Central.products_for_sale().get(t_key))
                
                print(f"\n✨🎉 Products ON PROMOTION:")
                for n_key in Central.product_on_promotion_subdict().keys():
                        print(Central.product_on_promotion_subdict().get(n_key))

                #-------------------------------------------------------------------------------------------------------------//
                # IN THE FIRST TIME IT'S NECESSARY TO VERIFY HOW MANY PRODUCTS ON PROMOTION THERE ARE FOR EACH AVALIABLE OFFER
                # PERFORMED  BY  THIS  FUNCTION. IT'S  IMPORTAT REMEMBER THAT THERE ARE NO MORE PRODUCTS IN THE  DICTIONARY OF 
                # PROMOTIONAL PRODUCTS THAN THE MAXIMUM QUANTITY ALLOWED BY THEIR CONTROLLERS ::
                #-------------------------------------------------------------------------------------------------------------\\
                counter: int = 0
                promotion = extract(Central.product_on_promotion_subdict().get(str(prod_cd)), 'promotion_value')
                print(f"\n📑 PERFORMING REPLACEMENT IN ACCORDANCE WITH THEIR SETTINGS..."); create_line(65, cmd='print')
                
                if(cnt >= mn_qnt):
                    #-------------------------------------------------------------------------------------------------------------//
                    # INTERNAL CONTROL FOR ITEMS GROUP AND <func> 'Repeat On Sale'. THAT CLAUSE VERIFIERS HOW MANY PRODUCTS AVAILABLE 
                    # IN THE RANGE OF PRODUCTS FOR SALE CAN TO RECEIVE THE PROMOTIONAL VALUE HAS FOUND FOR THIS PORMOTION CODE ON
                    # USAGE FOR EACH PRODUCT. THIS NEXT STATEMENT CREATE SIMILAR SOME LIKE A PRODUCTS PACKAGE, GROUPING EACH PRODUCT 
                    # ACCORDING TO THEIR 'max_qnt' DELIMITER TO APPLYING THE PROMOTION. LOOK AT THE STRUCTURE BELLOW ::
                    #-------------------------------------------------------------------------------------------------------------\\
                    safeguard = list(); delimiter:int = 0; repeat_on_sale:int = 0
                    print("🔧⚙ Internal structure attributes:" +
                          "\n🔹 safeguar: %s\n🔹 delimiter: %s\n🔹 repeat_on_sale: %s" %(safeguard, delimiter, repeat_on_sale))
                    print("\n📦 package of products on promotion".upper())
                    create_line(39, cmd='print')
                    
                    for r in Central.products_for_sale().keys():
                        elem = Central.products_for_sale().__getitem__(str(r))
                        print("-> elem[prod_code]: %s" %(elem['prod_code'],))
                        if(ope.eq(str(elem['prod_code']), prod_cd)):
                            safeguard.append(elem['prod_code'])
                            create_line(39, cmd='print')
                            #---------------------------------------------------------------------------------------------------//
                            # This statements bellow represent the maximmun counter for 'repeat on sale' function. It also works
                            # for pack of products in the promotion code on usage!
                            
                            #... IT'S IMPORTANT TO  KNOW THIS  CLAUSE CONSIDERS PROMOTIONS WITH 'mn_qnt' EQUAL TO int(1) DOESN'T
                            # NEEDS OF A COMPLEX CONTROL. IN THIS CASE, A SIMPLE COUNTER HAS AGGREGATED TO THE RANGE OF PRODUCTS
                            # ON SALE HAS ALREADY CAN CONTROL THE PROMOTINAL REPLACEMENT!
                            
                            # PAY ATENTION!
                            # To fix an existly ambiguity between 'max_qnt' and 'promo_max', the varibale 'max_qnt' assume the
                            # promo_max's value according to the MyCommerce ERP functionality as long as MyCommerce PDV.
                            # That clause is an adjustment speacially writen to do it and nothing more. Check for:
                            #---------------------------------------------------------------------------------------------------\\
                            if(ope.gt(promo_max, max_qnt)): max_qnt = promo_max
							
                            if(ope.ge(len(safeguard), max_qnt) and ope.lt(repeat_on_sale, repeat)):
                                delimiter = ope.mul(safeguard.__len__(), 1) # set to
                                create_line(39, cmd='print')
                                print("🔻❕ <list> [safeguard] has been cleared!" +
									"\n The delimiter is '%s' from rigth now!" %delimiter)
                                create_line(39, cmd='print')
                                safeguard.clear(); repeat_on_sale = ope.iadd(repeat_on_sale, 1)
                            else:
                                if(ope.lt(delimiter, max_qnt)):
                                    print("  🔰 Safeguard: %s\n  🧮 Nº Items: %s" %(safeguard, safeguard.__len__()))
                                    delimiter = ope.iadd(delimiter, (ope.mul(safeguard.__len__(), 1))) # update to
                                    print("  ✨ This element has been added to the list size control\n" +
										  "  for products on promotion according its allowed length.")
                                    create_line(60, cmd='print')
                                else:
                                    print("  🔒 The maximum length allowed by the promotional list control\n" +
										  "  has already been reached. No more elements will receive a discount!")
                                    create_line(60, cmd='print')
                                    pass
                        pass # End loop
                    print("\n🔧⚙ Delimiter for aplying of the promotion: %s" %delimiter)
                    
                    #\\ ... APPLYING PROMOTIONAL VALUE TO THE PRODUCTS TO REPLACING...
                    for e in Central.products_for_sale().keys():
                        elem = Central.products_for_sale().__getitem__(str(e))
                        print("\n🔍 CHECKING PRODUCT: '%s'" %elem['prod_code'])
                        print(f"   _property: Manager.product_for_sale as 'elem' in {e}: {elem}") 
                        if(((ope.eq(str(elem['prod_code']), prod_cd)) 
                            and (ope.lt(counter, delimiter)) is True)):
                            print('  ✅ This products is on promotion!'.upper())
                            elem['prod_price'] = promotion
                            elem['dsct_status'] = False if((elem['dsct_status'] is True) and (modifier_config is True)) else True
                            print(f"\n   ↻ UPDATING: <builtin>:dict_key {e} as 'elem_2' after updated: {elem}")
                            counter = ope.iadd(counter, 1)
                            print(f"  ▸ Look at the 'counter': {counter} for LIMIT: {max_qnt} and 'Repeat on Sale': {repeat}")
                        pass

                    DhLog1.info("%s" %(create_line(59, cmd='return'),))
                    DhLog1.info('%s' %(dlmt_space(59, ('[ INFO ]', f'Promotion Code: {self.promotion_code_on_use[i]}')),))
                    DhLog1.info("%s" %(create_line(59, cmd='return'),))
                    DhLog1.debug(msg='\rThis Customer have been contemplated by this promotion!'.upper())
                    DhLog1.info("%s" %(create_line(59, break_line=True, to_the_end=True, cmd='return'),))

                else:
                    print('❌ the minimum quantity of products for this promotion has not been reached!'.upper())
                    DhLog1.info("%s" %(create_line(59, cmd='return'),))
                    DhLog1.info('%s' %(dlmt_space(59, ('[ INFO ]', f'Promotion Code: {self.promotion_code_on_use[i]}')),))
                    DhLog1.info("%s" %(create_line(59, cmd='return'),))
                    DhLog2.debug("      the minimum quantity of products for this".upper())
                    DhLog2.debug("          Promotion has not been reached!".upper())
                    DhLog1.info("%s" %(create_line(59, break_line=True, to_the_end=True, cmd='return'),))
            pass
            # FINISHING THE PROCESS...                      
            print('\n📜 CREATING NEW LIST OF PRICES FOR CURRENT SALE...')
            create_line(47, cmd='print')
            for l in Central.products_for_sale().keys():
                print(f"'new_properties' for index {l}:" +
                      f"{Central.products_for_sale().__getitem__(l)}")
            print("%s%s" %(create_line(180, char='_', cmd='return'), f'//END OF [{i + 1}] PROMOTIONAL APPLYING PROCESS'))
            pass
            
   
    @keyword(name='Get Elements From The Stored Products')
    def Get_The_Elements_Stored(self):
        for e in Central.products_for_sale().keys():
            DhLog1.log(level=50, msg='%s' %Central.products_for_sale(gt_log=True).__getitem__(str(e)))
    

    @keyword(name='Get How Many Grid Product Are Selling')
    def Grid_Products_On_Sale(self):
        return self.qtd_grid_prod_on_sale


    @keyword(name='Clear Temporary Sale Properties')
    def Clear_Temporary_Attribute_Sale(self):
        Central.products_for_sale([], 'clear')
        Central.group_prod_for_sale([], 'clear')
        Storage.restore_sale_properties([], 'clear')
        Central.list_of_product_price([], 'clear')
        Central.product_on_promotion_subdict([], 'clear')
        Central.final_sale_value(float(0), 'set')
        Central.sale_value_with_diff(float(0), 'set')
        Central.difference_from_value(float(0), 'set')
        Central.current_erp_sale_code(int(), 'set')
        Central.customer_code(int(), 'set')
        Central.current_cpf_cnpj('None', 'set')
        Central.customer_discount(float(0), 'set')
        Central.current_nfce_number(int(), 'set')
        Central.current_sale_status('None')
        self.qtd_grid_prod_on_sale = 0
        DataHandler.Reset_Offer_Controll(self)
        DataHandler.Reset_Promotion_Controll(self)
        return


    @keyword(name='Replace Product Properties')
    def products_for_sale(self, 
            replace: bool = False, 
            _id: bool = False, barcode: bool = False,
            reference: bool = False, description: bool = False, 
            price_T1: bool = False, price_Tn: str = 'Empty', check_customer: bool = True):
        
        """DOCUMENTATION: ``FakerClass``
        
        THIS KEYWORD REPLACES THE ELEMENTS IN THE 'properties' -> ``self.property_entered``. 
        IT'S IMPORTANT  REMEMBER THAT THE PRODUCT'S PROPERTY STORED BY ``Store the Chosen Product Property``
        KEYWORD, WILL BE THE ELEMENT USED TO  REPLACE THE PROPETIES BETWEEN ``sel.products`` DICTIONARY AND
        ``self.property_entered`` CLASSES PROPERTY. FOR THECASE  WHEN  THIS  ELEMENT  STORED ISN'T A  VALID
        ARGUMENT, THIS KEYWORD WILL RETURN ``ValueError()`` TO PERFORM WHAT YOU WANTTHIS KEYWORD TO DO, PAY
        ATTENTION TO THE BOOLAN SETTINGS REFERRED TO AS FUNCTION ARGUMENTS.
        
        **FOR EXAMPLE:**
        
        ``if( replace is True ):`` -> It's ``False`` by defaul 
        -> This keyword will understand that it needs to perfomr a pricing list replacement. But for that
        to happen, it's  necessary  to  inform which product property  will be returned of this functions.
        This controll is done by the bollean variable that ``is not True``

        THEREFOR:

        ``Replace Product Properties :: replace=True :: price_Tn=varejo``
        THIS  KEYWORD  SETTINGS  WILL  RETURN  THE ELEMENT  OF ``self.product`` WHERE THERE IS 'varejo' AS 
        DICTIONARY ACCESS KEY.
        """
        #------------------------------------------------------------------------------------------------------//
        # MAIN  BOOLEAN SETTING: IT  DOES A LOOK-UP IN THE 'self.products' DICTIONARY AND REPLACE THE
        # VALUES OF THE 'properties' OBJECT BY SAME THE ELEMENT FOUND ON 'self.products' ACCORDING TO
        # THE BOOLEAN SETTING SET UP LIKE TRUE VALUE.
        # ... the replacement of the products entered for sale can only be done only if the customer's
        # ... registration is not 'INATIVA' or 'is Null' # -> 'self._registration_valid' . 
        #
        # THE SUBSEQEUNT BLOCK IS THE SYSTEMIC PROCESS THAT REPLACES THE PRODUCT PROPERTIES ::
        # ... transform all keys from the dictionary type string for interables ::
        # ... search by the 'self.property_entered[i]' inside of '_all_keys' list variable::
        # ... after the element is found, compare it to the slef.property_entered[i] ::
        #------------------------------------------------------------------------------------------------------\\
        extract = lambda x, y: x.get(y) if((isinstance(x, dict)) and (isinstance(y, (str, int)))) else None  
        if((replace is True) and (len(list(Central.products_for_sale().copy())) != 0)):
            
            block = ("INATIVA", "NULL")
            if((check_customer is True) and (self.registration_status in block)):
                DhLog1.info(msg="\nThis customer record isn't available to replace the price list!".upper())
                DhLog1.warn(msg='Customer Record Status: %s' %self.registration_status)
                return Exception()

            elif((check_customer is True) and (self.registration_status not in block)): pass
            elif((check_customer is False)): pass

            #|     REPLACEMENT     |     DICTIONARY KEYS FILTER     | CONSOLE LOGGER MESSAGE |   
            new_properties = list(); msg_log = list()
            print(f"debug of all keys from 'self.products dict()': {Central.products().keys()}")
            print('\nProducts launched for current sale:'.upper()); create_line(35, cmd='print')
            
            for e in Central.products_for_sale().keys():
                print("[%s]: %s" %(e, Central.products_for_sale().get(e)))
            
            for i in Central.products_for_sale().keys():
                print("[%s]: %s" %(i, Central.products_for_sale().get(str(i))))
                for ii in Central.products().keys():
                    elem:dict = Central.products().get(str(ii)); key_values = elem.values()
                    if(extract(Central.products_for_sale().get(str(i)), 'prod_code') in key_values):
                        # FOR SHOW THE CODE PRODUCT IN THE CONSOLE LOGGER ::
                        print(f"'elem': {elem}")
                        msg_log.append(elem['code_id']); break
                    else: continue
            
                if(_id != False): new_properties.append(elem['code_id'])
                elif(barcode != False): new_properties.append(elem['bar_code'])
                elif(reference != False): new_properties.append(elem['reference'])
                elif(description != False): new_properties.append(elem['descrpt'])
                elif(price_T1 != False): new_properties.append(elem['price_T1']) 
                elif(price_Tn != 'Empty'):
                    str(price_Tn).lower()
                    this_key = elem[price_Tn]
                    if(extract(Central.products_for_sale().get(i), 'dsct_status') is True):
                        if((this_key <= 0) or (this_key is None)):
                            Central.products_for_sale()[i]['prod_price'] = elem['price_T1']
                            print(f"varejo = {this_key}")
                        elif((this_key > 0) or (this_key is not None)):
                            Central.products_for_sale()[i]['prod_price'] = elem['varejo']
                            print(f"varejo = {this_key}")
                    else:
                        print('THIS PRODUCT IS ON PROMOTION!')
                        print(f"varejo = {this_key}")
                        
                    print("<dict> [%s]: %s" %(i, extract(Central.products_for_sale().get(i), 'prod_price')))
                # Will be continued for promotional price controller according to the table price parameters
                # ...
                else: print("Boolean settings is not valid for this Keyword!."); raise ValueError(); break
                create_line(200, '_', cmd='print')

            # CONSOLE LOGGER ::
            # THIS BLOCK PRINTS THE REPLACEMENT OF PRODUCTS THAT OCCURS AT THE TIME OF THE SUBTOTAL OF SALES
            DhLog1.info(msg='----------------------------')
            for e in Central.products_for_sale().keys():
                elem = Central.products_for_sale().get(e)
                if(elem['dsct_status'] is False):
                    DhLog1.info(msg=f"Product Code: {elem['prod_code']}")
                    DhLog1.log(level=40, msg=f"has replaced for:    {elem['prod_price']}")
                    DhLog1.info(msg='----------------------------')
                else:
                    DhLog1.info(msg=f"Product Code: {elem['prod_code']}")
                    DhLog1.log(level=50, msg=f"has replaced for:    {elem['prod_price']}")
                    DhLog1.info(msg='----------------------------')
            return new_properties
        else: 
            log.info(msg='\n', also_console=True)
            log.error(msg='...')
            DhLog1.error("\nThis method cannot complet the operation process.\nIt's provavely that some argument is not valid")
            return Exception()
        

    # CHQ PAYMENT WAY :: THE CHECK'S NUMBER IS REQUIRED TO CONSULT THE DATABASE.
    @keyword(name='Store The CHQ Serial Number')
    def Chq_Payment_Data(self, number):
        Payment.chq_serial_number(number, 'set')
        return
    

    @keyword(name='Recursion')
    def Sales_Recursion(self, delimiter:int):
        if(delimiter > 0):
            recursion = rr(1, 100)
            clause = True if(recursion <= delimiter) else False
            print('Look at the recursion delimiter has generated to this process: %s' %recursion)
            print('Result:\n%s => %s :: %s' %(recursion, delimiter, clause))
        else: return False
        return clause
    
    
    @keyword(name='Internal Counter')
    def Generic_Internal_Counter(self, counter:int, type_list: bool = False, obj: list = list()):
        rplc = self.internal_counters 
        rplc = ope.add(rplc, counter) if rplc < len(obj) else int(ope.sub(rplc, rplc))
        self.internal_counters = rplc
        return rplc if type_list is False else (ope.sub(rplc, 1))
    


    @keyword(name='Random Interger')
    def Get_Random_Interger(self, imin:int=1, imax:int=2):
        imax = 2 if ope.le(imax, 1) or ope.eq(imin, imax) else imax
        return rr((imin if(ope.gt(imin, int())) else 1), imax)



    @keyword(name='Machine Instructions')
    def Machine_Instructions(self, instruct:dict[str,]) -> None:
        """
        DOCUMENTATION: `DataHandler`
        This `@keyword` supports a PyAutoGUI apporach to the mouse's functions and keyboard's functions.
        To using this keyword as your intermediatary pyAutoGUI solutions, make sure to repass all of the
        nedded arguments for. Each behaviour has writen to this @keyword is based on own function's
        method recognized for the `instruct` `key_values`. Lets see an example about it.

        * `instruct={'type':'keyboard', 'function':'press_key', 'key':'wished_keyboard_key'}`
        
        ⇒ That parameter's combination when it's used to call the PyAutoGUI method, it will give the
        necessary instructions to the method's behaviour and hold for repectly answer from. The clause 
        has noticed to the method to perform an event type `keyoard_manifest` works a wished keyboard
        shortcut key that must be pressed, for example, the 'space' key. 
        
        `type` and `function` are obligatory parameters into `instruct` mapping.
        """
            
        #\.. Security Clause:
        #dict_keys = instruct.keys()
        values:tuple= ('type', 'function', 'key')  
        for kv in range(values.__len__()):
            if(values[kv] not in instruct.keys()):
                log.info(msg='\n', also_console=True); log.error(msg='...')
                DhLog1.info('%s' %(create_line(78, char= '=', break_line= True, cmd='return'),))
                DhLog1.error("Has not been noticed an instruction type to the call method's resources.")
                DhLog1.warn("Check for the function's parameters.")
                DhLog1.info('%s' %(create_line(78, cmd='return'),))
                DhLog2.debug("instruct.key_vales: %s" %(instruct, ))
                DhLog1.info('%s' %(create_line(78, char= '=', break_line= True, to_the_end= True, cmd='return'),))
                raise ValueError()
        
        #\\... GUI Evaluation for Keyboard machine instruction ::
        print("►⌨ Performing %s machine instruction..."
            %('keyboard' if(ope.eq(instruct.get('type'), 'keyboard')) else 'mouse'))
        print("❕ Dict key_values has been noticed as function's arguments")
        for kv in instruct.keys(): 
            print("• [%s]: %s" %(kv, str(instruct.get(kv)).lower()))
    
        if(instruct.get('key') not in gui.KEYBOARD_KEYS):
            log.info(msg='\n', also_console=True); log.error(msg='...')
            DhLog1.error("\nUnknowed Keyboard Key. Check for available keyboard keys on PyAutoGui web page." 
                +"\nGo to the page https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys")
        pass
        
        #\\.. Evaluate keyboard expression ::
        if(ope.eq(str(instruct.get('function')).lower(), 'press_key')):
            gui.press(
                str(instruct.get('key')).lower(),
                presses= 1 if('times' not in instruct.keys()) else int(instruct.get('times')), 
                interval= float(0) if('interval' not in instruct.keys()) else instruct.get('interval'))
            return
        if(ope.eq(str(instruct.get('function')).lower(), 'down')):
            if('while_down' not in instruct.keys()):
                gui.keyDown(str(instruct.get('key')).lower())
                print("PyAutoGUI KeyDown: %s" %(instruct.get('key'),))
            elif('while_down' in instruct.keys()):
                #\\... Perform a hold-on key press while another keys are simultaniously pressed too.
                with gui.hold(str(instruct.get('key')).lower()):
                    gui.press(
                        keys= (
                            str(instruct.get('while_down')).lower() 
                            if(not isinstance(instruct.get('while_down'), (list, tuple)))
                            else list(instruct.get('while_down'))
                            ),
                        presses= (
                            int(1) 
                            if(('times' not in instruct.keys()) 
                                and (not isinstance(instruct.get('while_down'), (list, tuple)))) 
                            else int(instruct.get('times'))
                                ),
                        interval= (
                            float(0) 
                            if('interval' not in instruct.keys()) 
                            else float(instruct.get('interval'))
                                )
                            )
                    print("PyAutoGUI HoldPress: %s & %s" %(instruct.get('key'), instruct.get('while_down')))
                pass
            return
        
        elif(ope.eq(str(instruct.get('function')).lower(), 'up')):
            #\\... It releases the keyboard ekeys has been previously pressed.
            gui.keyUp(str(instruct.get('key')).lower())
            return

        #\\... GUI Evaluation for mause machine instruction:
        elif(ope.eq(str(instruct.get('type')).lower(), 'mouse')):
            pass

        gui.press('space')
        return


    @keyword(name='Show Project Relatory')
    def Print_Relatories(self, relatory_type:int=1):
        if(ope.eq(relatory_type, int(1))):
            show_relatory(); system_version(end_line='double')
        elif(ope.eq(relatory_type, int(2))):
            show_cashier_relatory(); system_version(end_line='double')
        else: print("Invalid argument (%s) to the <fun> Print_Relatories"); raise ValueError()
        return


    @keyword(name='Check For Equivalence')
    def Is_Equal(self, first:bool, second:bool): 
        """Just for `boolean` comarisons"""
        return True if((first is True) and (second is True)) else False


    @keyword(name='Raise Exception')
    def Raise_Exception_At_Runtime(self, mssg:str = '') -> None:
        if(ope.ne(mssg, '')):
            log.info('', also_console=True); log.error('...')
            DhLog1.error("\n%s" %mssg)
        else: pass
        raise Exception()


    @keyword(name='Show Table Message')
    def Show_Table_Message(self, sale_value:int|float, nItems:int) -> None:
        DhLog2.info('%s' %(create_line(59, cmd='return'),))
        DhLog2.warning(dlmt_space(59, (f"• Sale Value: {sale_value}", f"QTY. Items: {nItems}")))
        DhLog2.info('%s' %(create_line(59, break_line=True, to_the_end=True, cmd='return'),))
        return

#\\... END OF LIBRARY ::