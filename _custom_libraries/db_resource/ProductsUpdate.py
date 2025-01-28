
import datetime as dt
import operator as ope
import mysql.connector as cnx

from input.ConfigLoader import PratesConfig
from Base import Centralizer as Central, ExternalFile

from utilities.TextFormater import *
from utilities.KeyGenerator import *
from random import randint, randrange
from utilities.ColorText import log, logger6
from time import strftime as st, localtime as lt

PdLog = logger6()

PROMOTION_DEBUG:bool = False

class ProductUpdate:
    MySQLconnection: cnx.MySQLConnection = None #type: ignore
    query_results: object = None
    products: dict = {} 
    p_controllers: dict = {}

    def __init__(cls) -> None:
        pass

    @classmethod
    def Set_MySQL_Connection(cls, cnn:cnx.MySQLConnection) -> cnx.MySQLConnection:
        """Create an explicit connection mapping to the @property: `MySQLConnection`"""
        cls.MySQLconnection = cnn; return

    @classmethod
    def Create_Products_Mapping(cls) -> None:
        #\\... LOADING PROJECT SETTINGS ::
        auto_update:bool = bool(PratesConfig.reader().get('auto_update_of_data'))
        custom_sequence:list = PratesConfig.reader().get('sequence_of_products')
        new_data:bool = bool(PratesConfig.reader().get('set_new_data')) 
        get_from_db:bool = bool(PratesConfig.reader().get('get_data_from_db'))
        use_pdv_price:bool = bool(PratesConfig.reader().get('use_pdv_price'))
        table_price:int = PratesConfig.reader().get('pricing_list_code_id')
        auto_promo:bool = bool(PratesConfig.reader().get('promotional_checking'))
        delimiter:int = PratesConfig.reader().get('limit_for_prod')
        randomize:bool = bool(PratesConfig.reader().get('randomize_choice'))
        print("""\n🔵 Project Settings:
        ◽ auto_update: %s
        ◽ custom_sequence: %s
        ◽ new_data: %s
        ◽ get_from_db: %s
        ◽ use_pdv_price: %s
        ◽ table_price: %s
        ◽ auto_promo: %s
        ◽ delimiter: %s
        ◽ randomize: %s"""%(
            auto_update, 
            custom_sequence, 
            new_data, 
            get_from_db,
            use_pdv_price,
            table_price,
            auto_promo, 
            delimiter, 
            randomize))

        cls.products = dict(
            K1=dict(code_id=615, bar_code='2047100006158', reference='REFERENCE', descrpt='SKOL PURO MALTE LATA 473ML UNID', price_T1=4.45, offer=0, promotion=0, varejo=0.0, otherTable=0, is_grid=True),
            K2=dict(code_id=1060, bar_code='124630', reference='2009582', descrpt='REFRIGERANTE BRASUC', price_T1=3.06, offer=0, promotion=0, varejo=3.95, otherTable=0, is_grid=False))


        # WHEN THE "PRATES" PROJECT IS RUNNING ON THE scanntech DATABASE, IT IS NOT NECESSARY TO DO ANYTHING
        # MORE THAN DOWNLOADING THE DATA. BUT THIS RESOURCE IS VALID ONLY FOR SCANNTECH DATABASE!
        if((auto_update is True) and (get_from_db is False) and (new_data is False)):
            print('\n\nDownloading Product Records...')
            ProductUpdate.Update_Product_Mapping(update= True, tblPrc_id= table_price)
            PdLog.info(msg="\n✅ Products's inner dataschema has bben updated!")
        

        # WETHER THE TESTER WISH TO USE A SPECIFIC SEQUENCE OF PRODUCTS FROM DATABASE, THEY MAY USE THIS 
        # STATEMENT AS AN OPTION TO DO SO. THIS STATEMENT DOES MOST OF THE WORK ALREADY DURING THE 
        # DATABASE QUERY. THEREFORE, IT IS NOT NECESSARY TO REPEAT THE DOWLOAD OF THE PRODUCT PROPERTIES 
        # IN THE 'Update_Local_Storage_Of_Products' FUNCTION. EXCEPT, OF COURSE, THE OFFERS AVAILABLE!
        elif((get_from_db is True) and (new_data is False)):
            cls.products.clear()
            print('\nQUERYING DATABASE...'.upper())
            create_line(20, break_line=True, to_the_end=True, cmd='print')
            records = ProductUpdate.Search_Products(delimiter, randomize, auto_promo)
            print('\n\n\n📝 TRANSFORMING INTERNAL DICTIONARY OF DATA...')
            print('-----------------------------------------------')  
            for i in range(len(records)):
                new = dict(
                    code_id=records[i][0],
                    bar_code=records[i][1], 
                    reference=records[i][2], 
                    descrpt=records[i][3],
                    price_T1=records[i][4],
                    offer=float(0),
                    promotion=float(0),
                    varejo=float(0),
                    otherTable=float(0),
                    is_grid=(True if(records[i][-1]) is not None else False))             
                
                dict_id = create_number_key()
                cls.products.update([(dict_id, new)])
                print("'index_id': %s\n@property cls.products in {%s}: %s\n" %(dict_id, dict_id, cls.products[dict_id]))              
            PdLog.info(msg="\n✅ Product's dataschema has been loaded!")
            ProductUpdate.Update_Product_Mapping(False, table_price, use_pdv_price)
            pass

        # WHEN THE "PRATES" PROJECT IS RUNNING IN ANOTHER DATABASE, IT IS NECESSARY TO VERIFY THE DATA BEFORE
        # DOWNLOADING IT TO THE INTERNAL STRUCTURE. PAY ATTENTION! THIS METHOD CONFIGURATION WILL DOWNLOAD ALL 
        # PRODUCTS  FROM [custom string] REGARDLESS OF YOUR  DATABASE  REGISTRATION  STATUS. TO MAKE AN IDEAL 
        # SEQUENCE OF DOWNLOADING PRODUCTS AND THEIR PROPERTIES, USE THE PREVIOUS SETTINGS.
        elif((new_data is True) and (get_from_db is False) and (ope.ne(custom_sequence, []))):
            cls.products.clear()
            print('\ncustom_sequence <list>: %s' %custom_sequence)
            print('\n📥 Downloading Custom Sequence of Products...'.upper())
            print('\n💬 REMOVING DUPLICATES FROM custom_sequence <list> WHETER EXISTS...')
            replace_list = [*set(custom_sequence)]
            custom_sequence.clear(); custom_sequence = replace_list
            create_line(52, break_line=True, to_the_end=True, cmd='print')
            for i in range(len(custom_sequence)):
                new = dict(
                    code_id=custom_sequence[i], 
                    bar_code='some', 
                    reference='any', 
                    descrpt='something', 
                    price_T1=0, 
                    offer=0, 
                    promotion=0, 
                    varejo=0, 
                    otherTable=0, 
                    is_grid=False)
                dict_id = create_number_key()
                cls.products.update([(dict_id, new)])
                print("'index_id': %s\n'cls.products' in {%s}: %s" %(dict_id, dict_id, cls.products[dict_id]))
            PdLog.info(
                msg="\n✅ Custom product's dataschema has been loaded!")
            ProductUpdate.Update_Product_Mapping(True, table_price, use_pdv_price)
            pass

        # INTERNAL SECURITY CLAUSE ::
        elif((ope.eq(custom_sequence, []) or (custom_sequence is None) and (new_data is True))):
            log.info('\n', also_console=True)
            log.error('\n...')
            PdLog.error(f"\nThe '<list>custom_sequence' variables cannot be EMPTY or NONE!\n".upper())
            raise ValueError()

        # Check for avaliable promotions...
        ProductUpdate.Apply_Promotions_When_Existly()
        Central.products(cls.products, 'set')
        # GET OUT DATA SEQUENCE....
        # Save these data sequence into of <Database_Content.yaml> file
        ProductUpdate.Save_Products_Data_Sequence()    
        ProductUpdate.Save_Products_Data_Sequence(is_promotion=True)    
        return

