
	"Codigo" : "CODIGO",
	"CodigoBarras" : "CODIGOBARRAS",
	"Referencia" : "REFERENCIA",
	"DataCadastro" : @dataExp1, (CURRENT_DATE)
	"UltimaAlteracao" : @dataExp2, (CURRENT_TIMESTAMP)
	"Descricao" : "DESCRICAO",
	"CodigoFabricante" : "CODIGOFABRICANTE",
	"Fabricante" : @exp1, (select fab.Descricao from fabricantes as fab where fab.Codigo = "CODIGOFABRICANTE"))
	"Detalhamento" : "DETALHAMENTO",
	"UNVenda" : "UM",
	"UNCompra" : None,
	"QuantidadeCX" : "QTDECXVENDA",
	"EstoqueMinimo" : None,
	"EstoqueIdeal" : None,
	"ValorCusto" : "VLR_CUSTO",
	"OutrosCustos" : @exp2, (VLR_CUSTOFINAL - VLR_CUSTO)
	"CustoFinal" : "VLR_CUSTOFINAL",
	"PercentualT1" : @exp3 ([("VALORVENDA" - "VLR_CUSTOFINAL") * 100] / "VLR_CUSTOFINAL")
	"VendaT1" : "VALORVENDA",
	"Moeda" : "R$",
	"Indexador" : None,
	"CodigoCadeiaPreco" : None,
	"CadeiaPreco" : None,
	"CodigoComissao" : None,
	"TComissao" : None,
	"CodigoSecao" : "CODIGOSECAO",
	"Secao" : @exp4, (select sec.Descricao from secoes as sec where sec.Codigo = "CODIGOSECAO"))
	"CodigoGrupo" : "CODIGOGRUPO",
	"Grupo" : @exp5, (select gp.Descricao from grupos as gp where gp.Codigo = "CODIGOGRUPO"))
	"CodigoSubGrupo" : "CODIGOSUBGRUPO",
	"SubGrupo" : @exp6, (select sgp.Descricao from subgrupos as sgp where sgp.Codigo = "CODIGOSUBGRUPO"))
	"Parteleira" : None,
	"Gondula" : None,
	"Gaveta" : None,
	"PesoBruto" : "PESO_BRUTO",
	"PesoLiquido" : "PESO_LIQUIDO",
	"Medidas" : None,
	"PrazoValidade" : None,
	"PrazoGarantia" : None,
	"ObservaVenda" : None,
	"TextoObserva" : None,
	"EnviaBalanca" : None,
	"EtiquetaGondula" : None,
	"CodigoCF" : None,
	"SituacaoTributaria" : None,
	"CodigoContaContabil" : None,
	"ContaContabil" : None,
	"IPI" : None,
	"CNN" : None,
	"AliquotaICMS" : "ALIQ_ICMS",
	"BaseCalculoICMS" : "BASE_ICMS",
	"Status" : "a",
	"NComercializavel" : 0,
	"DadosTecnicos" : None,
	"Ativo" : 1,
	"Terminal" : "PDV2",
	"Usuario" : "Visual",
	"DescontoMaximo" : "DESC_MAX",
	"CODIGOFABRICA" : "CODIGOFABRICA",
	"ModalidadeControle" : None,
	"CodigoGrade" : "CODGRADE",
	"VendaPDV" : "VALORVENDA",
	"Cofins" : None,
	"TipoProduto" : "TIPOPRODUTO",
	"AgrupaProdEtq" : None,
	"QtdePorVol" : None,
	"ExpDescricao" : None,
	"PrecodeMercado" : None,
	"Formacao_pComissao" : None,
	"Formacao_pFrete" : None,
	"Formacao_pDespesas" : None,
	"AliquotaIcmsCompra" : None,
	"TeclaBalanca" : None,
	"empresas" : None,
	"KitEditavel" : None,
	"ListaPreco" : None,
	"UserID" : "Visual Software",
	"QtdeFixaEtq" : None,
	"Cancelado" : None,
	"DataPromocao" : "DATAPROMOCAO",
	"ValorPromocao" : "VALORPROMOCAO",
	"QtdeMin_Promocao" : "QTDEMIN_PROMOCAO",
	"FC_Desc1" : None,
	"FC_Desc2" : None,
	"FC_Desc3" : None,
	"FC_IPI" : None,
	"FC_FRETE" : None,
	"FC_CustoInicial" : None,
	"BaixaComposicao" : None,
	"PFrete_UtlCompra" : None,
	"Volume" : None,
	"UnVolume" : None,
	"PrecoMaxCons_Med" : None,
	"NCM" : "NCM",
	"Promo_Desc1" : None,
	"Promo_Desc2" : None,
	"Promo_Desc3" : None,
	"TPMedicamento" : None,
	"Cst_Compra" : None,
	"Flex_vlrGanhar" : None,
	"UsuarioExclusao" : None,
	"TerminalExclusao" : None,
	"MotivoExclusao" : None,
	"DataHoraExclusao" : None,
	"CodigoColecao" : None,
	"Colecao" : None,
	"Pontuacao" : None,
	"ValorCustoFiscal" : None,
	"Medicamento_UsoControlado" : None,
	"Largura" : None,
	"Comprimento" : None,
	"Altura" : None,
	"NumDecretos" : None,
	"QtdeCxVenda" : None,
	"Paletizado" : None,
	"Ex_NPalete" : None,
	"CST_Simples" : "CST",
	"Cst_Simples_Texto" : @exp4,
	"Venda_Med_2dia" : None,
	"UltimaCompra" : None,
	"QtdeUltimaCompra" : None,
	"TPListaMed" : None,
	"Restricao_CPF" : None,
	"Restricao_QtdeLimitada" : None,
	"Restricao_Qtde" : None,
	"limitevendas" : None,
	"limiteacrescimo" : "LIMITEACRESCIMO",
	"FatorCadeia" : None,
	"UltimaEntrada" : None,
	"ICMS_Garantido" : None,
	"EANTrib" : "EANTRIB",
	"Controlado_Civil" : None,
	"CST_PIS" : "CST_PIS",
	"Aliq_PIS" : "ALIQ_PIS" ,
	"CST_COFINS" : "CST_COFINS",
	"Aliq_COFINS" : "ALIQ_COFINS",
	"Entrada_CST_Pis" : None,
	"Entrada_CST_Cofins" : None,
	"Venda_med_10Dias" : None,
	"UltimoFornecedor" : None,
	"DataCortePDA" : None,
	"PesoTara" : None,
	"Cst_Pis_Simples" : None,
	"Aliq_Pis_Simples" : None,
	"Cst_Cofins_Simples" : None,
	"Aliq_Cofins_Simples" : None,
	"Cst_Pis_LP" : None,
	"Aliq_Pis_LP" : None,
	"Cst_Cofins_LP" : None,
	"Aliq_Cofins_LP" : None,
	"CodNaturezaPis" : None,
	"Margem_Fixa" : None,
	"Controlado" : 0,
	"FORMACAO_pEmbalagem" : 0.0,
	"Ignora_Mov_Composicao" : None,
	"CodigoANP" : None,
	"Usa_Preco_Max_ST" : 1,
	"VolumeML" : None,
	"ICMSST_UltimaCompra" : "ICMSST_ULTIMACOMPRA",
	"ST_PercentualRecuperar" : None,
	"DataInicioPromocao" : None,
	"Resp_Formula" : None,
	"Resp_Qualidade" : None,
	"Fraciona" : 1,
	"FC_Desc4" : 0.0,
	"FC_ST" : 0.0,
	"FC_Vendor" : 0.0,
	"Cst_IPI_Simples" : None,
	"CSt_IPI" : None,
	"FCI_Valor_Saida_Inter" : None,
	"FCI_Valor_Importado" : None,
	"FCI_pCI" : None,
	"FCI_Numero" : None,
	"FCI_DataAlteracao" : None,
	"FCI_DataRegistro_Sefaz" : None,
	"FCI_DataGeracao" : None,
	"FCI_Protocolo" : None,
	"Controlado_Ibama" : None,
	"ListaPreco2" : None,
	"Venda_Med_10Dias2" : None,
	"Recalcula_Custo_Composicao" : 0,
	"BaseST_Retido" : "BASEST_RETIDO",
	"Fc_Outros" : 0.0,
	"Icms_SemRed_SN" : 0,
	"EXTIPI" : None,
	"CodigoLinhaProduto" : "PRO_CODIGO_LINHA",
	"LinhaProduto" : "LINHAPRODUTO",
	"EANEmbCompra" : None,
	"DadosTecnicosEtiquetas" : None,
	"Formacao_PIcmsST" : None,
	"TecladoBalanca" : None,
	"CodigoEnqIPI" : None,
	"AdicionalGelado" : "ADICIONALGELADO",
	"OutrasDespesas_UltimaCompra" : None,
	"ValorIpi_UltimaCompra" : None,
	"ValorSeguro_UltimaCompra" : None,
	"Cest" : None,
	"ceicom_exportado" : None,
	"magento_id" : None,
	"SemComissao" : None,
	"CodigoVasilhame" : None,
	"QuantidadeVasilhame" : None,
	"UnTrib" : None,
	"FORMACAO_vEmbalagem" : 0.0,
	"POutros" : 0.0,
	"SeparaPorEmpresa" : 0,
	"TipoAtu" : None,
	"SeqAtu" : None,
	"InfNutri_Qtde" : None,
	"InfNutri_Perc_Qtde" : None,
	"InfNutri_ValorEnergetico" : None,
	"InfNutri_Perc_ValorEnergetico" : None,
	"InfNutri_Carboidratos" : None,
	"InfNutri_Perc_Carboidratos" : None,
	"InfNutri_Proteinas" : None,
	"InfNutri_Perc_Proteinas" : None,
	"InfNutri_GordurasTotais" : None,
	"InfNutri_Perc_GordurasTotais" : None,
	"InfNutri_GordurasSat" : None,
	"InfNutri_Perc_GordurasSat" : None,
	"InfNutri_Colesterol" : None,
	"InfNutri_Perc_Colesterol" : None,
	"InfNutri_FibraAlimentar" : None,
	"InfNutri_Perc_FibraAlimentar" : None,
	"InfNutri_Calcio" : None,
	"InfNutri_Perc_Calcio" : None,
	"InfNutri_Ferro" : None,
	"InfNutri_Perc_Ferro" : None,
	"InfNutri_Ingredientes" : None,
	"InfNutri_Observacao" : None,
	"InfNutri_UM_Qtde" : None,
	"InfNutri_UM_ValorEnergetico" : None,
	"InfNutri_UM_Carboidratos" : None,
	"InfNutri_UM_Proteinas" : None,
	"InfNutri_UM_GordurasTotais" : None,
	"InfNutri_UM_GordurasSat" : None,
	"InfNutri_UM_Colesterol" : None,
	"InfNutri_UM_FibraAlimentar" : None,
	"InfNutri_UM_Calcio" : None,
	"InfNutri_UM_Ferro" : None,
	"Anvisa" : None,
	"InfNutri_GordurasTrans" : None,
	"InfNutri_Perc_GordurasTrans" : None,
	"InfNutri_UM_GordurasTrans" : None,
	"InfNutri_Sodio" : None,
	"InfNutri_Perc_Sodio" : None,
	"InfNutri_UM_Sodio" : None,
	"InfNutri_DescricaoPorcao" : None,
	"InfNutri_QuantidadeCaseira" : None,
	"InfNutri_QuantidadeCaseira_UM" : None,
	"TextoObservaEntradas" : None,
	"ObservaEntradas" : 0,
	"ExibeMyAcougue" : 0,
	"IDPrateleira" : None,
	"IDGondola" : None,
	"IDGaveta" : None,
	"ValorUnUltimaCompra" : None,
	"CodigoGradeKit" : "CODIGOGRADEKIT",
	"Gas_pGLP" : "GAS_PGLP",
	"Gas_pGNn" : "GAS_PGNN",
	"Gas_pGNi" : "GAS_PGNI",
	"Gas_vPart" : "GAS_VPART",
	"TipoExibicaoMyAcougue" : 0,
	"DataUltimaEtiqueta" : None,
	"Multiplo" : None,
	"pICMSEfet" : "PICMSEFET",
	"Cst_IPI_Compra" : None,
	"ICMS_UltimaCompra" : "ICMS_ULTIMACOMPRA",
	"FcpST_Retido" : "FCPST_RETIDO",
	"pFcpST_Retido" : "PFCPST_RETIDO",
	"pBCEfet" : "PBCEFET",
	"ValorFabricaMedicamento" : None,
	"Tela" : None,
	"ManutencaoKM" : None,
	"ManutencaoDias" : None,
	"PISCOFINS_UltimaCompra" : None,
	"ICMSST_PRESUMIDO_UltimaCompra" : None,
	"IsPneu" : 0,
	"TemFoto" : None,
	"MargemSugerida" : None,
	"TipoOferta" : 0,
	"CustoIcms_UltimaCompra" : None,
	"DataEmb" : 1,
	"InfNutri_UM_Caseira" : None,
	"PrazoValidade_PorEmpresa" : 0,
	"ValorCustoGerencUltimaCompra" : None,
	"Gelado_PorEmpresa" : 0,
	"ProducaoPropria" : None,
	"Sped_CustoMedio" : None,
	"Data_Exportacao" : None,
	"estoqueMaximo" : None,
	"estoqueTempoMax" : None,
	"wms_unidadePrimaria" : None,
	"endereco_padraoSaida" : None,
	"endereco_padraoEntrada" : None,
	"LinkVideo" : None,
	"NumeroLicencaAdapar" : None,
	"Imprimir_Vale" : 0,
	"NcmUltimaCompra" : None,
	"Ipi_UltimaCompra" : None,
	"Sped_CustoMedioAbatimento" : None,
	"QtdePalete" : None,
	"TipoProduto_ind" : None,
	"DCB_ID" : None,
	"CodigoPerfilB2B" : None,
	"DescricaoPerfilB2B" : None,
	"ValorGNRE_UltimaCompra" : None,
	"CodigoImagemPrincipal" : None,
	"CadWMS" : 0,
	"CodigoLinhaProducao" : None,
	"DescricaoLinhaProducao" : None,
	"ObservacaoProducao" : None,
	"Formacao_vCustoAdicionalCompra" : None,
	"Formacao_vMargemLucroLiquido" : None,
	"Formacao_vMargemLucroAplicado" : None,
	"InfNutri_AcucaresTotais" : None,
	"InfNutri_AcucaresAdicionados" : None,
	"InfNutri_UM_AcucaresAdicionados" : None,
	"InfNutri_UM_AcucaresTotais" : None,
	"InfNutri_Perc_AcucaresAdicionados" : None,
	"InfNutri_Perc_AcucaresTotais" : None,
	"ExibeSempreSimilar" : 0,
	"Formacao_pCustoOp" : None,
	"ListaPreco_PrecoSobConsulta" : None,
	"ListaPreco_EstoqueIndisponivel" : None,
	"ListaPreco_DiasDisponibilidade" : None,
	"Vlr_Icms_ADRem" : 0.0,
	"CodigoConservacao" : None,
	"CodigoCampoExtra1" : None,
	"CodigoCampoExtra2" : None,
	"CodigoCampoExtra3" : None,
	"CodigoCampoExtra4" : None,
	"ImportarFranquia" : None,
	"CodigoFornecedorBalanca" : None,
	"CodigoFracionadoraBalanca" : None,
	"Produto_Retornavel" : 0,
	"InfNutri_Qtde_429" : None,
	"InfNutri_Perc_Qtde_429" : None,
	"InfNutri_ValorEnergetico_429" : None,
	"InfNutri_Perc_ValorEnergetico_429" : None,
	"InfNutri_Carboidratos_429" : None,
	"InfNutri_Perc_Carboidratos_429" : None,
	"InfNutri_Proteinas_429" : None,
	"InfNutri_Perc_Proteinas_429" : None,
	"InfNutri_GordurasTotais_429" : None,
	"InfNutri_Perc_GordurasTotais_429" : None,
	"InfNutri_GordurasSat_429" : None,
	"InfNutri_Perc_GordurasSat_429" : None,
	"InfNutri_GordurasTrans_429" : None,
	"InfNutri_Perc_GordurasTrans_429" : None,
	"InfNutri_Colesterol_429" : None,
	"InfNutri_Perc_Colesterol_429" : None,
	"InfNutri_FibraAlimentar_429" : None,
	"InfNutri_Perc_FibraAlimentar_429" : None,
	"InfNutri_Calcio_429" : None,
	"InfNutri_Perc_Calcio_429" : None,
	"InfNutri_Ferro_429" : None,
	"InfNutri_Perc_Ferro_429" : None,
	"InfNutri_Sodio_429" : None,
	"InfNutri_Perc_Sodio_429" : None,
	"InfNutri_QuantidadeCaseira_429" : None,
	"InfNutri_UM_Qtde_429" : None,
	"InfNutri_UM_ValorEnergetico_429" : None,
	"InfNutri_UM_Carboidratos_429" : None,
	"InfNutri_UM_Proteinas_429" : None,
	"InfNutri_UM_GordurasTotais_429" : None,
	"InfNutri_UM_GordurasSat_429" : None,
	"InfNutri_UM_GordurasTrans_429" : None,
	"InfNutri_UM_Colesterol_429" : None,
	"InfNutri_UM_FibraAlimentar_429" : None,
	"InfNutri_UM_Calcio_429" : None,
	"InfNutri_UM_Ferro_429" : None,
	"InfNutri_UM_Sodio_429" : None,
	"InfNutri_DescricaoPorcao_429" : None,
	"InfNutri_QuantidadeCaseira_UM_429" : None,
	"InfNutri_AcucaresTotais_429" : None,
	"InfNutri_Perc_AcucaresTotais_429" : None,
	"InfNutri_AcucaresAdicionados_429" : None,
	"InfNutri_Perc_AcucaresAdicionados_429" : None,
	"InfNutri_UM_AcucaresTotais_429" : None,
	"InfNutri_UM_AcucaresAdicionados_429" : None,
	"InfNutri_UM_Caseira_429" : None,
	"InfNutri_Lactose_429" : None,
	"InfNutri_Perc_Lactose_429" : None,
	"InfNutri_UM_Lactose_429" : None,
	"InfNutri_Galactose_429" : None,
	"InfNutri_Perc_Galactose_429" : None,
	"InfNutri_UM_Galactose_429" : None,
	"InfNutri_CodigoAdicional_429" : None,
	"InfNutri_ValorCodigoAdicional_429" : None,
	"EnviaBalanca_Promocao" : 1