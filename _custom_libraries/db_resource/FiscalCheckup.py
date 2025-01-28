
import operator as ope
__name__ = 'Fiscal_Query'

def initital_query(fiscalDoc_number:int, company:int = 1) -> str:
    query:str = """
    SELECT 
        ns.NVenda, ns.Serie 
        FROM notassaidas AS ns
    WHERE ns.NF = {} 
	    AND ns.Empresa = {}
    ORDER BY ns.NVenda DESC LIMIT 1"""
    return query.format(fiscalDoc_number, company)

def get_quey(sale_code:int, fiscalDoc_number:int, fiscalDoc_serial:int, company:int= 1) -> dict:
    # /// FIRST QUERY TEXT BODY ::
    expected_fiscal_values:str = """
    -- SCALAR VARIBALES TO COMPUTE AND CALCULATE THE FISCAL TRIBUTES FROM PRODUCTS HAS SEND TO THE SALE.
    -- THESE VARIABLES WILL BE USED TRHOUGH THE NEXT DATABASE QUERIES TO FIND ANOTHER FISCAL DATA MUST BE
    -- CALCULATED IN THE SALE EVENT ::
    SELECT 
        ROUND(ROUND(SUM(Valor_Pis), 4), 2) AS EXPECTED_PIS,
        ROUND(ROUND(SUM(Valor_Cofins), 4), 2) AS EXPECTED_COFINS 
        FROM notassaidas_produtos AS nsp 
    WHERE nsp.NF = {} AND nsp.Serie = {}""".format(fiscalDoc_number, fiscalDoc_serial)
    
    # /// SECONDE QUERY TEXT BODY ::
    parsing:dict = {'nfc':fiscalDoc_number, 'serie':fiscalDoc_serial, 'saleCode':sale_code, 'company':company}
    taxes_calc_query:str = """
    SELECT 
        @total:= (
            (SELECT 
                ROUND(ROUND(SUM((nsp.ValorTotal - nsp.ValorDesconto)), 4), 2)
                FROM notassaidas_produtos AS nsp 
            WHERE nsp.NF = {nfc} 
                AND nsp.Serie = {serie}) + 
            (SELECT COALESCE(ns.OutrasDespesas, NULL, 0) 
                FROM notassaidas AS ns 
            WHERE ns.NF = {nfc}
                AND ns.NVenda = {saleCode} 
                AND ns.Empresa = {company} 
                AND ns.Serie = {serie})) AS TOTAL,
        @icms:= (
            SELECT 
                COALESCE(
                (SUM(ROUND(ROUND(
                (nsp.BaseCalculoICMS * (nsp.AliquotaICMS / nsp.BaseCalculo)), 4), 2))), NULL, 0)
                FROM notassaidas_produtos AS nsp
                JOIN notassaidas AS ns 
                    ON nsp.NF = ns.NF 
                    AND nsp.Serie = ns.Serie 
                    AND nsp.Empresa = ns.Empresa
            WHERE nsp.NF = {nfc}
                AND nsp.Serie = {serie}
                AND ns.Empresa = {company}) AS ICMS,
        @pis:= (
            SELECT SUM(ROUND(ROUND((nsp.Base_PisCofins * (nsp.Aliq_PIS / 100)) , 4), 2)) 
                FROM notassaidas_produtos AS nsp 
            WHERE nsp.NF = {nfc} 
                AND nsp.Serie = {serie} 
                AND nsp.CST_PIS IN('01', '02', '03')) AS CALCULO_PIS,
        @cofins:= (
            SELECT SUM(ROUND(ROUND(nsp.Base_PisCofins * (nsp.Aliq_COFINS / 100), 4), 2)) 
                FROM notassaidas_produtos AS nsp 
            WHERE nsp.NF = {nfc} 
                AND nsp.Serie = {serie} 
                AND nsp.CST_Cofins IN('01', '02', '03')) AS CALCULO_COFINS """
    taxes_calc_query = taxes_calc_query.format_map(parsing)
    # /// OUTPUT QUERIES ::
    queries_group:dict= {'expected_fiscal_values':expected_fiscal_values,'taxes_calc_query':taxes_calc_query}
    return queries_group