#=======================================================================================================================================
    # THIS IS A INTERNAL '@classmethod' OF THE PRODUCT DICTIONARY MANAGER. ITS FUNCTION IS TO UPDATE THE PRODUCT 
    # DICTIONARY WITH THE  NEW VALUES AVAILABLE  IN THE  DATABASE  WHERE THESE DATA ARE DIFFERENT FROM THEMSELVES
    # AND ARE STORED IN THE DICTIONARY. ON THE OTHER HAND, IF THERE ARE PROPERTIES OF PRODUCTS THAT HAVE ALREADY 
    # BEEN UPDATED BY ANOTHER CLAUSE OR METHOD OF OUR CODE, THIS PROCESS IS IGNORED TO ECONOMIZE DATA TREATMENT.

    @classmethod
    def Update_Product_Mapping(cls, 
            update: bool = False, 
            tblPrc_id: int = 0, 
            pdv_price: bool = True):
        
        print('\n\n\n📊 UPDATING TABLE PRICES, OFFERS VALUE AND GRID CODE OF THE PRODUCTS...')
        create_line(80, break_line=True, to_the_end=True, cmd='print')

        for e in cls.products.keys():
            elem = cls.products.get(str(e))
            print(f"\ndebug of 'elem' as `{e}` before updating: {elem}")
            elem_keys = list(elem); print(f"debug for elem_keys: {elem_keys}")
            
            #\\... MAIN PRODUCT PROPERTIES ::
            pro_proprt = (
                ProductUpdate.Product_Properties(
                    product_code= elem['code_id'], price_pdv= pdv_price) if update is True else None)   
            #\\... PRICING TABLE IF EXISTS ::
            table_price = (
                ProductUpdate.Product_Pricing_Table(tblPrc_id, elem['code_id']) if tblPrc_id != 0 else None)       
            #\\... PRODUCT OFFER IF EXISTS ::
            offer_data = ProductUpdate.Product_Offer(prod_code= elem['code_id'])
            
            # REPLACE DATA AND PRINT THE PROCESS IN THE OUTPUT FILE log.html ::
            print("\n*Main data of the product code [%s]: %s\n" %(elem[str(elem_keys[0])], pro_proprt))
            if(pro_proprt is not None):
                for ee in range(len(pro_proprt)):
                    if(ope.ne(elem[str(elem_keys[ee])], pro_proprt[ee])):
                        elem[str(elem_keys[ee])] = pro_proprt[ee]
                        if(ope.ne(elem_keys[ee], 'offer')):
                            print("%s =>: %s" %(elem_keys[ee], elem[str(elem_keys[ee])]))
                    else: print('%s is OK => [%s]' %(elem_keys[ee], pro_proprt[ee]))
                print("\n**UPDATING elem['is_grid'] DATA...")
                elem['is_grid'] = True if (pro_proprt[5] is not None) else False; print(f"-> {elem['is_grid']}")
            else: print("*UPDATING elem['is_grid'] DATA...\n-> %s" %elem['is_grid'])

            #\\... ELEM UPDATING AND log.html OUTPUT ::
            print("*UPDATING elem['varejo'] DATA...")
            elem['varejo'] = table_price[1] if table_price is not None else int()
            print(f"-> {elem['varejo']}")
            print("*UPDATING elem['offer'] DATA...")
            elem['offer'] = offer_data
            print(f"-> {elem['offer']}")
            print(f"debug of 'elem' after updating: {cls.products[str(e)]}")
            if(elem['offer'] is not None): 
                ProductUpdate.Create_Offer_Controll(elem['code_id'], offer_data)
            create_line(250, '_', cmd='print')
        return

