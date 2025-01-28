
# PROJECT FOLDER DEPENDENCES ::
from Base import Payment, ExternalFile
from Base import Centralizer as Central

# -> External Modules and Classes ::
import operator as ope
import mysql.connector as cnx
from mysql.connector import errors
from FireBirdConnector import FbConnector

# -> Custom Modules has created to the Porject ::
from utilities.TextFormater import *
from utilities.ColorText import log, logger1
from utilities.KeyGenerator import create_number_key
plog = logger1()

class PaymentWaysPDV:
    #Properties ::
    MySQLconnection:cnx.MySQLConnection = None #type: ignore
    query_results:object = None
    
    def __init__(cls) -> None:
        pass

    @classmethod
    def Set_MySQL_Connection(cls, cnn:cnx.MySQLConnection) -> cnx.MySQLConnection:
        """Create an explicit connection mapping to the @property: `MySQLConnection`"""
        cls.MySQLconnection = cnn; return

    @classmethod
    def Create_Payments_Mapping(cls):
        print("Connection Statues: %s " %(cls.MySQLconnection.is_connected(),))
        elements = dict(
            descrpt= 'Empty', pay_type= 'Empty', patter= None, 
            patter_pay= None, not_pdv= None, apply_addt= None, 
            additional_value= float(0), block_dscnt= None,
            min_dscnt_value= None, unq_key='Empty', key_code= int(0))
        
        # This query has been edicted according to the maximmun limit for quantity of payment methods
        # that can be downloaded to FireBird Server on PDVOFF Local Storage. The system PDV accepts only
        # 8 payment ways as 'finalizadoras' to the sales proccess.
        query = """
        SELECT
            Codigo, Descricao, Tipo, 
            Padrao, PadraoPagar, NaoEnviaPDV, 
            chkPercentualAdicionalPDV,
            PercentualAdicionalPDV, 
            chkBloqueioDescontoAplicadoPDV, 
            ValorMinimodescontoPDV
            FROM formarecebimento AS fmr
        WHERE NaoEnviaPDV <> 1
            ORDER BY Codigo LIMIT 8"""

        with cls.MySQLconnection.cursor() as cursor:
            cursor.execute(query)
            cls.query_results = cursor.fetchall()
            count = cursor.rowcount; cursor.close()
            print(f"HAS BBEN FOUND {count} RECORDS FROM <{cls.MySQLconnection.database}> DATABASE:")
            print(f"rows count: {count}"); print('\nLook at the available Payment Ways: ↴')
            for r in range(len(cls.query_results)): print("[%s] -> %s" %(r, cls.query_results[r]))
            
            # EXTRACT ELEMENTS AS 'elem' ON USE AND APPLY ITS VALUES AS PROPERTIES::
            if(ope.ne(cls.query_results, [])):

                for e in range(len(cls.query_results)):
                    master_key: int = cls.query_results[e][0]; print('\n🔑 master_key: %s' %master_key)
                    print("-> PAYMENT DICTIONARY IN [%s]" %master_key)
                    copy = elements.copy(); keys = list(copy); print("keys: %s" %(keys))
                    print("elements: %s" %(elements,))
                    for i in range(1, len(cls.query_results[e])):
                        copy[str(keys[i-1])] = (
                            bool(cls.query_results[e][i]) if ((i-1) not in (0, 1, 6, 8) and
                                                               (i-1) is not None) else cls.query_results[e][i])
                    
                    # Aplly the Unique Key for Payment Way: ↴
                    pay_type_edited = remove_punctuation(copy['pay_type'])
                    unq_key = PaymentWaysPDV.Set_Unique_Key(copy['descrpt'], pay_type_edited, master_key)
                    copy['unq_key'] = unq_key
                    Payment.payment_ways([(str(master_key), copy)], 'set')
                    print("@property Centralizer.payment_ways: %s" %(Payment.payment_ways(gt_log=True).get(str(master_key)),))
                
                print("\n\nLOOK AT THE PAYMENT MAPPING:\n----------------------------")
                for elem in Payment.payment_ways().keys(): print("[%s]: %s" %(elem, Payment.payment_ways(gt_log=True).get(elem)))
            else: 
                print("UNPOSSIBLE TO FIND PAYMENT METHODS ON %s DATABASE!" %cls.MySQLconnection.database)
                print('(InternalError): %s' %(cls.query_results,)); raise errors.InternalError()
        
        PaymentWaysPDV.Set_Key_Codes()
        PaymentWaysPDV.Find_And_Set_Card_Codes()
        FbConnector.Close_Connection()
        PaymentWaysPDV.Save_Payment_Data_Sequence()
        return 

