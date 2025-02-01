
#\\... Project Folder's Base Script ::
from Base import os
from Base import Centralizer as Central
from db_resource.EventQueries import MyQuery
from time import strftime as st, localtime as lt

#\\... python modules ::
from math import fabs
import datetime as dt
import operator as ope
import firebirdsql as cnn

#\\... Utilities to the project folder ::
from utilities.TextFormater import *
from utilities.ColorText import log, logger1, logger2, logger4, logger5

FbLog1 = logger4()
FbLog2 = logger5()
Fblog3 = logger1()
fBLog4 = logger2()

class FbConnector(object):
    _instance = None
    _date: dt = dt.date.today()
    # Initial FireBird Connection ::
    _e_host: str= 'localhost'
    _e_db: str= 'C:\Visual Software\MyCommerce\PDV\Offline\PDVOFF.FDB'
    _e_port: int = 3050
    _e_user: str = 'sysdba'
    _e_psswrd: str= 'password'
    _cnn_:dict = {
        'host':_e_host, 
        'port':_e_port, 
        'user':_e_user, 
        'password':_e_psswrd,
        'database':_e_db,
        'charset':'WIN1250'}
    
    # Only Two Possible Connections ::
    _pdv_db_path: str= 'C:\Visual Software\MyCommerce\PDV\Offline\PDVOFF.fdb'
    Central.cur_fbOff = _pdv_db_path
    _config_db_path: str = 'C:\Visual Software\MyCommerce\PDV\ConfigPDV.fdb'
    Central.cur_fbConfig = _config_db_path
    _fb_cnn: cnn.Connection = cnn.connect(**_cnn_)
    query_results = tuple()    

    def __init__(cls) -> None:
        pass

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FbConnector, cls).__new__(cls)
        return cls._instance

    @classmethod
    def e_host(cls, __sttr:str) -> None:
        """It set up the firebird conenction host name"""
        cls._e_host = __sttr
   
    @classmethod
    def e_db(cls, __sttr:str) -> None:
        """It set up the firebird conenction database path"""
        cls._e_db = __sttr
  
    @classmethod
    def e_port(cls, __sttr:int) -> None:
        """It set up the firebird conenction serial port `<type>: int`"""
        cls._e_port = __sttr
   
    @classmethod
    def e_user(cls, __sttr:str) -> None:
        """It set up the firebird conenction user name"""
        cls._e_user = __sttr
   
    @classmethod
    def e_psswrd(cls, __sttr:str) -> None:
        """It set up the firebird conenction user password to"""
        cls._e_psswrd = __sttr

    @classmethod
    def f_cnn(cls) -> dict:
        """Return a mapping of the current FireBird String Connection"""
        cls._cnn_ = {
            'host':cls._e_host, 
            'port':cls._e_port, 
            'user':cls._e_user, 
            'password':cls._e_psswrd,
            'database':cls._e_db,
            'charset':'WIN1250'}

        return cls._cnn_
    

    @classmethod
    def Set_Fbconnection(cls, use_default:bool=True, _custom:dict[str, ] = dict(x='')):
        """
        Turn on `FireBird` connection using a library standard connection arguments
        or  given  your  own connection's string  sequence  to conencting. It raise 
        `firebirdsql.ConenctionError` on failure.
        """
        if(use_default is True):
            FbConnector.e_db(cls._pdv_db_path)
            cls._fb_cnn = cnn.connect(**cls._cnn_)
        else:
            try:
                cls._fb_cnn = cnn.connect(**_custom)
            except: 
                FbLog1.error('\n❌ Connection Failed. Unpossible to establish a FireBird Connection')
                FbLog1.warn('Check for your connection parameters and try again.')
                print('❗ Connection Failed¡')
            else: print('✅ FireBird Connection successfully established!')
        return


    # CONNECTION MODULES :: CONNECTION MANAGER FOR INPUT AND OUTPUT DATA SEQUENCES ...
    @classmethod
    def Get_Current_Connection(cls) -> cnn.Connection: return cls._fb_cnn


    @classmethod
    def Get_Storage_Path(cls) -> str: return cls._e_db


    @classmethod
    def Show_Connection_Status(cls):
        fb_version = cnn.__version__
        Fblog3.debug(msg= str(create_line(59, char='=', break_line=True, cmd='return')))
        FbLog1.debug(msg=f"\r Database connection has successfully established!")
        Fblog3.debug(msg= str(create_line(59, char='=', cmd='return')))
        FbLog1.info(msg="\r%s" %(dlmt_space(59, ('Connection Host:', FbConnector._e_host))))
        Fblog3.debug(msg="\r%s" %(dlmt_space(59, ('Driver Version:', fb_version))))
        fBLog4.info(msg="\r%s" %(dlmt_space(59, ('Database Path:', str(FbConnector._e_db[:12] + '...' + FbConnector._e_db[-10:])))))
        Fblog3.debug(msg=str(create_line(59, char='=', cmd='return')))
        return

    @classmethod
    def Change_Connection(cls, chek_set:bool=True,
        e_host: str= 'localhost',
        e_db: str= 'C:\Visual Software\MyCommerce\PDV\Offline\PDVOFF.FDB',
        e_port: int = 3050,
        e_user: str= 'sysdba',
        e_psswrd: str= 'masterkey') -> cnn.Connection:
        if(chek_set is True):
            e_db = (
                cls._pdv_db_path 
                if ope.eq(e_db, cls._config_db_path) 
                else cls._config_db_path
                   )
        else:
            print("❗ Connection Changing is being done without <bool> 'check_set' security clause")
            
        FbConnector.e_host(e_host)
        FbConnector.e_db(e_db)
        FbConnector.e_port(e_port)
        FbConnector.e_user(e_user)
        FbConnector.e_psswrd(e_psswrd)

        cls._fb_cnn:cnn.Connection = cnn.connect(
            host= cls._e_host, 
            database= cls._e_db,
            user= cls._e_user, 
            password= cls._e_psswrd,
            charset= 'WIN1250')

        print("\n✅❕ FireBird Connection has been successfully changed!" +
              "\n► e_host: %s\n► e_db: %s\n► e_port: %s\n► e_user: %s\n► e_psswrd: %s"
              %(cls._e_host, cls._e_db, cls._e_port, cls._e_user, cls._e_psswrd))
        return cls._fb_cnn
    
    @classmethod
    def Restore_Connection(cls) -> cnn.Connection:
        "Restore FireBird String Conenction to the standard path on localhost `C:/.../`"
        # At the first is necessary to close some open connections...
        connection = dict()
        if(cls._fb_cnn is None):
            FbConnector.e_db(cls._pdv_db_path)
            connection = FbConnector.f_cnn()
        elif((isinstance(cls._fb_cnn, cnn.Connection)) and (cls._fb_cnn.is_disconnect() is not True)): 
            cls._fb_cnn.close()
            FbConnector.e_db(cls._pdv_db_path)
            connection = FbConnector.f_cnn()
        
        cls._fb_cnn = cnn.connect(**connection)
        print("\n↻ FireBird Connection has successfully restored! ✅")
        for _key in connection.keys(): print("🔑[%s]: %s" %(_key, connection.get(_key)))
        return cls._fb_cnn
    
    @classmethod
    def Close_Connection(cls):
        if((cls._fb_cnn is not None) and (cls._fb_cnn.is_disconnect() is False)): cls._fb_cnn.close(); return

    #------------------------------------------------------------------------------------------------------------//
    # EXTERNAL USABILITY. IT CAN BE USED FOR ANOTHER EXTERNAL MODULES FROM DISTINCT CLASSES...
    # THIS FUNCTION HAS BEEN CREATED TO USE THIS FUNCTION WITHOUT TO WRITE THE SAME CODE AGAIN!
    #------------------------------------------------------------------------------------------------------------\\
    @classmethod
    def Execute_Query_Function(cls,
            query_text:str, 
            table_name:str,
            query_format:tuple = ()) -> tuple:

        # Check for connection satus...
        print("◉ FireBird Connetion on use: %s" %(FbConnector.Get_Storage_Path(),))
        # Execute SELECT QUERY...
        this_resutls:tuple = ()
        data_query:str= query_text.format(query_format) if(ope.ne(query_format, ())) else query_text
        print('\n[%s]\r' %(table_name.upper()) + data_query)
        cursor = cls._fb_cnn.cursor(); cursor.execute(data_query); this_resutls = cursor.fetchone()
        count = cursor.rowcount; count = int(fabs(count)); cursor.close()
        print("\nFireBirdCornnector @property\n◽ Rowcount: %s\nItems in 'results': %s" 
            %(count, (this_resutls.__len__() if(this_resutls is not None) else int())))
        return this_resutls
    

    @classmethod
    def Syncronization(cls, __type:str, /, event:str= 'C | F', iterable:int=int()) -> None:
        """
        DOCUMENTATION: ``FireBirdConnector``

        Check up for the sale's synchronization attributes used to set up a sale's processing step
        on database records.
        """
        print("\nChecking for event type '%s'" %event.upper())
        #\\... CHECK FOR QUERY RESULT'S CONTENT ::
        if((cls.query_results is None) or ope.eq(cls.query_results, ())):
            log.info('', also_console=True); log.error('...')
            Fblog3.debug('%s' %(create_line(78, break_line=True, cmd='return'),))
            Fblog3.error('%s' %(dlmt_space(78, ('❌ [QueryError]:', '|')),))
            FbLog1.error('%s'
                %(dlmt_space(78, 
                ('► The Query Result has returned an empty object sequence!'.upper(), '|')),))
            Fblog3.debug('%s' %(create_line(78, cmd='return'),))
            print("@property: cls.query_results is empty or None: %s" %(cls.query_results,))
            print("❌[DatabaseError]: FireBirdConnector @property: cls.query_results is None or it's empty!")
            cls._fb_cnn.close(); raise cnn.DatabaseError(message="Empty Fields")
        
        #\\... CHECK FOR THE SALE'S SYNCHRONIZATION KEY ::
        elif((ope.ne(cls.query_results[iterable], 'F')) and (ope.eq(event.upper(), 'F'))):
            log.info('', also_console=True); log.error('...')
            Fblog3.debug('%s' %(create_line(78, break_line=True, cmd='return'),))
            Fblog3.error('%s' %(dlmt_space(78, ('❌ [DataError]:', '|')),))
            FbLog1.error('%s'
                %(dlmt_space(78, 
                ("► THE QUERY RESULTS IN `Status` TABLE FIELD IS DIFFERENT FROM 'F'!", '|')),))
            Fblog3.debug('%s' %(create_line(78, cmd='return'),))
            print("FireBirdConnector @property: cls.query_results in (STATUS) is different from 'F'.")
            print("❌ [DataError] for sale's finishing!")
            cls._fb_cnn.close(); raise cnn.DataError(message='Data Incongruency')

        #\\... CHECK FOR THE QUERY RESULT'S CONTENT TO THE SALE'S CANCELLING EVENT::
        elif((ope.ne(cls.query_results[iterable], 'C')) and (ope.eq(event.upper(), 'C'))):
            log.info('', also_console=True); log.error('...')
            Fblog3.debug('%s' %(create_line(78, break_line=True, cmd='return'),))
            Fblog3.error('%s' %(dlmt_space(78, ('❌ [DataError]:', '|')),))
            FbLog1.error('%s'
                %(dlmt_space(78, 
                ("► THE QUERY RESULTS IN `Status` TABLE FIELD IS DIFFERENT FROM 'C'!", '|')),))
            Fblog3.debug('%s' %(create_line(78, cmd='return'),))
            print("FireBirdConnector @property: cls.query_results in (STATUS) is different from 'C'.")
            print("❌ [DataError] for sale's cancelling!")
            cls._fb_cnn.close(); raise cnn.DataError(message='Data Incongruency')
        #\\... to be continued::
        else: pass
        return
    

    @classmethod
    def Firebird_Query_VENDAS(cls, 
            person_code:int,       
            person_user:str, 
            cancelling:bool=False) -> tuple:
        
        # Query execution type: Sale Results
        FbLog1.info("\nChecking for FireBird Localhost... 🔍")
        query_fields:tuple = (
            '$CODVENDA_ERP', 'v.SEQUENCIA', 'v.TOTALCUPOM', 'v.TOTAL_DESCONTOS', 
            'v.TOTAL_ACRESCIMO', 'v.VLR_TROCO', 'v.STATUS', 'v.PROCESSADO',
            'v.TABELA', 'v.CODIGOCLIENTE', '$DEST_NOME', '$CPF_CNPJ', 'v.SERIALECF',
            'v.NCUPOM', '$CSTAT', '$NAUTORIZACAO', 'v."DATA"', 'v.HORA')
        
        query = MyQuery.Fb_Query_VENDAS(query_fields, 
                                      {'personcode':person_code,
                                       'personuser':person_user})

        cursor = cls._fb_cnn.cursor(); cursor.execute(query)
        cls.query_results = cursor.fetchone()
        cls.query_results = tuple() if cls.query_results is None else cls.query_results
        count = cursor.rowcount; count = int(fabs(count))
        current_time = st('%H:%M:%S', lt())
        
        # INITIAL CONFERENCE AND DATA COMPARISON OF 'cls.query_results' CLASS PROPERTY ::
        FbConnector.Syncronization('', event= ('F' if(cancelling is False) else 'C'), iterable= 6)
        print("\nFireBirdConnector @property\n◽ Rowcount lines: %s" %count
            + "\n◽ Items in results: %s\n◽ cls.query_results: ↴" %cls.query_results.__len__())
        
        # CONSOLE AND HTML OUTPUT PROCESS ::
        create_line(78, cmd='print')
        print('%s[PDVOFF] VENDAS' %(expand(size= 28),))
        create_line(78, cmd='print')
        for i in range(cls.query_results.__len__()):
            n = lambda x, y: int(x) if ope.lt(str(y).__len__(), 2) else int(ope.sub(x, (str(y).__len__() - 1)))
            print("▪[%s] %s%s" %(i, format_space(n(30, i), query_fields[i]), cls.query_results[i]))
        create_line(78, char='=', cmd='print')

        query_fields = format_fields(
            27, query_fields, 
            to_the_end= ':', 
            del_punctuation= True, 
            split_text=(True, '.'))
        
        Fblog3.debug('%s' %(create_line(78, char='=', break_line=True, cmd='return'),))
        FbLog2.log(level=50, msg='%s[Firebird] VENDAS' %(expand(size=29),))
        FbLog1.info('%s' %(create_line(78, cmd='return'),))
        
        # SHOW TABLE ::
        for i in range (cls.query_results.__len__()):
            _field = query_fields[i]
            if(ope.eq(i, 0)): 
                (FbLog2.warn(f"{_field} {cls.query_results[i]}") if(cancelling is True)
                else (FbLog1.debug(f"{_field} {cls.query_results[i]}")))
            elif(ope.eq(i, 1)): FbLog2.log(level=50, msg=f"{_field} {cls.query_results[i]}")
            elif(ope.eq(i, 13)): FbLog2.info(f"{_field} {cls.query_results[i]}")
            elif(ope.eq(i, 5)): 
                ( Fblog3.error(f"{_field} {cls.query_results[i]}") if(cancelling is True)
                else Fblog3.debug(f"{_field} {cls.query_results[i]}"))
            else: Fblog3.debug(f"{_field} {cls.query_results[i]}")
        FbLog1.info('%s' %(create_line(78, cmd='return'),))
        Fblog3.info('This sale process has been successffully recorded!'.upper())
        Fblog3.debug('%s' %(create_line(78, char='=', cmd='return'),))

        if(cancelling is True):
            Central.current_sale_status('Uncompleted', 'set')
            return (True, )
        return cls.query_results #if cls.query_results is not None else tuple()

    @classmethod
    def Firebird_Query_CX_MOVIMENTOS(cls): pass

    async def run() -> None: return

#\\... END OF LIBRARY ::
