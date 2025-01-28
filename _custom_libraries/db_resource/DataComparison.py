
# SETTINGS 
# -> Project Libraries ::
from Base import Cashier, Payment
from Base import ExternalFile, Storage
from Base import Centralizer as Central

# -> External Modules, Resources and Robot Modules ::
import operator as ope
from robot.api import logger as log
from time import strftime as st, localtime as lt

# -> Custom Modules has created to the Porject ::
from utilities.TextFormater import *
from utilities.AbntRound import round2
from utilities.ColorText import logger3, t_status

# -> Classes instances to objects with startup constructor method.
clog = logger3()

# Data Coparison to the null excpetions ::
set_null_to:tuple= (
    None, '', ' ',
    '00000000191', 
    '00000000000', 
    '11111111111',
    '4404')

#========================================================================================================================//
# The Local Variables 'control1' and 'control2' has been created as controllers to this @calling function. It's very 
# important to know these variables represents the results has utilized in the final comparison has make between the data 
# process. Wheter the 'control1' or the 'control2' is <bool> `False`, the final status of the comparison performed at the 
# end of this course also will be 'False'. This concept is the same to the truth table for boolean processing data process.
#========================================================================================================================\\
# CHECK FOR THE FINAL SALE RESULTS ::

def First_Stage_ERP(results: tuple|list):
    expected_status: str = 'f'
    customer_ident = results[10] if(results[9] in set_null_to) else remove_punctuation(results[9])

    control1:bool= True; control2:bool= True
    print('\nPERFORMING COMPARISON OF THE FIST STAGE...'); create_line(42, cmd='print')
    print("Results has received in this program for the First Comparison Stage:\n📜 %s" %(str(str(results)[:77] + '...'),))
    if(ope.eq(results[7], expected_status)): print('-> Sale Status is OK!'); pass
    else:
        Storage.master_status(False, 'set'); control1 = bool(False)
        print("Sale Status Comparison: %s :: %s" %(results[7], expected_status))
        print("Sale Status is NOT OK!\nInternal Control: %s\n" %control1)
        clog.error(msg="The sale record was not successfully synchronized! for [VENDAS]".upper())
        clog.debug('%s' %(create_line(78, cmd='return'),))
    
    control2= Check_For_Sale_Value(results[4], record_output=True, difference= results[6])
    #------------------------------------------------------------------------------------------------------//
    # IF THE CUSTOMER CODE HAS LAUNCHED FOR SALE IS EQUAL 0, IT MEANS THAT THIS SALE PROCESS HAS NOT A
    # CUSTOMER CPF OR CNPJ CODE. BY DEFAULT, THE PDV SYSTEM HAS A CLIENT CODE NUMBER ONE TO REFERS TO
    # THE ANY CUSTOMER OR PERSON!
    #------------------------------------------------------------------------------------------------------\\
    check_for_cpf= True if ope.ne(results[10], customer_ident) else False
    control2= Check_For_Client_Code(customer_ident, check_for_cpf) if control2 is not False else control2
    # CONLUSION ::
    comparison:bool = True if((control1 is True) and (control2 is True)) else False
    t_status(comparison)
    return