#=======================================================================================================================================        
    @classmethod
    def Set_Unique_Key(cls, descrpt:str, pay_type:str, order:int= 0):
        unq_key: str = 'Empty'
        if((ope.eq(descrpt.upper(), 'DINHEIRO'))
            and (ope.eq(pay_type.lower(), 'moeda'))
                and (ope.eq(order, 1))):
            unq_key = 'DIN'; return unq_key
            
        elif((descrpt.upper() in ('CHEQUE', 'CHEQUES'))
            and (pay_type.lower() in ('cheque', 'cheques'))):
            unq_key = 'CHQ'; return unq_key
        
        elif((descrpt.upper() in ('CARTĂO', 'CARTAO', 'CARTÃO', 'CARTAO POS', 'CARTÃO POS'))
            and (pay_type.lower() in ('cartăo oper', 'cartao oper', 'cartão oper'))):
            unq_key = 'CRT'; return unq_key

        elif((descrpt.upper() in ('PRAZO', 'À PRAZO', 'CREDIÁRIO', 'CREDIARIO', 'CONVENIO', 'CONVÊNIO'))
            and (pay_type.lower() in ('cartăo próprio', 'cartão próprio', 'cartao proprio'))):
            unq_key = 'CRE'; return unq_key
        
        elif((descrpt.upper() in ('PIX', 'PIX SISTEMA'))
            and (pay_type.lower() in ('pix',))):
            unq_key = 'PIX'; return unq_key
        
        elif((descrpt.upper() in ('CARTĂO TEF', 'CARTÃO TEF', 'CARTAO TEF', 'TEF'))
            and (pay_type.lower() in ('cartăo oper', 'cartao oper', 'cartão oper'))):
            unq_key = 'TEF'; return unq_key

        elif((descrpt.upper() in ('VALE COMPRA', 'VALES', 'VALE'))
            and (pay_type.lower() in ('vales', 'vale'))):
            unq_key = 'VLE'; return unq_key
        
        elif((descrpt.upper() in ('BANCARIA', 'BANCÁRIA'))
            and (pay_type.lower() in ('bancaria', 'bancária', 'bancària'))):
            unq_key = 'BNC'; return unq_key
        else:
            log.console("", newline=True); log.error("...")
            plog.error("\nUnkow payment method was found as an available" +
                       "\npayment method recorded on databaase [%s]" %cls.MySQLconnection.database)
        return
    
#=======================================================================================================================================
    @staticmethod
    def Set_Key_Codes():
        # ANSI CODES FOR KEYBOARD KEY CODES ::
        KbCode_keys = Central.keyboard_keycodes.copy()
        FbConnector.Change_Connection()
        cnn = FbConnector.Get_Current_Connection()
        copy:dict = Payment.payment_ways().copy()

        paymnt_query = """
        SELECT 
            TECLADO_FIN01 , TECLADO_FIN02 , 
            TECLADO_FIN03 , TECLADO_FIN04 , 
            TECLADO_FIN05 , TECLADO_FIN06 , 
            TECLADO_FIN07 , TECLADO_FIN08
            FROM CONFIG_TECLADO as ct"""
        
        this_cursor = cnn.cursor(); this_cursor.execute(paymnt_query)
        fb_results = this_cursor.fetchone(); print("\n📜 <var>:results for payemnt shortcut 'key_codes': %s" %(fb_results,))
        print('\n► Look at the elements has extracted as keyboard codes to the payment methods!'.upper())
        list_keys = list(copy)
        for e in range(len(list_keys)):
            print('\nresults in [%s] -> FINALIZADORA [%s]: %s' %(e, (e+1), fb_results[e]))
            copy[str(list_keys[e])]['key_code'] = (
                KbCode_keys[fb_results[e]] if((copy[str(list_keys[e])]['key_code'] is not None) 
                                           and (fb_results[e] in KbCode_keys.keys())) else None)
            print("'copy' element from Paymets.payment_ways: %s to [%s] key_value"
                   %(copy[str(list_keys[e])]['key_code'], e) 
                  if(copy[str(list_keys[e])]['key_code'] is not None) 
                  else print('\n❗ [%s] serial Code has not been found!' %fb_results[e]))
        
        Payment.payment_ways(copy, 'set')
        print('\n💰 PAYMENT WAYS AFTER UPDATES:\n------------------------------\n')
        for this_key in Payment.payment_ways().keys():
            print('[%s]: %s' %(this_key, Payment.payment_ways(gt_log=True).__getitem__(this_key)))
        return