def parse_query_method(sale_number:int,
                       nfce_number:int, 
                       nfce_serial:int):
    """It returns a mapping of key values. This module stores and
    build ther SQL Query according to the variables has passed as
    argument to this function parameters. Each one those will be
    concated to literal sql string text as long as returned again
    to the modules has request to."""
    queries:dict = get_quey(sale_number, nfce_number, nfce_serial); return queries


def final_comparison(sale_code:int,
                     nfce_number:int,
                     serie:int,
                     company_code:int = 1, 
                     values:tuple = ()) -> str:
    
    parsing:dict = {
    'total':values[0], 'icms':values[1], 'pis':values[2], 'cofins':values[3], 'nfce_number':nfce_number,
    'nfce_serial':serie, 'salecode':sale_code, 'companycode':company_code, 'tolerance':0.01}
    
    # /// FINAL DATA COMPARISON BETWEEN THE QUERY RESULTS HAS COMPUTED PREVIOUSLLY ::
    final_comparison:str = """
    -- Comparing the singular processes done so far. 
    -- This next statement will show whether or not the data matches ::
    SELECT 
	ns.NF, 
    ns.Serie, 
	ns.NVenda, 
    v.NVendaExterna, 
	ns.TotalNF, 
    ROUND({total}, 2) AS TOTAL_CALC, 
	ns.TotalIcms, 
    @icms_rounded:= ROUND({icms}, 2) AS ICMS_CALC,
	ns.Total_PIS,
      @pis_rounded:= ROUND({pis}, 2) AS PIS_CALC,
	ns.Total_Cofins, 
    @cofins_rounded:= ROUND({cofins}, 2) AS COFINS_CALC,
	ns.TotalIcmsDesonerado,
    @icms_total_final:= ROUND(
        ROUND((@icms_rounded - ns.TotalIcmsDesonerado), 4), 2) AS ICMS_FINAL,
    CASE
		WHEN {total} = ns.TotalNF THEN 'TOTAL OK'
		ELSE 'NOT MATCH'
	END AS Result_Total,
    CASE
        WHEN @icms_rounded = ns.TotalIcms THEN 'ICMS OK'
        WHEN @icms_rounded IN(ROUND((@icms_rounded + {tolerance}), 2), 
            ROUND((@icms_rounded - {tolerance}), 2)) THEN 'TOLERANCE'
        ELSE 'NOT MATCH'
	END AS Result_Icms,
	CASE
		WHEN @pis_rounded = ns.Total_PIS THEN 'PIS OK'
		WHEN @pis_rounded IN (ROUND((@pis_rounded + {tolerance}), 2), 
			ROUND((@pis_rounded - {tolerance}), 2)) THEN 'TOLERANCE' 
		ELSE 'NOT MATCH'
	END AS Result_Pis,
	CASE
		WHEN @cofins_rounded = ns.Total_Cofins THEN 'COFINS OK'
		WHEN @cofins_rounded IN (ROUND(({cofins} + {tolerance}), 2), 
			ROUND(({cofins} - @tolerance), 2)) THEN 'TOLERANCE'
		ELSE 'NOT MATCH'
	END AS Result_Cofins
	FROM notassaidas AS ns
	JOIN vendas AS v
		ON ns.NF = v.NumeroNF 
		AND ns.Empresa = v.Empresa 
		AND ns.NVenda = v.Codigo
	WHERE ns.NF = {nfce_number}
		AND ns.NVenda = {salecode}
		AND ns.Empresa = {companycode}
		AND ns.Serie = {nfce_serial}
		AND ns.NF = {nfce_number}""".format_map(parsing)
    return final_comparison