#=======================================================================================================================================
    # THE 'Apply Offers When Existing' IS A FUNCTION THAT MANAGES THE PRODUCT OFFERS ACCORDING TO THE SETTINGS
    # APPLIED FOR EACH PARAMETER AVAILABLE IN THE  PROMOTION CONDITIONS. 

    # IN ADDITION, 'Apply promotion when existing' VERIFIES THE OFFER SETTINGS ENTERED IN THE DATABASE. THESE
    # SETTINGS  ARE RESPONSIBLE  FOR  CONTROLLING  HOW PROMOTIONS ARE APPLIED AND WHEN THEY CAN BE APPLIED.
    # THE 'self.prod_on_promotion_controller' CLASS  PROPERTY CALLED BELOW FOR THE CONDITIONAL STATEMENT, STORE 
    # THE PROMOTION SETTINGS FOR EVERY PRODUCT WITH AN OFFER AVAILABLE IN YOUR RECORD. THESE CONFIGURATIONS 
    # ARE CONSULTED DURING  THE  LAUNCH OF THIS PRODUCT FOR SALE, WHEN THE PRICE OF THIS PRODUCT IS APPLIED 
    # IN THE SALES TAX DOCUMENT.
    
    @classmethod
    def Apply_Promotions_When_Existly(cls):
        print('\n\n\n\n\n\n\n\n\n\n\n\n💡 CREATING PRODUCTS LIST TO UPDATE PROMOTIONS...')
        create_line(49, break_line=True, to_the_end=True, cmd='print')
        
        products_for_update = list()
        for e in cls.products.keys():
            elem = cls.products.get(str(e)); 
            products_for_update.append(elem['code_id'])

        print(f"debug of 'updated_products': {products_for_update}")
        print('\n\n🔖💲 UPDATING PRODUCT PROMOTIONS...')
        create_line(37, break_line=True, to_the_end=True, cmd='print')
        
        temp_keys = list(cls.products.copy())
        for i in range(len(products_for_update)):
            keys = dict(cls.products.get(str(temp_keys[i])))
            print(f"\ndebug of 'keys': {keys}\ndebug of 'keys_values': {keys.values()}")
            promotion_data = (
                ProductUpdate.Product_Promotion(
                    prod_code=products_for_update[i], 
                    info=PROMOTION_DEBUG))
            print(f"debug of 'promotion_data' value: {promotion_data}")
            if(promotion_data is not None):
                print('\n✅ THIS PRODUCT IS ON PROMOTION!')
                keys.update([('promotion',  promotion_data[0])])
                _controllers = promotion_data[1]
                print(f"- debug of '_controllers': {_controllers}")
                print("- debug of promotion value in <var> keys: %s" %(keys['promotion'],))
                ProductUpdate.Create_Promotion_Control(
                    _controllers[0],    # -> Product Code
                    _controllers[1],    # -> Promotion Code
                    _controllers[2],    # -> Minimmum Quantity
                    _controllers[3],    # -> Maximmum Quantity 
                    _controllers[4],    # -> Limited by CPf Serial Code ?
                    _controllers[5],    # -> Repeat on Sale
                    _controllers[6])    # -> Maximmum Quantity For Sale
            else: keys['promotion'] = 0
            cls.products.update([(str(temp_keys[i]), keys)])
            print(f" ProductUpdate @property: cls.products in '{temp_keys[i]}':" 
                  + f"\n🛒 {cls.products[str(temp_keys[i])]}")
            create_line(250, '_', cmd='print')   
        return

#=======================================================================================================================================

    # 'Create The Promotion Control' IS REQUIRED FOR APPLY THE PRODUCT PROMOTION ACCORDING TO THE SEETINGS HAS WRITHEN
    # FOR IT. THE PROMOTION WILL BE APPLYED ONLY IF THIS PRODUCT IS NOT RELEASED MORE THAN ALLOWED FOR CURRENT SALE.
    # PERFORM THE ORIGIN OF THIS CONTROL IS RESPONSIBILITY OF THIS PYTHON FUNCTION! A COPY OF  ALL DICTIONARIES
    # OF THE PRODUCTS ON PROMOTION IS STORAGE IN THE Class: Manager.py IN 'self.store_prod_on_promotion: dict'

    @classmethod
    def Create_Offer_Controll(cls,
            prod_code: int, 
            cntrls: tuple) -> None:
        
        print('\n🔧💰 CREATING OFFER CONTROLLER ON <class>: Centralizer.py')
        value: float = cntrls[0]
        minimun: int = cntrls[1]
        Central.prod_on_offer_controller(
            [(str(prod_code), 
                {'price':value, 
                 'minimum':minimun, 
                 'counter':int(0)})], 'set')
        
        Central.offer_controllers_storage(Central.prod_on_offer_controller(), 'set')
        #\\... Print items from promotion's controller ::
        create_line(120, break_line=True, cmd='print')
        print('🗝 Central.prod_on_promotion_controller.keys(): %s' %(Central.prod_on_offer_controller().keys(),))
        for _key in Central.prod_on_offer_controller().keys():
            print("   🔑[%s]: %s"
            %(_key, Central.prod_on_offer_controller(gt_log=True).__getitem__(_key)))
        #\\... Same here ::
        create_line(120, cmd='print')
        print('🗝 Central.prod_on_promotion_controller.keys(): %s' %(Central.offer_controllers_storage().keys(),))
        print(Central.offer_controllers_storage().keys())
        for _key in Central.offer_controllers_storage().keys():
             print("   💾📂[%s]: %s" %(_key, Central.offer_controllers_storage().__getitem__(_key)))
        return

    # =-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=||
    @classmethod
    def Create_Promotion_Control(cls,
            prd_prom_code: int, 
            _prom_code: int, 
            _min: int, 
            _max: int, 
            cpf: bool, 
            repeat:int, 
            promo_max:int) -> None:
        
        print('\n🔧📊 CREATING PROMOTION CONTROLLER ON <class>: Centralizer.py')
        Central.prod_on_promotion_controller(
            [(str(prd_prom_code), 
                {'prom_code':_prom_code,
                 'min':_min, 'max':_max,
                 'cpf':cpf,
                 'repeat':repeat,
                 'max_promo':promo_max,
                 'counter':0})], 'set')

        Central.promotion_controller_storage(Central.prod_on_promotion_controller(), 'set')
        #\\... Print items from promotion's controller ::
        create_line(135, break_line=True, cmd='print')
        print('🗝 Central.prod_on_promotion_controller.keys(): %s' %(Central.prod_on_promotion_controller().keys(),))
        for _key in Central.prod_on_promotion_controller().keys():
             print("   🔑[%s]: %s" %(_key, Central.prod_on_promotion_controller().__getitem__(_key)))
        #\\... Same here ::
        create_line(135, cmd='print')
        print('🗝 Central.promotion_controller_storage.keys(): %s' %(Central.promotion_controller_storage().keys(),))
        print("Last Promotion Controller recorder: %s" %(Central.promotion_controller_storage(gt_log=True),))
        print("\n📥 All of controllers on storage:")
        for _key in Central.promotion_controller_storage().keys():
             print("   💾📂[%s]: %s" %(_key, Central.promotion_controller_storage().__getitem__(_key)))
        create_line(135, break_line=True, to_the_end=True, cmd='print')
        return