#=======================================================================================================================================
    # SAVE DATA SEQUENCE...
    @staticmethod
    def Save_Payment_Data_Sequence(is_card:bool= False, is_taxes:bool= False):
        # As the standard path <str> value to the <class>:OutWriter is automatically loaded to
        # store the cashier dependences, it's necessary to replace that path file to the current
        # data file on usage.
        ExternalFile.set_file_path(Central.path_local_storage)
        print("\n🔹📜 STORING DATA SEQUENCE:\n◉ Building Payment Sequence to the Local Storage...")
        create_line(55, cmd='print')
        # building sequence to storaging...
        replace = list(); this_content = ExternalFile.read_file(); counter:int = -1
        print("\n\n◉ Building the Payment Sequence to the Local Storage...\n")
        if((is_card is False) and (is_taxes is False)):
            for elem in Payment.payment_ways().keys():
                counter = ope.iadd(counter, int(1))
                replace.append(Payment.payment_ways(gt_log=True).__getitem__(elem))
                print("• last index in <list> replace[%s]:\n💾💲 %s" %(counter, replace[-1]))
                create_line(200, char='_', cmd='print')
            ExternalFile.update_file(file= this_content, key= 'zpayment_storage', new_value= replace)
        
        elif((is_card is True) and (is_taxes is False)):
            for elem in Payment.card_codes().keys():
                counter = ope.iadd(counter, int(1))
                replace.append(Payment.card_codes(gt_log=True).__getitem__(elem))
                print("• last index in <list> replace[%s]:\n💾📟 %s" %(counter, replace[-1]))
            ExternalFile.update_file(file= this_content, key= 'zcard_code', new_value= replace)
        
        elif((is_taxes is True) and (is_card is False)):
            for elem in Payment.card_taxes().keys():
                counter = ope.iadd(counter, int(1))
                replace.append(Payment.card_taxes(gt_log=True).__getitem__(elem))
                print("• last index in <list> replace[%s]:\n💾💳 %s" %(counter, replace[-1]))
                create_line(200, char='_', cmd='print')
            ExternalFile.update_file(file= this_content, key= 'zcard_taxes', new_value= replace)
        else:
            print("❗❓ Obligatory argument has not been noticed!\n👨‍💻 [bool, `is_card`: ?, `is_taxes`: ?].")
            raise Exception()
        # Dump File ::
        ExternalFile.write_on_file(this_content)
        return
    
