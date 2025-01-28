
# SETTINGS 
# -> Project Libraries on usage ::
from Base import Centralizer as Central

# -> External Modules and Resources ::
import os
import yaml
import operator as ope

# Robot Modules on usage ::
from utilities.ColorText import log, logger1
from utilities.TextFormater import *

CfLog = logger1()

class PratesConfig(object):
    _this_instance = None
    prates_user_config = Central.path_main_config
    prates_config_bckp = Central.path_config_bckp
    def __init__(self) -> None:
        pass

    def __new__(cls):
        if cls._this_instance is None:
            cls._this_instance = super(PratesConfig, cls).__new__(cls)
        return  cls._this_instance
    
    # Like 'this_instance' starts Config_Writer class with more than one argument, their startup requires the
    # explicit *arg has writen as function resource. Each method will receive the own class as a fisrt argument
    # from itself as well as will receive too another necessary arguments from 'self' into of *args resource.
    # That feature works for all method in this class <ConfigWriter>

    @classmethod
    def reader(cls, c_user:bool=True) -> dict:
        content = cls.prates_user_config if c_user is True else cls.prates_config_bckp
        with open(content, 'r') as element:
            elements = yaml.safe_load(element)
            return elements
    
    @classmethod
    def writer(cls, contents:object = None):
        with open(cls.prates_config_bckp, 'w') as dump_file:
            yaml.safe_dump(contents, dump_file, line_break=True, 
                           explicit_start=True, explicit_end= True)
        return
    
    @classmethod
    def file_getter(cls, file_content:dict, access_key:str = ''):
        if(access_key in file_content.keys()): return file_content.get(access_key)
        else:
            print("No <dict_key> has been found into <dict>: 'file_content'" +
                  "\nLook at the keys available in the `file_content` object:")
            if((file_content is not None) and ope.ne(file_content, {})):
                for _key in file_content.keys():
                    print("[%s]: %s" %(_key, file_content[_key]))
            else: print("<dict>: 'file_content' is empty or this component is an invalid data type!")

    @classmethod
    def file_printer(cls, c_user:bool=True):
        contents = PratesConfig.reader(c_user)
        for elem in contents.keys():
            if(not isinstance(contents[elem], dict)):
                print('%s: %s' %(elem, contents[elem]))
            else:
                sub_elem = list(contents[elem])
                for ee in range(len(sub_elem)):
                    print('%s: %s' %(sub_elem[ee], 
                          contents[elem][str(sub_elem[ee])]))
        print('\n')
        return
    
    @classmethod
    def file_updater(cls, file:dict, key:str, value:str|int|float): file[key] = value

    @classmethod
    def file_replacer(cls):
        user_config = PratesConfig.reader()
        bckp_config = PratesConfig.reader(c_user=False)
        print("\n📌 Updating the settings file 'config_bckp' according to the 'user_config' system settings...")
        for elem in user_config.keys():
            if(not isinstance(user_config[elem], dict)):
                PratesConfig.file_updater(file= bckp_config, key= elem, value= user_config[elem]) 
            else:
                sub_elem = list(user_config[elem])
                for ee in range(len(sub_elem)):
                    PratesConfig.file_updater(
                        file= bckp_config[elem], 
                        key= str(sub_elem[ee]),
                        value= user_config[elem][str(sub_elem[ee])])
        PratesConfig.writer(contents= bckp_config)
        print("\n📑 Backup File ::\n".upper())
        PratesConfig.file_printer(c_user=False)
        return

    @classmethod
    def file_integrity_inspector(cls) -> None:
        userconfig = PratesConfig.reader()
        bckpconfig = PratesConfig.reader(c_user=False)
        print("\n👁‍🗨 Checking for the settings file integrity...")

        # First Check Up
        for this_key in userconfig.keys():
            if(this_key not in bckpconfig.keys()):
                log.info('\n', also_console=True); log.error('...')
                CfLog.debug('\n==============================================================================')
                CfLog.error(msg="¡[<Config.yaml> FileError]!")
                CfLog.warning(msg="\nThere is a problem with the Config.yaml file. At least one of their" +
                                 "\nparameters doesn't exists or it has been uncorrecting writen. Please check" +
                                 "\nfor the file components into of one and find where is the fail occurrence!")
                CfLog.debug('------------------------------------------------------------------------------')
                CfLog.critical(msg="key_error: [%s]" %this_key)
                CfLog.debug('==============================================================================')
                CfLog.error('Check for: %s' %cls.prates_user_config)
                PratesConfig.file_printer(c_user=True)
                raise KeyError(); break
        
        """
        # Second Check Up    
        for other_key in bckpconfig.keys():
            if(other_key not in userconfig.keys()):
                log.info('\n', also_console=True); log.error('...')
                CfLog.debug('\n==============================================================================')
                CfLog.error(msg="¡[<Config.yaml> FileError]!")
                CfLog.warning(msg="\nThe <dict> key_value ['%s'] has been not found in at least one\n" %other_key +
                                 "of the settings file. Please check for system parameters on directory:\n" +
                                 "%s" %cls.prates_user_config)
                CfLog.debug('------------------------------------------------------------------------------')
                CfLog.critical(msg="key_error: [%s]" %other_key)
                CfLog.debug('==============================================================================')
                PratesConfig.file_printer(c_user=False)
                raise KeyError(); break
        return
        """
    
    # DATA CHECK UP FOR SETTINGS FILE:
    @classmethod
    def file_status_checkup(cls):
        userconfig = PratesConfig.reader()
        _status:bool = False
        
        # Alert for inactived parameter: 'auto_update_of_data':
        if(ope.eq(userconfig['use_new_connect'], False) 
           and (str.lower(userconfig['database']) == 'scanntech')
            and ((userconfig['auto_update_of_data'] is False) or userconfig['auto_update_of_data'] is None)):
            log.info('\n', also_console=True); log.warn('...')
            CfLog.critical('\n==============================================================================')
            CfLog.warning(msg="¡[PAY ATTENTION]!")
            CfLog.warning(msg="\nThe parameter 'auto_update_of_data' on <Config.yaml> is inactived!" +
                                   "\nThe data library will not be updated to new possible data from database.")
            CfLog.critical('==============================================================================')
        

        # Checking for database attributes...                              
        # -> ADVANCED TRUE TABLE WITH TERNARY EXPRESSION STATEMENTS...
        if(ope.eq(userconfig['use_new_connect'], True)):
            _status= (PratesConfig.raise_file_exception("[Database]¹: THE PARAMENTERS ISAN'T OK! CHECK FOR SETTINGS..")
                if (
            ((userconfig['server_user'] is None) or (userconfig['server_user'] in ('', ' ')) is True)
            or ((userconfig['server_passwrd'] is None) or (userconfig['server_passwrd'] in ('', ' ')) is True)
            or ((userconfig['host_server'] is None) or (userconfig['host_server'] in ('', ' ')) is True)
            or ((userconfig['port'] is None) or (userconfig['port'] in ('', ' ', 0000, 1111)) is True)
            or ((userconfig['database'] is None) or (userconfig['database'] in ('', ' ')) is True)
            or ((userconfig['user_code_id'] is None) or (userconfig['user_code_id'] in ('', ' ')) is True)
            or ((userconfig['user_name'] is None) or (userconfig['user_name'] in ('', ' ')) is True)
            or ((userconfig['computer_name'] is None) or (userconfig['computer_name'] in ('', ' ')) 
                or (isinstance(userconfig['computer_name'], int)) is True)
            or ((userconfig['cashier_code'] is None) or (userconfig['cashier_code'] in ('', ' ', int(0))) is True)
            or ((userconfig['cashier_name'] is None) or (userconfig['cashier_name'] in ('', ' ')) 
                or (isinstance(userconfig['cashier_name'], int)) is True)
            and _status is False
                ) else PratesConfig.set_up_file_status("► <Config.yaml>: [Database]¹ is Ok!"))

        #\\... single clause out of truth table evaluating ::
        if(ope.eq(userconfig['data_recovery'], False)):
           
            if(((ope.eq(userconfig['get_data_from_db'], True)) and (ope.eq(userconfig['set_new_data'], True)) is True) 
               or((ope.eq(userconfig['get_data_from_db'], False)) and (ope.eq(userconfig['set_new_data'], False)) is True)):
                _status = PratesConfig.raise_file_exception('[Data Libraries Behaviour¹]: THE PARAMETERS COMBINATION IS IVALID!')

            if(ope.eq(userconfig['get_data_from_db'], True)):
                _status= (PratesConfig.raise_file_exception('[Data Libraries Behaviour²]: THE PARAMETERS COMBINATION IS IVALID!')
                    if (
                ((userconfig['limit_for_cust'] is None) or (ope.le(userconfig['limit_for_cust'], int(0))) is True)
                or ((userconfig['limit_for_prod'] is None) or (ope.le(userconfig['limit_for_prod'], int(0))) is True)
                or ((userconfig['randomize_choice'] is None) or (not isinstance(userconfig['randomize_choice'], bool)) is True)
                or ((ope.eq(userconfig['set_new_data'], True)) or (ope.eq(userconfig['auto_update_of_data'], True) 
                                                                if('auto_update_of_data' in userconfig.keys() is True) else None) is True)
                or ((ope.eq(userconfig['customer_sequence'], True)) or (ope.eq(userconfig['product_sequence'], True)) is True)
                and _status is False
                    ) else PratesConfig.set_up_file_status("► <Config.yaml>: [Data Libraries Behaviour³] is Ok!"))
                
            if(ope.eq(userconfig['set_new_data'], True)):
                _status= (PratesConfig.raise_file_exception('[Data Libraries Behaviour²]: THE PARAMETERS COMBINATION IS IVALID!')
                    if(
                ((ope.eq(userconfig['sequence_of_products'], []))) or (ope.eq(userconfig['sequence_of_customers'], []) is True)
                or ((not isinstance(userconfig['sequence_of_products'], list)) or (not isinstance(userconfig['sequence_of_customers'], list)))
                or ((ope.ne(userconfig['sequence_of_products'], []) is True) and (None, '' in userconfig.get('sequence_of_products') is True))
                or ((ope.ne(userconfig['sequence_of_customers'], []) is True) and (None, '' in userconfig.get('sequence_of_customers') is True))
                or (ope.eq(userconfig['promotional_checking'], True) is True)
                    ) else PratesConfig.set_up_file_status("► <Config.yaml>: [Data Libraries Behaviour²] is Ok!"))
        else:
            if((ope.eq(userconfig['get_data_from_db'], True) or (ope.eq(userconfig['set_new_data'], True)))):
                _status = PratesConfig.raise_file_exception('[Data Libraries Behaviour¹]: THE PARAMETERS COMBINATION IS IVALID!')

        #-----------------------------------------------------------------------------------------------------------------------------------//
        
        # Checking for customers attributes...
        if(ope.eq(userconfig['use_client_selection'], True)):
            _status= (PratesConfig.raise_file_exception('[Customers Tasks]¹: THE PARAMETERS COMBINATIONS IS INVALID!')
                if (
            ((userconfig['use_client_selection'] is None) or (not isinstance(userconfig['use_client_selection'], bool)) is True)
            or ((ope.eq(userconfig['use_default_client'], True)) 
                and ((userconfig['default_client_code'] in (None, '', ' ', int(0))) or (ope.le(userconfig['default_client_code'], int(0)))
                                                                    or (ope.eq(userconfig['customer_sequence'], True))) is True)
            or ((ope.eq(userconfig['use_client_search_win'], True))
                and ((userconfig['filter_by_social_name'] is None) or (not isinstance(userconfig['filter_by_social_name'], bool)) 
                    or ((userconfig['filter_by_client_code'] is None) or (not isinstance(userconfig['filter_by_client_code'], bool)))
                    or ((userconfig['filter_by_cnpj_cpf'] is None) or (not isinstance(userconfig['filter_by_cnpj_cpf'], bool)))) is True)
            or ((ope.eq(userconfig['customer_sequence'], True)) 
                and ((userconfig['custom_client_sequence'] is None) or (None in userconfig['custom_client_sequence'])) 
                    or (ope.eq(userconfig['randomize_cpf_code'], True)) is True) 
            and _status is False
                ) else PratesConfig.set_up_file_status("► <Config.yaml>: [Customers Tasks]¹ is Ok!"))
        #-----------------------------------------------------------------------------------------------------------------------------------//
        
        # Checking for products porperties...
        if(ope.eq(userconfig['randomize_qnt_product'], True)): 
            _status= (PratesConfig.raise_file_exception('[Products Tasks]¹: THE PARAMETERS COMBINATION IS INVALID!')
                if (
            ((userconfig['qnt_max_prod_for_sale'] is None) or ((not isinstance(userconfig['qnt_max_prod_for_sale'], int)) 
                                                                or (ope.le(userconfig['qnt_max_prod_for_sale'], int(0)))) is True)
            or ((ope.eq(userconfig['product_sequence'], True)) is True)
                ) else PratesConfig.set_up_file_status("► <Config.yaml>: [Products Tasks]¹ is Ok!"))
        
        if(ope.eq(userconfig['choose_prod_in_the_layout'], False)):
            _status= (PratesConfig.raise_file_exception('[Products Tasks]²: THE PARAMETERS COMBINATION IS INVALID!')
                if (
            ((userconfig['filter_by_code'] is None) or (not isinstance(userconfig['filter_by_code'], bool)) is True)
            or ((userconfig['filter_by_barcode'] is None) or (not isinstance(userconfig['filter_by_barcode'], bool)) is True)
            or ((userconfig['filter_by_refe'] is None) or (not isinstance(userconfig['filter_by_refe'], bool)) is True)
            or ((userconfig['filter_by_desc'] is None) or (not isinstance(userconfig['filter_by_desc'], bool)) is True)
            or (((userconfig['filter_by_code'] is True) 
                and (userconfig['filter_by_barcode'] is True)
                    and (userconfig['filter_by_refe'] is True) 
                        and (userconfig['filter_by_desc'] is True)) is True)
            and _status is False
                ) else PratesConfig.set_up_file_status("► <Config.yaml>: [Products Tasks]² is Ok!"))
        
        if(ope.eq(userconfig['product_sequence'], True)):
            _status= (PratesConfig.raise_file_exception('[Products Tasks]³: THE PARAMETERS COMBINATION IS INVALID!')
                if (
            ((userconfig['custom_prod_sequence'] is None) or (None in (userconfig['custom_prod_sequence'])) is True)
            and _status is False
                ) else PratesConfig.set_up_file_status("► <Config.yaml>: [Products Tasks]³ is Ok!"))
        #-----------------------------------------------------------------------------------------------------------------------------------//
        
        # Checking for the envent type: 'sangria'...
        if(ope.eq(userconfig['sangria'], True)):
            _status= (PratesConfig.raise_file_exception('[Cashier Behaviour]¹: THE PARAMETERS COMBINATION IS INVALID!')
                if (
            ((userconfig['cash_event'] is None) 
                or ((userconfig['cash_event'] is False) and (userconfig['check_event'] in (None, False))) is True)
            or ((userconfig['check_event'] is None) 
                or ((userconfig['check_event'] is False) and (userconfig['cash_event'] in (None, False))) is True)
            or ((userconfig['minimun_necessary'] is None) 
                or (ope.le(userconfig['minimun_necessary'], int(0))) 
                    or (not isinstance(userconfig['minimun_necessary'], (int, float))) is True)
            or ((userconfig['value_extracted'] is None) 
                or (ope.le(userconfig['value_extracted'], int(0)))
                    or (not isinstance(userconfig['value_extracted'], (int, float))) is True)
            or (ope.gt(userconfig['value_extracted'], userconfig['minimun_necessary']) is True)
            and _status is False
                ) else PratesConfig.set_up_file_status("► <Config.yaml>: [Cashier Behaviour]¹ is Ok!"))
        #-----------------------------------------------------------------------------------------------------------------------------------//
        
        # CONLUSION ::
        print('\n%s Settings File Operational Status: %s' %(('❕', '✅ Ok!') if _status is True else ('❗', '❌ NOT OK!')))
        PratesConfig.file_replacer() if _status is True else None
        #Central.prates_current_settings(userconfig, 'set')
        CfLog.info("\n%s► [Config.yaml] ◄" %expand(size=6))
        CfLog.debug("%s" %(create_line(32, char='=', cmd='return')))

    # CONSOLE OUTPUT:
    @staticmethod
    def raise_file_exception(mssg:str, level:str= 'ERROR') -> None:
        if(level in ('ERROR', 'Error', 'error')):
            log.info(msg='\n', also_console=True); log.error(msg='...')
            CfLog.debug('\n==============================================================================')
            CfLog.error('%s' %mssg)
            CfLog.warning('-> Check for the settings of this automated test sequence...')
            CfLog.debug('==============================================================================')
        elif(level in ('WARN', 'Warn', 'warn')):
            log.info(msg='\n', also_console=True); log.warn(msg='...')
            CfLog.debug('\n==============================================================================')
            CfLog.warning('%s' %mssg)
            CfLog.warning('-> Check for the settings of this automated test sequence...')
            CfLog.debug('==============================================================================')
        writer = PratesConfig(); writer.file_printer()
        raise ValueError()
    
    @staticmethod
    def set_up_file_status(mssg:str) -> None:
        print('\n%s' %mssg)
        return True