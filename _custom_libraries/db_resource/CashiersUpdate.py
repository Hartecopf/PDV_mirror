
import operator as ope
import mysql.connector as cnx

from utilities.ColorText import log, logger5
from utilities.TextFormater import *
from Base import Centralizer as Central, ExternalFile
CaLog = logger5()

class CashierAutoUpdate:
    MySQLconnection:cnx.MySQLConnection = None #type: ignore

    def __init__(cls) -> None:
        pass

    @classmethod
    def Set_MySQL_Connection(cls, cnn:cnx.MySQLConnection) -> cnx.MySQLConnection:
        """Create an explicit connection mapping to the @property: `MySQLConnection`"""
        cls.MySQLconnection = cnn; return
    
    @classmethod
    def Cashier_Auto_Adjustment(cls, kwords:dict, cashier_log:bool) -> None:
        """\rThe `Cacshier_Auto_Adjustement` is a module reponsible to update the current
        content on Automated Test Cases to the `prates` project folder. The prates cashier
        get stored inside folder of the `_output` that contains the cashier outuput file and
        its properties. For each cycle on test sequence, their content must be updated according
        to the database records for all cashier's event has performed for current cashier open 
        code at movement. This python function `<def>:Casheir_Atuo...` has been created to do it."""

        #\\ ... cashier content from cashier output data file ::
        ExternalFile.set_file_path(Central.path_cashier_output)
        ca_content:dict = ExternalFile.read_file()
        
        #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\||
        #\\ ... promgram startup ::
        print("\nExecuting Query 🔍...[caixamovimentos]")
        cashier_events:str="""
        -- CASHIER AUDIT FOR EACH CASHIER MOVEMENT HAS COMPUTED FOR THE SYSTEM CASHIER BREAKDOWN ::	
        SELECT
            ca.CodigoCaixa,
            ca.Caixa,
            ca.CodigoAbertura,
            ca.Sequencia,
            ca.`Data`,
            ca.`Hora`,
            ca.SaldoAnterior,
            ca.ValorPago,
            COALESCE(ca.NVenda, NULL, 0) AS NVenda,
            ca.Saldo,
            ROUND(
                SUM(ROUND((ca.SaldoAnterior + ca.ValorPago), 3)), 2)
            AS AUDITED_AMOUNT
            FROM caixamovimentos AS ca
            JOIN vendas AS v
                ON ca.Nvenda = v.Codigo
                AND ca.Empresa = v.Empresa
        WHERE COALESCE(ca.MovPDV, NULL, 0) <> 0
            AND ca.CodigoCaixa = {ca_code}
            AND ca.Empresa = {company}
            AND ca.CodigoAbertura = {open_code}
            AND COALESCE(ca.NVenda, NULL, '', 0) <> 0
            AND LOWER(v.`Status`) = 'f'
        GROUP BY ca.Sequencia
        ORDER BY ca.Sequencia""".format_map(kwords)
        #print('%s\n' %cashier_events)

        cur_a = cls.MySQLconnection.cursor(buffered=True); cur_a.execute(cashier_events)
        reslts = cur_a.fetchall(); cur_a.close()
        #for e in range(len(reslts)): print(reslts[e])
        if((isinstance(reslts, list)) and (ope.ne(reslts, []))):
            
            #\\ ... format and print table results from database query ::
            create_line(130, cmd='print')
            title:tuple= (
                'CASHIER_CODE', 'CASHIER', 
                'OPEN_CODE', 'SEQUENCE', 
                'DATA', 'HOUR', 
                'PREV_AMOUNT', 'PAYM_AMOUNT',
                'SALE_CODE', 'CUR_AMOUNT', 'AUDIT')
            
            title = format_fields(15, title[3:], separator=' ')
            print('| '.join(map(str, title[:])))
            create_line(130, cmd='print')
            
            for i in range(len(reslts)):
                table:tuple = format_fields(15, reslts[i][3:], separator=' ')
                print('| '.join(map(str, table[:])))
            create_line(130, cmd='print')

        #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\||
        #\\ CASHEIR BREAKDOWN ::
        #\\ ... CURRENT TOTAL AMOUNT ON CASHIER ::

        print("\nExecuting Query 🔍...[caixamovimentosformas]")
        total_amount:str = """
        -- CURRENT TOTAL AMOUNT ON CASHIER ::
        SELECT
            COUNT(cmf.Sequencia) AS QTDE_MOV,
            COALESCE(SUM(
                ROUND(ROUND(cmf.Valor, 4), 2)), NULL, 0)
            AS CASHIER_AMOUNT
            FROM caixamovimentosformas AS cmf
        WHERE cmf.CodigoAbertura = {open_code}
            AND cmf.CodigoForma IN (
                SELECT 
                    f.Codigo 
                    FROM formarecebimento AS f
                WHERE LOWER(f.Tipo) IN(
                'moeda', 'cheques', 'vales'))
            AND LOWER(cmf.Mov) = 'r'""".format_map(kwords)
        print('%s' %total_amount)
        
        cur_b = cls.MySQLconnection.cursor(buffered=True); cur_b.execute(total_amount)
        reslts = cur_b.fetchone(); cur_b.close()
        create_line(75, cmd='print', break_line=True)
        print("Query content: %s" %(reslts,))
        if((isinstance(reslts, tuple)) and (reslts is not None)):
            ca_content = ExternalFile.read_file()
            if(ope.ne(ca_content.get('total_on_cashier'), reslts[-1])):
                print("🔁 Updating cashier's content for key: 🗝 [total_on_cashier]"
                    + "\n🔸 Previously amount on cashier: %s" %(ca_content.get('total_on_cashier'),))
                ExternalFile.update_file(ca_content, 'total_on_cashier', reslts[-1])
                ExternalFile.write_on_file(ca_content); ca_content = ExternalFile.read_file()
                print("🔹 New amount on cashier: %s" %(ca_content.get('total_on_cashier'),))
            else: print("✅ The cashier's content match!")
        else: print("❌ Nothing was made! The Query results is empty or 'None'.")
        create_line(75, cmd='print')

        #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\||
        #\\ CASHEIR BREAKDOWN ::
        #\\ ... CASHBACK TOTAL AMOUNT ON CASHIER ::

        print("\nExecuting Query 🔍...[caixamovimentosformas]")
        cashback:str = """
        -- CURRENT CASHBACK AMOUNT ON CASHIER CONTENT ::
        SELECT
            COUNT(cmf.Sequencia) AS QTDE_MOV,
            COALESCE(
                SUM(ROUND(ROUND(cmf.Valor, 4), 2) ), NULL, 0)
            AS CASHBACK_AMOUNT
            FROM caixamovimentosformas AS cmf
        WHERE cmf.CodigoAbertura = {open_code}
            AND cmf.CodigoForma = 1
            AND LOWER(cmf.Tipo) = 'moeda'
            AND LOWER(cmf.Mov) = 'r'""".format_map(kwords)
        print('%s' %cashback)
        
        cur_c = cls.MySQLconnection.cursor(buffered=True); cur_c.execute(cashback)
        reslts = cur_c.fetchone(); cur_c.close()
        create_line(75, cmd='print', break_line=True)
        print("Query content: %s" %(reslts,))
        if((isinstance(reslts, tuple)) and (reslts is not None)):
            ca_content = ExternalFile.read_file()
            payments:dict = ca_content.get('payment_methods')
            if(ope.ne(payments['cashback'], reslts[-1])):
                print("🔁 Updating cashier's content for key: 🗝 [cashback]"
                    + "\n🔸 Previously Cashback amount on cashier: %s" %(payments.get('cashback'),))
                ExternalFile.update_file(ca_content['payment_methods'], 'cashback', reslts[-1])
                ExternalFile.write_on_file(ca_content)
                ca_content = ExternalFile.read_file()
                payments:dict = ca_content.get('payment_methods')
                print("🔹 New Cashback amount on cashier: %s" %(payments.get('cashback'),))
            else: print("✅ The cashier's cashback amount match!")
        else: print("❌ Nothing was made! The Query results is empty or 'None'.")
        create_line(75, cmd='print')

        #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\||
        #\\ CASHEIR BREAKDOWN ::
        #\\ ... CHECK TOTAL AMOUNT ON CASHIER ::

        print("\nExecuting Query 🔍...[caixamovimentosformas]")
        check:str = """
        -- CURRENT CHECK AMOUNT ON CASHIER CONTET::
        SELECT
            COUNT(cmf.Sequencia) AS QTDE_MOV,
            COALESCE(SUM(
                ROUND(ROUND(cmf.Valor, 4), 2) ), NULL, 0)
            AS CHQ_AMOUNT
            FROM caixamovimentosformas AS cmf
        WHERE cmf.CodigoAbertura = {open_code}
            AND cmf.CodigoForma IN(
                SELECT
                    f.Codigo
                    FROM formarecebimento AS f
                WHERE LOWER(f.Tipo) = 'cheques'
                    AND COALESCE(f.NaoEnviaPDV, NULL, 0) <> 1)
            AND cmf.Mov IN ('R', 'P')""".format_map(kwords)
        print('%s' %check)
        
        cur_d = cls.MySQLconnection.cursor(buffered=True); cur_d.execute(check)
        reslts = cur_d.fetchone(); cur_d.close()
        create_line(75, cmd='print', break_line=True)
        print("Query content: %s" %(reslts,))
        if((isinstance(reslts, tuple)) and (reslts is not None)):
            ca_content = ExternalFile.read_file()
            payments:dict = ca_content.get('payment_methods')
            if(ope.ne(payments['check'], reslts[-1])):
                print("🔁 Updating cashier's content for key: 🗝 [check]"
                    + "\n🔸 Previously Check amount on cashier: %s" %(payments.get('check'),))
                ExternalFile.update_file(ca_content['payment_methods'], 'check', reslts[-1])
                ExternalFile.write_on_file(ca_content)
                ca_content = ExternalFile.read_file()
                payments:dict = ca_content.get('payment_methods')
                print("🔹 New Check amount on cashier: %s" %(payments.get('check'),))
            else: print("✅ The cashier's check amount match!")
        else: print("❌ Nothing was made! The Query results is empty or 'None'.")
        create_line(75, cmd='print')

        #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\||
        #\\ CASHEIR BREAKDOWN ::
        #\\ ... CUSTOMER CREDIT TOTAL AMOUNT ON CASHIER ::

        print("\nExecuting Query 🔍...[contasareceber]")
        cust_credit:str = """
        -- CURRENT CUSTOMER CREDIT AMOUNT  AVAILABLE ON CASHIER CONTENT ::
        SELECT
            COUNT(cr.Sequencia) AS QTDE_MOV,
            COALESCE(
                (SUM(ROUND(ROUND(cr.Valor, 4), 2))), NULL, 0) 
            AS CUSTOM_CREDIT
            FROM contasareceber AS cr
        WHERE cr.DataLancamento = CURDATE()
            AND cr.Terminal = '{computer_name}'
            AND cr.CodigoVendedor = {user_code}
            AND cr.Empresa = {company}
            AND cr.Quitado <> 1
            AND cr.idCaixaAbertura = {open_code}""".format_map(kwords)
        print('%s' %cust_credit)
        
        cur_e = cls.MySQLconnection.cursor(buffered=True); cur_e.execute(cust_credit)
        reslts = cur_e.fetchone(); cur_e.close()
        create_line(75, cmd='print', break_line=True)
        print("Query content: %s" %(reslts,))
        if((isinstance(reslts, tuple)) and (reslts is not None)):
            ca_content = ExternalFile.read_file()
            payments:dict = ca_content.get('payment_methods')
            if(ope.ne(payments['customer_payment'], reslts[-1])):
                print("🔁 Updating cashier's content for key: 🗝 [customer_payment]"
                    + "\n🔸 Previously Customer Payment amount on cashier: %s" %(payments.get('customer_payment'),))
                ExternalFile.update_file(ca_content['payment_methods'], 'customer_payment', reslts[-1])
                ExternalFile.write_on_file(ca_content)
                ca_content = ExternalFile.read_file()
                payments:dict = ca_content.get('payment_methods')
                print("🔹 New Customer Payment amount on cashier: %s" %(payments.get('customer_payment'),))
            else: print("✅ The cashier's Customer Payment amount match!")
        else: print("❌ Nothing was made! The Query results is empty or 'None'.")
        create_line(75, cmd='print')

        #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\||
        #\\ CASHEIR BREAKDOWN ::
        #\\ ... CREDIT CARD TOTAL AMOUNT ON CASHIER ::

        print("\nExecuting Query 🔍...[caixamovimentosformas]")
        credit_card:str = """
        -- CURRENT 'POS' CARD CURRENT AMOUNT ON CASHIER CONTET ::
        SELECT
            COUNT(cmf.Sequencia) AS QTDE_MOV,
            COALESCE(SUM(
                ROUND(ROUND(cmf.Valor, 4), 2)), NULL, 0)
            AS CARD_AMOUNT
            FROM caixamovimentosformas AS cmf
        WHERE cmf.CodigoAbertura = {open_code}
            AND cmf.CodigoForma IN (
                SELECT 
                    f.Codigo
                    FROM formarecebimento AS f
                WHERE LOWER(f.Tipo) = 'cartão oper.'
                    AND COALESCE(f.Usa_TEF, NULL, 0) <> 1)
            AND cmf.Mov = 'R'""".format_map(kwords)
        print('%s' %credit_card)
        
        cur_f = cls.MySQLconnection.cursor(buffered=True); cur_f.execute(credit_card)
        reslts = cur_f.fetchone(); cur_f.close()
        create_line(75, cmd='print', break_line=True)
        print("Query content: %s" %(reslts,))
        if((isinstance(reslts, tuple)) and (reslts is not None)):
            ca_content = ExternalFile.read_file()
            payments:dict = ca_content.get('payment_methods')
            if(ope.ne(payments['credit_card'], reslts[-1])):
                print("🔁 Updating cashier's content for key: 🗝 [credit_card]"
                    + "\n🔸 Previously Credit Card Payment amount on cashier: %s" %(payments.get('credit_card'),))
                ExternalFile.update_file(ca_content['payment_methods'], 'credit_card', reslts[-1])
                ExternalFile.write_on_file(ca_content)
                ca_content = ExternalFile.read_file()
                payments:dict = ca_content.get('payment_methods')
                print("🔹 New Credit Card amount on cashier: %s" %(payments.get('credit_card'),))
            else: print("✅ The cashier's Credit Card amount match!")
        else: print("❌ Nothing was made! The Query results is empty or 'None'.")
        create_line(75, cmd='print')
        
        CaLog.info("\n✅ Cashier's Content has updated according to database!")
        #cls.MySQLconnection.disconnect()
        #\\ End fuction.
        return