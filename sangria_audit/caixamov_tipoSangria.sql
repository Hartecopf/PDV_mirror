
#--------------------------------------------- SET THE STATIC VARIABLES :: 
SET
	# PDV && MYC GENERAL VARIABLES ::
	@CONFIG_company_code = 1,
	@CONFIG_pdv_cashier_code = 74,
	@CONFIG_pdv_cashier_name = 'AUTO_PDV1',
	@CONFIG_user_name = 'FUNCIONARIO',
	@CONFIG_OUT_pdv_cashier_code = 2028,
	@VAR_client_code = 1,
	@CONFIG_value_extracted = 130,
	@CONFIG_computer_name = 'CQP-MATHEUS-165',
	@CONFIG_myc_cashier_code = 2,
	@CONFIG_myc_cashier_name = 'CAIXA ADMINISTRATIVO';

#--------------------------------------------- SET THE SCALAR VARIABLES :: 
SELECT @myc_user:= Usuario AS USER_NAME
	FROM caixas AS ca 
WHERE ca.Codigo = @CONFIG_myc_cashier_code 
	AND ca.Descricao = @CONFIG_myc_cashier_name;
	
SELECT @myc_cashier_oppening_code:= ca.Sequencia AS MYC_CASHIER_OPENING_CODE
   FROM caixaaberturas AS ca
WHERE CodigoCaixa = @CONFIG_myc_cashier_code
   AND caixa = @CONFIG_myc_cashier_name
   AND Terminal = @CONFIG_computer_name
   AND STATUS <> 'Fechado'
ORDER BY Sequencia DESC LIMIT 1;

SELECT
	@last_cmf_code:= trf.Sequencia AS LAST_CMF_SEQ
	FROM transferenciasentrecaixas AS trf
WHERE trf.CodigoCaixaS = @CONFIG_pdv_cashier_code
	AND trf.TerminalS = @CONFIG_computer_name
	AND trf.CaixaS = @CONFIG_pdv_cashier_name
	AND trf.UsuarioS = @CONFIG_user_name
	AND trf.CodigoCaixaE = @CONFIG_myc_cashier_code
	AND trf.CaixaE = @CONFIG_myc_cashier_name
	ORDER BY trf.Sequencia DESC LIMIT 1;
		
SELECT @pdv_prevsly_cashier_amount:= cm.Saldo AS PREV_CASHIER_AMOUNT
	FROM caixamovimentos AS cm 
WHERE cm.CodigoCaixa = @CONFIG_pdv_cashier_code
	AND cm.CodigoAbertura = @CONFIG_OUT_pdv_cashier_code
--	AND cm.TipoMovimento = 'Crédito'
--	AND cm.ContaRP = 'R'
ORDER BY cm.Sequencia DESC LIMIT 1;

SET @pdv_current_cashier_amount:= (@pdv_prevsly_cashier_amount - @CONFIG_value_extracted);
SELECT @pdv_current_cashier_amount AS CURRET_CASHIER_AMOUNT;

#----------------------------- FIRST INPUT ::>> SET DEBT TO PDV CASHIER MOVEMENT ::
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
		@CONFIG_company_code, @CONFIG_pdv_cashier_code, 
		@CONFIG_pdv_cashier_name, @CONFIG_OUT_pdv_cashier_code, 
		@VAR_client_code, 'TRANSFERÊNCIA ENTRE CAIXAS', 
		NULL, NULL, 
		1, @CONFIG_value_extracted, 
		0, @CONFIG_value_extracted, 
		CURDATE(), CURDATE(), 
		'SANGRIA', @pdv_prevsly_cashier_amount, 
		@pdv_current_cashier_amount, 'Débito', 
		1, 'T', 
		NULL, NULL, 
		NULL, NULL, 
		0, 0, 
		NULL, NULL, 
		NULL, NULL, 
		@myc_user, @CONFIG_computer_name,
		0, 0, 
		NULL, 0, 
		0, CURDATE(),
		NULL, 0, 
		NULL, NULL,
		0, NULL);

SELECT @output_movement_code:= ca.Sequencia AS OUT_MOV_CODE
 	FROM caixamovimentos AS ca
WHERE ca.Empresa = @CONFIG_company_code
	AND ca.CodigoCaixa = @CONFIG_pdv_cashier_code
	AND ca.CodigoAbertura = @CONFIG_OUT_pdv_cashier_code
	AND ca.CodigoCliente = @VAR_client_code
	AND ca.Descricao = 'SANGRIA'
	AND ca.ContaRP = 'T'
	AND ca.Terminal = @CONFIG_computer_name
