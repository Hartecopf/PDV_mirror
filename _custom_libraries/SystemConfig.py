
# SETTINGS 
# -> Project Libraries ::
#from DataCentralizer import DataCentralizer

# -> Built-in Modules, External Resources and Robot Modules ::
import operator as ope
from random import randint as rint
from utilities.TextFormater import *
from utilities.ColorText import log, logger5

from FireBirdConnector import FbConnector
from Base import Centralizer as Central, ExternalFile

PcLog = logger5()

class PDVConfig(object):
    _name = 'SystemConfig'
    _config_instance = None
    config_path:str = Central.path_pdv_settings

    def __new__(cls):
        if cls._config_instance is None:
            cls._config_instance = super(PDVConfig, cls).__new__(cls)
        return cls._config_instance
        
    def __init__(self) -> None:
        pass

    # KEYBOARD SHORTCUT...
    @staticmethod
    def Create_And_Call_Keyboard_Query():
        format_text = list()
        ExternalFile.set_file_path(Central.path_pdv_settings)
        config_file = ExternalFile.read_file()
        config_query:str = 'SELECT %s FROM CONFIG_TECLADO WHERE CONFIG_ID = 0'

        keyboard_keys:dict = config_file['keyboard_keys']
        for elem in keyboard_keys.keys():
            format_text.append(elem)
        format_text = tuple(format_text)
        # debug in ...//log.html file 
        print("👀 Look at The Results to 'format_text':\n")
        for i in range(0, len(format_text), 3):
            print(format_text[i:(i+3)]) if(ope.lt((i+3), len(format_text))) else print(format_text[i:])
        #... and goes on    
        var:str = ', '.join(map(str, format_text[:])); config_query = (config_query %var)
        print("\n◆ RESULT AFTER FORMATING PROCESS:\n'config_query': %s" %(config_query,))
        FbConnector.Change_Connection()
        result:tuple = FbConnector.Execute_Query_Function(
            query_text= config_query, table_name= 'CONFIG_TECLADO')
        
        print("\nLook at results from FbConnector.Connection:")
        for e in range(len(result)):
            print('%s: %s' %(format_text[e], result[e]))
        PDVConfig.Set_File_Settings(config_file, result, config_file['keyboard_keys'])
    
    @staticmethod
    def Set_File_Settings(
            full_file:dict, 
            file_get:tuple|dict, 
            file_set:dict, 
            set_byname:bool=False):
        
        print("\n▶ Applying the new values in the".upper() + " 'file_set'...")
        if((set_byname is False) and (not isinstance(file_get, dict))):
            count:int = 0
            for elem in file_set.keys():
                file_set.__setitem__(elem, file_get[count])
                print("▸ '%s' ↻: %s" %(elem, file_set.get(elem)))
                count = ope.iadd(count, int(1))
            ExternalFile.write_on_file(full_file)
            print("\n✅ The file has been updated!\n")

        # This clause bellow considers the <builtin>:'dict_keys' equals between 
        # 'file_set' and 'file_get' when both are dictionaries...
        elif((set_byname is True) and (isinstance(file_get, dict))):
            for e_named in file_set.keys():
                extraction:dict = file_get.get(e_named)
                file_set.__setitem__(e_named, extraction.get('_value'))
                print("▸ '%s' ↻: %s" %(e_named, file_set.get(e_named)))
            ExternalFile.write_on_file(full_file)
            print("\n✅ The file has been updated!\n")
        else:
            print("¡This function requires a value for <bool> 'set_byname' argument!")
            raise ValueError()
        return


    # ANOTHER DATABASE SETTINGS...
    @staticmethod
    def Create_And_Call_System_Functions_Quey():
        #------------------------------------------------------------------------------------------------------------//
        # FIRST STEP...                                          [ConfigPDV.FDB]
        # Format necessary to the compreension and building of the SELECT QUERY:
        #------------------------------------------------------------------------------------------------------------\\
        functs_seq:list = [
            ('CONFIG_NFPAULISTA', 'NFPAULISTA_HABILITADO'),
            ('CONFIG_NFCE', 
                'NFCE_SOLICITAIMPRESSAONFCE',
                'NFCE_SERIENFCE'),
            ('CONFIG_OPCOES',
                'OPCOES_BAIXACREDIARIO',
                'OPCOES_BLOQUEARDESCONTOPROMOCAO',
                'OPCOES_IMPRIMEDAV',
                'OPCOES_SANGRIAOBSERVACAO', 
                'OPCOES_SOLICITAOBSERVACAOVENDA',
                'OPCOES_RECEBIMENTOCARTAOTAXAACR',
                'OPCOES_PROMOFINALIZADORAS',
                'OPCOES_IMPRESSAOPIX'), 
            ('CONFIG_CAIXA', 'CAIXA_TIMERPIX') ]             
        
        # This object will store the results against from Firebird Server Connection...
        local_results = list(); dict_result = dict()
        config_file = ExternalFile.read_file()
        # ptrin on html output file...
        for i in range(len(functs_seq)):
            if((isinstance(functs_seq[i], tuple)) and (len(functs_seq[i]) <= 2)):
                print('functs_seq[%s]: %s' %(i, functs_seq[i]))
            else:
                for e in range(len(functs_seq[i])):
                    print('%s functs_seq[%s] in [%s]: %s' %(expand(size=4), i, e, functs_seq[i][e]))

        print("\n👀 Look at the concating process has made from <list> 'functs_seq' indexes:".upper())
        create_line(70, break_line=True, to_the_end=True, cmd='print')

        # It Reads and concats the compreension tuple replacing their components
        # where is necessary to the 'dinamic_query' adjustment...
        FbConnector.Change_Connection()
        for seq in range(len(functs_seq)):
            dinamic_query:str = 'SELECT {} FROM {} WHERE CONFIG_ID = 0'
            print("seq: [%s]" %seq + "\nElement in functs_seq[%s]: %s" %(seq, functs_seq[seq]))
            compreension:tuple = (
                functs_seq[seq][0], 
                (functs_seq[seq][1] if(ope.le(len(functs_seq[seq]), 2)) else tuple(functs_seq[seq][1:])))
            print("compreension: %s" %(compreension,))
            dinamic_query = (
                dinamic_query.format(
                    (compreension[1]
                     if(isinstance(compreension[1], str)) 
                     else ', '.join(map(str, compreension[1]))), compreension[0])) #-> tuple
            print('\n🔍 dinamic_query:\n%s\n' %(dinamic_query,))
            
            # Querying Database...
            result = FbConnector.Execute_Query_Function(
                query_text= dinamic_query, table_name= compreension[0])
            # Recording Data Results...
            print("\nLook at results from FbConnector.Connection:\nRESULT: %s" %(result,))
            if((isinstance(result, tuple)) and (ope.gt(len(result), int(1)))):
                for i in range(len(result)):
                    local_results.append(result[i]) if(result[i] not in ('', ' ')) else None
                    dict_result.update([(compreension[1][i], {'_value':local_results[-1], })])
            else: 
                local_results.append(result[0])
                dict_result.update([(compreension[1], {'_value':local_results[-1], })])
            print("<list>: 'local_results' has been updated: %s" %(local_results,))
            create_line(250, break_line=True, to_the_end=True, cmd='print')

        #------------------------------------------------------------------------------------------------------------//
        # SECOND STEP...                         [PDVOFF.FDB]
        # Replace string conenction to the FireBird Server...
        #------------------------------------------------------------------------------------------------------------\\
        other_seq:list = [
            ('CONFIG', 
                'VALORMINIMOSANGRIAPDV', 
                'TROCA_VALORES_CASO_TOTAL_MAIOR', 
                'TABELA_PRECO_TROCA_VALORES',
                'VALOR_PARA_TROCA_VALORES', 
                'NAOPROMOCAOVENDAPRAZO', 
                'CONTROLACREDITOCLIENTES')]

        for e in range(len(other_seq)): print('other_seq[%s]: %s' %(e, other_seq[e]))
        print("\n👀 Look at the concating process has made from <list> 'other_seq' indexes:".upper())
        create_line(70, break_line=True, to_the_end=True, cmd='print')

        FbConnector.Restore_Connection()
        for seq in range(len(other_seq)):
            dinamic_query:str = 'SELECT {} FROM {} WHERE SEQUENCIA = 1'
            print("seq: [%s]" %seq + "\nElement in 'other_seq'[%s]: %s" %(seq, other_seq[seq]))
            compreension:tuple = (
                other_seq[seq][0], 
                (other_seq[seq][1] if(ope.le(len(other_seq[seq]), 2)) else tuple(other_seq[seq][1:])))
            print("compreension: %s" %(compreension,))
            dinamic_query = (
                dinamic_query.format(
                    (compreension[1] 
                     if(isinstance(compreension[1], str)) 
                     else ', '.join(map(str, compreension[1]))), compreension[0])) #-> tuple
            print('\n🔍 dinamic_query:\n%s\n' %(dinamic_query,))
            # Querying Database...
            result = FbConnector.Execute_Query_Function(
                query_text= dinamic_query, table_name= compreension[0])
            # Recording Data Results...
            print("\n👁‍🗨 Look at results from FbConnector.Connection:\nRESULT: %s" %(result,))
            if((isinstance(result, tuple)) and (ope.gt(len(result), int(1)))):
                for i in range(len(result)):
                    local_results.append(result[i]) if(result[i] not in ('', ' ')) else None
                    dict_result.update([(compreension[1][i], {'_value':local_results[-1], })])
            else: 
                local_results.append(result[0])
                dict_result.update([(compreension[1], {'_value':local_results[-1], })])
            print("<list>:'local_results' has been updated: %s" %(local_results,))
            create_line(250, break_line=True, to_the_end=True, cmd='print')
        
        # FINISHING...
        print("\n▶ Applying this settings from [ConfigPPDV.FDB] & [PDVOFF.FDB] to the {ConfigPDV.yaml} file...".upper() +
            "\n  This system settings will be part of the libraries behaviour and its data groups.")
        for _key in dict_result.keys(): print("▸ dict_results in '%s': %s" %(_key, dict_result[_key]))
        PDVConfig.Set_File_Settings(config_file, dict_result, config_file['function_keys'], set_byname=True)
        return
    
    # FINISHING DATA SERIALIZATION AND CLOSE CONNECTION ::
    @staticmethod
    def Close_System_Settings_Loading(): 
        FbConnector.Close_Connection(); return

    @staticmethod
    def Read_System_Config(show:bool=True):
         ExternalFile.set_file_path(Central.path_pdv_settings, show)
         return ExternalFile.read_file()