# CHECK FOR THE TAX DOCUMENT ISSUE ::
def Second_Stage_ERP(results: tuple|list):
    # results[0] is the same to self.query_results[0][0] -> Sequence ID :  yyyy
    # results[1] is the same to self.query_results[0][1] -> Sale Code : xxxx
    # Therefore...
    sale_code = results[1]
    final_value = results[6] 
    mov_pdv = results[4]
    diff_value = results[7]
    status = results[8]
    client_code = results[10]
    expected_status: int = 100
    customer_ident: tuple|int = ((remove_punctuation(results[12]), ) if(results[12] is not None) else client_code)
    
    control1:bool= True; control2:bool= True
    print('\nPERFORMING COMPARISON OF THE SECOND STAGE...')
    create_line(44, break_line=True, to_the_end=True, cmd='print')
    print("Results has received in this program for the Second Comparison Stage:\n📜 %s" %(str(str(results)[:77] + '...'),))
    if((Central.cstat_check_out() is False) or (ope.eq(status, expected_status))): 
        print('\n-> Tax Document Status/CSTAT is OK!'); pass
    else:
        Storage.master_status(False, 'set'); control1 = False
        print("NFC-e Status Comparison: %s :: %s" %(status, expected_status))
        print("NFCE-e Status is NOT OK!\nInternal Control: %s\n" %control1)
        clog.error(msg="There was a problem with the issuing of the fiscal document!".upper())
        clog.error(msg='¡CSAT code is different from 100!')
        clog.debug(msg='------------------------------------------------------------------------------')
    
    if(ope.eq(mov_pdv, 1)): print('-> MOV. PDV is OK!'); pass
    else:
        Storage.master_status(False, 'set'); control1 = bool(False)
        print("PDV Movement Comparison: %s :: %s" %(status, bool(1)))
        print("PDV Movement is NOT OK!\nInternal Control: %s\n" %control1)
        clog.error(msg="There was a problem with the issuing of the fiscal document!".upper())
        clog.error(msg='¡It was not a Movement generated by the PDV system!')
        clog.debug(msg='------------------------------------------------------------------------------')
    
    control2= Check_For_Sale_Code(sale_code)
    control2= Check_For_Sale_Value(final_value, difference= diff_value) if control2 is not False else control2
    
    # IF THE CUSTOMER CODE HAS LAUNCHED FOR SALE IS EQUAL 0, IT MEANS THAT THIS SALE PROCESS HAS NOT A
    # CUSTOMER CPF OR CNPJ CODE. BY DEFAULT, THE PDV SYSTEM HAS A CLIENT CODE NUMBER ONE TO REFERS TO
    # THE ANY CUSTOMER OR PERSON!
    check_for_cpf = True if ope.ne(client_code, customer_ident) else False
    control2= Check_For_Client_Code(customer_ident, check_for_cpf) if control2 is not False else control2
    comparison:bool = True if((control1 is True) and (control2 is True)) else False
    t_status(comparison)
    return


# CHECK FOR CASHIER MOVEMENT RECORDS ::
def Third_Stage_ERP(
        results: tuple|list, 
        cash: bool= False, 
        chq: bool= False, 
        customer_pay: bool= False, 
        card: bool= False, 
        pix: bool= False, 
        bank_transfer: bool= False):
    #-----------------------------------------------------------------------------------------------------------------//   
    # This Local Variables has been created as controllers to this <def> python method. It's very important to know
    # these varibles represents the results has utilized in the final comparison between data process. Wheter the 
    # 'control1' or the 'control2' if <bool> False, the final status of the comparison performed at the end of this
    # course also will be 'False'. This concept is similar to the truth table for computiong data process.
    #-----------------------------------------------------------------------------------------------------------------\\
    control1:bool= True; control2:bool= True
    
    if(chq is True):
        customer_code = results[9]
        sale_code = results[1] 
        final_value = results[7]

        if(results[6] in movement): pass
        else:
            Storage.master_status(False, 'set'); control1 = False
            print("Movement Description Comparison: %s :: %s" %(results[6], movement))
            print("Movement Description is NOT OK!\nInternal Control: %s\n" %control1)
            clog.error(msg="The Movement description should be equal to: 'Crédito'.".upper())
            clog.debug(msg='------------------------------------------------------------------------------')
        
        # GENERAL COMPARISON BETWEEN VALUES ::
        control2= Check_For_Client_Code(customer_code, cpfCnpj= False)
        control2= Check_For_Sale_Code(sale_code) if control2 is not False else control2
        control2= Check_For_Sale_Value(final_value) if control2 is not False else control2
        
    elif(customer_pay is True):
        customer_code = results[1] 
        fiscal_doc = results[4]
        final_value = results[5] 
        expected_status: tuple= (0, False, None)
        
        if(results[7] in expected_status): pass
        else:
            Storage.master_status(False, 'set'); control1 = False
            print("Payment Status for this Customer should be in: %s :: %s" %(results[7], expected_status))
            print("Type Movement is NOT OK!\nInternal Control: %s\n" %control1)
            clog.error(msg="Type movement should be equal: 'R'.".upper())
            clog.debug(msg='------------------------------------------------------------------------------')
            
        control2= Check_For_Client_Code(customer_code, cpfCnpj= False)
        control2= Check_For_Tax_DocNumber(fiscal_doc) if control2 is not False else control2
        control2= Check_For_Sale_Value(final_value) if control2 is not False else control2
        pass

    elif((card is True) or (pix is True)):
        customer_code = results[3] 
        fiscal_doc = results[4]
        sale_code = results[3]
        final_value = results[6]
        movement: tuple = ('CREDITO', 'Crédito', 'credito')

        if(results[7] in movement): pass
        else:
            Storage.master_status(False, 'set'); control1 = False
            print("Movement Description: %s :: %s" %(results[6], movement))
            print("Type Movement is NOT OK!\nInternal Control: %s\n" %control1)
            clog.error(msg="The Movement description should be equal to: 'Crédito'.".upper())
            clog.debug(msg='%s' %(create_line(78, cmd='return')))

        control2= Check_For_Client_Code(customer_code, cpfCnpj= False)
        control2= Check_For_Tax_DocNumber(fiscal_doc) if control2 is not False else control2
        control2= Check_For_Sale_Value(final_value) if control2 is not False else control2

    # CONSLUSION ::
    comparison:bool = True if((control1 is True) and (control2 is True)) else False
    t_status(comparison)
    return


