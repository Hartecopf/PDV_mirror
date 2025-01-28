
# -> Built-in Modules, External Resources and Robot Modules ::
import datetime as dt
import operator as ope
import mysql.connector as cnx
from mysql.connector import errors
from FireBirdConnector import FbConnector

# PROJECT FOLDER DEPENDENCES :: 
from SystemConfig import PDVConfig
from Base import ExternalFile, Storage
from Base import Centralizer as Central
from input.ConfigLoader import PratesConfig

from db_resource.FiscalCheckup import *
from db_resource.DataComparison import *
from db_resource.DataHandling import Handling
from db_resource.ProductsUpdate import ProductUpdate
from db_resource.PaymentsUpdate import PaymentWaysPDV
from db_resource.CustomersUpdate import CustomerUpdate
from db_resource.CashiersUpdate import CashierAutoUpdate

from utilities.TextFormater import *
from robot.api.deco import library, keyword
from db_resource.EventQueries import MyQuery, Commom_Queries
from utilities.ColorText import log, logger1, logger4, logger5
from time import localtime, strftime as st, localtime as lt
from datetime import datetime

MyLog1 = logger4()
MyLog2 = logger5()
MyLog3 = logger1()


@library(scope='GLOBAL', version='14.0', auto_keywords=False, doc_format='reST')
class MySQLConnector(object):
    
    # <class> Properties ::
    _name:str = 'MyCnn'
    _instance = None
    _cnn_config: dict = {
        'user': PratesConfig.reader().get('server_user'), 
        'password': PratesConfig.reader().get('server_passwrd'),
        'host': PratesConfig.reader().get('host_server'),
        'port': PratesConfig.reader().get('port'),
        'database': PratesConfig.reader().get('database')}
    db_name = str(PratesConfig.reader().get('database'))
    
    #\\... Initinal connection parameters ::    
    try:
        #\\... set connection according to the PratesConfig arguments ::
        MySQLconnection:cnx.MySQLConnection = cnx.connect(**_cnn_config)
        Central.cur_mysqlcnn.update(_cnn_config)
    except:
           #\\... wheter isn't possible then set a default MySQL localstorage ::
        MySQLconnection:cnx.MySQLConnection = cnx.connect(**{'user':'root', 'password':'root'})
        MyLog2.info("Dismissed intial settings to MySQLConnection :: %s" %(_cnn_config,))
    else: pass

    #\\... Static Data ::
    today: dt = dt.date.today()
    
    #\\... Variable Data ::
    query_results: object = None
    cur_rowcount: int = int()
    firebird_check: bool = False
    fb_sales_code: int = int()
    
    def __init__(cls) -> None:
        pass
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MySQLConnector, cls).__new__(cls)
        return  cls._instance
    
    @classmethod
    def Get_Connection(cls) -> cnx.MySQLConnection:
        if(cls.MySQLconnection.is_connected() is False):
            try:
                cls.MySQLconnection = MySQLConnector.Reconnect()
                print('CONNECTION HAS BEEN SUCCESSFULLY RESTORED!')
            except:
                log.info(msg='', also_console=True); log.error(msg='...')
                MyLog2.error(msg='\n¡Impossible to establish connection to the [%s]!' %cls.db_name)
                MyLog2.warn(msg='It likely the database is off-line or unavailable at this moment!')
        else: pass
        print("Connection: %s"
        %('✅ Connected' if cls.MySQLconnection.is_connected() is True else '❌ Disconnected'))
        return cls.MySQLconnection
    
    @classmethod
    def Get_Database_Name(cls) -> str:
        return str(cls.db_name)

    @classmethod
    def Close_Connection(cls) -> None:
        if(cls.MySQLconnection.is_connected() is False):
            cls.MySQLconnection.close()
        return
    
    @classmethod
    def Reconnect(cls):
        cls.MySQLconnection = cnx.connect(**cls._cnn_config)
    
    @classmethod
    def Disconect(cls) -> None:
        cls.MySQLconnection.close()
        return
    

    @keyword(name='Create Connection To Database')
    def Create_Connection(cls,
            __local:bool=False,
            user_cnx:str='root', 
            psswrd:str='root', 
            host_cnx:str='10.1.1.127', 
            host_port:int=3306, 
            db_name:str=''):
        
        #\\... close the current connection has established previously ::
        MySQLConnector.Close_Connection()
        #\\... and then create a new connection like at this ::
        try:
            #\\... and then create it again ::
            if(__local is False):
                cls.MySQLconnection = cnx.connect(
                    user=user_cnx, password=psswrd, 
                    host=host_cnx, port=host_port,
                    database=db_name)
                
                cls._cnn_config.update({
                'user':user_cnx, 'password':psswrd,
                'host':host_cnx, 'port':host_port,
                'database':db_name})
            
            else: cls.MySQLconnection = cnx.connect(**cls._cnn_config)
            
        except:
            print("There are a problem with conncection to %s MySQL database"
            %(db_name if __local is False else cls._cnn_config.get('database')))
            log.info('', also_console=True); log.error('...')
            MyLog1.error("Unable to establish a connection to database %s" %db_name)
            raise errors.OperationalError()
        else: 
            print("✅ Connection to the [%s] has been successfully stablisehd!" %(
            db_name if __local is False else cls._cnn_config.get('database')))
            cls.db_name = db_name if __local is False else cls._cnn_config.get('database')
        return
    
    @keyword('Show Connection')
    def Show_Connection(cls):
        db_name = MySQLConnector.Get_Database_Name()
        version = cnx.__version__
        sv_version = '.'.join(map(str, cls.MySQLconnection.get_server_version()))
        MyLog3.debug('%s' %(create_line(78, char='=', double_break=True, cmd='return'),))
        MyLog1.info('%s'
            %(dlmt_space(78,  
                ('MySQL Driver Version: %s%sServer Version: %s'
                 %(version, expand(size=3), sv_version), '[%s]'%(db_name))),))
        MyLog3.debug('%s' %(create_line(78, char='=', cmd='return'),))
        pass    

        
    @keyword(name='Database Log')
    def colored_log(cls, 
            mssg:str= 'message', 
            level:str= 'DEBUG, INFO, WARN, ERROR, NULL'):

        options = (
            'DEBUG', 'INFO', 'WARN', 'ERROR', 
            'NULL', 'DEB2', 'INF2', 'WAR2', 'ERR2', 'CRT2')
        
        level = level.upper()
        if(level in options):
            if(ope.eq(level, 'DEBUG')): MyLog1.debug(msg = mssg); return
            elif(ope.eq(level, 'INFO')): MyLog1.info(msg = mssg); return
            elif(ope.eq(level, 'WARN')): MyLog1.warning(msg = mssg); return
            elif(ope.eq(level, 'ERROR')): MyLog1.error(msg = mssg); return
            elif(ope.eq(level, 'DEB2')): MyLog2.debug(msg = mssg); return
            elif(ope.eq(level, 'INF2')): MyLog2.info(msg = mssg); return
            elif(ope.eq(level, 'WAR2')): MyLog2.warning(msg = mssg); return
            elif(ope.eq(level, 'ERR2')): MyLog2.error(msg = mssg); return
            elif(ope.eq(level, 'CRT2')): MyLog2.critical(msg = mssg); return
            else: MyLog1.log(level=50, msg = mssg); return
        else: 
            with ValueError() as ve:
                print('%s: Invalid argument!' %ve); raise ValueError()
            

    @keyword(name='Show MySQL Connection Status')
    def Connection_Status(cls):
        if(cls.MySQLconnection.is_connected() is True):
            MyLog3.debug(msg= str(create_line(59, char='=', break_line=True, cmd='return')))
            MyLog1.debug(msg=f"\r Database connection has successfully established!")
            MyLog3.debug(msg= str(create_line(59, char='=', cmd='return')))
            MyLog1.info(msg="\r%s" %(dlmt_space(59, ('Connection Host:', str(cls.MySQLconnection.server_host)))))
            MyLog1.warning(msg="\r%s" %(dlmt_space(59, ('Database:', str(cls.MySQLconnection.database)))))
            MyLog3.debug(msg= str(create_line(59, char='=', cmd='return')))
        else:
            log.info('\n', also_console=True); log.error('...')
            MyLog1.error(msg='\n[ConnectionError]: Database connection has failed!\n')
            raise errors.DatabaseError()
        
        # SET CONNECTION FOR OTHER CLASSES WRITEN AS MySQLConnector.py LIBRARY EXTENSION ::
        # EVERY OTHER LIBRARIES USES THIS cls.MySQLconnection AS THEIR OBJECT TYPE MySQLConnection.
        PaymentWaysPDV.Set_MySQL_Connection(cls.MySQLconnection)
        CustomerUpdate.Set_MySQL_Connection(cls.MySQLconnection)
        ProductUpdate.Set_MySQL_Connection(cls.MySQLconnection)
        CashierAutoUpdate.Set_MySQL_Connection(cls.MySQLconnection)
        return


    @keyword(name='Show FireBird Connection Status')
    def Fb_Conenction_Status(cls):
        return FbConnector.Show_Connection_Status()


    @keyword(name='Show Internal Data')
    def Load_Internal_Data(cls):
        """
        DOCUMENATION: `MyConenctor`
        Show the project data has been loaded for the Library Startup in `base.robot` script
        """

        Storage.db_cashier_code(Cashier.cashier_code(), 'set')
        print("""
        \r-> STRUCTURE INTERNAL DATA:\nCashier Code: %s\nCashiser Name: %s 
        \r\nMachine ID: %s\nSales Person Code: %s\nSales Person Name: %s""" %(
            Cashier.cashier_code(), 
            Cashier.cashier_name(), 
            Central.machine_name,
            Central.sales_person_code, 
            Central.sales_person_name))
        Central.company_internal_code(PratesConfig.reader().get('company_code'), 'set')
        MySQLConnector.Load_Cashier_Open_Code(cls)
        pass


    #---------------------------------------------------------------------------------------------------------------//
    # THE CASHIER OPENNING CODE MUST BE LOADED AS CLASSE'S PROPERTY. ITS CONTENT IS USED THROUTH THE LIBRARY IN
    # SEVERAL OTHERS MYSQL QUERYES MADE FOR EACH SALE EVENT PERFORMED DURINT THE ATUMATED TEST CASE AT RUNTIME.
    #--------------------------------------------------------------------------------------------------------------\\
    @keyword(name='Check For Cashier Open Code')
    def Load_Cashier_Open_Code(cls):
        """It looking for the cashier openning code and load it"""
        if(cls.MySQLconnection.is_connected() is False): MySQLConnector.Reconnect()
        else: print("\nConnection Established! [%s]" %cls.MySQLconnection.database)
        
        query = MyQuery.cashier_open_code(
            (Cashier.cashier_code(), 
            Cashier.cashier_name().lower(), 
            Central.machine_name.lower()))
        
        print("Looking for the Cashier Open Code... 🔍\n %s" %query)
        cursor = cls.MySQLconnection.cursor(buffered=True)
        cursor.execute(query); result:tuple = cursor.fetchone(); cursor.close()
        
        if(ope.ne(result, None)):
            Cashier.cashier_open_code(int(result[0]), 'set')
            print("🔑 Cashier Open Code: %s" %(Cashier.cashier_open_code(),))
            print("❕ This code represent the current cashier code used during the cashier operations")
            ExternalFile.set_file_path(Central.path_cashier_output)
            yaml_file = ExternalFile.read_file()
            ExternalFile.update_file(yaml_file, 'cashier_serial_code', int(result[0]))
            ExternalFile.write_on_file(yaml_file)
        else: 
            print("%s MyQuery.cashier_open_code(*args) has returned: %s"
            %(('❕' if ope.ne(result, None) else '❗'), result))
        return


    @keyword(name='Load System Versions')
    def Load_System_Version_On_Usage(cls):
        """It looking for the system version and load it"""

        if(cls.MySQLconnection.is_connected() is False):
            MySQLConnector.Reconnect()
        else: 
            print("\nConnection Established! [%s]" %cls.MySQLconnection.database +
                  "\n🔍 Looking for Systems Version recorded on database... ")
        query = MyQuery.pdv_version(
            (PratesConfig.reader().get('computer_name'), 
             PratesConfig.reader().get('company_code')))
        
        print("[PDV_VERSION]:\n%s" %query)
        cursorA = cls.MySQLconnection.cursor(buffered=True)
        cursorA.execute(query); result:tuple = cursorA.fetchone(); cursorA.close()
        Central.pdv_version = str(result[0]) if result is not None else 'Empty'

        query = MyQuery.erp_version()
        print("[ERP_VERSION]:\n%s" %query)
        cursorB = cls.MySQLconnection.cursor(buffered=True)
        cursorB.execute(query); result:tuple = cursorB.fetchone()
        if((result is not None) and ('0.0.0.0' not in result)):
            Central.erp_version = str(result[0])
        else: Central.erp_version = 'Empty'
        cursorB.close()
        return


    @keyword(name='Load Custom Settings')
    def Load_Data_Settings(cls,
            e_use_dav:bool = bool(PratesConfig.reader().get('print_dav')), 
            check_nfce_status:bool = bool(PratesConfig.reader().get('cstat_check_out')), 
            standard_product:int = PratesConfig.reader().get('standard_product'), 
            standard_customer:int = PratesConfig.reader().get('pattern_client_code'),
            default_customer_code:int = PratesConfig.reader().get('default_client_code'),
            use_data_recovery:bool = bool(PratesConfig.reader().get('data_recovery'))):

        Central.use_nfce_document((False if(e_use_dav is True) else True), 'set')
        Central.cstat_check_out((True if((check_nfce_status is True) and (e_use_dav is False)) else False), 'set')
        Central.standard_product_code(standard_product, 'set')
        Central.standard_customer_code(standard_customer, 'set')
        Central.default_customer_code(default_customer_code, 'set')
        Central.recovery_db_contents(use_data_recovery, 'set')

        # BOOLEAN DATA HAS GIVEN FOR PDV SETTIGNS LOOKING LIBRARY ::
        sys_sttg:dict = PDVConfig.Read_System_Config(show=False); pdv_sttgs:dict = sys_sttg.get('function_keys')
        Central.block_discount_for_promotion((bool(pdv_sttgs['OPCOES_BLOQUEARDESCONTOPROMOCAO'])), 'set')
        
        # HTML Output ...
        print("""
        \r🔃 -> DATA DOWNLOAD FROM DATABSE:\r  • Limit of Customers: %s\r  • Limit of Products: %s 
        \r🔧 -> SYSTEM BEHAVIOUR FOR QUERIES:\r  • SELECT TYPE: %s\r  • NFC-e Conference: %s
        \r  • Default Product Code: %s\r  • Default Customer Code: %s\r  • Data Recovery: %s"""
        %(PratesConfig.reader().get('limit_for_cust'), PratesConfig.reader().get('limit_for_prod'),
        ('Random' if(bool(PratesConfig.reader().get('randomize_choice')) is True) else 'Normal'), 
        Central.cstat_check_out(), 
        Central.standard_product_code(), 
        Central.standard_customer_code(), 
        Central.recovery_db_contents()))
        return

    
    @classmethod
    def MYSQL_Queries(cls, 
        e_sale1:bool= False,            e_sale2:bool= False,              e_chq_audict:bool = False, 
        e_chq_mov:bool= False,          e_cnts_aRec:bool= False,          e_card_record:bool= False, 
        e_card_mov:bool= False,         e_pix_mov:bool= False,            e_cnts_cMov:bool= False, 
        e_cnts_aRec_pix:bool= False,    e_cancel_sale:bool = False,       e_cashier_mov:bool = False, 
        e_fiscal_document:bool= False,  e_uncompleted_sale:bool= False,   e_cancel_tax_docmt:bool = False,
        e_cashier_code:bool= False,     e_sangria_event:bool= False,      e_uncompleted_sangria:bool= False,
        e_counter_sangria:bool = False):
    
        # THIS IS SIMILAR TO THE __init__() FUNCTION IN THE CLASSES ::
        return Commom_Queries(
            cls._name, 
            sale1= e_sale1,                    sale2= e_sale2,                         chq_audit= e_chq_audict,
            chq_mov= e_chq_mov,                cnts_aRec= e_cnts_aRec,                 card_record= e_card_record,
            card_mov= e_card_mov,              pix_mov= e_pix_mov,                     cnts_cMmov= e_cnts_cMov,
            cnts_aRec_pix= e_cnts_aRec_pix,    cashier_mov= e_cashier_mov,             fiscal_document= e_fiscal_document,
            cancel_sale= e_cancel_sale,        uncompleted_sale= e_uncompleted_sale,   cancel_tax_docmt= e_cancel_tax_docmt,
            cashier_code= e_cashier_code,      sangria_event= e_sangria_event,         uncompleted_sangria= e_uncompleted_sangria,
            cnt_sangria = e_counter_sangria)
        

    #==================================================================================================================//
    #                                             AUTO UPDATE SECTION
    #------------------------------------------------------------------------------------------------------------------
	# AUTO UPDATE OF DATA TO THE INTERNAL STORAGE OF THE "PRATES". THIS INFORMATION IS USED DURING TEST CASES' STARTUP. 
    # AFTER  WE HAVE GOT THE TYPES OF THE DATA NEEDED TO PERFORM  THE PERFORMATIVE TEST SEQUENCE, WE CAN CARRY OUT
    # INTERNAL QUERIES DEDICATED TO THE PRATES STRUCTURE. THIS BEHAVIOR SAVES THE DATA FLOW OF THE DATABASE IN USE!
    #==================================================================================================================\\
    # AUTO UPDATE FOR PAYMENT WAYS :: 
    @classmethod
    def Download_PaymentWays(cls):
        print("\n💰 Loading payment methods...")
        if(Central.recovery_db_contents() is False):
            PaymentWaysPDV.Create_Payments_Mapping()
        else:
            PaymentWaysPDV.Recovery_Payment_Sequence()
            PaymentWaysPDV.Recovery_Payment_Sequence(is_card=True)
            PaymentWaysPDV.Recovery_Payment_Sequence(is_taxes=True)
        return
    
	# AUTO UPDATE FOR CUSTOMER'S DICTIONARY AND THEIR PROPERTIES ::
    @classmethod
    def Dowload_Customer_Records(cls):
        print("\n📜 Loading customers dataschema...")
        if(Central.recovery_db_contents() is False):
            CustomerUpdate.Create_Customer_Mapping()
        else: 
            CustomerUpdate.Recovery_Data_Sequence()
        return
    
    # AUTO UPDATE FOR PRODUCT'S DICTIONARY AND THEIR PROPERTIES ::
    @classmethod
    def Download_Product_Records(cls):
        print("\n🛒 Loading products dataschema...")
        if(Central.recovery_db_contents() is False):
            ProductUpdate.Create_Products_Mapping()
        else:
            ProductUpdate.Recovery_Data_Sequence()
            ProductUpdate.Recovery_Data_Sequence(is_promotion=True)
            #ProductUpdate.Apply_Promotions_When_Existing()
        return

    # AUTO UPDATE TO THE CASHIER'S CONTENT ::
    @classmethod
    def Cashier_Auto_Adjustment(cls, log:bool= False)-> None:
        print("\n💱 Loading cashier's content...")
        info:dict= {
            'ca_code':Cashier.cashier_code(),
            'company':Central.company_internal_code(),
            'ca_name':Cashier.cashier_name(), 
            'open_code':Cashier.cashier_open_code(), 
            'computer_name':Central.machine_name, 
            'user_code':Central.sales_person_code}
        CashierAutoUpdate.Cashier_Auto_Adjustment(kwords= info, cashier_log= log)
        return
    

    #==================================================================================================================//
    #                                            ENVIROMENT UPDATE SECTION
    #------------------------------------------------------------------------------------------------------------------
	# THE ENVIROMENT FOR UPDATE DATABASE TABLES IS HERE. THIS SECTTION USES INSERT AND UPDATE CLAUSES TO PERFORM A
    # DATABASE HANDLING ACCORDING TO THE NEEDED SCHEMATIC ENVIROMENT ON MYSQL DATABASE CONNECTION. THERE ARE SEVERAL
    # REASON AND CIRCUNSTANCES WHEN HANDLER DATABASE IS NECESSARY. THIS BLOCK HAS BEEN WRITEN TO DO THAT.
    #==================================================================================================================\\
    @keyword(name='Set Query Inserts')
    def Set_Query_Inserts(cls, /, insert_type:str) -> None:

        #\\... SECURITY CLAUSE FOR 'insert_type' ARGUMENT VALUE ::
        insert_type = insert_type.lower()
        wished_inserts:tuple = (
            'accept_sangria', 'create_custm_user', 'create_custm_cashier', 'create_custm_nfce')
        
        #\\... SECURITY CLAUSE FOR 'table' ARGUMENT VALUE ::
        if(insert_type not in wished_inserts):
            log.info('', also_console=True); log.error('...')
            MyLog3.debug('%s' %(create_line(78, break_line=True, cmd='return'),))
            MyLog3.error('%s' %(dlmt_space(78, ("❌ [ArgumentError]:", '|')),))
            MyLog3.error("THE 'insert_type' FUNCTION ARGUMENT MUST BE AN ACEPTABLE VALUE!")
            MyLog1.debug('%s' %(create_line(78, cmd='return'),))
            raise ValueError()
        else: pass
        MySQLConnector.Create_Connection(MySQLConnector, True)

        # Query execution type: Cashier Event type "Sangria" for cashier movements
        if(ope.eq(insert_type, 'accept_sangria')): 
            format_keys:dict = {
                'company_code':Central.company_internal_code(),
                'cashier_code':Cashier.cashier_code(),
                'client_code':1,
                'pdv_cashier_name':Cashier.cashier_name(),
                'user_name':Central.sales_person_name,
                'pdv_opng_cashier_code':Cashier.cashier_open_code(),
                'value_extracted':PratesConfig.reader().get('value_extracted'),
                'computer_name':Central.machine_name,
                'myc_cashier_code':PratesConfig.reader().get('myc_cashier_code'),
                'myc_cashier_name':PratesConfig.reader().get('myc_cashier_name')}
            return Handling.Accept_Sangria_Cashier_Event(cls._name, cls.MySQLconnection, format_keys)

        # Query execution type: Create Custom User for login on PDV System
        elif(ope.eq(insert_type, 'create_custm_user')): 
            format_keys:dict = {
                'custom_inner_code':00000,
                'custom_cpf_code':'69394801960',
                'custom_name':Central.sales_person_name,
                'custom_password':'Yp['}
            return Handling.Create_Custom_User(cls._name, cls.MySQLconnection, format_keys)

        # Query execution type: Create Custom Cashier Code for usage on PDV System
        elif(ope.eq(insert_type, 'create_custm_cashier')): 
            return Handling.Create_Custom_Cashier(cls._name, cls.MySQLconnection)

        # Query execution type: Create Custom Fiscal Document Serieal Number
        elif(ope.eq(insert_type, 'create_custm_nfce')): 
            return Handling.Create_Custom_NFCe(cls._name, cls.MySQLconnection)
        

    #==================================================================================================================//
    #                                           LIBRARY'S KEYWORDS FOR ROBOT
    #------------------------------------------------------------------------------------------------------------------
    # THE FOLLOWING METHOD HAS BEEN ASSIGNED AS INTERNAL MySQLConnector's CLASS. IT'S A KEYWORDS CAN BE 
    # CALLED FOR THE ROBOT REQUEST IN 'Get Firebird Query Results' KEYWORD, SIMILAR ON THE 'Get Query Results'
    # FOR MySQL Connection.
    #------------------------------------------------------------------------------------------------------------------\\
    @keyword(name='Get Firebird Query Results')
    def Get_FbQuery_Results(cls, show_fbcnn:bool= False, table:str=''):
        FbConnector.Set_Fbconnection()
        if(show_fbcnn is True): FbConnector.Show_Connection_Status()
        
        #\\... SECURITY CLAUSE FOR 'table' ARGUMENT VALUE ::
        if(table.lower() in ('', ' ')):
            log.info('', also_console=True); log.error('...')
            MyLog3.debug('%s' %(create_line(78, break_line=True, cmd='return'),))
            MyLog3.error('%s' %(dlmt_space(78, ("❌ [ArgumentError]:", '|')),))
            MyLog3.error("THE 'table' FUNCTION ARGUMENT MUST BE AN ACEPTABLE VALUE!")
            MyLog1.debug('%s' %(create_line(78, cmd='return'),))
            FbConnector.Close_Connection()
            raise ValueError()
        else: pass
        
        if(ope.eq(table.lower(), 'vendas')):
            results = FbConnector.Firebird_Query_VENDAS(
                person_code= Central.sales_person_code,
                person_user= Central.sales_person_name.lower())
            #\\... PDVOFF sale's sequence AUTO_INCREMENT            
            Central.current_pdv_sale_code(results[1], 'set')
            #cls.fb_sales_code = results[1]
            print("\n💠 NVendaExterna: %s" %(Central.current_pdv_sale_code(),))
            cls.firebird_check = bool(True)
            return

        #\\... IT HAS NOT BEEN IMPLEMENTED YET ::
        elif(ope.eq(table.lower(), 'cancelavenda')): 
            pass

        #\\... IT HAS NOT BEEN IMPLEMENTED YET ::
        elif(ope.eq(table.lower(), 'cx_movimentos')): 
            pass

        #\\... IT HAS NOT BEEN IMPLEMENTED YET ::
        elif(ope.eq(table.lower(), 'cx_aberturas')):
            pass
        return

    
    @keyword(name='Get Query Results')
    def Get_Query_Results(cls, /, table:str='table name'):
        """
        DOCUMENTATION ``MySQLConnector``:

        The callings method for Queries on database can be made througth this @keyword.
        Notice wich qurie's type you wish to peform and the clause send as return will
        be the query results against database table.
        """
        table = table.lower()
        wished_tables:tuple = (
            'vendas', 'notassaidas', 'chequest', 'contasareceber', 'caixamovimentos', 
            'caixamovimentosformas','cartaomovimento','pixmovimento', 'controlecaixa', 
            'cancelavenda', 'vendaincompleta', 'sangriacaixa', 'sangria_incomp')
        
        #\\... SECURITY CLAUSE FOR 'table' ARGUMENT VALUE ::
        if(table not in wished_tables):
            log.info('', also_console=True); log.error('...')
            MyLog3.debug('%s' %(create_line(78, break_line=True, cmd='return'),))
            MyLog3.critical('%s' %(dlmt_space(78, ("❌ [ArgumentError]:", '|')),))
            MyLog3.error("THE 'table' FUNCTION ARGUMENT MUST BE AN ACEPTABLE VALUE!")
            MyLog3.debug('%s' %(create_line(78, cmd='return'),))
            raise ValueError()
        else: pass
        
        MySQLConnector.Create_Connection(MySQLConnector, True)
        _time = localtime()

        # Query execution type: Sale Results
        if(ope.eq(table, 'vendas')): 
            return MySQLConnector.MySQL_Query_VENDAS(_time)
        # Query execution type: Fiscal Document Check up
        elif(ope.eq(table, 'notassaidas')): 
            return MySQLConnector.MySQL_Query_NOTASSAIDAS()
        # Query execution type: Check Payment Check Up
        elif(ope.eq(table, 'chequest')): 
            return MySQLConnector.MySQL_Query_CHEQUEST()
        # Query execution type: Customer Payment Record
        elif(ope.eq(table, 'contasareceber')): 
            return MySQLConnector.MySQL_Query_CONTASARECEBER()
        # Query execution type: Credit/Debt Payment Record
        elif(ope.eq(table, 'cartaomovimento')): 
            return MySQLConnector.MySQL_Query_CARTAOMOVIMENTO()
        # query execution type: PIX Movement
        # elif(ope.eq(table, 'pixmovimento')): 
        #    return MySQLConnector.Query_Pix_Payment()
        # Query execution type: Cashier Movement Inspector
        elif(ope.eq(table, 'controlecaixa')): 
            return MySQLConnector.MySQL_Query_CAIXAMOVIMENTOS()
        # Query execution type: Cashier Movement Inspector
        elif(ope.eq(table, 'caixamovimentosformas')): 
            return MySQLConnector.MySQL_Query_CAIXAMOVIMENTOS_E_FORMAS()
        # Query execution type: Cenceled Sale Event
        elif(ope.eq(table, 'cancelavenda')): 
            return MySQLConnector.Query_Canceling_Sale_Event()
        # Query execution type: Uncompleted Sale Event
        elif(ope.eq(table, 'vendaincompleta')): 
            return MySQLConnector.PSQL_FireBird_VENDAS(_time)
        # Query Execution type: Event 'Sangria' and 'Sangria' like a cashier movement
        elif(ope.eq(table, 'sangriacaixa')): 
            return MySQLConnector.Query_Cashier_Sangria_Event()
        # Query execution type: Check For Uncompleted Cashier Event Type: 'Sangria'
        elif(ope.eq(table, 'sangria_incomp')): 
            MySQLConnector.MySQL_Query_TRANSFERENCIASENTRECAIXAS_EMABERTO()
            MySQLConnector.MySQL_Query_TRANSFERENCIASENTRECAIXAS_COUNTER()
            return True
    

    @keyword(name='Database Record Incomplete')
    def Database_Record_Incomplete(cls) -> None:
        log.info('\n', also_console=True); log.error(msg='...')
        MyLog1.critical("%s" %(create_line(78, break_line=True, cmd='return'),))
        MyLog1.error(msg='THERE IS AN ERROR IN THE DATABASE FILES. LIKELY THIS RECORD IS EMPTY OR NULL!')
        MyLog1.error(msg='CHECK THE DATABASE: <%s>!' %cls._cnn_config.get('database'))
        MyLog1.critical("%s" %(create_line(78, break_line=True, to_the_end=True, cmd='return'),))
        Storage.master_status(False, 'set')
        return

    @keyword(name='Allowed Loop Time Has Been Exceeded')
    def Exceeded_Loop_Times(cls) -> None:
        log.info('\n', also_console=True); log.error(msg='...')
        MyLog1.critical("%s" %(create_line(78, break_line=True, cmd='return'),))
        MyLog1.error(msg='THE ALLOWED LOOP TIMES FOR DATABASE QUERIES HAS BEEN EXCEEDED!')
        MyLog1.error(msg='NO ACEPTABLE DATA VALUES HAS BEEN FOUND.')
        MyLog1.critical("%s" %(create_line(78, break_line=True, to_the_end=True, cmd='return'),))
        Storage.master_status(False, 'set')
        return


    @classmethod
    def Calculate_Current_Time(cls):
        #\\...  Timing  regress ::
        lc = localtime(); gv = [lc.tm_hour, lc.tm_min, lc.tm_sec]
        gv[2] -= 15 if gv[2] >= 15 else - 35
        if gv[2] <= 0: gv.insert(2, 45); gv[1] -= 1 if gv[1] > 0 else - 35
        if gv[1] <= 0: gv.insert(1, 59); gv[0] -= 1 if gv[0] > 0 else - 12
        if gv[0] <= 0: gv.insert(0, 23)
        the_time = (str(gv[0]).zfill(2), ':', str(gv[1]).zfill(2), ':', str(gv[2]).zfill(2))
        the_time = ''.join(the_time)
        return the_time
    
    
    #------------------------------------------------------------------------------------------------------------//
    # THIS METHOD LOOKING FOR UNCOMPLETED CASHIER EVENT TYPE "SANGRIA DE CAIXA". WHENEVER ISN'T POSSIBLE TO
    # FINALIZE A CASHIER EVENT LIKE THAT, THIS ONE STAYS UNCOMPLETED ON DATABASE RECORD. AS LONG AS IT'S
    # NEEDED ADJUST THAT EVENT RECORD.
    #------------------------------------------------------------------------------------------------------------\\
    @classmethod
    def MySQL_Query_TRANSFERENCIASENTRECAIXAS_EMABERTO(cls):
        print(f"\n🔎 PERFORMING QUERY TYPE 'SELECT' ON DATABASE {cls.MySQLconnection.database}")    
        print("\n💱 Current Cashier Open Code: %s\nCurrent NFC-e Number: %s\nCurrent ERP Sale Code: %s"
                %(Cashier.cashier_open_code(), Central.current_nfce_number(), Central.current_erp_sale_code()))

        query_fields:tuple = ('Sequencia', '`Status`')
        query = MyQuery.Query_TRANSFERENCIASNETRECAIXAS_ABERTO(query_fields, 
            {'openCode':Cashier.cashier_open_code(), 'cashierCode':Cashier.cashier_code()})

        with cls.MySQLconnection.cursor(buffered=True) as cursorA:
            cursorA.execute(query)
            cls.query_results = cursorA.fetchone()
            cursorA.close()
        pass


        if((cls.query_results is not None)):
            log.info('\n', also_console=True); log.warn('...')
            MyLog1.critical('%s' %(create_line(78, char='=', break_line=True, cmd='return'),))
            MyLog1.warning(msg="THERE IS AN UNCOMPLETED CASHIER EVENT TYPE 'SANGRIA' AVAILABLE ON DATABASE!")
            MyLog1.warning(msg='CHECK THE DATABASE: <%s>!' %cls.MySQLconnection.database)

            sequence:int = cls.query_results[0]
            new_query:str = """
            SELECT 
                Sequencia, 
                CodigoCaixaS,
                CaixaS, 
                Descricao, 
                Valor, 
                usuarioS, 
                DataS, 
                HoraS, 
                `Status` 
                FROM transferenciasentrecaixas AS 
            WHERE Sequencia = {}""".format(sequence)
            print("Query:\r%s" %new_query)
            with cls.MySQLconnection.cursor(buffered=True) as cursorB:
                cursorB.execute(new_query)
                results = cursorB.fetchone()
                MySQLConnector.Synchronization('default', cursorB.rowcount, int())
                cursorB.close()
            pass
            
            query_fields:tuple = (
                'Sequencia', 'CodigoCaixaS', 'CaixaS', 'Descricao', 
                'Valor', 'usuarioS', 'DataS', 'HoraS', 'Status')

            #\\... HTML OUTPU ::
            create_line(78, cmd='print')
            print('%s[ERP] TRANSFERENCIASENTRECAIXAS' %(expand(size=22),))
            create_line(78, cmd='print')
            for i in range(results.__len__() if results is not None else int()):
                n = lambda x, y: int(x) if ope.lt(str(y).__len__(), 2) else int(ope.sub(x, (str(y).__len__() - 1)))
                print("▪[%s] %s%s" %(i, format_space(n(30, i), query_fields[i]), results[i]))
            create_line(78, char='=', cmd='print')

            #\\... CONSOLE OUTPUT ::
            query_fields = format_fields(27, query_fields, to_the_end=':')
            MyLog1.critical('%s' %(create_line(78, char='=', cmd='return'),))
            MyLog1.info(msg=f"Cashier Code: {Cashier.cashier_code()} :: Cashier Open Code: {Cashier.cashier_open_code()}")
            MyLog1.info('%s' %(create_line(78, cmd='return'),))
            for i in range(len(query_fields)):
                if(ope.eq(i, 0)): MyLog1.warning(msg= str(query_fields[i] + str(results[i])))
                elif(ope.eq(i, 1)): MyLog1.info(msg= str(query_fields[i] + str(results[i])))
                else: MyLog1.critical(msg= str(query_fields[i] + str(results[i])))
            MyLog1.critical('%s' %(create_line(78, char='=', cmd='return'),))
            Central.sangria_status_is_open(True, 'set')
        else: print("❕ There isn't an available cashier event type: 'Sangria' on database records!")
        return

    
    #------------------------------------------------------------------------------------------------------------//
    # STARTUP FUNCTION... IT'S CALLED BEFORE THE TEST CASE SEQUENCE STARTUP TO VERIFIER POSSIBLE CASHIER'S EVENT
    # TYPE 'Sagria 'NOT CONCLUED!
    #------------------------------------------------------------------------------------------------------------\\
    @classmethod
    def MySQL_Query_TRANSFERENCIASENTRECAIXAS_COUNTER(cls):
        print(f"\n🔎 PERFORMING QUERY TYPE 'SELECT' ON DATABASE {cls.MySQLconnection.database}")    
        print("\n💱 Current Cashier Open Code: %s\nCurrent NFC-e Number: %s\nCurrent ERP Sale Code: %s"
                %(Cashier.cashier_open_code(), Central.current_nfce_number(), Central.current_erp_sale_code()))
        
        query_fields:tuple= ('$Sequencia',)
        query = MyQuery.Query_TRANSFERENCIASENTRECAIXAS_COUNTER(
                        fields= query_fields, 
                        filters= {'cashierCode':Cashier.cashier_code(),
                                'terminal':Central.machine_name.lower(), 
                                'openCode':Cashier.cashier_open_code(),
                                'username':Central.sales_person_name.lower(),
                                'salecode':Central.current_erp_sale_code()})
        
        results = tuple()
        with cls.MySQLconnection.cursor(buffered=True) as cursor:
            cursor.execute(query)
            results = cursor.fetchone()
            cursor.close()
        pass

        if((results is not None) and (ope.gt(results[0], Cashier.qnt_sangria()))):
            #\\... HTML OUTPUT ::
            create_line(78, cmd='print')
            print('%s[ERP] CONTASARECEBER + FORMASRECEBIMENTO' %(expand(size=22),))
            create_line(78, cmd='print')
            for i in range(len(results)):
                n = lambda x, y: int(x) if ope.lt(str(y).__len__(), 2) else int(ope.sub(x, (str(y).__len__() - 1)))
                print("▪[%s] %s%s" %(i, format_space(n(30, i), query_fields[i]), results[i]))
            create_line(78, char='=', cmd='print')

            #\\... CONSOLE OUTPUT ::
            log.info('\n', also_console=True); log.warn('...')
            MyLog1.critical('%s' %(create_line(78, char='=', break_line=True, cmd='return'),))
            MyLog1.warning(msg="THE CASHIER'S BREAKDOWN NOT MATCH TO THE DATABASE CASHIER MOVEMENTS!")
            MyLog1.warning(msg="THERE IS AN OPEN EVENT TYPE 'Sangria' THAT REQUIRES ADJUSTMENT")
            MyLog1.warning(msg='CHECK THE DATABASE: <%s>!' %cls.MySQLconnection.database)
            MyLog1.critical('%s' %(create_line(78, cmd='return'),))
            MyLog1.info("Performing Cashier adjustment...")
            MyLog1.critical('%s' %(create_line(78, char='=', cmd='return'),))
            Central.sangria_counter_controller(True, 'set')
        else: print("❕ There isn't an available cashier event type: 'Sangria' on database records!")
        return
    

    #------------------------------------------------------------------------------------------------------------//
    # THIS METHOD WRITEN BELLOW HAS BEEN CREATED TO PERFOMING A FIRST CHECKING FOR EACH SALE EVENT HAS PERFORMED
    # FOR THE PROJECT SOLUTIONS. A SALE'S EVENT RECORDET GET A FIELD CALLED `STATUS` THAT WRITEN JUST AFTER ITS
    # ALL OF SYNCHRONIZATION PROCESS WHAT CONSIDERS THE `STATUS` AS THE FINAL FIELD TO RECORDING.
    #------------------------------------------------------------------------------------------------------------\\
    @classmethod
    def Synchronization(cls, __type:str, /, rowcount:int, statIter:int, table:str='') -> bool | None:
        """
        DOCUMENTATION: ``MySQLConnector``

        Check up for the sale's synchronization attributes used to set up a sale's processing step
        on database records.

        Positional-Only argument `<str> type` can be set up to `'default'` when its usage 
        not concern the `[vendas]` or `[notassaidas]` tables.
        """
        #\\... BEGIN ::
        expected_types:tuple = (
            'single', 'double', 'trouble')
        expected_tables:tuple = (
            'any', 'sale', 'salec', 'taxdoc', 'taxdocc', 'chequest', 
            'ticket', 'card', 'pix', 'contasreceb')
        
        status:object = None; count:int = int()
        #\\... Cascate Ternary Expression for rowcount epect value for each table query ::
        count = (1 if(ope.eq(__type.lower(), 'single')) 
                 else(2 
                      if ope.eq(__type.lower(), 'double') 
                      else(3 
                           if(ope.eq(__type.lower(), 'trouble'))
                             else -1)))
        
        if((__type.lower() not in expected_types) 
           or (ope.lt(count, int())) 
             or (table not in expected_tables)):

            log.info('', also_console=True); log.error('...')
            MyLog3.debug('%s' %(create_line(78, break_line=True, cmd='return'),))
            MyLog2.error('%s' %(dlmt_space(77, ('⭕ [LibraryException]:', '|')),))
            MyLog1.error('%s'
            %(dlmt_space(78,
                ('Unexpected value got as argument to the @classmethod [Synchronization]'.upper(), '|')),))
            MyLog3.debug('%s' %(create_line(78, cmd='return'),))
            raise ValueError()
        else: pass
        
        #\\... SET UP THE CLAUSES FOR METHOD'S BEHAVIOUR ::
        if(ope.eq(table.lower(), 'sale')): status = str('f')
        elif(ope.eq(table.lower(), 'salec')): status = str('c')
        elif(ope.eq(table.lower(), 'taxdoc')): status = int(100)
        elif(ope.eq(table.lower(), 'taxdocc')): status = int(101)
        elif(ope.eq(table.lower(), 'chequest')): status = str('registered')
        elif(ope.eq(table.lower(), 'contasreceb')): status = str('success')

        #\\... ESCAPE CLASE ::
        if(ope.eq(table.lower(), 'any')): return

        #\\... CHECK FOR ROWCOUNT BIGGEST THAN EXPECTED COUNTER FOR LINES::
        if(ope.gt(rowcount, count)):
            log.info('', also_console=True); log.error('...')
            MyLog1.critical('%s' %(create_line(78, break_line=True, cmd='return'),))
            MyLog2.error('%s' %(dlmt_space(77, ('🔴 [QueryError]:', '|')),))
            MyLog1.error('%s'
            %(dlmt_space(78, ('The Query Result has returned most of expected rowcount!'.upper(), '|')),))
            MyLog1.critical('%s' %(create_line(78, cmd='return'),))
            raise errors.DataError()
        
        #\\.. CHECK FOR EMPTY ARRAY FROM DATABASE ::
        elif(ope.eq(cls.query_results, []) or ope.eq(rowcount, int())):
            log.info('', also_console=True); log.error('...')
            MyLog1.critical('%s' %(create_line(78, break_line=True, cmd='return'),))
            MyLog2.error('%s' %(dlmt_space(77, ('🟠 [QueryException]:', '|')),))
            MyLog1.error('%s'
            %(dlmt_space(78, ('► The Query Result has returned an empty object sequence!'.upper(), '|')),))
            MyLog1.critical('%s' %(create_line(78, cmd='return'),))
            print("❌ @property: cls.query_results is Empty: %s" %(cls.query_results,))
            cls.MySQLconnection.close()
            return False
        
        #\\... CHECK FROM DIFFERENT STATUS FOR AN EXPECTED STATUS VALUE ::
        elif(ope.ne(
            str.lower(cls.query_results[0][statIter])
            if (isinstance(cls.query_results[0][statIter], str)) 
            else (cls.query_results[0][statIter]), status)):
            
            log.info('', also_console=True); log.warn('...')
            MyLog1.critical('%s' %(create_line(78, break_line=True, cmd='return'),))
            MyLog2.warning('%s' %(dlmt_space(77, ('🟡 [QueryWarning]:', '|')),))
            MyLog1.warning("%s" %(dlmt_space(78,
                ("► THE [%s] QUERY RESULTS IN `Status` IS DIFFERENT FROM %s"%(table, status), "|")),))
            MyLog1.critical('%s' %(create_line(78, cmd='return'),))
            print("\n@property: cls.query_results in (`Status`) field is different from 'f'")
            cls.MySQLconnection.close()
            return False if table.lower() in ('sale', 'taxdoc', 'contasareceber') else True
        #\\... END LIKE ::
        else: return

    #-------------------------------------------------------------------------------------------------------------//
    # QUERYING FOR THE SALE EVENT ON ERP [VENDAS] ::
    # THIS METHOD IS CALLING FOR THE FIREBIRD SERVER CONNECTION AND LOOKING FOR SOME SALE'S DATA RECORDED THERE.
    #-------------------------------------------------------------------------------------------------------------\\
    @classmethod
    def MySQL_Query_VENDAS(cls, given_time:object = None):   
        print(f"\n🔎 PERFORMING QUERY TYPE 'SELECT' ON DATABASE {cls.MySQLconnection.database}")        
        print("\n👨‍💼 Current CPF/CNPJ serial code: %s\nThe same one has previously stored: %s"
                %(Central.current_cpf_cnpj(), (Storage.last_customer_ident().__getitem__(-1) 
                if(ope.ne(Storage.last_customer_ident().__len__(), 0)) else ['Empty',])))
        
        query_fields:tuple = (
            'Codigo', 'NVendaExterna', 'NumeroNF', 'TotalPedido', 'ValorFinalPagamentos',
            'QuantidadePag', 'VLR_TROCO_PDV', '`Status`', 'Cancelada', 'Tabela',
            'CodigoCliente', 'RazaoCliente', 'CNPJ', '`Data`', 'Hora')
        
        query = MyQuery.Query_VENDAS(
                query_fields, 
                {'nvendaexterna':Central.current_pdv_sale_code(),
                'codigovendedor':Central.sales_person_code,
                'usuario':Central.sales_person_name.lower(),
                'terminal':Central.machine_name.lower(),
                'empresa':Central.company_internal_code()})

        with cls.MySQLconnection.cursor(buffered=True) as cursor:
            cursor.execute(query)
            cls.query_results = cursor.fetchall()    
            sync = MySQLConnector.Synchronization(
                'single', 
                cursor.rowcount, 
                statIter=7, 
                table='sale')
            cursor.close()
            if sync is not None: return sync
        pass

        Central.current_erp_sale_code(cls.query_results[0][0], 'set')
        Central.current_sale_status(cls.query_results[0][7], 'set')
                
        # HTML OUTPUT ::
        create_line(78, cmd='print')
        print('%s[ERP] VENDAS' %(expand(size=32),))
        create_line(78, cmd='print')
        for i in range(len(cls.query_results[0])):
            n = lambda x, y: int(x) if ope.lt(str(y).__len__(), 2) else int(ope.sub(x, (str(y).__len__() - 1)))
            print("▪[%s] %s%s" %(i, format_space(n(30, i), query_fields[i]), cls.query_results[0][i]))
        create_line(78, char='=', cmd='print')
        
        # CONSOLE OUTPUT ::
        current_time = st('%H:%M:%S', lt()) 
        MyLog1.critical('%s' %(create_line(78, char='=', break_line=True, cmd='return'),))
        MyLog1.info('%s'
            %(dlmt_space(
                78, (f'Date: {cls.today}', f'Time Query Between: {given_time} AND {current_time}')),))
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        MyLog2.debug('%s[ERP] VENDAS' %(expand(size=32),))
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        query_fields = format_fields(29, query_fields, to_the_end=':')
        for i in range (len(cls.query_results[0])):
            if(ope.eq(i, 0)): MyLog2.debug(f"{query_fields[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 1)): MyLog2.log(level=50, msg=f"{query_fields[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 2)): MyLog2.info(f"{query_fields[i]} {cls.query_results[0][i]}")
            else: MyLog1.critical(f"{query_fields[i]} {cls.query_results[0][i]}")
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        First_Stage_ERP(results= cls.query_results[0])
        return True


    #-------------------------------------------------------------------------------------------------------------//
    # QUERYING FOR THE SALE EVENT ON [NOTASSAIDAS] ::
    # THIS METHOD CONTAINS THE SQL FISCAL CHECKUP WRITEN INSIDE ITSELF.
    #-------------------------------------------------------------------------------------------------------------\\
    @classmethod
    def MySQL_Query_NOTASSAIDAS(cls):
        print(f"\n🔎 PERFORMING QUERY TYPE 'SELECT' ON DATABASE {cls.MySQLconnection.database}")        
        print("\n👨‍💼 Current CPF/CNPJ serial code: %s\nThe same one has previously stored: %s"
                %(Central.current_cpf_cnpj(), (Storage.last_customer_ident().__getitem__(-1) 
                if(ope.ne(Storage.last_customer_ident().__len__(), 0)) else ['Empty',])))

        query_fields:tuple = (
            'ns.Sequencia', 'ns.Nvenda', 'ns.NF', 'ns.Serie', 'ns.MovPDV', 'ns.SequenciaNotaPDV', 
            'ns.TotalNF', 'ns.TrocoPDV', '$Cstat', 'ns.Dest_Nome', 'ns.CodigoCliente', 
            '$IdentificacaoCliente', '$DocumentoCliente', 'ns.DataSaida', 'ns.HoraSaida', 
            'Situacao', 'ns.MsgRetorno', 'ns.VersaoPDV', 'ns.ChaveNFE')

        query = MyQuery.Query_NOTASSAIDAS(
                    query_fields,
                    {'empresa':Central.company_internal_code(),
                    'codigovendedor':Central.sales_person_code,
                    'terminal':Central.machine_name.lower(),
                    'nvenda':Central.current_erp_sale_code()})
        
        with cls.MySQLconnection.cursor(buffered=True) as cursor:
            cursor.execute(query)
            cls.query_results = cursor.fetchall()
            sync = MySQLConnector.Synchronization(
                'single', 
                cursor.rowcount, 
                statIter=8,
                table='taxdoc')
            cursor.close()
            #if sync is not None: return sync
        pass

        Central.current_nfce_number(cls.query_results[0][2], 'set')

        # HTML OUTPUT ::
        create_line(78, cmd='print')       
        print('%s[ERP] NOTASSAIDAS' %(expand(size=32),))                                                                              
        create_line(78, cmd='print')
        for i in range(len(cls.query_results[0])):
            n = lambda x, y: int(x) if ope.lt(str(y).__len__(), 2) else int(ope.sub(x, (str(y).__len__() - 1)))
            print("▪[%s] %s%s" %(i, format_space(n(30, i), query_fields[i]), cls.query_results[0][i]))
        create_line(78, char='=', cmd='print')
        
        # CONSOLE OUTPUT ::
        MyLog1.critical('%s' %(create_line(78, char='=', break_line=True, cmd='return'),))
        MyLog1.info('%s'
            %(dlmt_space(
            78, (f'User Code: {Central.sales_person_code}{expand()}     User Name: {Central.sales_person_name}', 
                 f'Sales Code: {Central.current_erp_sale_code()}')),))
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        MyLog2.info('%s[ERP] NOTASSAIDAS' %(expand(size=29),))
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        query_fields = format_fields(
            29, query_fields, 
            to_the_end=':', 
            del_punctuation=True,
            split_text= (True, '.'))
        
        for i in range (len(cls.query_results[0])):
            _field = query_fields[i]
            if(ope.eq(i, 1)): MyLog2.debug(f"{_field} {cls.query_results[0][i]}")
            elif(ope.eq(i, 2)): MyLog2.info(f"{_field} {cls.query_results[0][i]}")
            elif(ope.eq(i, 7)): MyLog2.log(level=50, msg=f"{_field} {cls.query_results[0][i]}")
            elif(ope.eq(i, (query_fields.__len__() - 2))):
                MyLog2.log(level=50, msg=f"{_field} {cls.query_results[0][i]}")
            elif(ope.eq(i, (query_fields.__len__() - 1))):
                MyLog1.critical(f"{_field}" +
                    f"{str(str(cls.query_results[0][i])[:20] + '...' + str(cls.query_results[0][i])[-4:])}")
            elif(ope.eq(i, (len(cls.query_results[0])))):
                MyLog1.info('%s' %(create_line(78, cmd='return'),))
                MyLog1.warning(f"{_field} {cls.query_results[0][i]}")
            else: MyLog1.critical(f"{_field} {cls.query_results[0][i]}")
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        Second_Stage_ERP(results= cls.query_results[0])

        #---------------------------------------------------------------------------------------------------------------//
        #                                         INTERNAL FISCAL CHECKUP 2.0
        #--------------------------------------------------------------------------------------------------------------\\
        # THIS MODULE HAS BEEN WRITEN AS A LIBRARY EXTENSION FOR SALE'S AUDIT. ITS JOB IS CHECKING FOR DIFFERENCES OR
        # ERRORS RAISED FROM SALE'S SYNCHRONIZATION PROCESS PERFORMED AT RUNTIME AFTER ITS ENDING. THE NFC-e IS A TAX
        # DOCUMENT WHOSE CONTAINS ALL OF FISCAL TAXES AND THEIRS APPLICATION FOR EACH PRODUCTS FORWARD TO THE SALE.
        #---------------------------------------------------------------------------------------------------------------\\

        if(not cls.MySQLconnection.is_connected()):
            MySQLConnector.Create_Connection(MySQLConnector, True)

        # To be Continued from here...
        # NEW SQL QUERY :: FISCAL CHECKUP...
        queries_group = parse_query_method(
            sale_number= Central.current_erp_sale_code(), 
            nfce_number= Central.current_nfce_number(),
            nfce_serial= cls.query_results[0][3])
        
        fiscal_query = queries_group.get('taxes_calc_query')
        print(str(queries_group.get('expected_fiscal_values')) 
              + '\n' + str(queries_group.get('taxes_calc_query')))
        
        fsc_cursor = cls.MySQLconnection.cursor(buffered=True)
        fsc_cursor.execute(str(fiscal_query))
        this_query_result = fsc_cursor.fetchall()
        fsc_cursor.close()
        # Data extraction from database results::
        extract:tuple = (
            tuple(this_query_result[0])
            if((isinstance(this_query_result, list))
               and (ope.ne(this_query_result, []))) else this_query_result)
        
        # HTML LOG OUTPUT ::
        print("\n► 'taxes_calc_query' results: 📜 %s" %(this_query_result,))
        #print("► 'extract' variable from 'taxes_calc_query' results: 📜 %s" %(extract,))
        if(extract is None):
            log.info('\n'); log.error('...')
            MyLog1.info('%s' %(create_line(78, char='=', break_line=True, cmd='return'),)) 
            MyLog1.error("At least one of the query elements on 'taxes_calc_query' is empty or IS NULL")
            MyLog1.warning('Use the Fiscal_CheckUp.py to find what is the Tax Document Issue')
            MyLog1.info('%s' %(create_line(78, char='=', cmd='return'),)) 
            cls.MySQLconnection.close()
            return True  #-> Exit Function
        
        # SQL Mathmatical Functions. Check for the SQL QUERY has writen to does it.
        comparison_query = final_comparison(
            Central.current_erp_sale_code(),
            Central.current_nfce_number(),
            cls.query_results[0][3],
            company_code= Central.company_internal_code(),
            values= (extract[0], extract[1], extract[2], extract[3]))
        
        # NEW SQL QUERY ::
        print('\n◉ FINAL COMPARISON QUERY:\n' + comparison_query)
        fsc_cursor = cls.MySQLconnection.cursor(buffered=True)
        fsc_cursor.execute(comparison_query)
        final_result = fsc_cursor.fetchall()
        fsc_cursor.close()
        print("\n► 'final_comparison' query resuls:\n📜 %s" %(final_result,))
        
        fields = (
            'NF', 'Serie', 'NVenda', 'NVendaExterna', 'TotalNF', 'Total_Auditado', 'TotalIcms',
            'ICMS_Auditado', 'Total_PIS', 'PIS_Auditado', 'Total_Cofins', 'COFINS_Auditado', 
            'TotalIcmsDesonerado', 'ICMS_Total_Final', 'Comparacao_Total', 'Comparacao_ICMS',
            'Comparacao_PIS', 'Comparacao_COFINS')
        formated_msg = format_fields(25, fields, to_the_end=':'); table = list()

        # PRINT EVALUATING ::
        fiscal_status:int = 0
        for e in range((len(final_result[0])-5), (len(final_result[0]))): 
            if(ope.eq(final_result[0][e], 'NOT MATCH' )): fiscal_status = 2; break
            elif(ope.eq(final_result[0][e], 'TOLERANCE')): fiscal_status = 1; break
    
        print("\nComparison Slice: %s" %(final_result[0][-4:],))
        print("%s Fiscal Status of the Tax Document Number %s: %s ↦ '%s'\n" %(
            ('✅' if (fiscal_status == 0) else ('❕' if (fiscal_status == 1) else '❌')), 
            Central.current_nfce_number(), fiscal_status, 
            ('NOT MATCH' if(fiscal_status == 2) else ('TOLERANCE' if fiscal_status == 1 else 'MATCH'))))
        if(ope.ne(final_result, [])):
            for i in range(len(final_result[0])):
                table.append(str(str(formated_msg[i]) + str(final_result[0][i])))
                print("<list>:table[i] %s" %(table[i],))
        
        # Data outuput on cosole log...
        table = format_fields(38, table)
        MyLog1.critical('...%s' %(create_line(78, char='=', break_line=True, cmd='return'),))
        if(fiscal_status == 0): MyLog2.info("%s► FISCAL INFERENCE" %expand(size=30))
        elif(fiscal_status == 1): MyLog2.warning("%s► FISCAL INFERENCE" %expand(size=30))
        else: MyLog1.error("%s► FISCAL INFERENCE" %expand(size=30))
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        broke_table:bool = True
        interval:int= 2 if(ope.eq(ope.mod(len(table), 2), 0)) else 3
        for e in range(interval, (len(table) + interval), interval):
            comp:int = ope.sub(e, interval) if(ope.ge(e, interval)) else int(0)
            if(ope.ge(comp, ope.sub(len(table), 5))):
                if(broke_table is True):
                    MyLog1.info('%s' %(create_line(78, cmd='return'),))
                    MyLog2.warn("%s► DATA COMPARISON" %expand(size=30))
                    MyLog1.info('%s' %(create_line(78, cmd='return'),))
                    broke_table = False
                if(fiscal_status == 0): MyLog2.info(str('    '.join(map(str, table[comp:e]))))
                elif(fiscal_status == 1): MyLog2.warning(str('    '.join(map(str, table[comp:e]))))
                else: MyLog1.error(str('    '.join(map(str, table[comp:e]))))
            else: MyLog1.critical(str('    '.join(map(str, table[comp:e]))))
        MyLog1.critical('%s' %(create_line(78, char='=', cmd='return'),))
        return True
        

    #-------------------------------------------------------------------------------------------------------------//
    # QUERYING FOR THE SALE EVENT ON TABLE [CONTASARECEBER] ::
    # THIS METHOD CONTAINS THE SQL QUERY FOR TABLES [CONTASARECER] + [FORMARECEBIMENTO]
    #-------------------------------------------------------------------------------------------------------------\\
    @classmethod
    def MySQL_Query_CONTASARECEBER(cls):
        print(f"\n🔎 PERFORMING QUERY TYPE 'SELECT' ON DATABASE {cls.MySQLconnection.database}")    
        print("\n💱 Current Cashier Open Code: %s\nCurrent NFC-e Number: %s\nCurrent ERP Sale Code: %s"
                %(Cashier.cashier_open_code(), Central.current_nfce_number(), Central.current_erp_sale_code()))
        
        query_fields:tuple =(
            'cr.Sequencia', 'cr.NDocumento', 'cr.CodigoVenda', 'cr.ValorOriginal', 'cr.Valor', 'cr.Quitado',
            'cr.Cancelada', 'cr.idCaixaAbertura', 'cr.CR_COD_FORMA_REC', '$NaturezaRegistro', 'fr.Descricao',
            'fr.Tipo', 'cr.Descricao', '$FinalStatus')

        query = MyQuery.Query_CONTASARECEEBR(
        query_fields, {'terminal':Central.machine_name.lower(), 
                       'openCode':Cashier.cashier_open_code(),
                       'fiscaldocument':Central.current_nfce_number(),
                       'salecode':Central.current_erp_sale_code()})
        
        with cls.MySQLconnection.cursor(buffered=True) as cursor:
            cursor.execute(query)
            cls.query_results = cursor.fetchall()
            sync = MySQLConnector.Synchronization(
                'single', 
                cursor.rowcount, 
                statIter=ope.sub(query_fields.__len__(), 1), 
                table='contasreceb')
            cursor.close()
            if sync is not None: return sync
        pass
        
        # HTML OUTPUT ::
        create_line(78, cmd='print')
        print('%s[ERP] CONTASARECEBER + FORMASRECEBIMENTO' %(expand(size=22),))
        create_line(78, cmd='print')
        for i in range(len(cls.query_results[0])):
            n = lambda x, y: int(x) if ope.lt(str(y).__len__(), 2) else int(ope.sub(x, (str(y).__len__() - 1)))
            print("▪[%s] %s%s" %(i, format_space(n(30, i), query_fields[i]), cls.query_results[0][i]))
        create_line(78, char='=', cmd='print')

        # CONSOLE OUTPUT ::
        MyLog1.critical('%s' %(create_line(78, char='=', break_line= True, cmd='return'),))
        MyLog1.info('%s' 
        %(dlmt_space(78, (f'Vendor Name: {Central.sales_person_name}', f'Customer Code: {Central.customer_code()}'))))
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        MyLog1.info('%s[ERP] CONTASARECEBER ▶ %s' %(expand(size=25), Payment.current_paymnt_on_use()))
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        query_fields = format_fields(
            29, 
            query_fields, 
            to_the_end=':', 
            del_punctuation=True)
        
        for i in range(len(cls.query_results[0])):
            if(ope.eq(i, 0)): MyLog1.info(f"{query_fields[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 1)): MyLog2.info(f"{query_fields[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 2)): MyLog1.debug(f"{query_fields[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 3)): 
                (MyLog3.debug(f"{query_fields[i]} {cls.query_results[0][i]}") 
                 if(ope.eq(Central.final_sale_value(), cls.query_results[0][i]))
                 else (MyLog1.error(f"{query_fields[i]} {cls.query_results[0][i]}")))
            else: MyLog3.debug(f"{query_fields[i]} {cls.query_results[0][i]}")
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        
        if ope.eq(Payment.current_paymnt_on_use(), 'CRE'): Store_Data_Sale()
        return

    
    #-------------------------------------------------------------------------------------------------------------//
    # QUERYING FOR THE SALE EVENT ON TABLE [CAIXAMOVIMENTOS] AS {ControleCaixa} STEP 1 ::
    # THIS METHOD CONTAINS THE SQL QUERY FOR TABLES [CAIXAMOVIMENTOS] + [CAIXAMOVIMENTOSFORMAS] + [VENDAS]
    #-------------------------------------------------------------------------------------------------------------\\
    @classmethod
    def MySQL_Query_CAIXAMOVIMENTOS_E_FORMAS(cls):
        print(f"\n🔎 PERFORMING QUERY TYPE 'SELECT' ON DATABASE {cls.MySQLconnection.database}")    
        print("\n💱 Current Cashier Open Code: %s\nCurrent NFC-e Number: %s\nCurrent ERP Sale Code: %s"
                %(Cashier.cashier_open_code(), Central.current_nfce_number(), Central.current_erp_sale_code()))    
        
        query_fields:tuple = (
            'cmf.Sequencia', 'cm.Sequencia', 'cm.CodigoConta', 'cmf.CodigoMovimento', 'v.Codigo', 
            'cm.nDocumento', 'cm.ValorDocumento', 'cm.ValorPago', '$Status', 'v.CodigoCliente', 
            'v.RazaoCliente', 'v.TotalPedido', 'v.ValorFinalPagamentos', 'cmf.Valor', '$TipoMovimento',
            'cmf.Forma', 'cmf.Tipo', 'cm.SaldoAnterior', 'cm.Saldo', 'cm.ContaRP', 'cm.`Data`')

        query = MyQuery.Query_CAIXAMOVIMENTOSFORMAS(
        query_fields, {'openCode':Cashier.cashier_open_code(),
                       'fiscaldocument':Central.current_nfce_number(),
                       'salecode':Central.current_erp_sale_code()})
        
        with cls.MySQLconnection.cursor(buffered=True) as cursor:
            cursor.execute(query)
            cls.query_results = cursor.fetchall()
            cls.cur_rowcount = cursor.rowcount
            MySQLConnector.Synchronization(
                'single', 
                cursor.rowcount, 
                statIter= int(),
                table='any')
            cursor.close()
        pass

        # HTML OUTPUT ::
        create_line(78, cmd='print')
        print('%s[ERP] CAIXAMOVIMENTOS + CAIXAMOVIMENTOSFORMAS' %(expand(size=22),))
        create_line(78, cmd='print')
        for i in range(len(cls.query_results[0])):
            n = lambda x, y: int(x) if ope.lt(str(y).__len__(), 2) else int(ope.sub(x, (str(y).__len__() - 1)))
            print("▪[%s] %s%s" %(i, format_space(n(30, i), query_fields[i]), cls.query_results[0][i]))
        create_line(78, char='=', cmd='print')

        # CONSOLE OUTPUT ::
        MyLog3.debug('%s' %(create_line(78, char='=', break_line=True, cmd='return'),))
        MyLog1.info(f'Date: {cls.today}  ::  Sales Person Code: {Central.sales_person_code}' +
                        f'  ::  Sales Person Name: {Central.sales_person_name}')
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        MyLog2.warning('%s[ERP] CAIXAMOVIMENTOS & FORMAS ▶ %s' %(expand(size=20), Payment.current_paymnt_on_use()))
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        query_fields = format_fields(
            29, query_fields, 
            to_the_end=':', 
            del_punctuation=True)
        
        for i in range (len(cls.query_results[0])):
            if(ope.eq(i, 0)): MyLog2.warning(f"{query_fields[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 1)): MyLog1.warning(f"{query_fields[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 2)): MyLog1.info(f"{query_fields[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 4)): MyLog1.debug(f"{query_fields[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 5)): MyLog2.info(f"{query_fields[i]} {cls.query_results[0][i]}")
            elif(i in (6, 11, 13)): 
                (MyLog3.debug(f"{query_fields[i]} {cls.query_results[0][i]}")
                 if(ope.eq(Central.final_sale_value(), cls.query_results[0][i]))
                 else MyLog1.error(f"{query_fields[i]} {cls.query_results[0][i]}"))
            else: MyLog1.critical(f"{query_fields[i]} {cls.query_results[0][i]}")
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        return True
    

    #-------------------------------------------------------------------------------------------------------------//
    # QUERYING FOR THE SALE EVENT ON TABLE [CHEQUEST] ::
    # THIS METHOD CONTAINS THE SQL QUERY FOR TABLE [CHEQUEST] + [CONTASARECEBER] DATA COMPARISON.
    #-------------------------------------------------------------------------------------------------------------\\
    @classmethod
    def MySQL_Query_CHEQUEST(cls):
        print(f"\n🔎 PERFORMING QUERY TYPE 'SELECT' ON DATABASE {cls.MySQLconnection.database}")        
        query_fields:tuple = (  
            'c.Sequencia', 'c.idTransf', 'c.CodVenda', 'c.IdCaixaMovimento', 'c.CodigoContaReceber',
            '$ContaReceberStatus', 'c.NCheque', 'c.Banco', 'c.Agencia', 'c.NConta', 'c.Valor', 
            'c.CodigoCliente', 'c.Cliente', 'c.CPF_Emitente', 'c.DataPre', 'c.Observacoes')
        
        query = MyQuery.Query_CHEQUEST(query_fields, {'ncheque':Payment.chq_serial_number(), })
        with cls.MySQLconnection.cursor(buffered=True) as cursor:
            cursor.execute(query)
            cls.query_results = cursor.fetchall()
            cls.cur_rowcount = cursor.rowcount
            MySQLConnector.Synchronization(
                'single', 
                cursor.rowcount, 
                statIter= 5,
                table='chequest')
            cursor.close()
        pass

        # HTML OUTPUT ::
        create_line(78, cmd='print')
        print('%s[ERP] CHEQUEST + CONTASARECEBER ' %(expand(size=22),))
        create_line(78, cmd='print')
        for i in range(len(cls.query_results[0])):
            n = lambda x, y: int(x) if ope.lt(str(y).__len__(), 2) else int(ope.sub(x, (str(y).__len__() - 1)))
            print("▪[%s] %s%s" %(i, format_space(n(30, i), query_fields[i]), cls.query_results[0][i]))
        create_line(78, char='=', cmd='print')

        # CONSOLE OUTPUT ::
        MyLog1.critical('%s' %(create_line(78, char='=', break_line=True, cmd='return'),))        
        MyLog1.info('%s'
            %(dlmt_space(
                78, (f'Date: {cls.today}  ::  User Name: {Central.sales_person_name}', 
                     f'   ::   Sales Code: {Central.current_erp_sale_code()}')),))
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        MyLog3.debug('%sERP [CHEQUEST]' %(expand(size=30),))
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        query_fields = format_fields(
            29,
            query_fields, 
            to_the_end=':', 
            del_punctuation=True, 
            split_text=(True, '.'))
        #10 valor
        for i in range (len(cls.query_results[0])):
            if(ope.eq(i, 2)): MyLog2.debug(f"{query_fields[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 3)): MyLog1.warning(f"{query_fields[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 4)): MyLog1.info(f"{query_fields[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 10)):
                (MyLog3.debug(f"{query_fields[i]} {cls.query_results[0][i]}") 
                 if(ope.eq(cls.query_results[0][i], Central.final_sale_value()))
                 else MyLog2.error(f"{query_fields[i]} {cls.query_results[0][i]}"))
            else: MyLog3.debug(f"{query_fields[i]} {cls.query_results[0][i]}")
        MyLog3.debug('%s' %(create_line(78, char='=', cmd='return'),)) 
        return True


    #-------------------------------------------------------------------------------------------------------------//
    # QUERYING FOR THE SALE EVENT ON TABLE [CARAOMOVIMENTO] ::
    # THIS METHOD CONTAINS THE SQL QUERY FOR TABLE [CARTAOMOVIMENTO] ONLY
    #-------------------------------------------------------------------------------------------------------------\\
    @classmethod
    def MySQL_Query_CARTAOMOVIMENTO(cls):
        print(f"\n🔎 PERFORMING QUERY TYPE 'SELECT' ON DATABASE {cls.MySQLconnection.database}")    
        print("\n💱 Current Cashier Open Code: %s\nCurrent NFC-e Number: %s\nCurrent ERP Sale Code: %s"
                %(Cashier.cashier_open_code(), Central.current_nfce_number(), Central.current_erp_sale_code()))
        
        query_fields:tuple = (
            'Sequencia', 'CodigoVenda', '`DATA`', 'Hora', 'CodigoOperadora', 'CodigoProduto',
            'CV', 'NParcelas', 'Valor', 'Tarifa', 'ValorTaxaOperacao', 'ValorLiquido')
        
        query = MyQuery.Query_CARTAOMOVIMENTO(
        query_fields, {'terminal':Central.machine_name.lower(),
                       'fiscaldocument':Central.current_nfce_number(),
                       'salecode':Central.current_erp_sale_code()})

        with cls.MySQLconnection.cursor(buffered=True) as cursor:
            cursor.execute(query)
            cls.query_results = cursor.fetchall()
            cls.cur_rowcount = cursor.rowcount
            MySQLConnector.Synchronization(
                'single',
                cursor.rowcount, 
                statIter= int(),
                table='any')
            cursor.close()
        pass

        # HTML OUTPUT ::
        create_line(78, cmd='print')
        print('%s[ERP] CONTASARECEBER + FORMASRECEBIMENTO' %(expand(size=22),))
        create_line(78, cmd='print')
        for i in range(len(cls.query_results[0])):
            n = lambda x, y: int(x) if ope.lt(str(y).__len__(), 2) else int(ope.sub(x, (str(y).__len__() - 1)))
            print("▪[%s] %s%s" %(i, format_space(n(30, i), query_fields[i]), cls.query_results[0][i]))
        create_line(78, char='=', cmd='print')

        # CONSOLE OUTPUT ::
        log.info('', also_console=True)
        MyLog1.critical('%s' %(create_line(78, char='=', break_line=True, cmd='return'),))
        MyLog1.info('%s' 
        %(dlmt_space(78, (f'Vendor Name: {Central.sales_person_name}', f'Customer Code: {Central.customer_code()}'))))
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        MyLog1.warning('%sCARTAOMOVIMENTO ' %(expand(size=29),))
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        query_fields = format_fields(22, query_fields)
        for i in range (len(cls.query_results[0])):
            if(ope.eq(i, 0)): MyLog1.warning(f"{query_fields[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 11)): MyLog2.debug(f"{query_fields[i]} {cls.query_results[0][i]}")
            else: MyLog1.critical(f"{query_fields[i]} {cls.query_results[0][i]}")
        MyLog1.critical('%s' %(create_line(78, char='=', break_line=True, to_the_end=True, cmd='return'),))
        # Calling the Aduit Card Method with their arguments respectively...
        sequence:int = cls.query_results[0][0]

        #---------------------------------------------------------------------------------------------------------------//
        #                                         INTERNAL CARD MOVEMENT 1.0
        #--------------------------------------------------------------------------------------------------------------\\
        # THIS MODULE HAS BEEN WRITEN AS A LIBRARY EXTENSION FOR SALE'S AUDIT. ITS JOB IS LOOKING  FOR  DIFFERENCES OR
        # ERRORS RAISED FROM SALE'S SYNCHRONIZATION PROCESS PERFORMED AT RUNTIME AFTER SALE ENDING. THE ADUIT FOR CARD
        # MOVEMENT MADE FOR CARD CREDIT PAYMENT WAY MUST COMPARED TO THEIR FISCAL PROPERTIER WHENEVER THERE ARE FISCAL
        # PROPERTIES TO BE COMPUTED JOIN THE CARD REGISTERS ON DATABASE.
        #---------------------------------------------------------------------------------------------------------------\\
        
        sys_sttg:dict = PDVConfig.Read_System_Config()
        keys_in:dict = sys_sttg.get('function_keys')
        
        query_fields:tuple = (
            'crtm.CodigoVenda', 'crtm.Sequencia', 'crtm.CodigoOperadora', 'crtm.CodigoProduto', 
            'opct.Operacao', 'crtm.CV', '$NS_ValorInicial_Venda', 'crtm.ValorLiquido', 'crtm.Valor',
            '$NS_ValorComputado_Venda', 'crtm.Tarifa', '$ValorTaxa', 'opct.TaxaOperacao', '$Operacao',
            '$ValorVenda_Auditado', '$ValorTaxa_Operacao', '$Auditoria_TaxaCartao', '$Resultado')

        query = MyQuery.Query_AUDITORIA_CARTAOMOVIMENTO(
        query_fields, {'sale_code':Central.current_erp_sale_code(),
                       'company':Central.company_internal_code(),
                       'nfce':Central.current_nfce_number(),
                       'card_sequence':sequence,
                       'replace_tax':keys_in.get('OPCOES_RECEBIMENTOCARTAOTAXAACR')})
        
            
        with cls.MySQLconnection.cursor(buffered=True) as cursor:
            cursor.execute(query)
            cls.query_results = cursor.fetchone()
            MySQLConnector.Synchronization(
                'single',
                cursor.rowcount, 
                statIter= int(),
                table='any')
            cursor.close()
        pass
        
        # HTML OUTPUT ::
        create_line(78, cmd='print')
        print('%s[ERP] CARTAOMOVIMENTO + OPERADORACARTAOPROD' %(expand(size=22),))
        create_line(78, cmd='print')
        for i in range(cls.query_results.__len__()):
            n = lambda x, y: int(x) if ope.lt(str(y).__len__(), 2) else int(ope.sub(x, (str(y).__len__() - 1)))
            print("▪[%s] %s%s" %(i, format_space(n(30, i), query_fields[i]), cls.query_results[i]))
        create_line(78, char='=', cmd='print')

        # CONSOLE OUTPUT ::
        MyLog3.debug('%s' %(create_line(78, char='=', break_line=True, cmd='return'),))
        MyLog1.info(f'Date: {cls.today}  :: User Name: {Central.sales_person_name}' + 
                     f'  ->:  Sale Code: {Central.current_erp_sale_code()}')
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        MyLog2.info('%s► CARD MOVEMENT AUDIT' %(expand(size=27),))
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        query_fields = format_fields(
            29, query_fields, 
            to_the_end=':', 
            del_punctuation=True,
            split_text= (True, '.'))
        
        for i in range(cls.query_results.__len__()):
            if(ope.eq(i, 0)): MyLog2.debug(f"{query_fields[i]} {cls.query_results[i]}")
            elif(ope.eq(i, 1)): MyLog1.warning(f"{query_fields[i]} {cls.query_results[i]}")
            elif(i in (6, 7)): MyLog2.critical(f"{query_fields[i]} {cls.query_results[i]}")
            elif(i in (9, 11, 15)): MyLog2.warning(f"{query_fields[i]} {cls.query_results[i]}")
            elif(ope.ge(i, (ope.sub(cls.query_results.__len__(), 2)))): 
                (MyLog2.info(f"{query_fields[i]} {cls.query_results[i]}") 
                 if(ope.ne(cls.query_results[-1], 'NOT MATCH'))
                 else MyLog1.error(f"{query_fields[i]} {cls.query_results[i]}"))
            else: MyLog3.debug(f"{query_fields[i]} {cls.query_results[i]}")
        if(ope.eq(cls.query_results[-1], 'NOT MATCH')):
            MyLog3.debug('%s' %(create_line(78, cmd='return'),))
            MyLog2.error('[AUDIT ERROR]')
            MyLog1.error(
                '\nThe final result has computed for the comparison between Card Tax subtracted' +
                "\nfrom Card Movement Value is not in accordance with the system's calc has" + 
                '\ndone to Card Mov. Audit in this sale event. Check for the database record.')
        else:
            MyLog3.debug('%s' %(create_line(78, cmd='return'),))
            MyLog2.debug(msg= '%s' %(dlmt_space(78, ('TEST CASE STATUS:', '| PASS |')),))
        MyLog3.debug('%s' %(create_line(78, char='=', to_the_end=True, cmd='return'),))
        return


    @classmethod
    def Query_CONTASCORRENTESMOV(cls, origin_code: int):
        with cls.MySQLconnection.cursor(buffered=True) as cursor:
            query = MySQLConnector.MYSQL_Queries(e_cnts_cMov=True)
            cursor.execute(query, (origin_code,))
            cls.query_results = cursor.fetchall()
            count = cursor.rowcount
            print('\n[CONTASCORRENTESMOV]\n\r%s' %(query %(origin_code,)))
            print("'count' lines: %s\n" %count)
            for i in range(len(cls.query_results)):
                print("'self.query_results' in CCR_MOV[%s]: %s" %(i, cls.query_results[i]))

        # CONSOLE OUTPUT ::
        MyLog3.debug('%s' %(create_line(78, char='=', break_line=True, cmd='return'),))
        MyLog1.info(f'Date: {cls.today}  ::  User Code: {Central.sales_person_code}' +
                     f'  ::  User Name: {Central.sales_person_name}')
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        MyLog2.warning('%sCONTASCORRENTESMOV' %(expand(size=28),))
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        format_msg = ('Value:               ', 'Description:         ',
                      'Type Movement:       ', 'Mov. Origin Code:    ')
        for i in range (len(cls.query_results)):
            MyLog2.warning(f"Sequence: {cls.query_results[i][0]}\n")
            for e in range(len(format_msg)):
                if(e < (len(format_msg) - 1)): MyLog3.debug(f"{format_msg[e]} {cls.query_results[i][e + 1]}")
                else: MyLog1.warning(f"{format_msg[e]} {cls.query_results[i][e + 1]}")
            MyLog3.debug('%s' %(create_line(78, cmd='return'),)) if i < 1 and count > 1 else None
        MyLog3.debug('%s' %(create_line(78, char='=', cmd='return'),))
        cursor.close()
        

    
    #-------------------------------------------------------------------------------------------------------------//
    # QUERYING FOR THE SALE EVENT ON TABLE [CAIXAMOVIMENTOS] AS {ControleCaixa} STEP 2 ::
    # THIS METHOD CONTAINS THE SQL QUERY FOR [CAIXAMOVIMENTOS] + [CAIXAMOVIMENTOSFORMAS] + [VENDAS]
    #-------------------------------------------------------------------------------------------------------------\\
    @classmethod
    def MySQL_Query_CAIXAMOVIMENTOS(cls):
        print(f"\n🔎 PERFORMING QUERY TYPE 'SELECT' ON DATABASE {cls.MySQLconnection.database}")    
        print("\n💱 Current Cashier Open Code: %s\nCurrent NFC-e Number: %s\nCurrent ERP Sale Code: %s"
                %(Cashier.cashier_open_code(), Central.current_nfce_number(), Central.current_erp_sale_code())) 
       
        query_fields:tuple = (
            'ca.CodigoAbertura', 'ca.Sequencia', 'cmf.CodigoMovimento', 'ca.CodigoConta', 'v.Codigo', 
            'v.NumeroNF', 'SaldoAnterior', 'ca.ValorPago', 'v.VLR_TROCO_PDV', 
            'cmf.Valor', '$TipoMov', 'cmf.Forma', 'ca.Saldo')
        
        query = MyQuery.Query_CONTROLECAIXA(
            query_fields,
            filters= {'openCode':Cashier.cashier_open_code(),
                'nvenda':Central.current_erp_sale_code(),
                'fiscaldocument':Central.current_nfce_number()})

        with cls.MySQLconnection.cursor(buffered=True) as cursor:
            print(" 🔍 Quering for Cashier Control...")
            cursor.execute(query)
            cls.query_results = cursor.fetchall()
            count = cursor.rowcount
            cursor.close()
    
            # HTML OUTPUT ::
            create_line(78, cmd='print')
            print('%s[ERP] CAIXAMOVIMENTOS + CAIXAMOVIMENTOSFORMAS + VENDAS' %(expand(size=10),))
            create_line(78, cmd='print')
            for i in range(len(cls.query_results[0])):
                n = lambda x, y: int(x) if ope.lt(str(y).__len__(), 2) else int(ope.sub(x, (str(y).__len__() - 1)))
                print("▪[%s] %s%s" %(i, format_space(n(30, i), query_fields[i]), cls.query_results[0][i]))
            create_line(78, char='=', cmd='print')
            
            #\\... SPECIAL CASHIER EVALUATING ::
            if(((ope.eq(cls.query_results, []) is True) and (Cashier.cashiers_event() > 0)) or (count > 1)):
                log.info('\n', also_console=True); log.error('...')
                MyLog3.debug('%s' %(create_line(78, break_line= True, cmd='return'),))
                MyLog1.error(msg='THERE IS AN ERROR IN THE DATABASE FILES ABOUT THE CASHIER AUDIT!')
                MyLog1.error(msg='CHECK THE DATABASE: <%s>!' %cls.MySQLconnection.database)
                MyLog3.debug('%s' %(create_line(78, break_line= True, to_the_end= True, cmd= 'return'),))
                raise errors.DataError() #-> break up the programm execution.
            elif(((ope.eq(cls.query_results, [])) and (ope.eq(Cashier.qnt_sales(), 0)))
                 or ((ope.eq(cls.query_results, [])) and (ope.eq(Cashier.cashiers_event(), 0)))):
                log.info('\n', also_console=True); log.warn('...')
                MyLog3.debug('%s' %(create_line(78, break_line= True, cmd='return'),))
                MyLog1.warning(msg='NO CASHIERS EVENT HAS BEEN CONCLUED YET!')
                MyLog2.info(msg='CHECK THE DATABASE: <%s>!' %cls.MySQLconnection.database)
                MyLog3.debug('%s' %(create_line(78, break_line= True, to_the_end= True, cmd= 'return'),))
                Store_Data_Sale(); return True
            else: pass
        
        # CONSOLE OUTPUT ::
        MyLog3.debug('%s' %(create_line(78, char='=', break_line=True, cmd='return'),))
        MyLog1.info(f'Cashier Code: {Cashier.cashier_code()}   ::   Last Sale Code: {Central.current_erp_sale_code()}'
                    f'   ::   Fsc. Document: {Central.current_nfce_number()}')
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        MyLog1.warning('%s[ERP] CAIXAMOVIMENTOS ▶ CONTROL' %(expand(size=23),))
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        query_fields = format_fields(
            29, query_fields, 
            to_the_end=':', 
            del_punctuation=True)
        
        for i in range (len(cls.query_results[0])):
            if(ope.eq(i, 0)): MyLog2.critical(f"{query_fields[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 1)): MyLog1.warning(f"{query_fields[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 3)): MyLog1.info(f"{query_fields[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 4)): MyLog1.debug(f"{query_fields[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 5)): MyLog2.info(f"{query_fields[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 7)):
                (MyLog2.debug(f"{query_fields[i]} {cls.query_results[0][i]}") 
                 if(ope.eq(cls.query_results[0][i], Central.final_sale_value()))
                 else MyLog2.error(f"{query_fields[i]} {cls.query_results[0][i]}"))
            elif(ope.eq(i, (len(query_fields) - 1))):
                (MyLog2.debug(f"{query_fields[i]} {cls.query_results[0][i]}") 
                 if(ope.eq(cls.query_results[0][i], round(Cashier.total_on_cashier(), 2)))
                 else MyLog2.error(f"{query_fields[i]} {cls.query_results[0][i]}"))
            else: MyLog3.debug(f"{query_fields[i]} {cls.query_results[0][i]}")

        #\\... COMPARISON FOR TOTAL ON CASHIER ::
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        if(ope.eq(cls.query_results[0][i], round(Cashier.total_on_cashier(), 2))):
            MyLog3.debug('LOCAL CASHIER:%s%s' %(expand(size=17), round(Cashier.total_on_cashier(), 2)))
        else: MyLog1.error('LOCAL CASHIER:%s%s' %(expand(size=17), round(Cashier.total_on_cashier(), 2)))
        MyLog3.debug('%s' %(create_line(78, char='=', break_line= True, to_the_end= True, cmd='return'),))
        
        #\\... STORE SALE'S EVENT PROPERTIES ::
        Store_Data_Sale()
        cls.MySQLconnection.close()
        return True
    

    @classmethod
    def Query_Canceling_Sale_Event(cls, given_time: object = None, current_time: object = None):
        with cls.MySQLconnection.cursor(buffered=True) as cursor:
            # Query execution type:  Sale Results
            print(f"PERFORMING QUERY TYPE 'SELECT' ON DATABASE {cls.MySQLconnection.database}")
                      
            query = MySQLConnector.MYSQL_Queries(e_cancel_sale=True)
            print('\n[VENDAS]\r' + (query %Storage.last_sale_code().__getitem__(-1)))
            cursor.execute(query, (Storage.last_sale_code().__getitem__(-1),))
            cls.query_results = cursor.fetchall()
            count = cursor.rowcount; cursor.close()
            current_time = st('%H:%M:%S', lt())
            print("\n@property self.query_results:\n%s\n'rowcount' lines: %s\nitems in results: %s" 
                %(cls.query_results, count, 
                  (len(cls.query_results[0]) if(ope.ne(cls.query_results, [])) else 0)))
            
            # INITIAL CONFERENCE AND DATA VALIDATION OF 'self.query_results' CLASS PROPERTY ::
            if(count > 1):
                log.info('\n', also_console=True); log.error('...')
                MyLog1.critical('%s' %(create_line(78, char='=', break_line=True, cmd='return'),))
                MyLog2.error('\nThe Query Result has returned most of one line!'.upper())
                MyLog1.critical('%s' %(create_line(78, char='=', cmd='return'),))
                raise errors.DataError()
            elif(ope.eq(cls.query_results, [])): 
                print("\n@property: self.query_results is (Empty)!")
                cls.MySQLconnection.close(); return False
            elif(ope.ne(cls.query_results[0][4], 'x')): 
                print("\n@property: self.query_results in (STATUS) is different from 'x' -> CANCELED")
                cls.MySQLconnection.close(); return False
            else: pass
            
        Central.current_sale_status(cls.query_results[0][4], 'set')
        
        # CONSOLE OUTPUT ::
        MyLog1.critical('%s' %(create_line(78, char='=', break_line=True, cmd='return'),))
        MyLog1.info("%s" %(dlmt_space(78, 
                            ("Date: %s" %str(cls.today), 
                             "Time Query Between: %s AND %s" %(str(given_time), current_time)))))
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        MyLog1.critical('%s[ERP] VENDAS' %(expand(size=30),))
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        
        format_msg = (  
            'Sale Code:', 'PDV Sale Code:', 'N.F. Number:', 'Final Value:', 'Status:', 'Canceled ?',
            'Table Price:', 'Client Code:', 'Client Name:', 'Client CPF/CNPJ:', 'Sale Date:', 'Sale Hours:')
        format_msg = format_fields(20, format_msg)
        
        for i in range (len(cls.query_results[0])):
            if(ope.eq(i, 0)): MyLog2.debug(f"{format_msg[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 2)): MyLog2.info(f"{format_msg[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 4)): 
                MyLog1.log(level=40, msg=f"{format_msg[i]} {cls.query_results[0][i]}")
            else: MyLog1.critical(f"{format_msg[i]} {cls.query_results[0][i]}")

        format_results:tuple = (
            cls.query_results[0][0], 
            cls.query_results[0][2], 
            cls.query_results[0][3], 
                (cls.query_results[0][7], 
                 cls.query_results[0][9]))
        
        check = Check_For_Cancelling_ERP(
            results= format_results, 
            sale_status= cls.query_results[0][4], 
            record_status= cls.query_results[0][5])
        
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        (MyLog1.debug('✅ This sale process has been canceled!') if check is True
         else MyLog1.error("❌ This sale process hasn't been canceled!"))
        MyLog1.critical('%s' %(create_line(78, char='=', cmd='return'),))
        MyLog1.critical('%s' %(create_line(78, char='/', cmd='return'),))
        
        if(Central.use_nfce_document() is True):
            check = MySQLConnector.Query_Cancel_Fiscal_Document()

        if(check is True):
            MyLog1.info('%s' %(create_line(78, cmd='return'),))
            MyLog1.debug('%s' %(dlmt_space(78, ('TEST CASE STATUS:', '| PASS |')),))
            MyLog1.critical('%s' %(create_line(78, char='=', cmd='return'),))
        else:
            log.info(msg='\n', also_console=True); log.error(msg='...')
            MyLog1.critical('%s' %(create_line(78, char='=', break_line=True, cmd='return'),))
            MyLog1.error(msg="\nThe Cancelling Sale Process isn't OK!\nCheck for log.html file for more information")
            MyLog1.critical('%s' %(create_line(78, char='=', cmd='return'),))
            
        MySQLConnector.MySQL_Query_CAIXAMOVIMENTOS()
        return True


    @classmethod
    def Query_Cancel_Fiscal_Document(cls):
        with cls.MySQLconnection.cursor(buffered=True) as ndoc_cursor:
            # Query execution type:  Tax Document Results
            print(f"PERFORMING QUERY TYPE 'SELECT' ON DATABASE {cls.MySQLconnection.database}")
                      
            query = MySQLConnector.MYSQL_Queries(e_cancel_tax_docmt=True)
            print('\n[NOTASSAIDAS]\n\r' + (query %(cls.today, Storage.last_sale_code().__getitem__(-1))))
            ndoc_cursor.execute(query, (cls.today, Storage.last_sale_code().__getitem__(-1)))
            cls.query_results = ndoc_cursor.fetchall(); count = ndoc_cursor.rowcount
            print("\n@property self.query_results:\n%s\n'rowcount' lines: %s\nitems in results: %s" 
                  %(cls.query_results, count, 
                    (len(cls.query_results[0]) if(ope.ne(cls.query_results, [])) else 0)))
            
            # INITIAL CONFERENCE AND DATA VALIDATION OF 'self.query_results' CLASS PROPERTY ::
            if(count > 1):
                log.info('\n', also_console=True); log.error('...')
                MyLog1.critical('%s' %(create_line(78, char='=', break_line=True, cmd='return'),))
                MyLog2.error('The Query Result has returned most of one line!'.upper())
                MyLog1.critical('%s' %(create_line(78, char='=', cmd='return'),))
                raise errors.DataError()
            elif(ope.eq(cls.query_results, [])): 
                print("\n@property: self.query_results is (Empty)!")
                cls.MySQLconnection.close(); return False
            elif(cls.query_results[0][13] not in ('Cancelada, cancelada, Cancelado, cancelado')):
                print("\n@property: self.query_results in (Doc. Status) is different of: 'Cancelada'")
                cls.MySQLconnection.close(); return False
            else: pass
                   
        # CONSOLE OUTPUT ::
        MyLog1.critical('%s' %(create_line(78, char='=', cmd='return'),))
        MyLog1.info(
            f'Sales Person Code: {Central.sales_person_code}      ' +
            f'Sales Person Name: {Central.sales_person_name}      ' +
            f'Sales Code: {Central.current_erp_sale_code()}')
        
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        MyLog2.info('%sNOTASSAIDAS' %(expand(size=33),))
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        
        format_msg = (  
            'Sequence ID:', 'Sale Code:', 'Fiscal Doc:', 'Mov. PDV:', 'PDV Seq. Code:', 'Total Value:', 'CSTAT:', 
            'Issued Date:', 'Issue Time:', 'Client Code:', 'Addressee:', 'Addresse CNPJ:', 'Addresse CPF:',
            'Doc. Status:', 'Cancelling Nº:', 'Cancelling Msg:', 'Cancelling Date:', 'PDV Version:')
        
        format_msg = format_fields(20, format_msg)
        for i in range (len(cls.query_results[0])):
            if(ope.eq(i, 1)): MyLog2.debug(f"{format_msg[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 2)): MyLog2.info(f"{format_msg[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 6) or (ope.eq(i, 13))): 
                MyLog1.log(level=40, msg=f"{format_msg[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 14) or (ope.eq(i, 15))):
                MyLog2.warning(f"{format_msg[i]} {cls.query_results[0][i]}")
            else: MyLog1.critical(f"{format_msg[i]} {cls.query_results[0][i]}")
        
        format_results:tuple = (
            cls.query_results[0][1], 
            cls.query_results[0][2], 
            cls.query_results[0][5], 
                (cls.query_results[0][9], 
                cls.query_results[0][11], 
                cls.query_results[0][12]))
        
        check = Check_For_Cancelling_ERP(
            results= format_results, 
            sale_status= cls.query_results[0][6], 
            record_status= cls.query_results[0][13]) 
        
        MyLog1.info('%s' %(create_line(78, cmd='return'),))
        (MyLog1.debug('✅ This Tax Document has been successfully canceled!') if check is True 
         else MyLog1.error("❌ This Tax Document hasn't been successfully canceled!"))
        ndoc_cursor.close()
           
        return check


    @classmethod
    def PSQL_FireBird_VENDAS(cls) -> bool:
        FbConnector.Restore_Connection()
        status = FbConnector.Firebird_Query_VENDAS(
            person_code= Central.sales_person_code,
            person_user= Central.sales_person_name, 
            cancelling= True)
        FbConnector.Close_Connection()
        MySQLConnector.MySQL_Query_CAIXAMOVIMENTOS()
        return True if True in status else False


    @classmethod
    def Query_Cashier_Sangria_Event(cls):
        with cls.MySQLconnection.cursor(buffered=True) as sangria_cursor:
            data_query = (Cashier.cashier_open_code(), Cashier.cashier_code(), Cashier.cashier_name)
            query = MySQLConnector.MYSQL_Queries(e_sangria_event= True)                                        
            sangria_cursor.execute(query, data_query)
            cls.query_results = sangria_cursor.fetchall()
            count = sangria_cursor.rowcount
            print('\n[CAIXAMOVIMENTOS] -> SANGRIA\n\r' + (query %data_query))
            print("\n@property self.query_results:\n%s\n'rowcount' lines: %s" %(cls.query_results, count))
            if(((ope.eq(cls.query_results, []) is True) and (Cashier.qnt_sales() > 0)) or (count > 1)):
                log.info('\n', also_console=True); log.error('...')
                MyLog1.critical('\n------------------------------------------------------------------------------')
                MyLog1.error(msg="THERE IS AN ERROR IN THE DATABASE FILES ABOUT THE CASHIER EVET TYPE: 'Sangria'!")
                MyLog1.error(msg='CHECK THE DATABASE: <%s>!' %cls.MySQLconnection.database)
                MyLog1.critical('------------------------------------------------------------------------------\n')
                raise errors.DataError()
            else: pass

        # CONSOLE OUTPUT ::
        MyLog1.critical('\n==============================================================================')
        MyLog1.info(f'Cashier Code: {Cashier.cashier_code()}   ::   Cashier Open Code: {Cashier.cashier_open_code()}')
        MyLog1.info    ('------------------------------------------------------------------------------')
        MyLog1.warning('                               CAIXAMOVIMENTOS                                ')
        MyLog1.info    ('------------------------------------------------------------------------------')
        format_msg =    ('Sequence:              ', 'Cashier Code:          ', 'Cashier Name:          ', 
                        'Cashier Opn. Code:     ', 'Docmnt. Amount:        ', 'Payment Value:         ',
                        'Cashier Movement:      ', 'Description:           ', 'Movement Type:         ',
                        'Previous Cash. Value:  ', 'Current Csh. Value:    ', 'User:                  ',
                        'Machine Id:            ') 
        
        for i in range (len(cls.query_results[0])):
            if(ope.eq(i, 0)): MyLog1.warning(f"{format_msg[i]} {cls.query_results[0][i]}")
            elif(i in (1, 2)): MyLog2.warning(f"{format_msg[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 3)): MyLog1.info(f"{format_msg[i]} {cls.query_results[0][i]}")
            elif((ope.eq(i, 8)) and (cls.query_results[0][8] in ('Débito','DÉBITO','Debito','debito','DEBITO'))): 
                MyLog2.error(f"{format_msg[i]} {cls.query_results[0][i]}")
            elif(ope.eq(i, 10)):
                (MyLog1.debug(f"{format_msg[i]} {cls.query_results[0][i]}") 
                if(ope.eq(cls.query_results[0][i], round(Cashier.total_on_cashier(), 2)))
                else MyLog1.error(f"{format_msg[i]} {cls.query_results[0][i]}"))
            else: MyLog1.log(level=50, msg=f"{format_msg[i]} {cls.query_results[0][i]}")

        MyLog1.info('------------------------------------------------------------------------------')
        sangria_cursor.close()
        status:bool= Check_For_Sangria_Mov(db_cashier_content= cls.query_results[0][10])
            
        if(status is True):
            print("Everything is OK!")
        else:
            print("There is a problem against data results from database query has perfomed!\n"+
                  "Some data is not match with the automated data proccess expected for the coding structure!")
        return True
    
#\\... END OF LIBRARY ::
