from _custom_libraries.utilities.TextFormater import *
from _custom_libraries.utilities.ColorText import log, logger4, logger1

EvLog1 = logger1(); EvLog2 = logger4()

def query_builder(
            table:str, 
            fields:tuple[str],
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

        #\\... FORMATING THE DINAMIC QUERY TEXT ::
        if(ope.eq(connection_type.lower(), 'mysql')):
            dinamic_query = (dinamic_query.format(', '.join(map(str, new_fields)), table))
        
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
        print("💡 Dinamic Query: [%s]" %(table,))
        create_line(78, break_line=True, cmd='print')
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
        #print("\nInternal Print:\n%s%s" %(dinamic_query, where_clause))
        dinamic_query = str(dinamic_query + ' ' + where_clause)
        return dinamic_query

def Fb_Query_Sale(fields:tuple[str,], filters:dict[str:str,]) -> str:
        """
        It Returns the `Fb_Query_Sale` created according to the query builder
        arguments has been noticed as function's parameter sequence.
        * `tuple[args...]` ⇾ Table Fields on Query
        * `dict[str]`      ⇾ Custom Fields to Replacing for PSQL text
        """        

        replacers = dict(
            CODVENDA_ERP="""IIF((v.CODVENDA_ERP = 0), 
            'Sync', 
            v.CODVENDA_ERP
            ) AS ERP_CODVENDA""",
            DEST_NOME="""IIF((v.DEST_NOME = c.RAZAOSOCIAL), 
            v.DEST_NOME, 
            'CUST. NAME NOT MATCH'
            ) AS DEST_NOME""",
            CPF_CNPJ="""IIF((v.CPF = c.CNPJCPF), 
            v.CPF, 
            'CP/CNPJ NOT MATCH'
            ) AS "CPF/CNPJ" """,
            CSTAT="""CASE v.CSTAT 
            WHEN NULL THEN 'CSTAT ERROR'
            WHEN 0 THEN 'WEB SERVICE OFFLINE'
            ELSE v.CSTAT 
            END AS "CSTAT" """)

        where:str="""INNER JOIN CLIENTES AS c
        ON v.CODIGOCLIENTE = c.CODIGO
        WHERE v."DATA" = CURRENT_DATE
        AND v.VEN_CODIGO = {personcode}
        AND lower(v.USERVENDA) = '{personuser}'
        ORDER BY v.SEQUENCIA DESC""".format_map(filters)

        #\\... END LIKE :
        query = query_builder(
            table= 'VENDAS AS V', 
            fields= fields,
            where_clause= where, 
            custom_field= replacers, 
            connection_type= 'firebird',
            custom_select_clause= 'SELECT FIRST 1')
        return query

query_fields: tuple = (
            '$CODVENDA_ERP', 'v.SEQUENCIA', 'v.TOTALCUPOM', 'v.TOTAL_DESCONTOS', 
            'v.TOTAL_ACRESCIMO', 'v.VLR_TROCO', 'v.STATUS', 'v.PROCESSADO',
            'v.TABELA', 'v.COSDIGOCLIENTE', '$DEST_NOME', '$CPF_CNPJ', 'v.SERIALECF',
            'v.NCUPOM', '$CSTAT', 'v.NAUTORIZACAO', 'v."DATA", v.HORA')
        
query = Fb_Query_Sale(query_fields, 
                    {'personcode':int(2160),
                    'personuser':str('visual')})