#=======================================================================================================================================
    @classmethod
    def Search_Products(cls, delimiter:int, randomize:bool= False, prom_auto:bool= False) -> list:        
        with cls.MySQLconnection.cursor() as cursor:
            count: int = 0
            if(randomize):
                cls.query_results = ProductUpdate.Get_From_Database_Range(limit= delimiter)
                print('\n@property self.query_results: %s' %(cls.query_results,))
                count = len(cls.query_results)         
            else:
                queryB = """
                SELECT
                    Codigo, 
                    CodigoBarras,  
                    Referencia, 
                    Descricao, 
                    if(({a} = 1), VendaPDV, VendaT1) as Preco,
                    CodigoGrade
                    FROM produtos AS p
                WHERE COALESCE(p.CodigoBarras, NULL, '') <> ''
                    AND (p.VendaPDV IS NOT NULL AND p.VendaPDV > 0)
                    AND p.NCM IS NOT NULL
                    AND p.NComercializavel <> 1
                    AND CodigoVasilhame IS NULL
                    AND STATUS = 'n'
                    AND Ativo <> 0
                    AND Cancelado IS NULL
                ORDER BY Codigo DESC LIMIT {b}""".format_map(
                    {'a':(1 if Central.prates_current_settings().get('use_pdv_price') is True else 0), 'b':delimiter})
                
                cursor.execute(queryB)
                cls.query_results = list(cursor.fetchall())
                count = cursor.rowcount; cursor.close()
                print('\n@property self.query_results: %s' %(cls.query_results,))
                
        print(f"\n🔍 HAS BBEN FOUND {count} RECORDS FROM <{cls.MySQLconnection.database}> DATABASE:")
        print(f"rows count: {count}\n")

        # IT'S NECESSARY TO ADD THE DEFAULT PRODUCT CODE IN THE PRODUCTS SEQUENCE ::
        default_prod = ProductUpdate.Product_Properties(prod_code= Central.standard_product_code())
        
        if((default_prod is not None) and (default_prod not in cls.query_results)):
            list(cls.query_results).append(default_prod)
            print('\nDEFAULT PRODUCT:%s' %(create_line(17, break_line=True, cmd='return')))
            print("📝 The sequence: %s has been added in the @propert self.query_results" %(default_prod,))
        else:
            print("\n❌ Default Product has not been found in the database <%s>." %cls.MySQLconnection.database)

        if((isinstance(cls.query_results, list)) and (ope.ne(cls.query_results, []))):
            for i in range(len(cls.query_results)): print('[%s]: %s' %(i, cls.query_results[i]))
        else: 
            print("\n❓ UNPOSSIBLE TO FIND PRODUCTS RECORD ON [%s] DATABASE!" %cls.MySQLconnection.database)
            print('(InternalError): %s' %(cls.query_results,))
            raise Exception()

        # WHENEVER THIS VARIABLE IS `True`,APPEND AUTOMATICALLY PROMOTIONAL ITENS TO THE LIST OF PRODUCT 
        # TO LOADING ON DATA LIBRARY AT BUIDING ::
        if(prom_auto is True):
            prod_prpt = tuple(); products = list()
            for p in ProductUpdate.Find_Promotion_Automatically():products.append(p)
            for o in ProductUpdate.Find_Offers_Automatically(): products.append(o)
            products = [*set(products)]
            
            if(products is not None):
                for i in range(len(products)):
                    print("\n🔍 Looking for product code: %s" %(products[i],))
                    print("... Append to @property cls.query_results data sequence type mapping/dictionary.")
                    prod_prpt = ProductUpdate.Product_Properties(prod_code= products[i])
                    if((prod_prpt is not None) and (prod_prpt not in cls.query_results)):
                        cls.query_results.append(prod_prpt)
                        print("📝✔ The sequence: %s has been added in the @propert cls.query_results" %(products[i],))
                    else:
                        print("\n❌ The Product Code informed as agument has not been found in the database <%s>."
                        %(cls.MySQLconnection.database))
            else: 
                print("\n❗ Has not been found Promotional or Offering items in the Database [%s]" %cls.MySQLconnection.database)
                print("\n-> Check for Connection Status or another possible issues and try again!" +
                      "\n❕ You also can check if the product's range for automatic promotional looking" +
                      "\nfor isn't empy ot null. That data sequence requiere at least one element")
        return cls.query_results

#=======================================================================================================================================
    @classmethod
    def Get_From_Database_Range(cls, limit:int) -> list:
        queryA = "SELECT Codigo FROM produtos as p ORDER BY codigo LIMIT 1"
        queryB = "SELECT Codigo FROM produtos as p ORDER BY codigo DESC LIMIT 1"
        range_start: object = None; range_end: object = None

        print('💡 GETTING FOR DATABASE LENGTH...')
        print('---------------------------------')
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
        def Execute(prod_code:int) -> tuple | None:
            result: object = None
            queryA = """
            SELECT
                Codigo, 
                CodigoBarras,  
                Referencia, 
                Descricao, 
                if(({a} = 1), VendaPDV, VendaT1) as Preco, 
                CodigoGrade
                FROM produtos AS p
            WHERE p.CodigoBarras IS NOT NULL
                AND (p.VendaPDV IS NOT NULL AND p.VendaPDV > 0)
                AND p.NCM IS NOT NULL
                AND p.NComercializavel <> 1
                AND CodigoVasilhame IS NULL
                AND STATUS = 'n'
                AND Ativo <> 0
                AND Cancelado IS NULL
                AND Codigo = {b}""".format_map(
                    {'a':(1 if Central.prates_current_settings().get('use_pdv_price') is True else 0), 'b':prod_code})
            
            with cls.MySQLconnection.cursor() as this_cursor:
                this_cursor.execute(queryA)
                result = this_cursor.fetchone()
                this_cursor.close()
            return result

        # Internal process of Product Selection according the query results from Execute() method...
        print('\n🔍 SEARCHING PRODUCTS FROM DATABASE...')
        create_line(39, break_line=True, to_the_end=True, cmd='print')
        range_list = list(); int_num: int = 0; results = list()
        
        while(len(range_list) < limit):
            int_num = randrange(range_start[0], range_end[0])
            if(ope.eq(range_list, []) or (int_num not in range_list)):
                x = Execute(prod_code= int_num)
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
                        x = Execute(prod_code= int_num) #print('x: %s' %(x,))
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
    def Product_Properties(cls, prod_code: int, pdv_price: bool = True):
        
        # -> This temporary inner element ``temp_internal_elem``
        # serves as such a way that we don't change the @property
        # self.query_results in usage at runtime but return
        # the value of 'temp_internal_elem' instead.

        results:object = None
        type_price = 'VendaPDV' if pdv_price is True else 'VendaT1'
        query = """                                              
        SELECT 
            p.Codigo, 
            p.CodigoBarras, 
            p.Referencia,
            p.Descricao, 
            p.{}, 
            p.CodigoGrade
            FROM produtos AS p 
        WHERE codigo = {}""".format(type_price, prod_code)
        
        with cls.MySQLconnection.cursor() as cursor:
            cursor.execute(query)
            #if internal_usage is False: 
            results = cursor.fetchone()
            #else: temp_internal_elem = cursor.fetchone()
            count = cursor.rowcount; cursor.close()
            print("The product code {%s} is being updated to: %s" %(prod_code, results))
            print(f"◾ rows count: {count}")
            if(results is None): 
                print("🔺 [DataError]: The query result returned more than one row or is 'None'")
        return results 


