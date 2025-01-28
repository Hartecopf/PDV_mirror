# SETTINGS 
# -> Project Libraries or classes on usage ::
import mysql.connector as cnx
import operator as ope

class Handling:
    def __init__(cls) -> None:
        pass
        
    @staticmethod
    def check_for_instance(instance_name:str) -> None:
        if(ope.eq(instance_name, 'MyCnn')): pass
        else:
            print("<class>:Handling requieres an atributte type self@MyConnector")
            raise AttributeError()
        return
    
    @staticmethod
    def Accept_Sangria_Cashier_Event(instance:str, cnn:cnx.MySQLConnection, keys:dict) -> None:
        Handling.check_for_instance(instance)
        
        print("\nExecuting Query 🔍...")
        myc_user:str = """
        SELECT @myc_user:= Usuario AS USER_NAME
            FROM caixas AS ca 
        WHERE ca.Codigo = {myc_cashier_code} 
            AND ca.Descricao = '{myc_cashier_name}'""".format_map(keys)
        print('%s' %myc_user)
        
        cur = cnn.cursor(buffered=True)
        cur.execute(myc_user); rslt:tuple = cur.fetchone(); cur.close()
        if(ope.ne(rslt, None)): 
            keys.update([('myc_user', rslt[0])])
            print("\n❕ <dict>:keys has been updated!")
            for elem in keys.keys():print("🔑 [%s]: %s" %(elem, keys[elem]))
            pass
        # ---------------------------------------------------------------------------------------------------//
            
        print("\nExecuting Query 🔍...")
        myc_opng_code:str = """
        SELECT @myc_cashier_oppening_code:= ca.Sequencia AS MYC_CASHIER_OPENING_CODE
            FROM caixaaberturas AS ca
        WHERE CodigoCaixa = {myc_cashier_code}
            AND caixa = '{myc_cashier_name}'
            -- AND Terminal = '{computer_name}'
            AND STATUS <> 'Fechado'
        ORDER BY Sequencia DESC LIMIT 1""".format_map(keys)
        print('%s' %myc_opng_code)

        cur2 = cnn.cursor(buffered=True)
        cur2.execute(myc_opng_code); rslt:tuple = cur2.fetchone(); cur2.close()
        if(ope.ne(rslt, None)):
            keys.update([('myc_cashier_oppening_code', rslt[0])])
            print("\n❕ <dict>:keys has been updated!")
            for elem in keys.keys():print("🔑 [%s]: %s" %(elem, keys[elem]))
            pass
        # ---------------------------------------------------------------------------------------------------//

        print("\nExecuting Query 🔍...")
        last_cmf_code:str = """
        SELECT
            @last_cmf_code:= trf.Sequencia AS LAST_CMF_SEQ
            FROM transferenciasentrecaixas AS trf
        WHERE trf.CodigoCaixaS = {cashier_code}
            AND trf.TerminalS = '{computer_name}'
            AND trf.CaixaS = '{pdv_cashier_name}'
            AND trf.UsuarioS = '{user_name}'
            AND trf.CodigoCaixaE = {myc_cashier_code}
            AND trf.CaixaE = '{myc_cashier_name}'
            ORDER BY trf.Sequencia DESC LIMIT 1""".format_map(keys)
        print('%s' %last_cmf_code)

        cur3 = cnn.cursor(buffered=True)
        cur3.execute(last_cmf_code); rslt:tuple = cur3.fetchone(); cur3.close()
        if(ope.ne(rslt, None)):
            keys.update([('last_cmf_code', rslt[0])])
            print("\n❕ <dict>:keys has been updated!")
            for elem in keys.keys():print("🔑 [%s]: %s" %(elem, keys[elem]))
            pass
        # ---------------------------------------------------------------------------------------------------//

        print("\nExecuting Query 🔍...")
        pdv_prev_cash_amount:str = """
        SELECT @pdv_prevsly_cashier_amount:= cm.Saldo AS PREV_CASHIER_AMOUNT
            FROM caixamovimentos AS cm 
        WHERE cm.CodigoCaixa = {cashier_code}
            AND cm.CodigoAbertura = {pdv_opng_cashier_code}
        --	AND cm.TipoMovimento = 'Crédito'
        --	AND cm.ContaRP = 'R'
        ORDER BY cm.Sequencia DESC LIMIT 1""".format_map(keys)
        print('%s' %pdv_prev_cash_amount)

        cur4 = cnn.cursor(buffered=True)
        cur4.execute(pdv_prev_cash_amount); rslt:tuple = cur4.fetchone(); cur4.close()
        if(ope.ne(cur4, None)):
            keys.update([('pdv_prevsly_cashier_amount', rslt[0])])
            print("\n❕ <dict>:keys has been updated!")
            for elem in keys.keys():print("🔑 [%s]: %s" %(elem, keys[elem]))
            pass

        # Mathmatical Operation to compute the cashier current amount ::
        print("\n🧮💲 Computing Cashier Amount...")
        pdv_current_cash_amount:float = ope.sub(keys['pdv_prevsly_cashier_amount'], keys['value_extracted'])
        keys.update([('pdv_current_cashier_amount', pdv_current_cash_amount)])
        print("\n❕ <dict>:keys has been updated!")
        for elem in keys.keys(): print("🔑 [%s]: %s" %(elem, keys[elem]))
        # ---------------------------------------------------------------------------------------------------//

        print("\nExecuting Statement... 💬")
        first_cm_insert:str = """
        -- FIRST INPUT SET DEBT TO PDV CASHIER MOVEMENT
        INSERT INTO `caixamovimentos` (
            `Data`, `Hora`, 
            `Empresa`, `CodigoCaixa`, 
            `Caixa`, `CodigoAbertura`, 
            `CodigoCliente`, `RazaoSocial`, 
            `nDocumento`, `NVenda`, 
            `NPagamento`, `ValorDocumento`,
            `ValorJuros`, `ValorPago`, 
            `DataDocumento`, `Vencimento`, 
            `Descricao`, `SaldoAnterior`, 
            `Saldo`, `TipoMovimento`, 
            `CodigoConta`, `ContaRP`, 
            `nComissao`, `TipoComissao`, 
            `FuncComissao`, `CodigoMovEstorno`, 
            `Historico`, `ValorSemJuros`, 
            `NCompra`, `Observacao`, 
            `CodModalidade`, `EmpOrigem`, 
            `Usuario`, `Terminal`, 
            `ValorPendente`, `QtdePagamentos`, 
            `EmpresaOrigemConta`, `ValorMulta`, 
            `ValorCorrecao`, `DataCompetencia`, 
            `CodVendedor`, `TipoTransferencia`, 
            `MovPDV`, `CXM_UUID_PDV`, 
            `IdCampanhaDoacao`, `IdPix`) 
            VALUES (
                CURDATE(), CURTIME(), 
                {company_code}, {cashier_code}, 
                '{pdv_cashier_name}', {pdv_opng_cashier_code}, 
                {client_code}, 'TRANSFERÊNCIA ENTRE CAIXAS', 
                NULL, NULL, 
                1, {value_extracted}, 
                0, {value_extracted}, 
                CURDATE(), CURDATE(), 
                'SANGRIA', {pdv_prevsly_cashier_amount},
                {pdv_current_cashier_amount}, 'Débito', 
                1, 'T', 
                NULL, NULL, 
                NULL, NULL, 
                0, 0, 
                NULL, NULL, 
                NULL, NULL, 
                '{myc_user}', '{computer_name}',
                0, 0, 
                NULL, 0, 
                0, CURDATE(),
                NULL, 0, 
                NULL, NULL,
                0, NULL)""".format_map(keys)
        
        print("%s" %first_cm_insert)
        insert_cur1 = cnn.cursor(buffered=True)
        insert_cur1.execute(first_cm_insert); insert_cur1.close(); cnn.commit()
        # ---------------------------------------------------------------------------------------------------//

        print("\nExecuting Query 🔍...")
        out_mov_code:str = """
        SELECT @output_movement_code:= ca.Sequencia AS OUT_MOV_CODE
            FROM caixamovimentos AS ca
        WHERE ca.Empresa = {company_code}
            AND ca.CodigoCaixa = {cashier_code}
            AND ca.CodigoAbertura = {pdv_opng_cashier_code}
            AND ca.CodigoCliente = {client_code}
            AND ca.Descricao = 'SANGRIA'
            AND ca.ContaRP = 'T'
            AND ca.Terminal = '{computer_name}'
        ORDER BY ca.Sequencia DESC LIMIT 1""".format_map(keys)
        print("\n%s" %out_mov_code)
        
        cur5 = cnn.cursor(buffered=True)
        cur5.execute(out_mov_code); rslt:tuple = cur5.fetchone(); cur5.close()
        if(ope.ne(rslt, None)):
            keys.update([('output_movement_code', rslt[0])])
            print("\n❕ <dict>:keys has been updated!")
            for elem in keys.keys():print("🔑 [%s]: %s" %(elem, keys[elem]))
            pass
        # ---------------------------------------------------------------------------------------------------//

        print("\nExecuting Query 🔍...")
        myc_prev_cash_amount:str = """
        -- Get previously cashier amount to the MyC cashier openning code
        SELECT @myc_prevsly_cashier_amount:= cm.Saldo AS PREV_CASHIER_AMOUNT
            FROM caixamovimentos AS cm 
        WHERE cm.CodigoCaixa = {myc_cashier_code}
            AND cm.CodigoAbertura =  {myc_cashier_oppening_code}
        --	AND cm.TipoMovimento = 'Crédito'
        --	AND cm.ContaRP = 'R'
        ORDER BY cm.Sequencia DESC LIMIT 1""".format_map(keys)
        print('%s' %myc_prev_cash_amount)

        cur6 = cnn.cursor(buffered=True)
        cur6.execute(myc_prev_cash_amount); rslt:tuple = cur6.fetchone(); cur6.close()
        if(ope.ne(rslt, None)):
            keys.update([('myc_prevsly_cashier_amount', rslt[0])])
            print("\n❕ <dict>:keys has been updated!")
            for elem in keys.keys():print("🔑 [%s]: %s" %(elem, keys[elem]))
            pass
        
        # Mathmatical Operation to compute the cashier current amount ::
        print("\n🧮💲 Computing Cashier Amount...")
        myc_current_cash_amount:float = ope.add(keys['myc_prevsly_cashier_amount'], keys['value_extracted'])
        keys.update([('myc_current_cashier_amount', myc_current_cash_amount)])
        print("\n❕ <dict>:keys has been updated!")
        for elem in keys.keys():print("🔑 [%s]: %s" %(elem, keys[elem]))
        # ---------------------------------------------------------------------------------------------------//

        print("\nExecuting Statement... 💬")    
        second_cm_insert:str = """
        -- SECOND INPUT SET CREDIT TO MYC CASHIER MOVEMENT
        INSERT INTO `caixamovimentos` (
            `Data`, `Hora`, 
            `Empresa`, `CodigoCaixa`, 
            `Caixa`, `CodigoAbertura`, 
            `CodigoCliente`, `RazaoSocial`, 
            `nDocumento`, `NVenda`, 
            `NPagamento`, `ValorDocumento`, 
            `ValorJuros`, `ValorPago`, 
            `DataDocumento`, `Vencimento`, 
            `Descricao`, `SaldoAnterior`, 
            `Saldo`, `TipoMovimento`, 
            `CodigoConta`, `ContaRP`, 
            `nComissao`, `TipoComissao`, 
            `FuncComissao`, `CodigoMovEstorno`, 
            `Historico`, `ValorSemJuros`, 
            `NCompra`, `Observacao`, 
            `CodModalidade`, `EmpOrigem`, 
            `Usuario`, `Terminal`, 
            `ValorPendente`, `QtdePagamentos`, 
            `EmpresaOrigemConta`, `ValorMulta`, 
            `ValorCorrecao`, `DataCompetencia`, 
            `CodVendedor`, `TipoTransferencia`, 
            `MovPDV`, `CXM_UUID_PDV`, 
            `IdCampanhaDoacao`, `IdPix`) 
            VALUES (
                CURDATE(), CURTIME(), 
                {company_code}, {myc_cashier_code}, 
                '{myc_cashier_name}', {myc_cashier_oppening_code},
                {client_code}, 'TRANSFERÊNCIA ENTRE CAIXAS', 
                NULL, NULL, 
                1, {value_extracted}, 
                0, {value_extracted}, 
                CURDATE(), CURDATE(), 
                'SANGRIA', {myc_prevsly_cashier_amount}, 
                {myc_current_cashier_amount}, 'Crédito', 
                1, 'T', 
                NULL, NULL, 
                NULL, NULL, 
                0, 0, 
                NULL, NULL,
                NULL, NULL, 
                '{myc_user}', '{computer_name}',
                0, 0, 
                NULL, 0, 
                0, CURDATE(), 
                NULL, 2, 
                NULL, NULL,
                0, NULL)""".format_map(keys)
        
        print('%s' %second_cm_insert)
        insert_cur2 = cnn.cursor(buffered=True)
        insert_cur2.execute(second_cm_insert); insert_cur2.close(); cnn.commit()
        # ---------------------------------------------------------------------------------------------------//

        print("\nExecuting Query 🔍...")  
        entry_mov_code:str = """
        SELECT @entry_movement_code:= ca.Sequencia AS ENTRY_MOV_CODE
            FROM caixamovimentos AS ca
        WHERE ca.Empresa = {company_code}
            AND ca.CodigoCaixa = {myc_cashier_code}
            AND ca.CodigoAbertura = {myc_cashier_oppening_code}
        --	AND ca.CodigoCliente = {client_code}
            AND ca.Descricao = 'SANGRIA'
            AND ca.ContaRP = 'T'
            AND ca.Terminal = '{computer_name}'
        ORDER BY ca.Sequencia DESC LIMIT 1""".format_map(keys)
        print('%s' %entry_mov_code)

        cur7 = cnn.cursor(buffered=True)
        cur7.execute(entry_mov_code); rslt:tuple = cur7.fetchone(); cur7.close()
        if(ope.ne(rslt, None)):
            keys.update([('entry_movement_code', rslt[0])])
            print("\n❕ <dict>:keys has been updated!")
            for elem in keys.keys():print("🔑 [%s]: %s" %(elem, keys[elem]))
            pass
        # ---------------------------------------------------------------------------------------------------//
        
        print("\nExecuting Statement... 💬")   
        third_cm_insert:str = """
        -- THIRD INPUT
        INSERT INTO `caixamovimentosformas` (
        `CodigoMovimento`, 
            `CodigoForma`, `Forma`, 
            `Valor`, `Tipo`, 
            `CodigoAbertura`, `Data`,
            `Mov`, `Historico`, 
            `CXF_UUID_PDV`, `ContaRP`) 
            VALUES (
                ('0' + {output_movement_code}),
                1, 'DINHEIRO',
                (0 - {value_extracted}), 'Moeda', 
                {pdv_opng_cashier_code}, CURDATE(), 
                'P', NULL, 
                NULL, NULL)""".format_map(keys)
        print('%s' %third_cm_insert)

        insert_cur3 = cnn.cursor(buffered=True)
        insert_cur3.execute(third_cm_insert); insert_cur3.close(); cnn.commit()
        # ---------------------------------------------------------------------------------------------------//

        print("\nExecuting Statement... 💬")   
        fourthy_cm_insert:str = """
        -- FOURTHY INPUT
        INSERT INTO `caixamovimentosformas` (
            `CodigoMovimento`, 
            `CodigoForma`, `Forma`, 
            `Valor`, `Tipo`,
            `CodigoAbertura`, `Data`,
            `Mov`, `Historico`,
            `CXF_UUID_PDV`, `ContaRP`) 
            VALUES (
                ('0' + {entry_movement_code}),
                1, 'DINHEIRO',
                {value_extracted}, 'Moeda', 
                {myc_cashier_oppening_code}, CURDATE(),
                'R', NULL,
                NULL, NULL)""".format_map(keys)
        print('%s' %fourthy_cm_insert)
        
        insert_cur4 = cnn.cursor(buffered=True)
        insert_cur4.execute(third_cm_insert); insert_cur4.close(); cnn.commit()
        # ---------------------------------------------------------------------------------------------------//

        print("Finishing the SQL Statements... 💬")
        updating:str = """
        -- FINISHMENT
        -- UPDATE BUILDING FOR CASHIER EVENT TYPE SANGRIA
        UPDATE `transferenciasentrecaixas` 
            SET `DataA`=CURDATE(), 
                `HoraA`=CURTIME(), 
                `UsuarioA`= '{myc_user}',
                `TerminalA`= '{computer_name}',
                `CodMovS`= {output_movement_code}, 
                `CodMovA`= {entry_movement_code}, 
                `Status`='F', 
                `CodigoAberturaE`= {myc_cashier_oppening_code},
                `ObsSangria`= 'Movement has done by Robot Framewok For Automated Test Cases'
            WHERE `Sequencia`= {last_cmf_code}""".format_map(keys)
        
        update_cur = cnn.cursor(buffered=True)
        update_cur.execute(updating); update_cur.close(); cnn.commit()

        print("Has been executed the currently SQL QUERY on database [%s]" %cnn.database)
        return
    
    @staticmethod
    def Create_Custom_Client(instance_name:str, cnn:cnx.MySQLConnection, keys:dict) -> None:
        return
    @staticmethod
    def Create_Custom_User(instance_name:str, cnn:cnx.MySQLConnection, keys:dict) -> None:
        return
    @staticmethod
    def Create_Custom_Cashier(instance_name:str, cnn:cnx.MySQLConnection, keys:dict) -> None:
        return
    @staticmethod
    def Create_Custom_NFCe(instance_name:str, cnn:cnx.MySQLConnection, keys:dict) -> None:
        return
