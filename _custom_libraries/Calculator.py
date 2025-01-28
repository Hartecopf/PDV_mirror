
# SETTINGS 

# -> Project Libraries ::
from SystemConfig import PDVConfig
from input.ConfigLoader import PratesConfig
from Base import ExternalFile, Payment, Cashier
from Base import Centralizer as Central, Storage

# -> Built-in Modules and Robot Modules ::
import math
import operator as ope
from builtins import len
from datetime import date
from random import randint as rint
from robot.api.deco import keyword, library
from time import localtime as lt, strftime as st
from utilities.ColorText import log, logger4, logger5

# -> Custom Modules has created to the Porject ::
from utilities.TextFormater import *
from utilities.AbntRound import round2

CaLog1 = logger4()
CaLog2 = logger5()
    

@library(scope='GLOBAL', version='14.0', auto_keywords=False, doc_format='reST')
class Calculator:
    """
    `Calculator`

    `<class>` Calculator.py Library Scope has been created to calculate mathmatical
    operations  for  using on Robot  Framework. Its properties include the
    math module, operator module and all components of  them. The keywords
    has  been  written to  calculate  the values passed like parameters to
    module ``def`` that will return the operations result\n
    """

    def __init__(self):
        self.current_sale_value: float = 0
        self.product_price_offer: float = 0
        self.all_discount: float = 0
        self.all_addition: float = 0
        return

    #======================================================================================================//
    # CONTROLLER'S KEYWORDS ::
    #------------------------------------------------------------------------------------------------------\\
    #  -> These keywords gives the results processed during the sale execution using  the value
    # ... of  the  internal  controller's variables. For example, to  consult which the final
    # ... result that a variable received during its course, one of these keywords bellow can
    # ... be called by the robot framework request returning the solicited information.
    #======================================================================================================//
    
    @keyword(name='Check For Uncompleted Cashiers Event Type Sangria')
    def Uncompleted_Cashiers_Event(self) -> int:
        if(Central.sangria_status_is_open() is True):
            print("There is an uncompleted cashier event type 'Sangria'!")
            return int(1)
        elif(Central.cancelling_sale_status() is True):
            print("There is an uncompleted cashier event type 'Cancelling Sale'!")
            return int(2)
        else: CaLog1.info(msg="\n\nCashier's event are Ok!"); return int(0)
    
    @keyword(name='Check For The Cashier Events Type Sangria')
    def Check_For_Internal_Counter(self):
        if(Central.sangria_counter_controller() is True):
            event_type = ('CASH' 
                if(PratesConfig.reader().get('cash_event') is True) 
                else 'CHECK')
            this_amount = PratesConfig.reader().get('value_extracted')
            Calculator.Remotion_From_Cashier_Amount(self, this_amount, event_type)
            CaLog1.info("\nThe cashiers amount has been recovered!")    
        else: print("Internal Counter For Cashiers Event is Ok!")

    @keyword(name='Sales Counter')
    def Sale_Counter(self, add:bool = True):
        calc = (ope.sub(Cashier.qnt_sales(), 1) 
                if((add is False) and (Cashier.qnt_sales() > 0)) 
                else ope.add(Cashier.qnt_sales(), 1))
        Cashier.qnt_sales(calc, 'set')
        yaml_file = ExternalFile.read_file()
        ExternalFile.update_file(yaml_file, 'sales_quantity', calc)
        ExternalFile.write_on_file(yaml_file)
        pass

    @keyword(name='Add Amount To The Current Sale')
    def Add_Element(self, products_price: int|float):
        """
        **DOCUMENTATION:** ``Calculator``

        THIS KEYWORD APPLIES THE VALUE PASSED AS AN ARGUMENT OR PARAMETER TO THE
        FUNCTION METHOD, STORING THE ELEMENTS IN THE THE INTERNAL DATA STRUCTURE
        OF THE CLASS Calculator.py"""

        Central.list_of_product_price(products_price, 'set')
        print(f'products_price = {Central.list_of_product_price()}')
        return
    
    @keyword(name='Remove Amount From Current Sale')
    def Remove_Element(sefl, last:bool=True, amount:int|float = 0):
        def log_output():
            for i in range(Central.list_of_product_price().__len__()): 
                print("[%s]: %s" %(i, Central.list_of_product_price().__getitem__(i)))
        
        # /// FIRST CLAUSE ::
        if(last is True):
            Central.list_of_product_price().pop(-1)
            print("\n❌ The last index from list range has been removed!" +
                  "\n\n👁‍🗨 Look at the new sequence so than:")
            log_output()
        # /// SECOND CLAUSE ::
        elif((last is False) and (ope.gt(amount, 0))):
            Central.list_of_product_price(-amount, 'set')
            print("\n❗ The <list> Ce.list_of_products_price has been extended for one" +
                  " negative value according to the <int|float> amount has informed as argument." +
                  "\n\n👁‍🗨 Look at the new sequence so than:")
            log_output()
            pass
        # /// THIRD CLAUSE FOR EXCEPTION TRATEMENT ::
        else:
            log.info('\n', also_console=True); log.error('...')
            CaLog1.error("\n[Calculator Excepetion]")
            CaLog1.warning("No valid argument has been passed as argument to this function.")
            pass
        return
        
    @keyword(name='Show The Current Sale Value')
    def Logger_Current_Sale(self, field_len:int=59):
        total_calc = math.fsum(Central.list_of_product_price())
        total_calc = '{:.2f}'.format(total_calc)
        msgformated = dlmt_space(field_len, 
                        (f"• Sale Value: {total_calc}", 
                        f"QTY. Items: {str(Central.list_of_product_price(gt_log= True).__len__())}"))
        print(msgformated)
        #CaLog1.warning(msg=f"• Sale Value: {total_calc}")
        CaLog1.warning(msg=msgformated)

    @keyword(name='Get The Current Sale Value')
    def Current_Sale(self, numeric_type:bool=False):
        """
        **DOCUMENTATION:** ``Calculator``

        THIS KEYWORD WILL RETURN TO THE ROBOT'S ORDER, THE CURRENT SALES VALUE
        REGISTERED  UNTIL THE CURRENT MOMENT WHEN  YOUR  INSTANCE IS CALLED IN
        RUNTIME."""
        
        total_calc = math.fsum(Central.list_of_product_price())
        return '{:.2f}'.format(total_calc) if(numeric_type is False) else round2(total_calc)
    
    @keyword(name='Restore The Sale Properties')
    def Retore_Sale_From_Storage(self):
        print('\nRESTORE!\n--------')
        Central.products_for_sale().clear()
        print("@property: Centralizer.products_for_sale -> %s" %(Central.products_for_sale(),))
        self.all_addition = 0; self.all_discount = 0
        rplc = Storage.restore_sale_properties(); Central.products_for_sale(rplc, 'set')
        print("\nThe old dictionary of products has launched to the sale is restored!")
        print("Look at the new @property self.Cetralizer.products_for_sale:\n")
        for elem in Central.products_for_sale().keys():
            print("properties in '[%s]': %s" %(elem, Central.products_for_sale().__getitem__(str(elem)),))
            print("-> has been replaced to: %s" %(Storage.restore_sale_properties().__getitem__(str(elem)),))
            create_line(80, char='_', cmd='print')
        pass

    @keyword(name='Calculate The Final Sale Value')
    def Calc_The_Final_Sale_Value(self, check_for_pay_blocked:bool = False, compute_difference:bool = False):
        internal_sale_value: float = 0

        # EXTRACT ITEMS FROM <dict> 'self.Manager.products_for_sale' ::
        print('Products for sale:'.upper())
        print('-----------------')
        list_of_prices = list()
        for elem in Central.products_for_sale().keys():
            print("product in '[%s]': %s" %(elem, Central.products_for_sale().get(str(elem))),)
            replace:dict = Central.products_for_sale().get(str(elem))
            list_of_prices.append(replace['prod_price'])
        print("Products computed in this process: %s" %len(list_of_prices))

        #===============================================================================================================//
        # CHECK POSSIBLE MODIFIERS IN THIS CURRENT SALE ::
        # THIS PROCESS APPLIES THE DIFFERENCE IN THE SALE VALUE ACCORDING TO THE PAYMENT METHOD AND ITS MODIFICATORS.
        # WITHOUT MODIFICATIONS TO THE PAYMENT METHOD, NOTHING HAPPENS TO THE SALE VALUE. ON THE OTHER HAND, IF THERE
        # IS A VALID MODIFIER SUBSCRIBED BY THE PAYMENT METHOD IN USE, ITS AMOUNT WILL BE APPLIED TO THE FINAL AMOUNT 
        # OF THE SALE IN SUCH A WAY THAT WE CAN COMPARE THE TWO VALUES.
        #===============================================================================================================\\
        total_sale = round(math.fsum(list_of_prices), 4); print("\n-> TOTAL SALE VALUE: %s" %total_sale)
        can_apply = (Calculator.Check_For_Payment_Modifiers(self, total_sale, calculate_modifer= False)
                     if (check_for_pay_blocked is True) else True)
        
        if((can_apply is True) and ((Central.customer_discount() > 0))):
            print('\nCUSOMTER DISCOUNT: %s\n-----------------------' %Central.customer_discount())
            CaLog1.warn(msg="""\nThis  Customer has a percentage  discount on their registration!
            \rThe value of %s was applied to this sale as a customer discount!\n""" %Central.customer_discount())
            values = Calculator.Customer_Discount_Func(self, e_total= total_sale)
            CaLog1.critical(msg='===========================================================')
            CaLog1.critical(msg='               DISCOUNT PERCENTAGE BREAKDOWN               ')
            CaLog1.critical(msg='-----------------------------------------------------------')
            CaLog1.critical(msg='Sale Value:                                        {:.2f}'.format(values['amount']))
            CaLog2.warning( msg='Prices Sum:                                        {:.2f}'.format(values['prices_sum']))
            CaLog2.warning( msg='Discount Ratio:                                    {:.2f}'.format(values['ratio']))
            CaLog1.critical(msg='Discount Not Ratio:                                {:.2f}'.format(values['not_ratio']))
            CaLog1.info(    msg='Remainder:                                         {:.2f}'.format(values['others']))
            CaLog1.critical(msg='-----------------------------------------------------------')
            CaLog1.critical(msg='Adjustment:                                        {:.2f}'.format(values['remainder']))
            CaLog1.critical(msg='Process Discount Value:                            {:.2f}'.format(values['dsct_value']))
            self.all_discount = ope.add(values['dsct_value'], ope.sub(math.fsum(Central.list_of_product_price()), total_sale))
            self.all_discount = round2(self.all_discount)
            CaLog2.debug(   msg='Sum Of Discount Value:                             {:.2f}'.format(self.all_discount))
            internal_sale_value = values['real_value']

        else:
            print('\nNO CUSOMTER DISCOUNT TO CALCULATE!\n')
            for t in range(len(list_of_prices)):
                print("'temp_list_of_prices [%s]': %s" %(t, list_of_prices[t]))
            rplc:float = math.fsum(list_of_prices); internal_sale_value = round(rplc, 4)
        
        # 1. CONSIDER ANOTHER SALE PROPERTIES BEFORE CLOSING OF THE FINAL SALE VALUE ::
        # 2. CHECK FOR DIFFERENCE VALUE TO USE FOR CASHBACK PAYMENT METHOD ::
        print_clause:bool = False
        sale_value, self.all_addition = (
            Calculator.Check_For_Payment_Modifiers(self, 
                final_sale_value= internal_sale_value, 
                calculate_modifer= True))
        Central.final_sale_value(sale_value, 'set')
        new_sale_value, difference = Calculator.Set_And_Calc_Difference(Central.final_sale_value())
        if((compute_difference is True) and (ope.gt(Cashier.total_cashback_payments(), difference))):
            print_clause = True
            Central.final_sale_value(round2(ope.sub(new_sale_value, difference)), 'set')
            Central.sale_value_with_diff(new_sale_value, 'set')
            Central.difference_from_value(difference, 'set')
            print("\nTHE PROCESS OF <func> Set_And_Calc_Difference" +
                  " HAS RESULTED IN: %s" %Central.final_sale_value())
            print("LOOK AT THE ATTRIBUTES BELLOW:" +
                  "\n@var new_sale_value: %s\n@var difference: %s" %(new_sale_value, difference))
        else: pass

        # SALE PROPERTIES AND THEIR RESPECTLY VALUES ::
        Central.final_sale_value(round2(Central.final_sale_value()), 'set')
        print("self.Manager.final_sale_value: %s" %(Central.final_sale_value(),))
        CaLog1.critical(     msg='===========================================================')
        CaLog1.critical(     msg='                     FINAL SALE VALUE                      ')
        CaLog1.critical(     msg='-----------------------------------------------------------')
        CaLog1.debug(        msg='Total:                                             {:.2f}'.format(Central.final_sale_value()))
        CaLog1.critical(     msg='Discount:                                          {:.2f}'.format(self.all_discount))
        if(ope.gt(self.all_addition, float(0))):
             CaLog1.error(   msg='Addition:                                          {:.2f}'.format(self.all_addition)) 
        else:CaLog1.critical(msg='Addition:                                          {:.2f}'.format(self.all_addition))
        if((compute_difference is True) and (print_clause is True)):
            CaLog1.critical( msg='-----------------------------------------------------------')
            CaLog1.warning ( msg='Amount Entered:                                    {:.2f}'.format(new_sale_value))
            CaLog1.critical( msg='Difference:                                        {:.2f}'.format(difference))
        CaLog1.critical(msg='===========================================================\n')
        return True


    @keyword(name='Check For Card Taxes Or Debits')
    def Check_For_Another_Taxes(self, oper_code:int, product_card_code:int) -> None:
        print("📊 Checking for card code properties to the card option: %s -> %s" %(oper_code, product_card_code))
        prop:dict = Calculator.Calculate_Card_Taxes(self, oper_code, product_card_code, Central.final_sale_value())
        if(Payment.current_paymnt_on_use() in ('CRT', 'TEF')):
            CaLog1.critical(msg="===========================================================")
            CaLog1.info(    msg='              ► INFERENCE FOR CARD MOVEMENT                ')
            CaLog2.warning( msg="   This Product Type Card has Taxes or Debits to compute   ")
            CaLog1.critical(msg='-----------------------------------------------------------')
            CaLog1.critical(msg="Operational Code:              %s" %prop['ope_code'])
            CaLog1.critical(msg="Product Card Code:             %s" %prop['card_prod_code'])
            CaLog1.critical(msg="Replace Card Taxes?            %s" %prop['replace_taxes'])
            CaLog1.critical(msg='-----------------------------------------------------------')
            CaLog1.warning( msg="Sale Vale Withou Taxes:        %s" %Central.final_sale_value())
            CaLog2.warning( msg="Taxed Sale Value:              %s" %prop['audited_card_vle'])
            CaLog1.info(    msg="Final Sale Value:              %s" %prop['sale_value'])
            if(ope.gt(prop['card_taxes'], float(0))):
                  CaLog2.critical(msg="Card Taxes:                    %s" %prop['card_taxes'])
            else: CaLog1.critical(msg="Card Taxes:                    %s" %prop['card_taxes'])
            if(ope.gt(prop['ope_taxes'], float(0))):
                  CaLog2.critical(msg="Ope. Card Taxes:               %s" %prop['ope_taxes'])
            else: CaLog1.critical(msg="Ope. Card Taxes:               %s" %prop['ope_taxes'])
            if(ope.gt(prop['all_taxes'], float(0))):
                  CaLog1.error(   msg="Taxes Total Amount:            %s" %prop['all_taxes'])
            else: CaLog1.critical(msg="Taxes Total Amount:            %s" %prop['all_taxes'])
            CaLog1.critical(msg="===========================================================\n\n")
            Central.final_sale_value(round2(prop['sale_value']), 'set')
        else:
            print("\nThere is a problem with the payment method has informed. Check for Unique Key and try again.")
            raise ValueError()
        return
    

    # STANDARD CUSTOMER DISCOUNT TREATMENTS AND OTHER VALUE MODIFICATORS FOR SALE PRODUCTS ::
    def Check_For_Payment_Modifiers(self, final_sale_value:float, calculate_modifer:bool = True) -> bool | tuple:
        paymnt:str = Payment.current_paymnt_on_use()
        # Isoled Solution ::
        def Find_and_Get() -> dict:
            for elem in Payment.payment_ways().keys():
                paymnt_attr:dict = Payment.payment_ways().get(elem)
                if(ope.eq(paymnt, paymnt_attr['unq_key'])): 
                    break
                else: continue
            return paymnt_attr
        modifier = Find_and_Get()
        
        print("\nPAYMENT MODIFIERS:\n------------------")
        #print('modifier: %s\n' %modifier)
        for elem in modifier.keys():
            print("• [%s]: %s" %(elem, modifier[elem]))
        can_apply_modifer:bool = True; sale_value: float = 0

        if((modifier['block_dscnt'] is True)
           and ((modifier['min_dscnt_value'] is None) 
                or (modifier['min_dscnt_value'] == 0))): can_apply_modifer = True
        
        elif((modifier['block_dscnt'] is True) and (modifier['min_dscnt_value'] > 0)):
            can_apply_modifer = True if final_sale_value >= modifier['min_dscnt_value'] else False
        else: pass
        
        if(calculate_modifer is False): 
            print("🔧 Exiting from method with the clause value 'can_apply_modifier' to this payment: %s"%can_apply_modifer)
            return can_apply_modifer

        #===============================================================================================================//
        # THIS STEP OF OUR CODE REQUIRES THAT WE MAKE THE COMPARISON BETWEEN THE GENERAL VALUE OF THE MODIFIERS AND
        # THE MODIFIER APPLIED WITH THE MATHEMATICAL FUNCTION 'Ratio'. A MODIFIER IS EXTRACTED FROM THE SETTINGS OF
        # THE DATABASE WHERE THE PAYMENT METHODS ARE STORED. WHENEVER THE PAYMENT METHOD HAS A MODIFIER, THIS ELEMENT
        # MUST BE CONSIDERED IN THE FINAL VALUE OF THE SALE.
        #===============================================================================================================\\
        if((modifier['apply_addt'] is True) 
            and (modifier['additional_value'] is not None
                and modifier['additional_value'] > 0)):
            # -> This method has called bellow obtains the final value of the sale and calculates it according
            # to the modifiers available in the current payment method.
            sale_value, additional_value = Calculator.Percent_Addition(self,
                original_value= final_sale_value, 
                addition= modifier['additional_value'], 
                return_add_value= True)
            # Ouput...
            CaLog1.critical(msg='-----------------------------------------------------------')
            CaLog2.info(f"{expand(size=6)}► This Payment Method has an addition percentage".upper())
            CaLog2.info(f"{expand(size=12)}as modifier to the payment amount!""".upper())
            print('\n► ADDITIONAL VALUE FOR THIS CURRENT SALE SHOULD BE: %s' %additional_value)
            print('► FINAL RESULT FOR THIS PROCESS SHOULD BE: %s' %sale_value)
            ratio_value = Calculator.Ratio_Function(self, modifier= modifier['additional_value'], addt= True)
            print('\nRATIO VALUE TO THE PAYMENT MODIFIERS: %s' %ratio_value)
            
            remainder: float = 0
            if(ope.ne(sale_value, ratio_value)):
                remainder = round(ope.sub(sale_value, ratio_value), 4)
                print("\nThe Mathematical Processing of the Payment Modifiers resulted in the difference between two possible" +
                "\nvalues which are: General Value of the Modifier -> [%s] and its application as a 'Ratio' function. This is" %remainder +
                "\nthe result of the processing calculation made according to the payment method modifier, which may be an" +
                "\naddition or subtraction process.")
            else: print("\nThe Mathmatical Processing of the Payment Modifiers match!")
            print("\nMODIFIERS APPLICATION RESULT:\nFinal Sale Value: %s\nAdditional Value: %s" %(sale_value, additional_value))
        else: sale_value= final_sale_value; additional_value= 0
        return (sale_value, additional_value)


    def Calculate_Card_Taxes(self, 
        ope_code:int, 
        card_prod_code:int, 
        sale_value:float) -> dict:
        
        print("💳 Available card code options:")
        for k in Payment.card_taxes().keys(): 
            print("🗝 [%s]: 💳 %s" %(k, Payment.card_taxes().__getitem__(k)))
        
        def find_and_get() -> dict:
            print("\n🔍... Looking for card: %s -> %s" %(ope_code, card_prod_code))
            for k in Payment.card_taxes().keys():
                iitem:dict = Payment.card_taxes().__getitem__(k)
                
                if((ope.eq(iitem.get('ope_code'), ope_code))
                    and (iitem.get('prod_code'), card_prod_code)):
                    print("\n💡 The Card Code has been found!" +
                    "\n• Card Properties: 🔑 [%s]: 💳 %s" %(k, iitem))
                    break
                else: iitem.clear(); continue
            return iitem
        
        #===============================================================================================================//
        # 1. EXPLORE AND GET CARD PROPERTIES;
        # 2. READ SYSTEM CONFIG AND GET THE PARAMENTER OF CONTROL TO THIS CALCULATION PROCCESS;
        # 3. EXECUTE THE FINAL CALC ACCORDING  TO  THE  TAXES  REPLACEMENT FOR AN ACTIVED PARAMETER ON 
	    #    ... PDV SYSTEM SETTINGS. THIS PARAMETER IS A FUNCTIONS DELIMITER TO THE CLAUSES HAS WIRTEN BELLOW;
        #--------------------------------------------------------------------------------------------------------------\\
        # [ MATHMATICAL RATIO ] ↴
	    # -> Fist Clause :: ((sale_value + card_tax_value) - (ope_tax_value + card_tax_value)) 
	    # -> Second Clause :: (sale_value - (card_tax_value + ope_tax_value))
        #===============================================================================================================//
        card = find_and_get()
        print("\n🧾 Card Properties: %s" %(card,))
        perc_sale_value:float = round(ope.truediv(sale_value, 100), 4)
        card_tax_value = round2(round(ope.mul(perc_sale_value, card['card_tax_value']), 4))
        ope_tax_value = (round2(round(ope.mul(perc_sale_value, card['ope_tax_value']), 4))
            if(ope.eq(card['ope_tax_type'], '%')) else round(card['ope_tax_value'], 2))
       
        # FINISHING ...
        sys_sttg:dict = PDVConfig.Read_System_Config()
        keys_in:dict = sys_sttg.get('function_keys')
        card_config:str = (
            'Actived' 
            if(ope.eq(keys_in.get('OPCOES_RECEBIMENTOCARTAOTAXAACR'), 1)) 
            else 'Disabled')
        
        print("\n\n🧮 Mathmatical Elements:" +
            "\n• Repalce Taxes Amount:            %s" %card_config +
            "\n• Sale Value:                      %s" %sale_value +
            "\n• Card Tax Value %s:                %s" %('%', card['card_tax_value']) +
            "\n• Operational Tax Value:           %s" %(card['ope_tax_value'],) +
            "\n• Percentual Unity Of Sale Value:  %s" %perc_sale_value)

        # TAXES EVALUATING ::
        if(ope.eq(keys_in.get('OPCOES_RECEBIMENTOCARTAOTAXAACR'), 1)):
            print("\n❕ Performing replacement of Card Taxes...")
            sale_value = round2(round(ope.add(sale_value, card_tax_value), 4))
            audit = round2(ope.sub(sale_value, round(ope.add(ope_tax_value, card_tax_value), 4)))
            print("💱 Card Audit: (%s - (%s + %s)) = %s" %(sale_value, ope_tax_value, card_tax_value, audit))
        else:
            print("\n❕ Apllying the Card Taxes...")
            audit = round2(ope.sub(sale_value, round(ope.add(card_tax_value, ope_tax_value), 4)))
            print("🧮 Card Audit:\n(%s - (%s + %s) = %s" %(sale_value, card_tax_value, ope_tax_value, audit))
            
        all_taxes = round2(ope.add(card_tax_value, ope_tax_value))
        print("\n💱💲 Final Calc has done according to the card properties: %s" %sale_value)
        return {
            'ope_code':ope_code, 'card_prod_code':card_prod_code, 'sale_value':sale_value, 'audited_card_vle':audit, 
            'replace_taxes':card_config, 'card_taxes':card_tax_value, 'ope_taxes':ope_tax_value, 'all_taxes':all_taxes}


    def Customer_Discount_Func(self, e_total:float= 0):
        #===============================================================================================================//
        # AT FIRST, WE APPLY THE CUSTOMER'S DISCOUNT FOR SALES AND THEN COMPARE THE RESULTS AT THE END OF THIS FUNCTION.
        # MATHEMATICAL PRECISION MAY RESULT IN DIFFERENT VALUES FOR EACH PRODUCT PRICE CASE. FOR THIS REASON, WE COMPARE 
        # AND DEFINE THE FINAL SALE VALUE AFTER APPLYING THE DISCOUNT AS APPORTIONMENT. THE COMPARISON BETWEEN THE 
        # MATHEMATICAL FUNCTION ``RATIO()`` AND ITS OPPOSITION WHICH IS CALLED ``NOT RATIO`` GIVES US THE CALCULATION OF 
        # THE REAL VALUE. THIS IS THE REASON WE USE A MAIN PROCESS AND A SUBPROCESS WHERE THEY DO THE SAME THING BUT IN 
        # DIFFERENT WAYS.
        #===============================================================================================================\\

        not_ratio: float = 0; ratio: float  = 0; remainder: float = 0; real_value: float = 0
        print('APPLYING THE CUSTOMER DISCOUNT IN THE PRODUCTS FOR SALE...')
        main_calc_list= list(); sub_list = list(); cust_dsct= Central.customer_discount()
        print("Block discount/modifiers to the products on promotion? %s" %Central.block_discount_for_promotion())

        #===============================================================================================================//
        # THIS NEXT STATEMENT REPRESENTS OUR LIST OF PRODUCTS RELEASED FOR SALE. The <main_list> STORES THE PRODUCTS THAT
        # DO NOT HAVE MODIFIERS IN THE REGISTRATION. ON THE OTHER HAND THE <sub_list> WILL STORE ALL PRODUCTS THAT HAVE
        # MODIFIER IN ITS REGISTRATION EXTRACTED FROM THE DATABASE IN USE.
        #---------------------------------------------------------------------------------------------------------------\\
        #-> @property Centralizer.discount_to_modifiers is a delimiter!
        #-> 'main_list' store the products that can receive discount
        #-> ... while the 'sub_list' does just the opposite of that.
        #===============================================================================================================//
        for elem in Central.products_for_sale().keys():
            product = Central.products_for_sale().get(str(elem))
            if(Central.block_discount_for_promotion() is True):
                if product['dsct_status'] is True:                  
                    main_calc_list.append(product['prod_price'])
                else: sub_list.append(product['prod_price'])
            elif(Central.block_discount_for_promotion() is False): 
                main_calc_list.append(product['prod_price'])
        
        print('PRICE TABLE OF PRODUCTS THAT CAN RECEIVE THE DISCOUNT FOR CUSTOMERS:\n')
        for i in range(len(main_calc_list)):
            print('product_list[%s]: %s' %(i, main_calc_list[i]))
        print('____________________________________')
        
        #===============================================================================================================//
        # HERE IS THE DISTRIBUTION OF THE SALES AMOUNT AND THE DISCOUNT PERCENTAGE. IN THIS STEP OF OUR CODE WE DISTRIBUTE
        # THE SALES VALUE ACCORDING TO THE MODIFIERS IN USE. EACH MODIFIER IS COMPUTED IN ITS OWN SPACE AND IS CONSIDERED
        # FOR THE FINAL DATA COMPUTATION VALUE. THAT'S WHY WE ISOLATE ALL PARTS OF THE SALE TO CALCULATE ITS COMPONENTS.
        #===============================================================================================================\\
        
        # 1º STEP ::
        prices_sum = math.fsum(main_calc_list)
        not_ratio, dsct_value = Calculator.Percent_Discount(self, 
                                    original_value= prices_sum,
                                    discount= cust_dsct, 
                                    return_dsct_value= True)
        
        amount = round(ope.add((math.fsum(main_calc_list)), (math.fsum(sub_list))), 4)
        print('\n*Sale Value without any discount: %s' %amount)
        amount = round2(ope.sub(amount, dsct_value))
        print('\n*Sale Value with discount percentage: %s' %amount)
        
        # 2º STEP ::
        ratio, main_calc_list = Calculator.Ratio_Function(self, 
                                    modifier= cust_dsct, 
                                    dsct= True, unique= True, 
                                    return_modf= True, return_new_list= True)
        # 3º STEP ::
        others_prices = round2(math.fsum(sub_list))
        self.all_discount = ope.add(dsct_value, ope.sub(math.fsum(Central.list_of_product_price()), e_total))
        self.all_discount = round2(self.all_discount)

        # ///file/C:/..html OUTPUT
        print("\n==========================================================================================+|SALE MODIFIERS|")
        print("-> Not Ratio Result: %s\n-> Ratio Result: %s\n-> General Discount Value: %s\n-> All Discount: %s\n-> Total Amount: %s" 
              %(not_ratio, ratio, dsct_value, self.all_discount, amount))

        # COMPARE THE RESULT OF THE 'remainder' TO THE TRUE VALUE AND EXTRACT DIFFERNCE BETWEEN THEM ::
        if ope.ne(not_ratio, ratio): 
            remainder = round(ope.sub(ratio, not_ratio), 4)
        else: remainder = float(0)

        #===============================================================================================================//
        # THEN FINALLY WE WILL APPLY THE FINAL CALCULATION PROCESS. AS THE FINAL CALCULATION MUST CONSIDER THE VALUE OF
        # THE SALE WITH DISCOUNT PERCENTAGE AND THE 'sub_list' TO THE FINAL CALCULATION OF THE TOTAL, BOTH VALUES ARE
        # COMPUTED IN THIS STEP, IF THERE IS WHAT TO BE COMPUTED, OF COURSE.
        #===============================================================================================================\\
        real_value = not_ratio
        real_value += math.fsum(sub_list) if len(sub_list) != 0 else 0

        print("-> Difference Value: %s\n-> Remainder Value: %s\n-> *REAL VALUE: %s" %(remainder, others_prices, real_value))
        print("==========================================================================================================//")
        print('\nROUNDED VALUE OF THE SALE: %s' %real_value)

        #===============================================================================================================//
        # ONCE WE MODIFER THE PRICE OF THE PRODUCTS IN THIS STEP OF OUR CODE, IT'S NECESSARY APPLY THIS CHANGING TO THE
        # ORIGINAL DICTIONARY OF PRODUTS FOR SALE! THAT'S REASON OF THIS FUNCTION BELLOW ::
        #===============================================================================================================\\
        Calculator.Update_Products_Price(self, new_prices= main_calc_list)
        return {
            'ratio':ratio, 
            'not_ratio':not_ratio, 
            'remainder':remainder, 
            'real_value':real_value, 
            'prices_sum':prices_sum, 
            'amount':amount, 
            'dsct_value':dsct_value, 
            'others':others_prices}
    
    
    def Ratio_Function(self, 
            modifier: float, 
            addt:bool = False, 
            dsct: bool = False, 
            unique: bool = False, 
            return_modf: bool = True, 
            return_new_list: bool = False):
        
        temp_list: list = list(); local_discount: float = 0
        print("\nAPPLING RATIO() TO THE CURRENT MODIFIER\n---------------------------------------")
        for e in Central.products_for_sale().keys():
            elem = Central.products_for_sale().get(e)
            print(f"DEBUGGIN '{e}' -> {elem}")

            if((dsct is True) and (Central.block_discount_for_promotion() is True) and (unique is False)):
                result = (Calculator.Percent_Discount(self, elem['prod_price'], modifier, return_modf) 
                                                            if (elem['dsct_status'] is True) else elem['prod_price'])
                print("debug of 'result' after calculating the discount: %s" %(result,))
                temp_list.append(result[0]) if isinstance(result, tuple) else temp_list.append(result)
                print(f"debug of @var temp_list_of_prices in len(): {temp_list[-1]}")
                local_discount += result[1] if isinstance(result, tuple) else int(0)
                print("debug _property local_discount: %s" %round(local_discount, 3))

            #===============================================================================================================//
            # The 'unique' items clause assumes that only products with a status of 'True' can receive a percentage discount.
            # This assegure that the price list will contain your original extension. No products price are removed from the
            # range, but the products that contain 'False' status to the new modifiers in their {dsct_status}, receives 0 as
            # value in this new list. That is necessary to assegure the final result of the ratio function without anything
            # changes on 'Centralizer.products_for_sale' <list> range.
            #===============================================================================================================\\
                
            elif((dsct is True) and (Central.block_discount_for_promotion() is True) and (unique is True)):
                result = (Calculator.Percent_Discount(self, elem['prod_price'], modifier, return_modf) 
                                                            if (elem['dsct_status'] is True) else int(0))
                print("debug of 'result' after calculating the discount: %s" %(result,))
                temp_list.append(result[0]) if isinstance(result, tuple) else temp_list.append(result)
                print(f"debug of @var temp_list_of_prices in len(): {temp_list[-1]}")
                local_discount += result[1] if isinstance(result, tuple) else int(0)
                print("debug _property local_discount: %s" %round(local_discount, 3))

            #... This clause ignores product status for discount percentage ::
            elif((dsct is True) and (Central.block_discount_for_promotion() is False)):
                result = (Calculator.Percent_Discount(self, elem['prod_price'], modifier, return_modf))
                print("debug of 'result' after calculating the discount: %s" %(result,))
                temp_list.append(result[0]) if isinstance(result, tuple) else temp_list.append(result)
                print(f"debug of @var temp_list_of_prices in len(): {temp_list[-1]}")
                local_discount += result[1] if isinstance(result, tuple) else int(0)
                print("debug _property local_discount: %s" %round(local_discount, 3))

            #===============================================================================================================//
            # DIFFERENT OF THE ABOVE CLAUSE, THIS STATEMENT MAY APPLY AN ADDITIONAL PERCENTAGE TO THE FINAL SALES VALUE
            # REGARDLESS OF THE CONFIGURATIONS FOR THIS. OUR SYSTEM CONSIDERS AN ADDITIONAL PERCENTAGE AS A DIFFERENT RULE
            # FROM APPLYING A COMMON DISCOUNT.
            #===============================================================================================================\\
            elif(addt is True):
                result = Calculator.Percent_Addition(self, elem['prod_price'], modifier, return_modf)
                print("debug of 'result' after calculating the discount: %s" %(result,))
                temp_list.append(result[0]) if isinstance(result, tuple) else temp_list.append(result)
                print(f"debug of @var temp_list_of_prices in len(): {temp_list[-1]}")
                self.all_addition += result[1] if isinstance(result, tuple) else int(0)
                print("debug _property self.all_addition: %s" %round(self.all_addition, 3))

            elif((dsct is True) and (addt is True)):
                log.info(msg='\n', also_console=True)
                CaLog1.error(msg="Discount and Addition can not be computed in the same time!")
                raise Exception()
            create_line(120, cmd='print')
        
        print('\nNEW LIST OF PRICES AFTER RATIO() FUNCTION:')
        create_line(43, cmd='print')
        for i in range(len(temp_list)):
            print('product_list[%s]: %s' %(i, temp_list[i]))
        return math.fsum(temp_list) if(return_new_list is False) else (math.fsum(temp_list), temp_list)


    def Update_Products_Price(self, new_prices: list):
        #===============================================================================================================//
        # THE PRODUCT PRICE REPLACEMENT OCCURS WHEN THE RATIO FUNCTION SCROLLS THROUGH THE ARRAY IN THE LIST APPLYING THE 
        # DISCOUNT PERCENTAGE, IF ANY. IF THE VARIABLE 'X' IS ACTIVE, THIS ARRAY WILL RECEIVE THE NUMBER 0 AS AN ARGUMENT
        # IN ITS INDEX BOX WHERE THE PRODUCT IS WITH THE DISCOUNT STATUS EQUAL TO 'False'. THIS IS NECESSARY IN SUCH A WAY
        # THAT WE CANNOT ALTER THE PRICE LIST BY REMOVING ITS ELEMENTS. THIS MEANS THAT A PRODUCT WHICH CANNOT RECEIVE A
        # DISCOUNT PERCENTAGE WILL NOT CONTAIN ITS PRICE IN THE ARRAY.
        #===============================================================================================================\\

        index: int = 0; print("\nUPDATING PRODUCTS PRICE%s" %(create_line(26, break_line=True, cmd='return'),))
        for elem in Central.products_for_sale().keys():
            product = Central.products_for_sale().get(str(elem))
            if(Central.block_discount_for_promotion() is True):
                print('Updating price of the product code (%s) to: %s' 
                      %(product['prod_code'], (new_prices[index] if (new_prices[index] != 0) else product['prod_price'])))
                product['prod_price'] = new_prices[index] if (new_prices[index] != 0) else product['prod_price']; index += 1
            elif(Central.block_discount_for_promotion() is False): product['prod_price'] = new_prices[index]; index += 1
            print("@propt. Centralizer.products_for_sale: '%s': %s" %(elem, Central.products_for_sale().get(str(elem))))
            create_line(120, cmd='print')
        return


    def Percent_Discount(self, original_value: float|int, discount: float|int, return_dsct_value:bool = False):
        math_reason = round(ope.truediv(original_value, 100), 4)
        print(f"PRICE: {original_value} / 100: {math_reason}")
        discount_result = round(ope.mul(math_reason, discount), 4)
        print(f"DISCOUNT: ({math_reason} * {discount}) = {discount_result}")
        _final_calc = round(ope.sub(original_value, discount_result), 4)
        print(f"► FINAL CALC: ({original_value} - {discount_result}) = {round2(_final_calc)}")
        if return_dsct_value is False: return round2(_final_calc)
        else: return (round2(_final_calc), round2(discount_result))
    

    def Percent_Addition(self, original_value: float|int, addition: float|int, return_add_value:bool = False):
        math_reason = round(ope.truediv(original_value, 100), 4)
        print(f"PRICE: {original_value} / 100: {math_reason}")
        addition_result = round(ope.mul(math_reason, addition), 4)
        print(f"ADDITION: ({math_reason} * {addition}) = {addition_result}")
        _final_calc = round(ope.add(original_value, addition_result), 4)
        print(f"► FINAL CALC: ({original_value} + {addition_result}) = {round2(_final_calc)}")
        if return_add_value is False: return round2(_final_calc)
        else: return (round2(_final_calc), round2(addition_result))
    

    def Set_And_Calc_Difference(final_value:float|int):
        decimal, interger = math.modf(final_value);    
        decimal = round2(decimal) if(ope.ge(len(str(decimal).split()[0]), 3)) else decimal
        print("\n📝 SPLIT RESULT:\nTnterger Part: %s  Decimal Part: %s" %(int(interger), decimal))
        # Flow control variables ::
        delimiter:int = 2; addition:float = 0.0; count:int = 0; decimal_diff = float(0)
        while (ope.lt(delimiter, interger)):
            count = ope.iadd(count, 1); ctrl:int = rint(0, 9)
            operator = int(3) if((ope.ne(ope.mod(count, 2), 0)) and (ope.ge(ctrl, int(6)))) else int(2)
            addition = ope.iadd(delimiter, operator)
            delimiter = addition
        print("Has been performed %sº ocurrences of addition operation from sale value!" %count +
              "\n\n🧮 Final result of this process: @var calc: %s" %addition)
        if(ope.ne(addition, int(0))):
            if(ope.gt(decimal, float(0))):
                decimal_diff = 1 if(ope.gt(round(decimal, 3), float(0.50))) else float(0.50)
                addition = ope.add(addition, decimal_diff) if(ope.lt(addition, final_value)) else addition
            else: print("The final sale result as matched in an exactly amount. No difference computing is needed!")
        else: print("◎ The initial delimiter value is biggest than final sale value!"); addition = delimiter
        print("FULL AMOUNT: %s\nDIFFERENCE: %s" %(addition, round2(ope.sub(addition, final_value))))
        return (addition, round2(ope.sub(addition, final_value)))
        

    @keyword(name='Clear Temporary Sale Modifiers')
    def Clear_List_of_the_Products(self):
        self.all_discount = 0; self.all_addition = 0
        return


    @keyword(name='Get The Final Sale Value After Data Processing')
    def Get_The_Final_Sale_Value(self): return Central.final_sale_value()


    @keyword(name='Get Difference Has Computed From Final Sale Value')
    def Get_Difference_From_Sale_Value(self, dff:bool= False): 
        return Central.sale_value_with_diff() if dff is False else Central.difference_from_value()


    @keyword(name='Calculate List Prices')
    def Calculate_Prices(self, prices_element: list):
        total_calc = math.fsum(prices_element)
        total_calc = round(total_calc, 3)
        return '{:.2f}'.format(total_calc)


    @keyword(name='Calculate The Elements Discount')
    def Discount_for_Element(self, total_value: int|float,
                                discount_percentage: int|float):

        math_reason = ope.truediv(total_value, 100)
        discount_result = ope.mul(math_reason, discount_percentage)
        _final_calc = ope.sub(total_value, discount_result)    
        return round2(_final_calc)


    @keyword(name='Calculate The Elements Addition')
    def Addition_for_Element(self, total_value: int|float, 
                                addition_percentage: int|float):
        math_reason = ope.truediv(total_value, 100)
        addition_result = ope.mul(math_reason, addition_percentage)
        _final_calc = ope.add(total_value, addition_result)    
        return round2(_final_calc)
       

    @keyword(name='Subtraction Operator')
    def Subtraction(self, element_1: int|float, element_2: int|float):
        _calc = ope.sub(element_1, element_2)
        if(type(_calc) != int): return round2(_calc)
        else: return _calc


    @keyword(name='Addition Operation')
    def Addition(self, element_1: int|float, element_2: int|float):
        print("Data Operation:\n%s + %s" %(element_1, element_2))
        _calc = ope.add(element_1, element_2)
        print("Result: %s" %_calc)
        if(isinstance(_calc, float)): return round2(_calc)
        else: return _calc
       

    @keyword(name='Multiplication Operation', types=[int|float, int|float])
    def Mul(self, element_1, element_2):
        _calc = ope.mul(element_1, element_2)
        if(type(_calc) != int): return round2(_calc)
        else: return(int(_calc))
       

    @keyword(name='True Division Operation', types=[int|float, int|float])
    def True_Div(self, element_1: int|float, element_2: int|float):
        _calc = ope.truediv(element_1, element_2)
        if(type(_calc) != int): return round2(_calc)
        else: return(int(_calc))
        

    @keyword(name='Get Length Base Zero')
    def Real_Length(self, _list:list):
        _real_len = len(_list)
        _real_len -= 1
        return(_real_len) 


    @keyword(name='Clear Temporary List')
    def Clear_List(self, _list: list):
        _list.clear()
        return(_list)


    # CASHIER MANAGEMENT
    @keyword(name='Cashier Controller')
    def _cashier(self, 
            keep_on_cashier: bool,    
            add_to_total: bool = False,
            customer_payment: bool = False,
            is_eletronic_payment: bool = False,
            cashback: bool = False,
            chq_pay: bool = False,
            card_pay: bool = False,
            bank: bool = False,
            pix_pay: bool = False, 
            uncomplete_event:bool= False):

        sale_value = Central.final_sale_value()
        print('💲sale_value: %s' %sale_value)
        
        if(cashback is True):
            Cashier.total_cashback_payments(sale_value,'add')
            print('@property Centralizer.total_cashback_payments: %s' 
                  %(Cashier.total_cashback_payments(),))
            Calculator.Set_Data_Output(value= sale_value, pay_type= 'cash')
        
        elif(chq_pay is True): 
            Cashier.total_chq_payments(sale_value,'add')
            print('@property Centralizer.total_chq_payments: %s' 
                  %(Cashier.total_chq_payments(),))
            Calculator.Set_Data_Output(value= sale_value, pay_type= 'check')
        
        elif(customer_payment is True): 
            Cashier.total_customer_payments(sale_value, 'add')
            print('@property Centralizer.total_customer_payments: %s' 
                  %(Cashier.total_customer_payments(),))
            Calculator.Set_Data_Output(value= sale_value, pay_type= 'customer')

        elif(card_pay is True): 
            Cashier.total_credit_card_payments(sale_value,'add')
            print('@property Centralizer.total_credit_card_payments: %s' 
                  %(Cashier.total_credit_card_payments(),))
            Calculator.Set_Data_Output(value= sale_value, pay_type= 'card')
        
        elif(pix_pay is True): 
            Cashier.total_pix_payments(sale_value, 'add')
            print('@property Centralizer.total_pix_payments: %s' 
                  %(Cashier.total_pix_payments(),))
            Calculator.Set_Data_Output(value= sale_value, pay_type= 'pix')
        
        elif(bank is True): 
            Cashier.total_bank_tranference(sale_value, 'add')
            print('@property Centralizer.bank_tranference: %s' 
                  %(Cashier.total_bank_tranference(),))
            Calculator.Set_Data_Output(value= sale_value, pay_type= 'transfer')
        
        elif(uncomplete_event is True):
            Cashier.uncompleted_sales(1, 'add')
            Calculator.Set_Data_Output(pay_type= 'Empty', uncompleted_sale=True)
            print("\nThis sale event has not been conclued!".upper())
            return

        else: 
            print("Invalid explicit argument!\nAt least one payments argument must" +
                  "be passed as argument to this Keyword")
            log.info(msg='\n', also_console=True)
            log.error(msg='...')
            CaLog2.error(
                msg="\nIt's necessary to inform which the payment method\n" + 
                "in usage for this sale finalization!".upper())
            return ValueError()

        #===============================================================================================================//
        # PRATES RESULTS ::
        # OBS: This sequence allow us look the current cashier amount and their properties for different payment ways as
        # well as customer payment, for exmple. Whenever, this showing of data isn't the really cashier control. This
        # incumbence is a responsability of the 'yaml_file' data output!
        #===============================================================================================================\\
        
        # Se o valor recebido deve ser mantido em caixa e armazenado no saldo total de vendas à vista:
        # Exemplo: Dinheiro/Cash & CQH/Check
        if(ope.eq(keep_on_cashier, True) and ope.eq(add_to_total, True)):
            Cashier.total_on_cashier(sale_value, 'add')
            Cashier.total_sales_value(sale_value, 'add')
            Cashier.all_finished_sales(sale_value, 'add')
            Cashier.cashiers_event(1, 'add')
            return

        # Se o valor recebido for um pagamento do tipo crediário e não deve somar no saldo em caixa:
        elif(ope.eq(keep_on_cashier, False) and ope.eq(customer_payment, True)):
            Cashier.all_finished_sales(sale_value, 'add')
            Cashier.cashiers_event(1, 'add')
            return

        # Se o valor recebido for do tipo eletrônico e deve ser mantido no valor total de vendas à vista:
        # Exemplo: Pix (à vista), Cartão TEF/Credit Card, Tranferência Bancária/ Eletronic Tranference.    
        elif(ope.eq(add_to_total, True) and ope.eq(is_eletronic_payment, True)):
            Cashier.total_eletronic_payments(sale_value, 'add')
            Cashier.total_sales_value(sale_value, 'add')
            Cashier.all_finished_sales(sale_value,'add')
            Cashier.cashiers_event(1, 'add')
            return

        # Se o valor recebido for do tipo eletrônico e NÃO deve ser mantido no valor total de vendas à vista:
        # Exemplo: Cartão POS/Credit Card    
        elif(ope.eq(add_to_total, False) and ope.eq(is_eletronic_payment, True)):
            Cashier.all_finished_sales(sale_value, 'add')
            Cashier.cashiers_event(1, 'add')
            return

        # Se nenhuma das opções for contemplada, há um erro de atribuição de valores por tipo de pagamento.    
        else: print("This boolean settings isn't valid!"); return(ValueError)  
       

    @keyword(name='Get The Values On Cashier')
    def _get_cashier_values(self, compare_results:bool= False):
        """
        **DOCUMENTATION** ``Calculator

        THIS  KEYWORD GETS AND RETURNS THE ACTUAL CASH VALUE FOR THE EXACT MOMENT WHEN THIS RESOURCE IS 
        CALLED BY THE ROBOT'S API THROUGTH THE KEYWORD NAMED 'Get The Values On Cashier'.
        ``"""
        ExternalFile.set_file_path(Central.path_cashier_output)
        yaml_file = ExternalFile.read_file()
        value1:float = yaml_file['total_on_cashier']
        value2:float = round2(Cashier.total_on_cashier())
        
        if(compare_results is True):
            compare:bool= True if(ope.eq(value1, value2)) else False
            print("Look at the output file records and @property Centralizer.total_on_cashier:" +
                "\nComparison has made between %s :: %s "%(value1, value2))
            print("Everythyng is OK!") if(compare is True) else print("The results not match!")
            if(compare is True): 
                return value2 if((value2 is not None) and (value2 > 0)) else int(0)
            else: 
                print("\nOBS: ■ There is not equality between the values stored in the" +
                        " <yaml> file and @property centralizer.total_on_cashier.")
                return int(0)
        else: return value2


    @keyword(name='Get Values From Cashierr')
    def _get_values(self, 
            cashback:bool= False, 
            check:bool= False, 
            customer:bool= False, 
            eletronic:bool= False,
            total_sales:bool= False, 
            sales_finished:bool= False, 
            qtde_sales:bool= False, ):
        """
        **DOCUMENTATION** ``Calculator``

        THIS KEYWORD GIVES THE CASHIERS VALUES ACCORDING TO THE BOOLEAN SETTINGS HAS INFORMED AS ARGUMENT 
        TO THIS FUNCTION. WRITTEN ON ROBOT FRAMEWORK. THIS  KEYWORD  HAVE FIVE POSSIBILITIES FOR CONSULT 
        BEING THEY: TOTAL OF CUSTOMER PAYMENTS, TOTAL OF ELETRONIC PAYMENTS, TOTAL CASH SALES, THE QUANTITY 
        OF SALES FINISHED AND HOW MANY MONEY IS IN THE CASHIER. 
        """

        elem:float = 0
        if(cashback is True): elem = "{:.2f}".format(Cashier.total_cashback_payments())
        elif(check is True): elem = "{:.2f}".format(Cashier.total_chq_payments())
        elif(customer is True): elem= "{:.2f}".format(Cashier.total_customer_payments())
        elif(eletronic is True): elem = "{:.2f}".format(Cashier.total_eletronic_payments())
        elif(total_sales is True): elem = "{:.2f}".format(Cashier.total_sales_value())
        elif(sales_finished is True): elem = "{:.2f}".format(Cashier.all_finished_sales())
        elif(qtde_sales is True): elem = f"{Cashier.qnt_sales()}"
        else:
            log.info('\n', also_console=True); log.warn('...')
            CaLog2.warn(f"\n{ValueError()}: At least one parameter is required for this Kyword", html=True)
            raise Exception()
        print("Value has returned: %s" %elem); return elem


    @keyword(name='Cashier Breakdown')
    def Cashier_Breakdown(self):
        # ALISASES TO CLASSES PROPERTIES: 
        nmb_sales = Cashier.qnt_sales()
        total_onCx = '{:.2f}'.format(Cashier.total_on_cashier())
        sles_value = '{:.2f}'.format(Cashier.total_sales_value())
        T_all_sles = '{:.2f}'.format(Cashier.all_finished_sales())
        cust_paymt = '{:.2f}'.format(Cashier.total_customer_payments())
        eltr_paymt = '{:.2f}'.format(Cashier.total_eletronic_payments())

        CaLog1.critical(msg='\n\n===========================================================')
        CaLog1.warning(msg= "                    AUTOMATIONS CASHIER")
        CaLog1.critical(msg='-----------------------------------------------------------')
        CaLog1.warning(msg=f"\nNumber of Sales:                                 {nmb_sales}")
        CaLog1.warning(msg=f"\nThe Cashier Contains:                            {total_onCx}")
        CaLog1.critical(msg= "(Saldo em Caixa)")
        CaLog1.warning(msg=f"\nTotal of Sales Value:                            {sles_value}")
        CaLog1.critical(msg="(Total à Vista)")
        CaLog1.warning(msg=f"\nTotal of All Valid Sales:                        {T_all_sles}")
        CaLog1.critical(msg="(Total de Vendas)")
        CaLog1.critical(msg='===========================================================')
        CaLog1.warning(msg="                        BREAKDOWN:")
        CaLog1.critical(msg='-----------------------------------------------------------')
        CaLog1.warning(msg=f"Total of Customer Payment:                       {cust_paymt}")
        CaLog1.critical(msg='(Total à Prazo)')
        CaLog1.warning(msg=f"\nTotal of Eletronic Payment:                      {eltr_paymt}")
        CaLog1.critical(msg='[PIX + CARTÃO + BANCÁRIA]')
        CaLog1.critical(msg='-----------------------------------------------------------')
        CaLog2.warning(msg=f"Process ended at:                      {date.today()}, {st('%H:%M:%S', lt())}")
        CaLog1.critical(msg='===========================================================')
        return


    @staticmethod
    def Set_Data_Output(value:float= 0, pay_type:str= 'empty', uncompleted_sale:bool= False):
        #===============================================================================================================//
        # OUR CASHIER CONTROL SHOULD BE DONE IN THIS STEP OF THE OUR CODE. HERE ARE ALL METHODS THAT CHECKS AND CONSIDERS
        # THE FINAL RESULT HAS GOT FROM DATABASE IN USE. IS THE VALUES ARE APPROVED FOR THE COMPARISON METHODS, THEIR DATA
        # ARE BE WRITEN TO THE OUTPUT FILE <yaml.file> IN SUCH A WAY THAT WE CAN SAVE AND STORE THIS INFORMATION.
        #===============================================================================================================\\

        # CLAUSE OF SECURITY ::
        pay_ways:tuple= ('cash', 'check', 'customer', 'card', 'pix', 'transfer', 'ticket')
        pay_type = pay_type.lower()
        
        if((ope.ne(pay_type, 'empty')) and (pay_type not in pay_ways)): 
            print('Invalid Argument Combination to this @Keyword')
            raise Exception()
        
        # DATA OUTPUT LOG (html.log) ::
        print('Performing output data updates...\n')
        ExternalFile.set_file_path(Central.path_cashier_output)
        yaml_file = ExternalFile.read_file()
        print('Output file before:'.upper()); create_line(20, cmd='print')
        ExternalFile.print_file(yaml_file); create_line(62, cmd='print')
        
        # SINGULAR CLASUE FOR UNCOMPLETED SALE EVENT ::
        if(uncompleted_sale is True):
            ExternalFile.update_file(yaml_file, 'uncompleted_sale', 1, set= False, add= True)
            ExternalFile.update_file(yaml_file, 
                'total_uncompleted_sales', Central.final_sale_value(), set= False, add= True)
            ExternalFile.write_on_file(yaml_file)
            print('\nOutput file after updating:'.upper()); ExternalFile.print_file(yaml_file)
            return
        
        # GENERAL CASHIERS ATTRIBUTES ::
        ExternalFile.update_file(yaml_file, 'all_the_sales_finished', value, set= False, add= True)
        ExternalFile.update_file(yaml_file, 'sales_quantity', Cashier.qnt_sales())
        ExternalFile.update_file(yaml_file, 'cashiers_event', Cashier.cashiers_event())
        
        # SINGUALR CASHIERS PROPERTIES ::
        if(pay_type in ('cash', 'check', 'ticket')):
            ExternalFile.update_file(yaml_file, 'total_on_cashier', value, set= False, add= True)

        if(pay_type in ('cash', 'check', 'card', 'pix', 'ticket')):
            ExternalFile.update_file(yaml_file, 'total_sales_value', value, set= False, add= True)

        if(pay_type in ('card', 'pix', 'transfer')):
            ExternalFile.update_file(yaml_file, 'total_eletronic_payments', value, set= False, add= True)
        
        # CASHIER BREAKDOWN ::
        if(ope.eq(pay_type, 'cash')): 
            ExternalFile.update_file(yaml_file['payment_methods'], 'cashback', value, set= False, add= True)
        
        elif(ope.eq(pay_type, 'check')): 
            ExternalFile.update_file(yaml_file['payment_methods'], 'check', value, set= False, add= True)    
        
        elif(ope.eq(pay_type, 'customer')): 
            ExternalFile.update_file(yaml_file['payment_methods'], 'customer_payment', value, set= False, add= True)
        
        elif(ope.eq(pay_type, 'card')): 
            ExternalFile.update_file(yaml_file['payment_methods'], 'credit_card', value, set= False, add= True)
        
        elif(ope.eq(pay_type, 'pix')): 
            ExternalFile.update_file(yaml_file['payment_methods'], 'pix', value, set= False, add= True)
        
        elif(ope.eq(pay_type, 'transfer')): 
            ExternalFile.update_file(yaml_file['payment_methods'], 'bank_transfer', value, set= False, add= True)

        ExternalFile.write_on_file(yaml_file)
        print('\nOutput file after updating:'.upper()); ExternalFile.print_file(yaml_file)
        return
    

    @keyword(name='Remotion From Cashier Amount')
    def Remotion_From_Cashier_Amount(self, 
            amount:float = float(0), 
            event_type:str='standard', 
            payment_type:str='default', 
            just_check:bool= False):
        
        payment_type = payment_type.lower()
        ExternalFile.set_file_path(Central.path_cashier_output)
        yaml_file = ExternalFile.read_file()

        if(ope.eq(event_type.lower(), 'sangria')):
            cashback_amount:float = yaml_file['payment_methods']['cashback']
            check_amount:float = yaml_file['payment_methods']['check']

            # SECURITY CLAUSE ::
            print("❕ Payment Way on usage: %s" %payment_type)
            clause:bool = (True if((ope.eq(payment_type, 'cash')) 
                                and (cashback_amount >= amount)) 
                                    or ((ope.eq(payment_type, 'check'))
                                        and (check_amount >= amount)) 
                                            else False)
            # PROBABILYST RECURSION CLAUSE ::
            if(just_check is True):
                CaLog2.info(msg="\nTHE CASHIER MOVEMENT TYPE 'Sangria' HAS RESULT IN A %s\nCONDITIONAL CLAUSE!"
                        %("'TRUE'" if(clause is True) else "'FALSE'") + "%s" %('' if(clause is True) 
                        else ' BECAUSE OF THAT CIRCUNSTANCE THIS\nCASHIERS EVENT WILL NOT BE DONE!'))
                return clause
            
            # ESCAPE FUNCTION FOR UNEXPECTED CIRCUNSTANCES ::
            if(payment_type not in('cash', 'check')):
                log.info('\n', also_console=True); log.error('...')
                CaLog1.error("\n❌ Invalid payment way or unsuported resource '%s'" %payment_type)
                raise ValueError()
            
            elif((payment_type in ('cash', 'check')) and (clause is True)):
                Calculator.Output_Adjustment(pay_type= payment_type, sangria= True, amount= amount)
                return
            
        #\\... CALLING FOR `cancelling` CASHIER ADJUSTMENT ::
        elif(ope.eq(event_type.lower(), 'cancelling')):
            Calculator.Output_Adjustment(payment_type, cancelling=True, amount=Storage.last_sale_value().__getitem__(-1))
            return

        #\\... SECURITY CLAUSE FOR INVALID METHOD'S ARGUMENT SEQUENCE ::
        else: 
            print("\n\n<fun> 'Remotion_From_Cashier_Amount' in <class> Calculator.py " + 
                  "requires at least one valid value as fuction argument! ['sangria', 'cancelling']")
            raise ValueError()
    
    
    @staticmethod
    def Output_Adjustment(
            pay_type:str= 'CASH, CHECK, CUSTOMER, CARD...', 
            cancelling:bool= False, 
            sangria:bool= False,
            amount:int|float= 0) -> None:
        
        pay_type = pay_type.upper(); print("Payment Entered in the this function: '%s'" %pay_type)
        available_payments: tuple = ('CASH', 'CHECK', 'CUSTOMER', 'CARD', 'TRANSFER', 'PIX')
    
        if(pay_type not in available_payments): 
            print('Invalid explicit argument to this method. -> str(%s)!' %pay_type)
            raise Exception()
        else: pass

        # DATA OUTPUT ADJUSTMENT ::
        ExternalFile.set_file_path(Central.path_cashier_output)
        yaml_file = ExternalFile.read_file()
        print('Output file before:'); create_line(32, cmd='print')
        ExternalFile.print_file(yaml_file)
        _key = pay_type.lower()
        print("💱 Payment type in usage: '%s'" %_key)
        print('💲🔻 Amount to removing: %s' %amount)
    
        # INTERNAL PROCCESS TO CALC DIFFERENCE BETWEEN file.yaml[value] AND 'sale_value'
        def Subtraction_Process(file_key:object= None, another_key:str= ''):
            calc:float = 0
            if(isinstance(file_key, dict)):
                extraction: float = file_key[another_key]
                calc:float = ope.sub(extraction, amount)                             
    
            elif(isinstance(file_key, str)):
                extraction: float = yaml_file[file_key]
                calc:float = ope.sub(extraction, amount) 

            else: print("\n\n<fun> 'Output_Adjustment in <fun> Process() requires an valid value to the variable " +
                        "'itnernal_usage'. Check your code in this step!"); raise ValueError()
    
            # SECURITY CLAUSE FOR INVALID OR NULLABLE VALUE ::
            calc = float(0) if(calc <= 0) else round2(calc)
            print("◈ returning <float|int>:calc = %s" %calc)
            return calc

        print("\n🔄 Adjusting payment ways...".upper())
        # DATA ADJUSTMENT TO <dict>['payment_ways'][_key] ::
        if(ope.eq(_key, 'cash')):
            Cashier.total_cashback_payments(amount, 'sub')
            ExternalFile.update_file(yaml_file['payment_methods'], 'cashback', Cashier.total_cashback_payments())
            print('[cashback] has been updated to: %s' %yaml_file['payment_methods']['cashback'])
        
        elif(ope.eq(_key, 'check')):
            Cashier.total_chq_payments(amount, 'sub')
            ExternalFile.update_file(yaml_file['payment_methods'], 'check', Cashier.total_chq_payments())
            print('[check] has been updated to: %s' %yaml_file['payment_methods']['check'])

        elif(ope.eq(_key, 'customer')):
            Cashier.total_customer_payments(amount, 'sub')
            ExternalFile.update_file(yaml_file['payment_methods'], 'customer_payment', Cashier.total_customer_payments())
            print('[customer_payment] has been updated to: %s' %yaml_file['payment_methods']['customer_payment'])
        
        elif(ope.eq(_key, 'card')):
            Cashier.total_credit_card_payments(amount, 'sub')
            ExternalFile.update_file(yaml_file['payment_methods'], 'credit_card', Cashier.total_credit_card_payments())
            print('[credit_card] has been updated to: %s' %yaml_file['payment_methods']['credit_card'])

        elif(ope.eq(_key, 'transfer')):
            Cashier.total_bank_tranference(amount, 'sub')
            ExternalFile.update_file(yaml_file['payment_methods'], 'bank_transfer', Cashier.total_bank_tranference())
            print('[bank_transfer] has been updated to: %s' %yaml_file['payment_methods']['bank_transfer'])

        elif(ope.eq(_key, 'pix')):
            Cashier.total_pix_payments(amount, 'sub')
            ExternalFile.update_file(yaml_file['payment_methods'], 'pix', Cashier.total_pix_payments())
            print('[pix] has been updated to: %s' %yaml_file['payment_methods']['pix'])

        print("\nAdjusting Cashier Breakdown...".upper())
        print('@property Centralizer.total_on_cashier rigth now: %s' %Cashier.total_on_cashier())
        
        # DATA ADJUSTMENT FOR ANOTHER CASHIER PROPERTIES ::
        if((_key in ('cash', 'check', 'ticket')) and (sangria is False)):
            Cashier.total_on_cashier(amount, 'sub')
            ExternalFile.update_file(yaml_file, 'total_on_cashier', Cashier.total_on_cashier())
            print("[total_on_cashier] has been updated to: %s" %yaml_file['total_on_cashier'])

        if((_key in ('cash', 'check', 'card', 'pix', 'ticket')) and (sangria is False)):
            Cashier.total_sales_value(amount, 'sub')
            ExternalFile.update_file(yaml_file, 'total_sales_value', Cashier.total_sales_value())
            print("[total_sales_value] has been updated to: %s" %yaml_file['total_sales_value'])

        if((_key in ('card', 'pix', 'transfer')) and (sangria is False)):
            Cashier.total_eletronic_payments(amount, 'sub')
            ExternalFile.update_file(yaml_file, 'total_eletronic_payments', Cashier.total_eletronic_payments())
            print("[total_eletronic_payments] has been updated to: %s" %yaml_file['total_eletronic_payments'])
         
        # DATA ADJUSTMENT TO SINGULAR CASHIER PROPERTIES ::
        if(cancelling is True):
            print("\n⊽ [Cancelling Sale]:")
            Cashier.qnt_sales(1, 'sub'); Cashier.canceled_sales(1, 'add')
            ExternalFile.update_file(yaml_file, 'canceled_sale', 1, set= False, add= True)
            ExternalFile.update_file(yaml_file, 'total_canceled_sales', amount, set= False, add= True)
            ExternalFile.update_file(yaml_file, 'sales_quantity', Cashier.qnt_sales())
            print("► ([canceled_sale], [total_canceled_sale], [sales_quantity]) has been updated!")
        
        elif(sangria is True):
            print("\n⊽ [Sangria]:")
            if(amount in (int(0), float(0), None, '')):
                print("❓ Pay attention!\n<var> 'amount' for event type `sangria` cannot be NULL, None or <float|int> lesser than 0.")
                raise ValueError()
            else:
                new_amount = Subtraction_Process(yaml_file, 'total_on_cashier')
                ExternalFile.update_file(yaml_file, 'sangria_quantity', 1, set= False, add= True)
                ExternalFile.update_file(yaml_file, 'removed_values', amount, set= False, add= True)
                ExternalFile.update_file(yaml_file, 'total_on_cashier', new_amount)
                Cashier.qnt_sangria(1, 'add')
                print("► Was performed a remotion from cashier amount!\n💲 Total value: %s" %amount)
                print("Current amount on cashier: %s" %yaml_file['total_on_cashier'])
           
        else:
            print("\nThis method has been called for another function but was not informed which the clause of" +
                  "remotion must be performed during the cashier output adjustment. To call this method without" +
                  "no one argument for <arg>: 'sangria' or <arg>: 'cancel_event' can not be done!")
            CaLog1.error("\n❌ Calling method isn't correct!")
            CaLog1.warning("<def>: 'Output_Adjustment' for @keyword: 'Output_Adjustment'.")
            CaLog1.warning("❗ Invalid parameters for <arg> 'sangria' & <arg> 'cancel_event'")
            raise ValueError()

        ExternalFile.write_on_file(yaml_file)
        print('\nOutput file after:\n----------------------'.upper())
        ExternalFile.print_file(yaml_file)
        return


    @keyword(name='Show Data Output')
    def Show_Data_Output(self, nsequence:int):
        ExternalFile.set_file_path(Central.path_cashier_output)
        contents = ExternalFile.read_file()        
        this_dict: dict = {
            'Cashback':contents['payment_methods']['cashback'],
            'Check':contents['payment_methods']['check'],
            'Credit_Card':contents['payment_methods']['credit_card'],
            'Customer_Pay':contents['payment_methods']['customer_payment'],
            'PIX':contents['payment_methods']['pix'],
            'Bank_Transfer':contents['payment_methods']['bank_transfer'],
            'Ticket':contents['payment_methods']['ticket'],
            'Cashier_Content':contents['total_on_cashier'],
            'Eletronic_Payments':contents['total_eletronic_payments'],
            'Sales_Value':contents['total_sales_value'],
            'All_Sales':contents['all_the_sales_finished'],
            'Sales_Quantity':contents['sales_quantity'],
            'Canceled_Sales':contents['canceled_sale'],
            'Total_Canc_Sales':contents['total_canceled_sales'],
            'Uncompleted_Sales':contents['uncompleted_sale'],
            'Total_Uncplt_Sales':contents['total_uncompleted_sales'],
            'Sangria_Quantity':contents['sangria_quantity'],
            'Total_Sangria':contents['removed_values']}
        
        replacement = format_keyValues(38, mapping= this_dict)
        CaLog1.critical(msg='%s' %(create_line(49, char='=', double_break=True, cmd='return'),))
        CaLog2.info('%s%s' %(expand(size=7), ('%sª TEST SEQUENCE HAS BEEN CONLUED!' %nsequence)))
        CaLog1.critical(msg='%s' %(create_line(49, char='=', cmd='return'),))
        CaLog1.info(msg="%sCASHIER BREAKDOWN" %(expand(size=15),))
        CaLog1.critical(msg='%s' %(create_line(49, cmd='return'),))
        for i in range(len(replacement)):
            if(ope.eq(i, 7)):
                CaLog1.critical(msg='%s' %(create_line(49, char='=', cmd='return'),))
                CaLog1.critical(msg="%sCASHIER AUDICT" %(expand(size=16),))
                CaLog1.critical(msg='%s' %(create_line(49, cmd='return'),))
                CaLog1.debug(msg= replacement[i])
            elif(ope.eq(i, 12)):
                CaLog1.critical(msg='%s' %(create_line(49, char='=', cmd='return'),))
                CaLog1.critical(msg="%sCANCELED" %(expand(size=19),))
                CaLog1.critical(msg='%s' %(create_line(49, cmd='return'),))
                CaLog1.log(level=40, msg= replacement[i])
            elif(ope.eq(i, 13) or ope.eq(i, 15)):
                CaLog1.warn(msg= replacement[i])
            elif(ope.eq(i, 14)):
                CaLog1.critical(msg='%s' %(create_line(49, char='=', cmd='return'),))
                CaLog1.critical(msg="%sUNCOMPLETED" %(expand(size=18),))
                CaLog1.critical(msg='%s' %(create_line(49, cmd='return'),))
                CaLog2.warning(msg= replacement[i])
            elif(ope.eq(i, 16)):
                CaLog1.critical(msg='%s' %(create_line(49, char='=', cmd='return'),))
                CaLog1.critical(msg="%sREMOTIONS FROM CASHIER AMOUNT" %(expand(size=10),))
                CaLog1.critical(msg='%s' %(create_line(49, cmd='return'),))
                CaLog2.warning(msg= replacement[i])
            else: CaLog1.critical(msg= replacement[i])
        CaLog1.critical(msg='%s' %(create_line(49, char='=', cmd='return'),))
        return