def Check_For_Cancelling_ERP(
        results:tuple|list,
        sale_status:str|int,
        record_status:str|int):
    
    print('\nPERFORMING COMPARISON BETWEEN RESULTS HAS RECEIVED FROM DATABASE:')
    print('\nChecking for the Cancelling Sale Process...'.upper())
    
    tolerance:tuple = Tolerance(
        db_value= results[2], 
        return_values=True,
        procss_value= Storage.last_sale_value().__getitem__(-1))
    
    expected_status:tuple = ('x','X', 'c', 'C', int(1), int(101), 'Cancelada', 'cancelada')
    #----------------------------------------------------------------------------------------------------//
    # CONSIDERS THESE STATEMNTS BELLOW: 
    # They clausules can determine wheter the sales cancel was really done before its recording, or not!
    # OBS: the local variable 'check' is <bool> True until some clause says the contrary of that.
    #----------------------------------------------------------------------------------------------------\\
    check:bool= True
    #\\BEGIN
    check = (True 
             if((ope.eq(Storage.last_sale_code().__getitem__(-1), results[0])) 
                and (check is not False)) 
             else False)
    check = (True 
             if((Central.use_nfce_document() is False)
                or (ope.eq(Storage.last_fiscal_document().__getitem__(-1), results[1])) 
                and (check is not False))
             else False)
    check = (True 
             if(((ope.eq(Storage.last_sale_value().__getitem__(-1), results[2])) 
                 or (results[2] in tolerance)) 
                 and (check is not False))
             else False)
    check = (True 
             if((Storage.last_customer_ident().__getitem__(-1) in results[3]) 
                and (check is not False))
             else False)
    check = (True 
             if((sale_status in expected_status)
                and (record_status in expected_status) 
                and (check is not False))
             else False)
    #\\END
    print("Conclusion: %s" %('✔ OK' if check is True else 'NOT OK'))
    return check



def Check_For_Sangria_Mov(db_cashier_content:int|float):
    status:bool = Tolerance(Cashier.total_on_cashier(), db_cashier_content)
    print("Checking for the Cashier Content after 'Sangria' has been performed as a Cashier Movement...")
    if(status is True):
        print("-> Cashier Comparison is OK!")
    else:
        Storage.master_status(False, 'set')
        print("Cashier Content Comparison: %s :: %s" %(db_cashier_content, Cashier.total_on_cashier()))
        print("The Cashier Content is NOT OK!\nInternal Control: %s\n" %status)
        clog.error(msg="The Cashier Content isn't match to [CAIXAMOVIMENTOS]")
        clog.debug(msg='------------------------------------------------------------------------------')
    t_status(status)
    return status

#========================================================================================================================//
# ALL METHOD OF THE COMPARISON AND DATA VALIDATION ARE WRITTEN HERE. THE COMPARISON PROCESS IS EXECUTED ACCORDING THREE
# SEVERAL STEPS WHICH SETS THE FINAL STATUS OF EACH PROCESS.
#========================================================================================================================\\