ORDER BY ca.Sequencia DESC LIMIT 1;

#--------- Get previously cashier cmount to the MyC cashier openning code ::
SELECT @myc_prevsly_cashier_amount:= cm.Saldo AS PREV_CASHIER_AMOUNT
	FROM caixamovimentos AS cm 
WHERE cm.CodigoCaixa = @CONFIG_myc_cashier_code
	AND cm.CodigoAbertura =  @myc_cashier_oppening_code
--	AND cm.TipoMovimento = 'Crédito'
--	AND cm.ContaRP = 'R'
ORDER BY cm.Sequencia DESC LIMIT 1;

SET @myc_current_cashier_amount:= (@myc_prevsly_cashier_amount + @CONFIG_value_extracted);
SELECT @myc_current_cashier_amount AS CURRET_CASHIER_AMOUNT;
 
#------------------------- SECOND INPUT ::>> SET CREDIT TO MYC CASHIER MOVEMENT ::
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
		@CONFIG_company_code, @CONFIG_myc_cashier_code, 
		@CONFIG_myc_cashier_name, @myc_cashier_oppening_code, 
		@VAR_client_code, 'TRANSFERÊNCIA ENTRE CAIXAS', 
		NULL, NULL, 
		1, @CONFIG_value_extracted, 
		0, @CONFIG_value_extracted, 
		CURDATE(), CURDATE(), 
		'SANGRIA', @myc_prevsly_cashier_amount, 
		@myc_current_cashier_amount, 'Crédito', 
		1, 'T', 
		NULL, NULL, 
		NULL, NULL, 
		0, 0, 
		NULL, NULL,
		NULL, NULL, 
		@myc_user, @CONFIG_computer_name,
		0, 0, 
		NULL, 0, 
		0, CURDATE(), 
		NULL, 2, 
		NULL, NULL,
		0, NULL);

SELECT @entry_movement_code:= ca.Sequencia AS ENTRY_MOV_CODE
 	FROM caixamovimentos AS ca
WHERE ca.Empresa = @CONFIG_company_code
	AND ca.CodigoCaixa = @CONFIG_myc_cashier_code
	AND ca.CodigoAbertura = @myc_cashier_oppening_code
--	AND ca.CodigoCliente = @VAR_client_code
	AND ca.Descricao = 'SANGRIA'
	AND ca.ContaRP = 'T'
	AND ca.Terminal = @CONFIG_computer_name
ORDER BY ca.Sequencia DESC LIMIT 1;

#---------------------------------------------------------- THIRD INPUT ::
INSERT INTO `caixamovimentosformas` (
   `CodigoMovimento`, 
	`CodigoForma`, `Forma`, 
	`Valor`, `Tipo`, 
	`CodigoAbertura`, `Data`,
	`Mov`, `Historico`, 
	`CXF_UUID_PDV`, `ContaRP`) 
	VALUES (
		('0' + @output_movement_code),
		1, 'DINHEIRO',
		(0 - @CONFIG_value_extracted), 'Moeda', 
		@CONFIG_OUT_pdv_cashier_code, CURDATE(), 
		'P', NULL, 
		NULL, NULL);

#---------------------------------------------------------- FOURTHY INPUT ::
INSERT INTO `caixamovimentosformas` (
	`CodigoMovimento`, 
	`CodigoForma`, `Forma`, 
	`Valor`, `Tipo`,
	`CodigoAbertura`, `Data`,
	`Mov`, `Historico`,
	`CXF_UUID_PDV`, `ContaRP`) 
	VALUES (
		('0' + @entry_movement_code),
		1, 'DINHEIRO',
	   @CONFIG_value_extracted, 'Moeda', 
		@myc_cashier_oppening_code, CURDATE(),
		'R', NULL,
		NULL, NULL);
		
#---------------------------------------------------------- FINISHMENT ::
-- UPDATE BUILDING FOR CASHIER EVENT TYPE "SANGRIA" 
UPDATE `transferenciasentrecaixas` 
	SET `DataA`=CURDATE(), 
		`HoraA`=CURTIME(), 
		`UsuarioA`=@myc_user,
		`TerminalA`=@CONFIG_computer_name,
		`CodMovS`=@output_movement_code, 
		`CodMovA`=@entry_movement_code, 
		`Status`='F', 
		`CodigoAberturaE`=@myc_cashier_oppening_code,
		`ObsSangria`='Movement has done by Robot Framewok For Automated Test Cases'
	WHERE `Sequencia` = @last_cmf_code;
	