#=======================================================================================================================================
    @classmethod
    def Product_Pricing_Table(cls, 
            table_id: int, 
            prod_code: int) -> tuple|None:
        results:object = None
        check_table = """
        SELECT 
            Descricao, 
            Codigo, 
            Considera_Promocao, 
            Recalcula_promocao, 
            TP_Preco, 
            Exigecadastrocliente
            FROM tabelas 
        WHERE codigo = %s"""
        
        prod_proper = """
        SELECT 
            CodigoProduto, 
            Preco, 
            IdTabela
	        FROM tabelas_preco_produto AS tpp
        WHERE idtabela = %s 
            AND tpp.CodigoProduto = %s"""

        with cls.MySQLconnection.cursor() as this_cursor:
            this_cursor.execute(check_table, (table_id,))
            check_up = this_cursor.fetchone(); this_cursor.close()

        if(check_up is not None):
            print(f"Table Price _id: {table_id}\nTable Price Type: {check_up[0]}")
            ident: str = 'I'    # -> Indiviual table price
            if(ident not in check_up):
                log.info(msg='\n')
                log.error(msg=f"\n[Exception] This Table `code_id`: {table_id} is not valid!".upper())
                print("The pricing table must be of the Individual Type and not a Generic Type!".upper())
                raise Exception()
            else:
                with cls.MySQLconnection.cursor() as cursor:
                    cursor.execute(prod_proper, (table_id, prod_code))
                    results = cursor.fetchall()
                    count = cursor.rowcount; cursor.close()
                    # debug on report log...
                    print(f"The value of: '{results}' has been found for the product: '{prod_code}'" +
                          f" pricing table number: [{table_id}] -> {check_up[0]}")
                    print(f"rows count: {count}")
        else: print('Table Price id: [%a] was not found!' %table_id)
        return results

#=======================================================================================================================================
    @classmethod
    def Product_Offer(cls, prod_code: int) -> tuple | None:
        """It lookig for available offers to the product record"""

        results: object = None
        query = """
        select
            DataInicioPromocao as DataInicioOferta, 
            coalesce(
                DataPromocao, null, 
                subdate(curdate(), interval 1 day)
            ) as DatFimOfeta, 
            coalesce(ValorPromocao, null, 0) as ValorOferta, 
            QtdeMin_Promocao as QtdeMinOferta
            FROM produtos as p
        Where p.Codigo = %s"""
        
        with cls.MySQLconnection.cursor() as _cursor:
            _cursor.execute(query, (prod_code,))
            results = _cursor.fetchone(); _cursor.close()

        print('\n🔖 AVAILABLE OFFERS IN THE PRODUCT RECORD'); create_line(41, cmd='print')
        print(f"Product Code: {prod_code}\nAvailable Offers Data: {results}")
        
        # OFFERS CHECK UP ::
        if((results is not None) and (results[1] >= dt.date.today())):
            offer = (float(results[2]), int(results[3]), int(0))
            print("\n💱 Offer Breakdown:".upper())
            columns = ('DataInicioOferta', 'DataFimOferta', 'ValorOfera', 'QtdeMinOfertta')
            for i in range(columns.__len__()): print(" ◾ [%s]: %s" %(columns[i], results[i]))
            return offer
        else: return  None