def Check_For_Sale_Code(sale_code: int):
    cntrl:bool = True
    if(ope.eq(sale_code, Central.current_erp_sale_code())): 
        print('-> Sale Code is OK!\n✔ Internal Control: %s\n' %cntrl); pass
    else:
        Storage.master_status(False, 'set'); cntrl = bool(False)
        print("Sale Code Comparison: %s :: %s" %(sale_code, Central.current_erp_sale_code()))
        print("Sale Code is NOT OK!\nInternal Control: %s\n" %cntrl)
        clog.error(msg="The sale code isn't the same for [NOTASSAIDAS] and [VENDAS]".upper())
        clog.debug(msg='------------------------------------------------------------------------------')
    return cntrl


def Check_For_Sale_Value(
        database_final_value: int|float, 
        record_output:bool = False, 
        difference:int|float = 0):
    
    cntrl:bool= True
    if(ope.eq(database_final_value, Central.final_sale_value())):
        print('-> Sale Value is OK!\n✔ Internal Control: %s\n' %cntrl)
    else:
        print("Final Sale Value Comparison: %s :: %s ↴" 
              %(database_final_value, Central.final_sale_value()))
        
        calc = Tolerance(Central.final_sale_value(), database_final_value, record_result= record_output)
        
        clog.info(msg='The Comparison Between Tolerance and final value has been verified!'.upper())
        clog.info(msg='------------------------------------------------------------------------------')
        if(calc is False):
            Storage.master_status(False, 'set'); cntrl = bool(False)
            print("\n-> Sale Value is NOT OK!\nInternal Control: %s\n" %cntrl)
            clog.error(msg='The final value between processes are not matching!'.upper())
            clog.debug(msg='------------------------------------------------------------------------------')
        else: print('-> Sale Value is OK!\n✔ Internal Control: %s\n' %cntrl)
    
    # Check for the differences value from final sale amount has recorded in the database...
    if(ope.eq(difference, Central.difference_from_value()) 
       or (Tolerance(difference, Central.difference_from_value()) is True)):
        print('-> Difference from Sale Value is OK!\n✔ Internal Control: %s\n' %cntrl)
    else: 
        print("Difference from Sale Value Comparison: %s :: %s" 
              %(Central.difference_from_value(), difference))
        Storage.master_status(False, 'set'); cntrl = bool(False)
        print('-> Difference from Sale Value is NOT OK!\nInternal Control: %s\n' %cntrl)
    return cntrl


def Check_For_Tax_DocNumber(fiscal_doc: int|str):
    cntrl:bool = True
    if(ope.eq(fiscal_doc, Central.current_nfce_number()) 
       or (ope.eq(fiscal_doc, str(Central.current_nfce_number())))): 
        print('-> Tax Document Number is Ok!\n✔ Internal Control: %s\n' %cntrl); pass
    else:
        Storage.master_status(False, 'set'); cntrl = bool(False)
        print("Tax Document Code: %s :: %s" %(fiscal_doc, Central.current_nfce_number()))
        clog.error(msg="The Fiscal Document Number isn't the same for [NOTASSAIDAS] and [VENDAS]".upper())
        clog.debug(msg='------------------------------------------------------------------------------')
    return cntrl


def Check_For_Client_Code(customer_ident:object, cpfCnpj:bool = True):
    cntrl:bool = True
    element = Central.current_cpf_cnpj() if(cpfCnpj is True) else Central.customer_code()
    print("Comparing 'element' to the 'identification' -> %s :: %s" %(element, customer_ident))

    if((ope.eq(customer_ident, element)) 
       or (element in customer_ident if(isinstance(customer_ident, tuple)) else (int(1), ))):
        print('-> Customer Ident. is OK!\n✔ Internal Control: %s\n' %cntrl); pass
    else:
        Storage.master_status(False, 'set'); cntrl = bool(False)
        print("Look at the Comparion between the Customer Properties: %s :: %s" %(customer_ident, element))
        print("Customer Identification is NOT OK!\nInternal Control: %s\n" %cntrl)
        clog.error(msg="The customer identification doesn't correspond with data processing!".upper())
        clog.debug(msg='------------------------------------------------------------------------------')
    return cntrl


