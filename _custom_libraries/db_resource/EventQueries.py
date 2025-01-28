
import operator as ope
from utilities.TextFormater import *
from utilities.ColorText import log, logger4, logger1
EvLog1 = logger1(); EvLog2 = logger4()


class CnnInstance:
    def __init__(self) -> None:
        pass

    @classmethod
    def check_for_instance(__arg:str) -> None:
        if(ope.eq(__arg, 'MyCnn')): return
        else:
            log.info('\n', also_console=True); log.error('...')
            EvLog1.debug('%s' %(create_line(78, break_line=True, cmd='return'),))
            EvLog2.error("[InstanceError]: <class>._instance 'CnnInstance'")
            EvLog1.warn("A problem has been triggered for the <class> instance.")
            EvLog1.debug('%s' %(create_line(78, cmd='return'),))
            raise Exception()
        

class MyQuery:
    def __init__(cls) -> None:
        pass

    @classmethod
    def query_builder(cls, 
            table:str, 
            fields:tuple[str,],
            where_clause:str,
            custom_field:dict[str,] = {'',},
            connection_type:str='mysql',
            custom_select_clause:str='null') -> str:
        
        #\\... BEGIN ::
        new_fields = list(); dinamic_query:str = 'Empty yet'
        if((ope.eq(connection_type.lower(), 'mysql'))):
            dinamic_query = "SELECT {} FROM {}"     
        else:
            dinamic_query = (
                "{} {} FROM {}"  
                if((ope.eq(connection_type.lower(), 'firebird')) 
                   and (ope.ne(custom_select_clause.lower(), 'null'))) 
                else 'NULL')
        pass
        
        create_line(78, char='=', break_line=True, cmd='print')
        print("📑 Query fields interpreter...")
        create_line(78, cmd='print')
        
        #\\... `fileds` ITNERPRETER ::
        for seq in range(fields.__len__()):
            print("◽ seq[%s] » fields[%s]: %s" %(seq, seq, fields[seq]))
            if('$' in fields[seq]):
                new_fields.append(
                    str(custom_field.get(remove_punctuation(fields[seq], punct=('$',)))))
            else: new_fields.append(fields[seq])

        #\\... FORMATING DINAMIC QUERY TEXT ::
        if(ope.eq(connection_type.lower(), 'mysql')):
            dinamic_query = (dinamic_query.format(', '.join(map(str, new_fields)), table))

        elif(ope.eq(connection_type.lower(), 'mysql') and ope.ne(dinamic_query, 'NULL')):
             dinamic_query = custom_select_clause + 'FROM ' + table

        elif(ope.eq(connection_type.lower(), 'firebird') and ope.ne(dinamic_query, 'NULL')):
            dinamic_query = (
                dinamic_query.format(custom_select_clause, ', '.join(map(str, new_fields)), table))
        else:
            log.info('\n', also_console=True); log.error("...")
            EvLog1.debug('%s' %(create_line(78, break_line= True, cmd='return'),))
            EvLog1.critical('%s' %(dlmt_space(78, ('❌ [LibraryExtensionError]:', '|')),))
            EvLog1.error("The 'dinamic_query' couldn't be successffully assigned!")
            EvLog1.debug('%s' %(create_line(78, cmd='return'),))
            raise ValueError()
        
        #\\... OUTPUT ON HTML FILE ::
        create_line(78, char='=', cmd='print')
        print("💡 Dinamic Query: [%s]" %(table,)); create_line(78, cmd='print')
        print("\n... 🔎\r%s" 
              %("SELECT" if ope.eq(custom_select_clause, 'null') else custom_select_clause))
        
        for i in range(new_fields.__len__()):
            print("%s%s"
                  %(expand(size=6), 
                    (str(str(new_fields[i]) + ',') 
                     if
                     (ope.lt(i, (new_fields.__len__() - 1))) 
                     else 
                     str(new_fields[i]) + '')))
        print('FROM %s\n%s' %(table, where_clause))
        create_line(78, char='=', cmd='print')
        #\\... CONCATING THE DINAMIUC QUERY TEXT ::
        dinamic_query = str(dinamic_query + ' ' + where_clause)
        return dinamic_query
    

    @staticmethod
    def pdv_version(args:tuple[str, int]) -> str:
        """Retuns the PDV system version on usage."""
        query:str = """
        SELECT 
        tv.VersaoPdv 
        FROM terminal_versao AS tv 
        WHERE UPPER(tv.Terminal) = '%s'
        AND tv.Empresa = %s ORDER BY tv.DataHora LIMIT 1""" %(*args,)
        return query


    @staticmethod
    def erp_version() -> str:
        """It Returns the MyCommerce system version on usage."""
        query:str = "SELECT Versao FROM atualizadb"
        return query
    pass

    @staticmethod
    def cashier_open_code(args:tuple[int, str, str]) -> str:
        query="""
        SELECT 
            ca.Sequencia
        FROM caixaaberturas as ca
        WHERE ca.CodigoCaixa = %s              
            AND lower(ca.caixa) = '%s'
            AND lower(ca.Terminal) = '%s'
            AND ca.`Data` = CURDATE()
            AND lower(ca.Status) <> 'fechado'
            ORDER BY ca.Sequencia DESC LIMIT 1""" %(*args,)
        return query

    @staticmethod
    def Fb_Query_VENDAS(fields:tuple[str,], filters:dict[str,]) -> str:
        """
        It Returns the `Fb_Query_Sale` created according to the query builder
        arguments has been noticed as function's parameter sequence.

        * `tuple[args...]` ⇾ Table Fields on Query
        * `dict[str]`      ⇾ Custom Fields to Replacing for PSQL text
        """        

        replacers = dict(
            CODVENDA_ERP="""IIF((COALESCE(v.CODVENDA_ERP, null, 0) = 0), 
            'Sync...', 
            v.CODVENDA_ERP
            ) AS ERP_CODVENDA""" ,
            DEST_NOME="""IIF((v.DEST_NOME = c.RAZAOSOCIAL), 
            v.DEST_NOME, 
            'CUST. NAME NOT MATCH'
            ) AS DEST_NOME""" ,
            CPF_CNPJ="""IIF((COALESCE(c.CNPJCPF, NULL, '') NOT IN ('00000000000', '00000000019')),
		    IIF((COALESCE(v.CPF, NULL, 'NT') = COALESCE(c.CNPJCPF, NULL, 'NT')),
            v.CPF, 'CP/CNPJ NOT MATCH'), 'UNKNOW'
            ) AS "CPF/CNPJ" """ ,
            CSTAT="""CASE v.CSTAT 
            WHEN NULL THEN 'CSTAT ERROR'
            WHEN 0 THEN 'WEB SERVICE OFFLINE'
            ELSE v.CSTAT 
            END AS "CSTAT" """ ,
            NAUTORIZACAO= 'COALESCE(v.NAUTORIZACAO, NULL, 0) AS "NAUTORIZACAO"')

        where:str="""INNER JOIN CLIENTES AS c
        ON v.CODIGOCLIENTE = c.CODIGO
        WHERE v."DATA" = CURRENT_DATE
        AND v.VEN_CODIGO = {personcode}
        AND lower(v.USERVENDA) = '{personuser}'
        ORDER BY v.SEQUENCIA DESC""".format_map(filters)

        query = MyQuery.query_builder(
            table= 'VENDAS AS V', 
            fields= fields,
            where_clause= where, 
            custom_field= replacers, 
            connection_type= 'firebird',
            custom_select_clause= 'SELECT FIRST 1')
        return query
    
    
    @staticmethod
    def Query_TRANSFERENCIASENTRECAIXAS_COUNTER(fields:tuple[str,], filters:dict[str,]) -> str:
        replacers = dict(Sequencia="COUNT(Sequencia) as `COUNTER`",)
        where:str="""WHERE CodigoCaixaS = {cashierCode}
            AND lower(Descricao) = 'sangria'
            AND lower(usuarioS) = '{username}'
            AND lower(TerminalS) = '{terminal}'
            AND lower(STATUS) = 'f'
            AND DataS = CURDATE()
            AND CodigoAberturaS = {openCode}""".format_map(filters)
        
        query = MyQuery.query_builder(
            table="transferenciasentrecaixas",
            fields= fields,
            where_clause= where,
            custom_field= replacers)
        return query


    @staticmethod
    def Query_TRANSFERENCIASNETRECAIXAS_ABERTO(fields:tuple[str,], filters:dict[str,]) -> str:
        where:str= """WHERE LOWER(Descricao) = 'sangria'
            AND CodigoCaixaS = {cashierCode}
            AND CodigoAberturaS = {openCode}
            AND lower(`Status`) = 'a'
        ORDER BY Sequencia DESC LIMIT 1""".format_map(filters)
        query = MyQuery.query_builder(
            table= 'transferenciasentrecaixas',
            fields= fields,
            where_clause= where)
        return query


    @staticmethod
    def Query_VENDAS(fields:tuple[str,], filters:dict[str:str, ]) -> str:
        """
        It Returns the `Query_Sale` created according to the query builder
        arguments noticed as function's parameter sequence.

        * `tuple[args...]` ⇾ Table Fields on Query
        * `dict[str]`      ⇾ Custom Fields to Replacing for PSQL text
        """
        where:str="""WHERE `Data` = CURDATE()
        AND NVendaExterna = {nvendaexterna}
        AND CodigoVendedor = {codigovendedor}
        AND lower(Usuario) = '{usuario}'
        AND COALESCE(MovPDV, null, 0) <> 0
        AND lower(Terminal) = '{terminal}'
        AND Empresa = {empresa}
        ORDER BY Hora DESC""".format_map(filters)

        query = MyQuery.query_builder(table= 'vendas', fields= fields, where_clause= where)
        return query


    @staticmethod
    def Query_NOTASSAIDAS(fields:tuple[str,], filters:dict[str:str, ]) -> str:
        """
        It Returns the `Query_NOTASSAIDAS` created according to the query 
        builder arguments has been noticed as function's parameter sequence.

        * `tuple[args...]` ⇾ Table Fields on Query
        * `dict[str]`      ⇾ Custom Fields to Replacing for DSQL text
        """
        replacers = dict(
            Cstat="""COALESCE(ns.Cstat, null, 0) AS Cstat""" ,
            IdentificacaoCliente="""CASE LOWER(coalesce(ns.Dest_FisicaJuridica, null, ''))
            WHEN 'j' then 'DOC TYPE: CNPJ'
            WHEN 'f' then 'DOC TYPE: CPF'
            ELSE 'Unknow'
            END AS IdenticacaoCliente""" ,
            DocumentoCliente="""IF((char_length(coalesce(v.CNPJ, null, '')) > 11), 
            ns.Dest_CNPJ,
            ns.Dest_CPF)
            AS `NOTAS_CPF/CNPJ`""")
        
        where:str="""JOIN vendas as v
        ON v.NumeroNF = ns.NF 
        AND v.Codigo = ns.NVenda
        AND v.`Data` = ns.`Data`
        AND v.Empresa  = ns.Empresa
        AND v.MovPDV  = ns.MovPDV 
        AND v.CodigoVendedor = ns.CodigoVend
        WHERE v.`Data` = CURDATE()
        AND ns.Empresa = {empresa}
        AND ns.CodigoVend = {codigovendedor}
        AND COALESCE(ns.MovPDV, null, 0) <> 0
        AND lower(ns.Terminal) = '{terminal}'
        AND ns.NVenda = {nvenda}
        ORDER BY ns.NF DESC""".format_map(filters)

        query = MyQuery.query_builder(
            table= 'notassaidas AS ns', 
            fields= fields, 
            where_clause= where,
            custom_field= replacers)
        return query
    

    @staticmethod
    def Query_CHEQUEST(fields:tuple[str,], filters:dict[str,]) -> str:
        """
        It Returns the `Query_Fiscal_Document` created according to the query 
        builder arguments noticed as function's parameter sequence.

        * `tuple[args...]` ⇾ Table Fields on Query
        * `dict[str]`      ⇾ Custom Fields to Replacing for DSQL text
        """
        replacers = dict(
            ContaReceberStatus="""if( ( (select 
  			cm.CodigoConta 
  		    from caixamovimentos as cm 
		    where 
		       cm.Sequencia = c.IdCaixaMovimento 
		       and cm.Empresa = 1 ) = c.CodigoContaReceber), 
		       'Registered', 
      	    'Not Registered'
            ) as `ContaReceberStatus`""", )
        where = "WHERE NCheque = {ncheque}".format_map(filters)
        query = MyQuery.query_builder(
            table='chequest as c',
            fields= fields, 
            where_clause= where,
            custom_field= replacers)
        return query

    
    @staticmethod
    def Query_CARTAOMOVIMENTO(fields:tuple[str,], filters:dict[str,]) -> str:
        """
        It Returns the `Query_Fiscal_Document` created according to the query 
        builder arguments noticed as function's parameter sequence.

        * `tuple[args...]` ⇾ Table Fields on Query
        * `dict[str]`      ⇾ Custom Fields to Replacing for DSQL text
        """
        where:str ="""WHERE cm.CodigoVenda = {salecode}
            AND NF = {fiscaldocument}
            AND lower(Terminal) = '{terminal}'""".format_map(filters)
        
        query = MyQuery.query_builder(
            table= 'cartaomovimento AS cm',
            fields= fields,
            where_clause= where)
        return query
    

    @staticmethod
    def Query_AUDITORIA_CARTAOMOVIMENTO(fields:tuple[str,], filters:dict[str]) -> str:
        """
        It Returns the `Query_AUDITORIA_CARTAOMOVIMENTO` created according to the query 
        builder arguments has been noticed as function's parameter sequence.

        * `tuple[args...]` ⇾ Table Fields on Query
        * `dict[str]`      ⇾ Custom Fields to Replacing for DSQL text

        This query context is an audit process made trougth table's arguments of `[cartaomovimento]`
        and `[operadoracartaoprod]`. That source creates a `SQL INNER JOIN` between both table's
        content.`
        """
        replacers = dict(
        NS_ValorInicial_Venda="""(SELECT 
        SUM(ROUND(ROUND((nsp.ValorTabela * nsp.Qtde), 4), 2))
        FROM notassaidas_produtos AS nsp 
        WHERE nsp.NVenda = {sale_code}
        AND nsp.Empresa = {company}
        AND nsp.NF = {nfce}
        ORDER BY nsp.NF DESC LIMIT 1) AS Init_Sale_Vle""".format_map(filters) ,
        NS_ValorComputado_Venda="""(SELECT
        @sale_value:= SUM(ROUND(ROUND((nsp.ValorTotal - nsp.ValorDesconto), 4), 2))
        FROM notassaidas_produtos AS nsp 
        WHERE nsp.NVenda = {sale_code}
        AND nsp.Empresa = {company}
        AND nsp.NF = {nfce}
        ORDER BY nsp.NF DESC LIMIT 1) AS Computed_Sale_Vle""".format_map(filters) ,
        ValorTaxa="""(SELECT 
        @tax:= COALESCE(
        ROUND(ROUND(
        ((@sale_value / 100) * crtm.Tarifa), 4), 2), NULL, 0)) AS Tax_Value""" ,
        Operacao="(SELECT IF(opct.TipoTaxaOperacao = '%', (@ope:= 'PERCENT'), (@ope:= 'NATURAL $'))) AS Operation" ,
        ValorVenda_Auditado="""CASE
        WHEN {replace_tax} = 1 THEN
        @sale_value:= ROUND(ROUND((@sale_value + @tax), 4), 2)
        ELSE @sale_value:= ROUND(ROUND((@sale_value - @tax), 4), 2)
        END AS Audited_Sale_Value""".format_map(filters) ,
        ValorTaxa_Operacao="""CASE
        WHEN @ope = 'PERCENT' 
        THEN @tax_ope:= COALESCE(ROUND(ROUND(((@sale_value / 100) * opct.TaxaOperacao), 4), 2), NULL,  0)
        WHEN @ope = 'NATURAL $' 
        THEN @tax_ope:= COALESCE(ROUND(opct.TaxaOperacao, 2), NULL, 0)
        ELSE @tax_ope:= 0
        END AS Ope_Tax_Value""" ,
        Auditoria_TaxaCartao="""CASE
        WHEN {replace_tax} = 1 THEN 
        @sale_value:= ROUND(ROUND((@sale_value - (@tax_ope + @tax)), 4), 2)
        ELSE @sale_value:= ROUND(ROUND((@sale_value - @tax_ope), 4), 2)
        END AS Final_Card_Audit""".format_map(filters) ,
        Resultado="""CASE
        WHEN crtm.ValorLiquido = @sale_value THEN 'MATCH'
        WHEN crtm.ValorLiquido IN(
        ROUND((@sale_value + 0.01), 2), ROUND((@sale_value - 0.01), 2)) THEN 'TOLERANCE'
        ELSE 'NOT MATCH'
        END AS Result""")
        
        where:str= """JOIN operadoracartaoprod AS opct
		ON opct.Codigo = crtm.CodigoProduto
        AND opct.CodigoOperadora = crtm.CodigoOperadora
        WHERE crtm.Sequencia = {card_sequence}
        AND crtm.CodigoVenda = {sale_code}
        AND crtm.Empresa = {company} """.format_map(filters)

        query = MyQuery.query_builder(
            table="cartaomovimento AS crtm ", 
            fields= fields, 
            where_clause= where, 
            custom_field= replacers)
        return query
    

    @staticmethod
    def Query_CAIXAMOVIMENTOSFORMAS(fields:tuple[str,], filters:dict[str,]) -> str:
        """
        It Returns the `Query_CAIXAMOVIMENTOSFORMAS` created according to the query 
        builder arguments has been noticed as function's parameter sequence.

        * `tuple[args...]` ⇾ Table Fields on Query
        * `dict[str]`      ⇾ Custom Fields to Replacing for DSQL text

        This query context is a grouping made trougth table's arguments of `[caixamovimentos]`
        and `[caixamovimentosformas]`. That source creates a `SQL LEFT JOIN` between both table's
        content.`
        """
        replacers= dict(
            Status="""case lower(coalesce(v.Status, null, ''))
            when 'f' then 'Finalizada'
            when 'x' then 'Cancelada'
            when 'a' then 'Em Aberto'
            when '' then 'Empty'
            else 'Unknow term'
            end as V_StatusVenda""" ,
            TipoMovimento="""if(((cmf.Valor < 0) 
            and (lower(cm.TipoMovimento) 
            in ('crédito', 'credito'))), 
            'Cashier Log', 
            cm.TipoMovimento
            ) as CM_TipoMovimento""")
        
        where:str = """left join vendas as v
        on v.`Data` = cm.`Data` 
        and v.Codigo  = cm.NVenda 
        and v.NumeroNF = cm.nDocumento
        LEFT join caixamovimentosformas as cmf 
        on cm.`Data` = cmf.`Data`
        and lpad(cast(cm.Sequencia as char), 7, '0') = cmf.CodigoMovimento
        where cm.CodigoAbertura = {openCode}
            and cm.nDocumento = {fiscaldocument}
            and v.Codigo = {salecode}""".format_map(filters)
        
        query = MyQuery.query_builder(
            table= "caixamovimentos as cm", 
            fields= fields, 
            where_clause= where,
            custom_field= replacers)
        return query
    

    @staticmethod
    def Query_CONTASARECEEBR(fields:tuple[str,], filters:dict[str,]) -> str:
        """
        It Returns the `Query_CONTASARECEBER` created according to the query 
        builder arguments has been noticed as function's parameter sequence.

        * `tuple[args...]` ⇾ Table Fields on Query
        * `dict[str]`      ⇾ Custom Fields to Replacing for DSQL text

        This query context is a grouping made trougth table's arguments of `[contasaeceber]`
        and `[formarecebimento]`. That source creates a `SQL LEFT JOIN` between both table's
        content.`
        """

        replacers= dict(
            NaturezaRegistro= """case
            -- Step 1
            when ((coalesce(cr.CodigoVenda, null, 0) = 0)
                and coalesce(
                    (select 
                        v.SeqCR 
                        from valecompra as v 
                    where v.SeqCR = cr.Sequencia), null, 0) = cr.Sequencia
                and (cr.Quitado = 0)) then 'Geração Vale'
            -- Step 2
            when ((coalesce(cr.CodigoVenda, null, 0) = 0)
                and coalesce(
                    (select 
                        v.SeqCR_Vista
                        from valecompra as v 
                    where v.SeqCR_Vista = cr.Sequencia), null, 0) = cr.Sequencia
                and (cr.Quitado = 1)) then 'Quitação Vale'
            -- Step 3
            else 'Vendas/Outros'
            end as `NaturezaRegistro`""",
            FinalStatus="'Success' as `FinalStats`")

        where:str= """left join formarecebimento as fr
        on fr.Codigo = cr.CR_COD_FORMA_REC
        where cr.DataLancamento = curdate() 
        and lower(cr.Terminal)  = '{terminal}'
        -- and cr.idCaixaAbertura = {openCode}
        and cr.NDocumento = {fiscaldocument}
        and cr.CodigoVenda = {salecode}""".format_map(filters)

        query = MyQuery.query_builder(
            table= 'contasareceber as cr',
            fields= fields,
            where_clause= where,
            custom_field= replacers)
        return query
    
   
    @staticmethod
    def Query_CONTROLECAIXA(fields:tuple[str,], filters:dict[str,]) -> str:
        """
        It Returns the `Query_CONTROLECAIXA` created according to the query 
        builder arguments has been noticed as function's parameter sequence.

        * `tuple[args...]` ⇾ Table Fields on Query
        * `dict[str]`      ⇾ Custom Fields to Replacing for DSQL text

        This query context is a grouping made trougth table's arguments of `[caixamovimentos]`
        and `[caixamovimentosformas]` and else `[vendas]`. That source creates a `SQL LEFT JOIN`
        between all of those tables' content.
        """
        replacers = dict(
            TipoMov="""if(((cmf.Valor < 0) 
            and (lower(ca.TipoMovimento) 
            in ('crédito', 'credito'))), 
            'Debt Cashier Log', 
            ca.TipoMovimento
            ) as `TipoMov`""", )

        where:str = """LEFT JOIN caixamovimentosformas AS cmf
        ON(ca.Sequencia = lpad(cast(cmf.CodigoMovimento as char), 7, '0'))
        LEFT join vendas as v 
            on v.Codigo = ca.NVenda
            and v.Empresa = ca.Empresa 
            and v.`Data` = ca.DataDocumento
        WHERE ca.CodigoAbertura = {openCode}
            and ca.`Data` = curdate()
            and v.Codigo = {nvenda}
            and v.NumeroNF = {fiscaldocument}
        ORDER BY ca.Sequencia""".format_map(filters)

        query = MyQuery.query_builder(
            table='caixamovimentos AS ca',
            fields= fields,
            where_clause= where,
            custom_field= replacers)
        return query
    

    staticmethod
    def Query_CONTASCORRENTESMOV(fields:tuple[str,], filters:dict[str,]) -> str:
        pass
        return ''