#=======================================================================================================================================
    @classmethod
    def Product_Promotion(cls, prod_code: int = 0, info: bool = False):
        """It lookig for available promotion to the product record"""
        
        results:object = None
        today = dt.date.today(); current_time = st('%H:%M:%S', lt())
        print(f"query perfomred at: {today}, {current_time}")
        query_A = """
        SELECT 
            Sequencia, 
            SeqPromocao, 
            CodigoProduto, 
            Desconto, 
            QtdeMin, QtdeMax, 
            ValorVenda, ValorPromocao, 
            Cancelado, 
            LimitadoCPF, 
            QtdeMaxPromocao
            FROM promocao_produto AS p
        WHERE p.CodigoProduto = %s 
            AND p.Cancelado <> 1
        ORDER BY p.Sequencia DESC LIMIT 1"""

        query_B = """
        SELECT 
	        Status, 
            EnviaPDV, 
            DataFim, 
            QuantidadePack, 
            RepetirVenda
            FROM promocao AS p
        WHERE p.Sequencia = %s"""

        with cls.MySQLconnection.cursor(buffered=True) as cursor_A:
            cursor_A.execute(query_A, (prod_code,))
            results = cursor_A.fetchone()
            count = cursor_A.rowcount; cursor_A.close()
            print(f'query_results for query_A: {results}')
            print(f'query_rows: {count}')
            pass

        if((results != ()) and (results is not None)):
            promotion_code = results[1]
            with cls.MySQLconnection.cursor(buffered=True) as cursor_B:
                cursor_B.execute(query_B, (promotion_code,))
                _status = cursor_B.fetchone()
                count = cursor_B.rowcount; cursor_B.close()
                print(f"query_results for query_B: {promotion_code}, '_status:' {_status}")
                print(f'query_rows: {count}'); pass
            promotion_date = _status[2]; print(f"debug of 'promotion_date': {promotion_date}")
            
            if((ope.eq(_status[0], 1)) and (ope.eq(_status[1], 1)) and (promotion_date >= today)):
                if(info is True):
                    log.info('\n===================================================', also_console=True)
                    log.warn(f"""Has been found an available Promotion!
                            \r---------------------------------------------------
                            \rProduct Code:                                {results[2]}
                            \rPromotion Code:                              {results[1]}
                            \rProduct Promotion Code:                      {results[0]}
                            \rProduct Promotional Price:                   {results[7]}
                            \r---------------------------------------------------
                            \rLimited by CPF code:                             {results[9]}
                            \rPack Promotion:                                  {int(_status[3])}
                            \rRepeat Cycle Times:                              {int(_status[4])}
                            \r---------------------------------------------------""")
                    log.info('\n===================================================', also_console=True) 

                # AUTOMATIC VERIFICATION OF THE CPF CODE CONTROL OF THIS PROMOTION/OFFER IF THE CPF
                # CONTROL IS NOT NULL. AS THIS PROJECT WORKS WITH A PREVIOUSLY LOADED INTERNAL DATA
                # STRUCTURE, IN A FIRST MOMENT, WE LOAD ALL THE DATA AND INFORMATION OF THIS PRODUCT 
                # ON OFFER INTO THE INTERNAL DATA STRUCTURE. ::
                if(bool(results[9]) is True):
                    Central.there_is_promotion_by_CPF(True, 'set')
                    temp_record_dict: dict = dict(); temp_control_dict: dict = dict()
                    print(f'\n\n💬 LOADING THE CONTROL OF THE PROMOTION BY CPF CODE...')
                    create_line(57, cmd='print')
                    print("\n🟢 Available CPF/CNPJ for promotion's computing:")
                    for e in range(len(Central.CnpjCpf_on_promotion_list())):
                        print("[%s]: %s" %(e, Central.CnpjCpf_on_promotion_list().__getitem__(e)))
                    create_line(57, cmd='print')    
                    #\\...
                    for i in range(Central.CnpjCpf_on_promotion_list().__len__()):
                        print(f"-> SEARCHING FOR: {Central.CnpjCpf_on_promotion_list().__getitem__(i)}")
                        x_elem = ProductUpdate.Promotion_CPF_Query(
                            results[2], Central.CnpjCpf_on_promotion_list().__getitem__(i), results[0])
                        print(f"debug of 'x_elem' after query: {x_elem}\n")
                        
                        if(x_elem is not None):
                            create_line(200, cmd='print')
                            print('QUERYNG FOR THE PRODUCT COUNTER PER SALE:')
                            y_elem = ProductUpdate.Promotion_CPF_Counter(x_elem[1],results[2])
                            temp_record_dict.update(
                                [(str(Central.CnpjCpf_on_promotion_list().__getitem__(i)),
                                    {'cpf_cnpj': Central.CnpjCpf_on_promotion_list().__getitem__(i),
                                     'counter_used': y_elem,})])
                            print(f"debuf of 'temp_record_dict': {temp_record_dict}")
                            temp_control_dict.update(
                                [(str(results[2]),
                                    {'promo_code': results[1], 
                                     'cpf_code':temp_record_dict})])
                            print(f"\n'Centralizer.cpf_controller_storage' has updated to: {temp_control_dict}")
                            create_line(200, break_line=True, to_the_end=True, cmd='print')
                        else: continue

                    if(ope.ne(temp_control_dict, {})): 
                        Central.cpf_controller_storage(temp_control_dict, 'set')
                        #Centralizer.cpf_controller_storage = Centralizer.cpf_controller_storage # explicit _set function.
                        print('\n*FINAL RESULT FOR @property: Centralizer.cpf_controller_storage: %s' 
                              %Central.cpf_controller_storage(gt_log=True))
                    else: 
                        empty = dict(); 
                        empty.update(
                            [(str(results[2]),
                                {'promo_code': results[1], 
                                 'cpf_code':temp_record_dict})])
                        Central.cpf_controller_storage(empty, 'set')
                        print('\n*WAS CREATED AN EMPTY DICTIONARY FOR THE CONTROLLES OF THE PRODUCT PROMOTION BY CPF CODE: %s: -> %s'
                            %(results[2], Central.cpf_controller_storage()))
                        print("Centralizer.cpf_controller_storage: %s" %(Central.cpf_controller_storage(gt_log=True),))
                else: pass

                if(ope.ne(_status[3], 0)): 
                    pass # goes on...

                # THIS  FUNCTION  WILL RETURN  THE ITS RESULT ACCORDING TO THE FOLLOWING DECLARATIONS. THEREFOR, THEY
                # ARE REPONSIBLE FOR GENERATING THE OFFER CONTROLLERS ACCORDING TO THE DATABASE DATA DOWLOADED BY THE
                # SELECT QUERY WRITTEN ABOVE ::
                
                print('\n\n💲💰 LOADING PAYMENTS CONTROLLERS...%s' %(create_line(36, break_line=True, cmd='return')))
                print("Function debug of 'self.query_results' in Download_Product_Offer:")
                ProductUpdate.Promotion_Payment_Way(results[1])
                print(f"\nPromo_Value: {results[7]}")

                
                print('\n\n📝 LOADING ANOTHER PROMOTION CONTROLLERS...%s' 
                      %(create_line(44, break_line=True, cmd='return')))
                print(f"Prod_Code: {results[2]}" +
                    f"\nQnt_Min: {results[4]}" +
                    f"\nQnt_Max: {results[5]}" +
                    f"\nRepeat: {_status[4]}" +
                    f"\nLimitedCPF: {results[9]}" +
                    f"\nPromo_Max: {results[-1]}")
                
                mn = results[4]; mx = results[5]
                rpt = _status[4]; max_promo = results[-1]
                rpt = 9999 if rpt <= 0 else rpt
                return [float(results[7]),    # -> Promotion Value
                        (int(results[2]),     # -> Product Code
                        int(results[1]),      # -> Promotion Code
                        int(mn),              # -> Minimmun Qunatity
                        int(mx),              # -> Maximmum Qunatity
                        bool(results[9]),     # -> Limited by CPF Serial Code ?
                        int(rpt),             # -> Repeat on Sale
                        int(max_promo))]     # -> Maximmum Quantity For Sale
                
            else: print('\n❗ UNVAILABLE PROMOTION!'); return None
        else: return None