# Taxes Checking to the Card Movements entered on database. That taxes represents also the Fiscal Checkup
# for movements type eletronic as the card movements. Whenever that card has a tax amoun as a valid value
# to compute, this SQL QUERY bellow will do the needes evaluation and comparison about expected final results.
def Card_Movement_Audit(card_sequence:int, 
                        sale_code:int, 
                        tax_doc_nmbr:int, 
                        company:int, 
                        taxes_replcmnt:bool= False) -> str:
    
    parsing:dict = {'sale_code':sale_code, 'company':company, 'nfce':tax_doc_nmbr, 
                         'replace_tax':taxes_replcmnt, 'card_sequence':card_sequence}
    query:str = """
    SELECT
	crtm.CodigoVenda,
    crtm.Sequencia, 
	crtm.CodigoOperadora AS Ope_Code, 
	crtm.CodigoProduto,
	opct.Operacao,
    crtm.CV, 
	(SELECT 
		SUM(ROUND(ROUND((nsp.ValorTabela * nsp.Qtde), 4), 2))
		FROM notassaidas_produtos AS nsp 
	WHERE nsp.NVenda = {sale_code}
		AND nsp.Empresa = {company}
		AND nsp.NF = {nfce}
	ORDER BY nsp.NF DESC LIMIT 1) AS Init_Sale_Vle,
	crtm.ValorLiquido,
	crtm.Valor,
	-- COMPUTE THE ORIGINAL SALE VALUE WTHOUT ANY ADDITIONAL TAXES
	(SELECT 
		@sale_value:= SUM(ROUND(ROUND((nsp.ValorTotal - nsp.ValorDesconto), 4), 2))
		FROM notassaidas_produtos AS nsp 
	WHERE nsp.NVenda = {sale_code}
		AND nsp.Empresa = {company}
		AND nsp.NF = {nfce}
	ORDER BY nsp.NF DESC LIMIT 1) AS Computed_Sale_Vle,	
	-- Continue like ::
	crtm.Tarifa AS Percent_Tax,
	(SELECT 
		@tax:= COALESCE(ROUND(ROUND(((@sale_value / 100) * crtm.Tarifa), 4), 2), NULL, 0)) AS Tax_Value,
	opct.TaxaOperacao AS Ope_Tax,
	(SELECT IF(opct.TipoTaxaOperacao = '%', (@ope:= 'PERCENT'), (@ope:= 'NATURAL $'))) AS Operation,
	CASE
		WHEN {replace_tax} = 1 THEN
			@sale_value:= ROUND(ROUND((@sale_value + @tax), 4), 2)
		ELSE @sale_value:= ROUND(ROUND((@sale_value - @tax), 4), 2)
	END AS Audited_Sale_Value,
	CASE
		WHEN @ope = 'PERCENT' 
			THEN @tax_ope:= COALESCE(ROUND(ROUND(((@sale_value / 100) * opct.TaxaOperacao), 4), 2), NULL,  0)
		WHEN @ope = 'NATURAL $' 
			THEN @tax_ope:= COALESCE(ROUND(opct.TaxaOperacao, 2), NULL, 0)
		ELSE @tax_ope:= 0
	END AS Ope_Tax_Value,
	CASE
		WHEN {replace_tax} = 1 THEN 
			@sale_value:= ROUND(ROUND((@sale_value - (@tax_ope + @tax)), 4), 2)
		ELSE @sale_value:= ROUND(ROUND((@sale_value - @tax_ope), 4), 2)
	END AS Final_Card_Audit,
	CASE
		WHEN crtm.ValorLiquido = @sale_value THEN 'MATCH'
		WHEN crtm.ValorLiquido IN(
			ROUND((@sale_value + 0.01), 2), ROUND((@sale_value - 0.01), 2)) THEN 'TOLERANCE'
		ELSE 'NOT MATCH'
	END AS Result
	FROM cartaomovimento AS crtm 
	JOIN operadoracartaoprod AS opct
		ON opct.Codigo = crtm.CodigoProduto
			AND opct.CodigoOperadora = crtm.CodigoOperadora
    WHERE crtm.Sequencia = {card_sequence}
        AND crtm.CodigoVenda = {sale_code}
            AND crtm.Empresa = {company} """.format_map(parsing)
    return query