# CHECK FOR THE ALLOWED TOLERANCE BETWEEN THE FINAL SALE FROM DATABASE AND THE FINAL SALE OF THE SYSTEM PROCESS ::
def Tolerance(procss_value:float, db_value:float= 0.0, return_values:bool= False, record_result:bool= False):
    # Set up iguality between those proerties:
    procss_value = round2(procss_value); db_value = round2(db_value)
    print("\nCOMPARING (%s) TO THE TOLERANCE..." %db_value)
    tolerance: float = 0.01; print('Tolerance: %s' %tolerance)
    margin: tuple = (round((procss_value + tolerance), 2), round((procss_value - tolerance), 2))
    print('Margin: %s' %(margin,))
    result:bool = True if((db_value in margin) or (ope.eq(procss_value, db_value) is True)) else False
    print('Comparison Result: %s' %result)

    if(((ope.ne(procss_value, db_value)) and (db_value in margin) is True) and (record_result is True)): 
        Save_Decinal_Difference(procss_value, db_value)
    return result if(return_values is False) else margin


def Save_Decinal_Difference(value1:int|float, value2:int|float, sangria:bool= False):
    paymnt_way = Payment.current_paymnt_on_use()
    if(ope.eq(paymnt_way, 'DIN')): paymnt_way = 'cashback'
    elif(ope.eq(paymnt_way, 'CHQ')): paymnt_way = 'check'
    elif(ope.eq(paymnt_way, 'CRE')): paymnt_way = 'customer_payment'
    elif(paymnt_way in ('CRT', 'TEF')): paymnt_way = 'credit_card'
    elif(ope.eq(paymnt_way, 'BNC')): paymnt_way = 'bank_transfer'
    elif(ope.eq(paymnt_way, 'PIX')): paymnt_way = 'pix'
    else:
        if(sangria is False):
            log.info('\n', also_console=True); log.error(msg='...')
            clog.error("\nIn <Cashier_Adjustment> the `arg` [payment_way] cannot be Null or None!")
            clog.error("\nCheck the @property Centralizer.payment_on_use.")
            raise Exception()
        else: print("-> Has found difference between cashier content and database cashier amount!")

    remainder:float= round(ope.sub(value1, value2), 4)
    Storage.cashier_adjustment(remainder, 'set')
    print('\nRemainder value <%s> has been storage in the @property STORAGE.cashier_adjustment' %remainder)
    print("This value wiil be used to adjust the cashier amount by available payment method...")
    yaml_file = ExternalFile.read_file()
    ExternalFile.update_file(yaml_file['cashier_adjustment'], paymnt_way, remainder, set= False, add= True)
    ExternalFile.write_on_file(yaml_file)
    print('\n'); ExternalFile.print_file(yaml_file)
    return


def Conference_of_the_Closing_Cashier():
    # It will be writen...
    return


def Store_Data_Sale():
    print("\n💬 Recording Data in the STORAGE Data Group!".upper())
    # Like we work with @property buitl-in method to the paython programs, this process bellow requires
    # to be does an aliase function attribute. To set up a value to the <class> Centralizer properties
    # demands an intermediator between the value and their destination. 

    Storage.last_customer_code(Central.customer_code(), 'set')
    Storage.last_customer_ident(Central.current_cpf_cnpj(), 'set')
    Storage.last_sale_code(Central.current_erp_sale_code(), 'set')
    Storage.last_sale_value(Central.final_sale_value(), 'set')
    Storage.last_sale_difference(Central.difference_from_value(), 'set')
    Storage.last_sale_status(Central.current_sale_status(), 'set')
    Storage.last_fiscal_document(Central.current_nfce_number(), 'set')

    print("📝 Recording data...")
    print("\nLast Customer Code: %s" %Storage.last_customer_code().__getitem__(-1) +
          "\nLast Customer Identification: %s" %Storage.last_customer_ident().__getitem__(-1) + 
          "\nLast Sale Code: %s" %Storage.last_sale_code().__getitem__(-1) + 
          "\nLast Sale Value: %s" %Storage.last_sale_value().__getitem__(-1) +
          "\nLast Sale Difference: %s" %Storage.last_sale_difference().__getitem__(-1) +
          "\nLast Sale Status: %s" %Storage.last_sale_status() .__getitem__(-1)+
          "\nLast Fical Document: %s"  %Storage.last_fiscal_document().__getitem__(-1))
    return

#\\... END OF LIBRARY ::