#=======================================================================================================================================
    @classmethod
    def Promotion_CPF_Query(cls, 
            product_code_on_promotion: int = 0,  
            cpf_code: str = 'Empty',
            product_promotion_id: int = 0):
        
        query = """
        SELECT 
            Codigo
            FROM vendas AS v 
        WHERE v.CNPJ = %s 
            AND STATUS = 'f' 
            AND Codigo IN (
                SELECT CodigoVenda 
                    FROM vendasprodutos AS vp
                WHERE vp.CodigoProduto = %s 
                    AND vp.PrecoemPromocao IS NOT NULL 
                    AND pp_sequencia = %s 
                ORDER BY vp.CodigoVenda DESC)
        ORDER BY Codigo DESC"""

        with cls.MySQLconnection.cursor(buffered=True) as cursorC:
            print(f'QUERY RESULT FOR CPF ALREADY CONTEMPLATED :: {cls.MySQLconnection.database}...')
            data_query = (
                cpf_code, 
                product_code_on_promotion,
                product_promotion_id)
            cursorC.execute(query, data_query)
            local_result = cursorC.fetchall()
            count = cursorC.rowcount; cursorC.close()
            print(f'query_results for CPF query: {local_result}')
            print(f'query_rows: {count}')
            
        if((count > 0) and (len(local_result) > 1)):
            return (count, local_result)
        elif(((count > 0) and (len(local_result) <= 1))):
            return (count, local_result[0][0])
        else: return None

#=======================================================================================================================================
    @classmethod
    def Promotion_CPF_Counter(cls, sales_code: list|tuple|int, product_code:int):
        formated: object = None; query: str = 'Empty'
        if(isinstance(sales_code, list)):
            elem = list()
            for i in range(len(sales_code)): 
                elem.append(sales_code[i][i-i])
            formated = tuple(elem)
            query = """
            SELECT CodigoProduto 
                FROM vendasprodutos AS vp
            WHERE vp.CodigoVenda IN {}
                AND CodigoProduto = {} 
                AND PrecoEmPromocao IS NOT NULL""".format(formated, product_code)
        else: 
            formated = sales_code
            query = """
            SELECT CodigoProduto 
                FROM vendasprodutos AS vp
            WHERE vp.CodigoVenda = %s
                AND CodigoProduto = %s 
                AND PrecoEmPromocao IS NOT NULL""" %(formated, product_code)
        
        print('debuf of the func. formated: %s' %(formated,))
        print('debug query: %s' %(query))
        with cls.MySQLconnection.cursor(buffered=True) as cursorF:
            cursorF.execute(query)
            local_result = cursorF.fetchall()
            count = cursorF.rowcount; cursorF.close()
            print(f'query_rows: {count}')
            print(f'query_results for PRODUCT COUTNER query: {local_result}')
        return count
    
#=======================================================================================================================================
    @classmethod
    def Promotion_Payment_Way(cls, seq_promo: int):
        query = """
        SELECT SeqFormaRecebimento 
            FROM promocao_forma_recebimento
        WHERE SeqPromocao = %s"""

        results = list()
        with cls.MySQLconnection.cursor(buffered=True) as cursorD:
            print(f'QUERY RESULT FOR PAYMENT WAY TO THE PROMOTION CODE ' +
                  f'{seq_promo} :: <{cls.MySQLconnection.database}>...')
            cursorD.execute(query, (seq_promo,))
            local_result = cursorD.fetchall()
            count = cursorD.rowcount; cursorD.close()
            print(f'query_rows: {count}')
            print(f'query_results for PAYMENT WAY query: {local_result}')

            if(ope.ne(local_result, [])):
                for i in range(len(local_result)): results.append(local_result[i][0])
                print("\n'results' of payment way for promotion code: [%s] ->: %s"
                      %(seq_promo, results))
                Central.payment_controllers([(str(seq_promo), {'paymnt_method': results})], 'set')
                print('\n*FINAL RESULT FOR @property: Centralizer.payment_controllers: %s'
                      %(Central.payment_controllers(gt_log=True),))
            else:
                Central.payment_controllers([(str(seq_promo), {'paymnt_method':None})], 'set')
                print('\n*WAS CREATED AN EMPTY DICTIONARY FOR THE PAYMENT CONTROLLERS OF THE PROMOTION CODE %s: -> %s'
                    %(seq_promo, Central.payment_controllers(gt_log=True)))
            print("@property: Centralizer.payment_controllers: %s" %(Central.payment_controllers(gt_log=True),))
        return

#=======================================================================================================================================
    @classmethod    
    def Find_Promotion_Automatically(cls) -> list|None:
        local_results:object = None
        query = """
        SELECT 
            pp.Sequencia, 
            pp.SeqPromocao, 
            pp.CodigoProduto
            FROM promocao_produto AS pp
            JOIN promocao AS p
                ON pp.SeqPromocao = p.Sequencia
        WHERE pp.Cancelado <> 1
            AND p.EnviaPDV = 1
            AND p.DataFim >= CURDATE()
            AND p.`Status` = 1
            AND pp.SeqPromocao IS NOT NULL
            AND p.QuantidadePack = 0
        ORDER BY p.Sequencia DESC"""

        with cls.MySQLconnection.cursor(buffered=True) as lcl_cursor:
            lcl_cursor.execute(query); local_results = lcl_cursor.fetchall()
            count = lcl_cursor.rowcount; lcl_cursor.close()
            print("\n\n\n💲🔖 Promotional items found:".upper() + 
                  "\n------------------------------")
            print('📜 <list>:local_results for query:\n• Row Count: %s:' %count)
            for r in range(len(local_results)): print("[%s]: %s" %(r, local_results[r]))
            pass
            
        prod_list = list()
        if((local_results is not None) and (ope.ne(local_results, []))): 
            for i in range(len(local_results)):
                prod_list.append(local_results[i][-1])
            print("\n📑 List of Promotional Itens: %s" %(prod_list,))
        else:
            print("❕⚠ Likely there aren't promotional items on database [%s]" %(cls.MySQLconnection.database,))
            return None
        return prod_list if(ope.ne(prod_list, [])) else None

#=======================================================================================================================================
    @classmethod    
    def Find_Offers_Automatically(cls) -> list|None:
        local_results:object = None
        query = """
        SELECT
        p.Codigo ,
        p.CodigoBarras ,
        DataInicioPromocao as DataInicioOferta, 
        coalesce(
            DataPromocao, null, 
            subdate(curdate(), interval 1 day)
        ) as DatFimOfeta, 
        p.VendaT1 ,
        p.VendaPDV ,
        coalesce(ValorPromocao, null, 0) as ValorOferta, 
        QtdeMin_Promocao as QtdeMinOferta
        FROM produtos as p
        Where 
            coalesce(p.DataPromocao, null, subdate(curdate(), interval 2 day)) >= curdate()
        order by p.Codigo"""

        with cls.MySQLconnection.cursor(buffered=True) as p_cursor:
            p_cursor.execute(query); local_results = p_cursor.fetchall()
            count = p_cursor.rowcount; p_cursor.close()
            print("\n\n\n💲🔖 Offers has found:".upper() + 
                  "\n------------------------------")
            print('📜 <list>:local_results for query:\n• Row Count: %s:' %count)
            for r in range(len(local_results)): print("[%s]: %s" %(r, local_results[r]))
            pass
            
        prod_list = list()
        if((local_results is not None) and (ope.ne(local_results, []))): 
            for i in range(len(local_results)):
                prod_list.append(local_results[i][int()])
            print("\n📑 List of Products on Offer: %s" %(prod_list,))
        else:
            print("❕⚠ Likely there aren't promotional items on database [%s]" %(cls.MySQLconnection.database,))
            return None
        return prod_list if(ope.ne(prod_list, [])) else None
    