#=======================================================================================================================================
#\\\#RECOVER AND RESTORE DATA SEQUENCE...
#=======================================================================================================================================

    @staticmethod
    def Recovery_Payment_Sequence(is_card:bool = False, is_taxes:bool= False):
        print("📜 Opening and Reading the 'Database_Content.yaml' file content...\n")
        ExternalFile.set_file_path(Central.path_local_storage)
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
        
        #\\... Payment Ways Data Sequence ::
        if((is_card is False) and (is_taxes is False)):
            #-> The Numerical Code ID to the both @properties: <dictc>:Centralizer.payment_ways
            # and <dict>:Centralizer.card_codes can be found on FireBird Database as product code
            # for card code companies. Has already we automatically download these code sequence
            # from database range, we just need apply the same sequence to the card codes storage.
            data_sequence = list(content['zpayment_storage'])
            check_for(data_sequence)
            for i in range(len(data_sequence)):
                dict_id = ope.iadd(i, 1)
                Payment.payment_ways([(dict_id, data_sequence[i])], 'set')
                print("▪ 'index_id': %s\n@property Centralizer.payment_ways in [%s]:\n%s\n" 
                    %(dict_id, dict_id, Payment.payment_ways(gt_log=True).__getitem__(dict_id)))
            print('✅ Centralizer.payment_ways has been restored from external data sequence!\n')   
        
        #\\... Card Data Sequence ::
        elif((is_card is True) and (is_taxes is False)):
            data_sequence = list(content['zcard_code'])
            check_for(data_sequence)
            for i in range(len(data_sequence)):
                dict_id = ope.iadd(i, 1)
                Payment.card_codes([(dict_id, data_sequence[i])], 'set')
                print("▪ 'index_id': %s\n@property Centralizer.card_codes in [%s]:\n%s\n" 
                    %(dict_id, dict_id, Payment.card_codes(gt_log=True).__getitem__(dict_id)))
            print('✅ Centralizer.card_codes has been restored from external data sequence!\n')
        
        #\\... Card Taxes Data Sequence ::
        elif((is_taxes is True) and (is_card is False)):
            data_sequence = list(content['zcard_taxes'])
            check_for(data_sequence)
            for i in range(len(data_sequence)):
                dict_id = ope.iadd(i, 1)
                Payment.card_taxes([(dict_id, data_sequence[i])], 'set')
                print("▪ 'index_id': %s\n@property Centralizer.card_taxes in [%s]:\n%s\n" 
                    %(dict_id, dict_id, Payment.card_taxes(gt_log=True).__getitem__(dict_id)))
            print('✅ Centralizer.card_taxes has been restored from external data sequence!\n')            
        return

#=======================================================================================================================================
    @staticmethod
    def Find_And_Set_Card_Codes() -> dict|list:
        print("\n\n▶ Creating the Cards Mapping for @property Centralizer.card_codes...")
        cnn = FbConnector.Restore_Connection()
        queryA:str= "SELECT count(CODIGO) FROM OP_CARTAO AS oc"
        cnt_cursor = cnn.cursor(); cnt_cursor.execute(queryA)
        counter:object = cnt_cursor.fetchone(); cnt_cursor.close()
        print("\n🔍 [FB QUERY]: %s\n   - counter OP_CARTAO: %s" %(queryA, (counter
            if((counter is not None) or (counter != ())) else 'Empty or Null')))
        counter = counter if(not isinstance(counter, tuple)) else counter[0]
        if(counter is None): 
            print("\n▶ Has not been found records on database [FireBird Server]"); return
        print("\nPerforming FireBird SQL Query...".upper())
        
        card_code = list()
        for cnt in range(1, (counter + 1)):
            queryB:str= """
            SELECT
            CODIGO, 
            CODIGO_OP, 
            DESCRICAO, 
            OPERACAO, 
            TAXA_OPERACAO, 
            TIPO_TAXA_OPERACAO, 
            TAXA AS TARIFA 
            FROM OP_CARTAO_PROD ocp 
            WHERE CODIGO_OP = {}"""
            
            qry_cursor = cnn.cursor()
            queryB = queryB.format(cnt)
            print("[FB QUERY]: %s" %(queryB))
            qry_cursor.execute(queryB)
            results:object = qry_cursor.fetchall(); qry_cursor.close(); 
            print("\nQuery Results for 'queryB' in counter card number [%s]:" %cnt)
            if(ope.ne(results, [])):
                for t in range(len(results)): print("-> [%s]: %s" %(t, results[t]))
                for i in range(len(results)):
                    (print("\n<var>: `results` in [%s]:\n%s\nCard Code: %s" %(i, results[i], results[i][1])) 
                     if(ope.ne(results, [])) else "<var>: `result` is Empty or Null!")
                    card_code.append(results[i][0])
                    print("\n<list> card_code[%s]: %s" %(i, card_code[i]))
                print("\n📝 <list> card_code: %s\n" %(card_code,))
                create_line(110, cmd='print')
                print("\n▶ Building the Card Codes Structure...".upper())
                random_key = create_number_key()
                Payment.card_codes([(str(random_key), {'operator':cnt, 'codes':card_code.copy()})], 'set')
                #print("<dict>: card_map after <func>: update() -> %s\n" %(Centralizer.card_codes,))
                card_code.clear()

                print("\n► Look at the card codes available to the Card Payment way:")
                for elem in Payment.card_codes().keys():
                    print("🔑{%s} ->: 💳 %s" %(elem, Payment.card_codes(gt_log=True).__getitem__(elem)))
            else: 
                print("❗ @property self.fb_cnn has returned an empty list or tuple:\n<var>: `results` -> %s" %(results,))
                print("❌ Likely there isn't and OPE_CARTAO_PROD code %s. Check for your database..." %cnt)
                continue

        PaymentWaysPDV.Set_Card_Taxes(Payment.card_codes())
        PaymentWaysPDV.Save_Payment_Data_Sequence(is_card=True)
        return
    
