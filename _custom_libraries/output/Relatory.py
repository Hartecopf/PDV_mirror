
# SETTINGS 
# -> Project Libraries ::
import operator as ope
from Base import Centralizer as Central, Storage

# -> Custom Modules has created to the Porject ::
from utilities.TextFormater import *
from utilities.ColorText import log, logger1, logger2, logger3, logger5

RtLog1 = logger1()
RtLog2 = logger2()
RtLog3 = logger3()
RtLog5 = logger5()


def show_relatory(table_size:int= 51) -> None:
    data_format:tuple = ('Venda Nº', 'NFCe Nº', 'Valor Final', 'Troco', 'Status', 'Cliente', 'Ident.Cliente')
    msg_formated = format_fields(25, str_fields= data_format, to_the_end=':')
    all_s_cde:list = Storage.last_sale_code()            #\\ ... all the sale's code has performed
    all_docmt:list = Storage.last_fiscal_document()      #\\ ... all the tax documents has recorded
    all_s_vls:list = Storage.last_sale_value()           #\\ ... all the sale's value has computed
    all_s_dif:list = Storage.last_sale_difference()      #\\ ... all the sale's difference from final velues...
    all_s_sts:list = Storage.last_sale_status()          #\\ ... all the final sale's status after their finishment
    all_custm:list = Storage.last_customer_ident()       #\\ ... all the custmer's code has stored for each sale event
    text_structure = list(); customer:str=''; client_type:str='' 

    for i in range(len(all_s_cde)):
        if(all_custm[i] is not None):
            customer = all_custm[i]
            client_type: str = 'CNPJ' if ope.gt(str(all_custm[i]).__len__(), 11) else 'CPF'
        else:
            customer = 'Default'
            client_type = 'Not Informed'
        pass
        sale_status = 'Canceled' if(ope.eq(all_s_sts[i], 'x')) else str(all_s_sts[i])
        formating:tuple= (
            str(msg_formated[0] + str(all_s_cde[i])), 
            str(msg_formated[1] + str(all_docmt[i])),
            str(msg_formated[2] + str(all_s_vls[i])), 
            str(msg_formated[3] + str(all_s_dif[i])), 
            str(msg_formated[4] + sale_status),
            str(msg_formated[5] + customer),
            str(msg_formated[6] + client_type))
        text_structure.append(formating)

    RtLog1.debug("%s" %(create_line(table_size, char='=', double_break=True, cmd='return'),))
    RtLog5.info(msg='%sPRATES RELATORY' %(expand(size=17),))
    RtLog1.debug("%s" %(create_line(table_size, char='=', cmd='return'),))
    for e in range(len(text_structure)):
        RtLog1.warn('%s[SALE EVENT Nº %s]' %(expand(size=16), e+1))
        RtLog1.debug("%s" %(create_line(table_size, cmd='return'),))
        for ee in range(len(text_structure[e])):
            if(ope.eq(ee, 0)): RtLog2.debug(msg= text_structure[e][ee])
            elif(ope.eq(ee, 1)): RtLog2.info(msg= text_structure[e][ee])    
            elif(ope.eq(ee, 2)): RtLog2.warn(msg= text_structure[e][ee])
            else: RtLog1.debug(msg= text_structure[e][ee])
        if(e < len(text_structure)): 
            RtLog1.debug("%s" %(create_line(table_size, cmd='return'),))
        elif(ope.eq(e, (len(text_structure) - 1))): 
            RtLog1.debug("%s" %(create_line(table_size, char='=', cmd='return'),))
    return


def show_cashier_relatory(table_size:int= 51) -> None:
    rplc:dict = Storage.cashier_conference()
    RtLog1.debug("%s" %(create_line(table_size, char='=', double_break=True, cmd='return'),))
    RtLog1.warn('%s[GENERAL CASHIER AUDICT]' %(expand(size=7),))
    RtLog1.debug("%s" %(create_line(table_size, char='=', cmd='return'),))
    for elem in rplc.keys():
        extract:dict = rplc[elem]
        replacement:tuple = format_keyValues(18, mapping= extract)
        for u in range(len(replacement)):
            RtLog1.debug(msg= replacement[u])
        RtLog1.debug("%s" %(create_line(41, cmd='return'),))
    return


def system_version(tbl_size:int=51, end_line:str='double | single') -> None:
    if(ope.lt(tbl_size, 41)): 
        log.info('\n', also_console=True); log.error('...')
        RtLog1.error(
            "\n❗[ArgumentException]:\nThe argument [tbl_size] in <def>:system_version" +
            "cannot be less of 'int(41)'.")
    elif(end_line in ('', ' ', None, 'null')): 
        log.info('\n', also_console=True); log.error('...')
        RtLog1.error(
            "\n❗[ArgumentException]:\nThe argument [end_line] in <def>:system_version" +
            "must be in ('double', 'single') and nothing more!.")
    else: pass
    
    single:bool = True if(ope.eq(end_line.lower(), 'single')) else False
    double:bool = True if(ope.eq(end_line.lower(), 'double')) else False

    RtLog1.debug("%s" %(create_line(tbl_size, char='=', break_line=single, double_break=double, cmd='return'),))
    RtLog1.debug("%s" %(dlmt_space(tbl_size, ("Project Version:", Central.project_version))),)
    RtLog2.info("%s" %(dlmt_space(tbl_size, ("PDV Version:", Central.pdv_version))),)
    RtLog2.debug("%s" %(dlmt_space(tbl_size, ("ERP Version:", Central.erp_version))),)
    RtLog1.debug("%s" %(create_line(tbl_size, char='=', break_line=True, to_the_end=True, cmd='return'),))
    return