#=======================================================================================================================================        
    @staticmethod
    def Save_Products_Data_Sequence(is_promotion:bool= False, is_offer:bool= False) -> None:
        ExternalFile.set_file_path(Central.path_local_storage)
        replace = list(); counter:int = -1
        content = ExternalFile.read_file()
        print("\n🔹📜 STORING DATA SEQUENCE:\n◉ Building Products Sequence to the Local Storage...")
        create_line(55, cmd='print')

        # Security Clause ::
        if(ope.eq(Central.products(), {})):
            print("\n❓ There is a problem with @property cls.products in this process step!" +
                  "No elements to recording has been found in @entity Central.products()")
            raise Exception()
        else: pass

        # building sequence to storaging...
        if(is_promotion is False):
            for elem in Central.products().keys():
                counter = ope.iadd(counter, int(1))
                replace.append(Central.products(gt_log=True).__getitem__(elem))
                print("• last index in <list> replace[%s]:\n💾💲 %s" %(counter, replace[-1]))
                create_line(200, char='_', cmd='print')
            ExternalFile.update_file(file= content, key= 'product_sequence', new_value= replace)
        
        elif(is_promotion is True):
            #\\... Promotion Controller ::
            for elem in Central.promotion_controller_storage().keys():
                counter = ope.iadd(counter, int(1))
                replace.append([elem, Central.promotion_controller_storage(gt_log=True, elem_key=elem).__getitem__(elem)])
                print("• last index of <list> replace[%s]:\n💾💲 %s" %(counter, replace[-1]))
                create_line(120, char='_', cmd='print')
            ExternalFile.update_file(file= content, key= 'product_promotion', new_value= replace)
            replace.clear(); counter = int(-1)
            #\\... Promotion Payment Controller ::
            for elem in Central.payment_controllers().keys():
                counter = ope.iadd(counter, int(1))
                replace.append([elem, Central.payment_controllers(gt_log=True, elem_key=elem).__getitem__(elem)])
                print("• last index of <list> replace[%s]:\n💾💲 %s" %(counter, replace[-1]))
                create_line(120, char='_', cmd='print')
            ExternalFile.update_file(file= content, key= 'ppromotion_payment', new_value= replace)
        elif(is_offer is True):
            # It hasn't been writen yet... 
            pass
        else:
            print("❗❓ Obligatory argument has not been noticed!\n👨‍💻 [bool, `is_promotion`: ?].")
            raise Exception()
        # Dump File ::
        ExternalFile.write_on_file(content)
        return

#======================================================================================================================================= 
    # RECOVER AND RESTORE DATA SEQUENCE...
    @staticmethod
    def Recovery_Data_Sequence(is_promotion:bool= False, is_offer:bool= False) -> dict:
        ExternalFile.set_file_path(Central.path_local_storage)    
        build_property = dict()
        content = ExternalFile.read_file()
        data_sequence = list()
            
        # Security Statement ::
        def check_for(data) -> Exception | None:
            if(ope.eq(data_sequence, [])):
                print(
                "\n❓ There was a problem with <list>:data_sequence." +
                "\nNo elements has been found in both classes properties!")
                raise Exception()
            else: return
        
        #\\... Products Data Sequence ::
        if(is_promotion is False):
            data_sequence = list(content['product_sequence'])
            check_for(data_sequence)
            for g in range(len(data_sequence)):
                dict_id = create_number_key()
                build_property.update([(dict_id, data_sequence[g])])
                print("'index_id': %s\n@property cls.customers in [%s]: %s\n" %(dict_id, dict_id, build_property[dict_id]))
            PdLog.info(msg="\n✅ Product's Local Storage has been successffully recovered")
            Central.products(build_property.copy(), 'set')
            print('✅ Central.products() has been restored from external data sequence!\n')
        
        #\\... Promotions Data Sequence ::
        elif((is_promotion is True)):
            data_sequence = list(content.get('product_promotion'))
            check_for(data_sequence)
            for i in range(len(data_sequence)):
                dict_id = str(data_sequence[i][0])
                Central.prod_on_promotion_controller([(dict_id, data_sequence[i][1])], 'set')
                print("▪ 'index_id': %s\n@property Centralizer.prod_on_promotion_controller in [%s]:\n%s\n" 
                %(dict_id, dict_id, Central.prod_on_promotion_controller(gt_log=True).__getitem__(dict_id)))
            print('✅ Central.prod_on_promotion_controller() has been restored from external data sequence!\n')
            #\\... Retoring promotional data package to the promtion's control :: 
            print("\n🔧💰 Updating Central.promotion_controller_storage class' entity:")
            Central.promotion_controller_storage(Central.prod_on_promotion_controller(), 'set')
            #\\... html output ::
            print("\n👁‍🗨 LOOK AT Central.promotion_controller_storage entity properties:")
            for e in Central.promotion_controller_storage().keys():
                print(" [%s]: %s" %(e, Central.promotion_controller_storage().__getitem__(e)))
            print('')
            data_sequence.clear()

            #\\... Promotion Payment Controller ::
            data_sequence = list(content.get('ppromotion_payment'))
            check_for(data_sequence)
            for e in range(len(data_sequence)):
                dict_id = str(data_sequence[e][0])
                Central.payment_controllers([(dict_id, data_sequence[e][1])], 'set')
                print("▪ 'index_id': %s\n@property Centralizer.payment_controllers in [%s]:\n%s\n" 
                %(dict_id, dict_id, Central.payment_controllers(gt_log=True).__getitem__(dict_id)))
            print('✅ Central.payment_controllers() has been restored from external data sequence!\n') 
        return

#\\... END OF PROGRAM
#=======================================================================================================================================