
# PROJECT FOLDER DEPENDENCES :: 
from SystemConfig import PDVConfig
from Base import ExternalFile, Storage
from Base import Centralizer as Central
from Base import os, sys, co, subprocess
from input.ConfigLoader import PratesConfig
from robot.api.deco import library, keyword

from utilities.TextFormater import *
from utilities.ColorText import log, logger1, logger4, logger5

MyLog1 = logger4()
MyLog2 = logger5()
MyLog3 = logger1()


@library(scope= 'GLOBAL', version= '1.0', auto_keywords= False, doc_format= 'reST')
class ExternalPrograms(object):
    #\\ class' instance ::
    _external:object = None
   
    def __init__(cls) -> None:
        pass
    
    def __new__(cls):
        if cls._external is None:
            cls._external = super(ExternalPrograms, cls).__new__(cls)
        return  cls._external
    
    def check_for_tasklist() -> None:
        return
    
    def find_out_taskprocess() -> None:
        return
    
    def is_open() -> bool:
        return False | True
    
    @keyword(name='Call External Program')
    def Call_External_Program(cls, program_name:str) -> None:
        #\\... EXTENSIBLE PROGRAMS AVAILABLE ON nis PROJECT FOLDER ::
        programs:tuple = (
            'salesmatching',
            'fiscalcheckup', 
            'cardmovaudit', 
            'comparison', 
            'cashiermovement')

        #\\... EVALUATE FUNCRION ARGUMENT ACCORDING TO ::
        #1 Security clause ::
        if(program_name not in programs):
            log.info('', also_console=True); log.error('...')
            MyLog3.debug('%s' %(create_line(78, break_line=True, cmd='return'),))
            MyLog3.critical('%s' %(dlmt_space(78, ("❌ [ArgumentError]:", '|')),))
            MyLog3.error("THE 'program_name' FUNCTION ARGUMENT MUST BE AN ACEPTABLE VALUE!")
            MyLog3.debug('%s' %(create_line(78, cmd='return'),))
            raise ValueError()
        #2
        #\\... FiscalCheckup.py
        elif(ope.eq(program_name.lower(), 'fiscalcheckup')):
            create_line(78, cmd='print')
            nis = str(Central.nis_path + '\\fiscalcontrol\\config.yaml')
            print("🟢 Running External Program according to the seetings: %s" %nis)
            create_line(78, break_line= True, to_the_end= True, cmd='print')
            ExternalFile.set_file_path(nis)
            sttgs = ExternalFile.read_file()
            ExternalFile.print_file(sttgs)
            sys_sttg:dict = PDVConfig.Read_System_Config()
            pdv_sttgs:dict = sys_sttg.get('function_keys')
            exepath = str(Central.nis_path + '\\fiscalcontrol\\prates_FiscalCheckUp.py')
            os.system("start cmd /C python %s %s %s %s %s %s" %( 
                exepath, 
                Central.current_erp_sale_code(),
                Central.current_nfce_number(),
                pdv_sttgs.__getitem__('NFCE_SERIENFCE'),
                Central.company_internal_code(),
                str(Central.nis_path + '\\fiscalcontrol\\config.yaml')))
        return

    @keyword(name='PDV Info')
    def get_system_info(cls) -> None:
        "Show PDV's system info according to the `tasklist` line command."
        subprocess.run(["cmd", "/C", "tasklist", "/FI", "IMAGENAME eq MyCommercePDV.exe", "/V", "/FO", "LIST"])
        return
    