def Commom_Queries(instance:str, 
                   sale1:bool = False,          sale2:bool = False,            chq_audit:bool = False, 
                   chq_mov:bool = False,        card_record:bool = False,      card_mov:bool = False,        
                   pix_mov:bool = False,        cnts_cMmov:bool = False,       cnts_aRec:bool = False,       
                   cnts_aRec_pix:bool = False,  cashier_mov:bool = False,      fiscal_document:bool = False, 
                   cancel_sale:bool = False,    uncompleted_sale:bool= False,  cancel_tax_docmt:bool = False,
                   cashier_code:bool = False,   sangria_event:bool= False,     uncompleted_sangria:bool= False,
                   cnt_sangria:bool = False) -> str:
    
    if(ope.eq(instance, 'MyCnn')): pass
    else: print("<func>:Commom_Queries in <module>:Queries.py requieres an atributte type self@MyConnector"); raise Exception()
    query:str = None

    # VENDAS ::
    if(ope.eq(sale1, True)):
        query= """
        SELECT 
            Codigo, 
            NVendaExterna, 
            NumeroNF, 
            ValorFinalPagamentos, 
            VLR_TROCO_PDV,
            `Status`, 
            Tabela, 
            CodigoCliente, 
            RazaoCliente, 
            CNPJ, 
            Data, Hora
            FROM vendas AS v
        WHERE v.`Data` = %s
            AND NVendaExterna = %s
            AND v.CodigoVendedor = %s
            AND v.CNPJ = %s
            AND v.Usuario = %s
            AND v.MovPDV = 1
            AND v.Terminal = %s
        ORDER BY v.Hora DESC LIMIT 1"""
        
        # format ->: {date.datetime}, {Sales Person Code}, {Customer Ident.}, {Sales Person Name}, {Computer Name}
        return query
    
	# VENDAS ::
    elif(ope.eq(sale2, True)):
        query= """
        SELECT 
            Codigo, 
            NVendaExterna, 
            NumeroNF, 
            ValorFinalPagamentos, 
            v.VLR_TROCO_PDV,
            `Status`, 
            Tabela, 
            CodigoCliente, 
            RazaoCliente, 
            CNPJ, 
            Data, Hora
            FROM vendas AS v
        WHERE v.`Data` = %s AND
            AND NVendaExterna = %s
            AND v.CodigoVendedor = %s
            AND v.CNPJ IS NULL
            AND v.Usuario = %s
            AND v.MovPDV = 1
            AND v.Terminal = %s
        ORDER BY v.Hora DESC LIMIT 1"""
        
        # format ->: {date.datetime}, {Sales Person Code}, {Sales Person Name}, {Computer Name}
        return query

    # CHEQUEST ::
    elif(ope.eq(chq_audit, True)):
        query = """
        SELECT
            Sequencia, 
            CodVenda, 
            IdCaixaMovimento,
            Banco, Agencia, NConta, 
            NCheque, Valor, 
            DataCadastro, 
            CodigoCliente, Cliente
            FROM chequest AS c
        WHERE c.NCheque = %s"""
        return query
    
    # CONTASARECEBER ::
    elif(ope.eq(cnts_aRec, True)):
        query = """
        SELECT 
            Sequencia, 
            Codigo, 
            RazaoSocial,
            CodigoVenda, 
            NDocumento, 
            Valor,
            ValorPendente, 
            ValorPago, 
            Descricao
            FROM contasareceber AS crs
        WHERE crs.Codigo = {}
            AND CodigoVenda = {}
            AND NDocumento = {}
            AND CodigoVendedor = {}"""
        # format ->: {Customer Code}, {Sale Code}, {Fiscal Doc. (type <str>)}, {Sales Person Code}
        return query
    
    # CASHIER CONTROL <CAIXAMOVIMENTOS> ::
    elif(ope.eq(cashier_mov, True)):
        query= """
        SELECT 
            ca.Sequencia,
            SaldoAnterior, 
            ValorPago,
            TipoMovimento, 
            cam.Forma, 
            ca.Saldo
            FROM caixamovimentos AS ca
            INNER JOIN caixamovimentosformas AS cam
                ON(ca.Sequencia = cam.CodigoMovimento)
        WHERE ca.CodigoAbertura = %s
            AND ca.`Data` = %s
        ORDER BY Sequencia
        DESC LIMIT 1"""
        
        # format ->:  {Cashier Code}, {Cashier Name}, {Computer Name/Terminal} {Current time.datetime}
        return query
    
    #-----------------------------------------------------------------------------------------------
    #                                                                  CASHIER MOVEMENT :: PIX | CHQ
    #-----------------------------------------------------------------------------------------------
    # CAIXAMOVIMENTOS FOR CHEQUEST ::
    
    elif(ope.eq(chq_mov, True)):
        query = """
        SELECT
            Sequencia, 
            RazaoSocial, 
            CodigoCliente,
            nDocumento, 
            NVenda, 
            ValorPago, 
            TipoMovimento, 
            ContaRP
            FROM caixamovimentos AS cmx 
        WHERE cmx.Sequencia = %s"""
        return query
    #---------------------------------------------------------------------------------------------||
    # [CAIXAMOVIMENTOS] FOR [CONTASARECEBERPIX] AND [CONTASCORRENTESMOV] ::
    
    elif(ope.eq(pix_mov, True)):
        query = """
        SELECT
            Sequencia, 
            IdPix, 
            RazaoSocial, 
            CodigoCliente,
            nDocumento, 
            NVenda, 
            ValorPago, 
            TipoMovimento, 
            ContaRP, 
            MovPDV, 
            Descricao
            FROM caixamovimentos AS cmx 
        WHERE cmx.Sequencia IN(
            (SELECT 
                @VAR:= Sequencia
                FROM caixamovimentos AS cmx 
            WHERE cmx.NVenda = %s), (@VAR+1), (@VAR+2), (@VAR+3))"""
        return query
    #---------------------------------------------------------------------------------------------||
    # RECORD IN THE [CARTAOMOVIMENTO] ::

    elif(ope.eq(card_record, True)):
        query = """
        SELECT 
            Sequencia, 
            CodigoVenda,
            DATA, 
            Hora, 
            CodigoOperadora, 
            CodigoProduto, 
            CV, NParcelas, 
            Valor, Tarifa, 
            ValorTaxaOperacao, 
            ValorLiquido  
            FROM cartaomovimento AS cm 
        WHERE cm.CodigoVenda = %s
            AND NF = %s
            AND Terminal = %s"""
        # format ->: {Fiscal Document}, {Sales Code}, {Computer Name/Terminal}
        return query
    
    #---------------------------------------------------------------------------------------------||
    # [CAIXAMOVIMENTOS] FOR [CARTAOMOVIMENTO] ::
    elif(ope.eq(card_mov, True)):
        query = """
        SELECT 
            Sequencia, 
            DATA, 
            RazaoSocial, 
            CodigoCliente, 
            nDocumento, 
            Nvenda, 
            ValorPago,
            TipoMovimento, 
            ContaRP, 
            MovPDV, 
            Descricao
            FROM caixamovimentos AS cm 
        WHERE Sequencia IN (
            (SELECT 
                @VAR:= Sequencia 
                FROM caixamovimentos 
            WHERE NVenda = %s), (@VAR + 1))"""
        return query
        # format ->: {Sales Code}
    #--------------------------------------------------------------------------------------------END
    
    # [CONTASCORRENTESMOV] ::
    elif(ope.eq(cnts_cMmov, True)):
        query = """
        SELECT
            Sequencia, 
            Valor, 
            Descricao, 
            Tipo, 
            CodigoMovimentoOrigem 
            FROM contascorrentesmov AS crm 
        WHERE crm.CodigoMovimentoOrigem = %s"""
        return query
    
    # [CONTASARECEEBR_PIX] ::
    elif(ope.eq(cnts_aRec_pix, True)):
        query="""
        SELECT 
            ID, 
            idMovCaixa, 
            ChavePix, 
            Descricao, 
            ValorTotal,
            STATUS, 
            Recurso, 
            Terminal
            FROM contasareceber_pix AS crp 
        WHERE crp.ID = %s"""
        return query

    # [NOTASSAIDAS] ::
    elif(ope.eq(fiscal_document, True)):
        query = """
        SELECT
            Sequencia, 
            Nvenda, 
            NF, Serie, 
            MovPDV,
            SequenciaNotaPDV, 
            TotalNF, 
            TrocoPDV, 
            Cstat,
            DataSaida, HoraSaida, 
            CodigoCliente,
            Dest_FisicaJuridica, 
            Dest_CNPJ, Dest_CPF, 
            VersaoPDV
            FROM notassaidas AS ns
        WHERE DATA = %s AND ns.Nvenda = %s"""
        # format ->: {datetime.date}, {Sales Code}
        return query
    
    # [VENDAS] -> Cancel Process ::
    elif(ope.eq(cancel_sale, True)):
        query = """
        SELECT 
            Codigo, 
            NVendaExterna, 
            NumeroNF, 
            ValorFinalPagamentos,
            `Status`, 
            Cancelada, 
            Tabela, 
            CodigoCliente, 
            RazaoCliente, 
            CNPJ, 
            Data, Hora
            FROM vendas AS v
        WHERE Codigo = %s"""
        # fomart ->: {Sales Code}
        return query

    # [VENDAS] -> Uncompleted Sale Event ::
    elif(ope.eq(uncompleted_sale, True)):
        query="""
        SELECT 
            Codigo, 
            NVendaExterna, 
            NumeroNF, 
            ValorFinalPagamentos,
            `Status`, 
            Cancelada, 
            Tabela, 
            CodigoCliente, 
            RazaoCliente, 
            CNPJ, 
            Data, Hora
            FROM vendas AS v
        WHERE v.`Data` = %s AND
            v.CodigoVendedor = %s AND
            v.CNPJ = %s AND
            v.Usuario = %s AND
            v.MovPDV = 1 AND
            v.Terminal = %s
        ORDER BY v.Hora DESC LIMIT 1"""
        # format ->: {date.datetime}, {Sales Person Code}, {Customer Ident.}, {Sales Person Name}, {Computer Name}
        return query
    
    elif(ope.eq(cancel_tax_docmt, True)):
        query="""
        SELECT
            Sequencia, 
            Nvenda, 
            NF, MovPDV,
            SequenciaNotaPDV, 
            TotalNF, Cstat,
            DataSaida, HoraSaida, 
            CodigoCliente,
            Dest_FisicaJuridica, 
            Dest_CNPJ, Dest_CPF, 
            Situacao, 
            NCancelamento, 
            MsgRetornoCancelamento,
            DataCancelamento, 
            VersaoPDV
            FROM notassaidas AS ns
        WHERE DATA = %s AND ns.Nvenda = %s"""
        # fomat ->: {datetime.date}, {Sales Code}
        return query
    
    elif(ope.eq(cashier_code, True)):
        query="""
        SELECT 
            Sequencia
        FROM caixaaberturas
        WHERE CodigoCaixa = %s              
            AND caixa = %s
            AND lower(Terminal) = %s
            AND DATA = CURDATE()
            AND lower(STATUS) <> 'fechado'
            ORDER BY Sequencia DESC LIMIT 1"""
        # format ->: {Cashier Code}, {Cashier Name}, {Computer Name/ID}, {datetime.date}
        return query
    
    elif(ope.eq(sangria_event, True)): 
        query="""
        SELECT 
            Sequencia, 
            CodigoCaixa, caixa, 
            CodigoAbertura, 
            ValorDocumento, 
            ValorPago, 
            Descricao, 
            RazaoSocial, 
            TipoMovimento, f
            SaldoAnterior, 
            Saldo, 
            Usuario, 
            Terminal
            FROM caixamovimentos AS ca 
        WHERE Descricao IN('SANGRIA', 'sangria')
            AND CodigoAbertura = %s
            AND CodigoCaixa = %s
            AND caixa = %s
        ORDER BY Sequencia DESC LIMIT 1"""
        # format ->: {Cashier Open Code}, {Cashier Code}, {Cashier Name/Descprt.}
        return query
    
    elif(ope.eq(uncompleted_sangria, True)):
        query="""
        SELECT 
            Sequencia, 
            trc.`Status`
            FROM transferenciasentrecaixas AS trc 
        WHERE LOWER(Descricao) = 'sangria'
            AND CodigoCaixaS = %s
            AND CodigoAberturaS = %s
            AND trc.`Status` = 'A'
        ORDER BY Sequencia DESC LIMIT 1"""
        # format ->: {Cashier Code}, {Cashier Open Code}
        return query
    
    elif(ope.eq(cnt_sangria, True)):
        query="""
        SELECT 
            COUNT(Sequencia) 
            FROM transferenciasentrecaixas AS trc 
        WHERE CodigoCaixaS = %s
            AND LOWER(Descricao) = 'sangria'
            AND lower(usuarios) = %s
            AND lower(TerminalS) = %s
            AND STATUS = 'F'
            AND DataS = CURDATE()
            AND CodigoAberturaS = %s"""
        # format ->: {Cashier Code}, {Cashier User}, {Computer Name/ID}, {datetime.date}, {Cashier Open Code}
        return query
    
    else:
        log.error('\nNo valid boolean settings has given as parameter!\nCheck your method call.\n', html=True)
        return ValueError()