#=======================================================================================================================================    
    @staticmethod
    def Set_Card_Taxes(code_sqnc:dict) -> None:
        print("\n\n▶ Creating Card Taxes Mapping To The Card Code Dictionary...".upper())
        for k1 in code_sqnc.keys():
            list_code:list = code_sqnc[k1]['codes']
            for i in range(len(list_code)):
                cnn = FbConnector.Get_Current_Connection()
                print("\nPerforming FireBird SQL Query...".upper() + ' 🔍')
                queryC:str= """
                SELECT 
                CODIGO, OPERACAO, TAXA_OPERACAO, 
                TIPO_TAXA_OPERACAO, TAXA AS TARIFA 
                FROM OP_CARTAO_PROD ocp 
                WHERE CODIGO_OP = {}
                AND CODIGO = {}""".format(code_sqnc[k1]['operator'], list_code[i])

                print("[PDVOFF.FDB] :: [OP_CARTAO_PROD]" +
                "\n...WHERE CODIGO_OP = %s AND CODIGO = %s" %(code_sqnc[k1]['operator'], list_code[i]))
                cnt_cursor = cnn.cursor(); cnt_cursor.execute(queryC)
                result:object = cnt_cursor.fetchone(); cnt_cursor.close()
                if(result is None): 
                    print("\n❗ Has not been found records against database [FireBird Server]"); break
                else:
                    print("\n▸ Updating @property Payment.card_taxes like:")
                    random_key:int = create_number_key(numeric=True)
                    card_prop = dict(
                        ope_code= int(code_sqnc[k1]['operator']),
                        prod_code= (int(result[0]) 
                                    if(ope.eq(result[0], list_code[i])) else None), 
                        ope_type= str(result[1]), 
                        ope_tax_value= float(result[2]), 
                        ope_tax_type= str(result[3]), 
                        card_tax_value= float(result[4]))
                    Payment.card_taxes([(random_key, card_prop)], 'set')
                    pass
                print("✔ A new card_prod has been created to the code: %s" %list_code[i])
                print("• Look at the card code properties in [%s]:\n📟 %s" %
                      (random_key, Payment.card_taxes(gt_log=True).__getitem__(random_key)))
            print("\n@property Centralizer.card_taxes in <dict> master_key [%s]:" %k1)
            # HTML OUTPUT ::
            cnt:int = -1
            for k3 in Payment.card_taxes().keys():
                cnt = ope.iadd(cnt, 1)
                print(' 🔑 [%s]: %s %s' %
                      (k3, ('💳' if(ope.eq(ope.mod(cnt, 2), 0)) else '📟'), Payment.card_taxes().get(k3)))
        # Local Storagement ::
        PaymentWaysPDV.Save_Payment_Data_Sequence(is_taxes=True)
        return

#=============================================================================================================================//