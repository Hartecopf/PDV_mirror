
import os
import yaml
import operator as ope
from typing import Any
from robot.api import logger as log

class Initial(object):
    _startup  = None
    _main_path:str = os.getcwd() + '\\..\\_init_.yaml'
    
    def __init__(self) -> None:
        pass

    def __new__(cls):
        if cls._startup is None:
            cls._startup = super(Initial, cls).__new__(cls)
        return cls._startup

    @classmethod
    def read_initial_files(cls) -> dict:
        with open(cls._main_path, 'r') as content:
            attribures = yaml.safe_load(content)
        return attribures

class ClassError():
  def __init__(cls) -> None:
    pass

  @staticmethod
  def ArgumentError(argmnt:tuple[str, ...]) -> ValueError:
    if(not ope.gt(argmnt.__len__(), 1)):
      log.info('\n', also_console=True); log.error('...')
      log.info("\n❌![ValueError]: Argument value *%s " %(argmnt[0],), also_console=True)
    else:
      log.info('\n', also_console=True); log.error('...')
      log.info(
        "\n❌![ValueError]: Argument name *%s " %(argmnt[0],) +
        "\nUnsupported type or value for @argument like %s "
        %(str(', '.join(map(str, argmnt[1:]))),), also_console=True)
    raise ValueError()
  
  @staticmethod
  def EntityBuildinError(argumnt:tuple[str, ...]) -> str:
    #\\... to be continued... 
    return

  @staticmethod
  def ReferenceNullException(argmnt:object, /, entity:str='') -> ReferenceError | None:
      """
      Returns `None` if the `argmnt` value is a valid data to the method builder.
      However, it returns a `ReferenceError()` if isn't that one.
      """
      return (None 
          if argmnt not in (None, '', 'empty', [], (), {}, [()], {()}, [(None,)], [('',)]) 
          else ClassError.ArgumentError(('argmnt', 'value: '+ str(argmnt), type(argmnt), 'entity: '+ str(entity))))

    
class DataCentralizer(object):
  """
  It supports and control all of generic sale's data manipulated during the sales
  event execution. Each sale's element is an `@entity` of the `DataCentralizer`
  master class and its elements could only be accessed througt its `@classmethod`
  writen as handler for those one.
  """

  # PDV System info:
  pdv_version: str = 'Empty'
  erp_version: str = 'Empty'
  project_version: str = '1.08.00'
  machine_name:str = ''
  sales_person_code: int = int()
  sales_person_name: str = ''
  cur_mysqlcnn: dict = {}
  cur_fbConfig: str = ''
  cur_fbOff: str = ''
  keyboard_keycodes: dict = {
    # Letter Keys...
    65:'A', 66:'B', 67:'C', 68:'D', 69:'E', 70:'F', 71:'G', 72:'H', 73:'I', 74:'J',
    75:'K', 76:'L', 77:'M', 78:'N', 79:'O', 80:'P', 81:'Q', 82:'R', 83:'S', 84:'T',
    85:'U', 86:'V', 87:'W', 88:'X', 89:'Y', 90:'Z',
    # Number keys...
    48:'NUM0', 49:'NUM1', 50:'NUM2', 51:'NUM3', 52:'NUM4', 53:'NUM5', 54:'NUM6',
    55:'NUM7', 56:'NUM8', 57:'NUM9',
    # Function Keys...
    112:'F1', 113:'F2', 114:'F3', 115:'F4', 116:'F5', 117:'F6', 118:'F7', 119:'F8',
    120:'F9', 121:'F10', 122:'F11', 123:'F12', 32:'SPACE', 9:'TAB', 27:'ESC', 36:'HOME',
    45:'INSERT', 35:'END', 40:'DOWN', 37:'LEFT', 39:'RIGTH', 38:'UP', 16:'SHIFT'}
  
  # CLASS INSTANCE ::
  _centralizer = None
  _customers: dict = {}
  _products: dict = {}

  # THESE CLASS  PROPERTIES REPRESETS THE CURRENT DATA STRUCTURE USED
  # AT RUN TIME FOR EACH ONE PROCCESS EXECUTED ACCORDING TO THE ROBOT
  # REQUESTIES HAS MADE DURING THE TEST CASES.

  # STANDARD DATA STRUCTURE ABOUT THIS PROJECT WITH ITS EXTERNAL FILES ::
  _save_db_contents:bool = True
  _content = Initial.read_initial_files()
  initial_files_path = Initial._main_path
  path_main_config:str = _content.get('main_config')
  path_config_bckp:str = _content.get('cnfg_backp')
  path_cashier_output:str = _content.get('cashier_output')
  path_local_storage:str = _content.get('local_storage')
  path_pdv_settings:str = _content.get('system_settings')
  nis_path:str = _content.get('nis_path')

  # USER SETTINGS FOR PERFORMATIC TEST SEQUENCE ::
  _prates_current_settings: dict = {}
    
  # DataCentralizer.py PROPERTIES ::
  _company_internal_code: int = int()
  _customer_code: int = 1
  _custom_code_on_sale: int = int()
  _current_cpf_cnpj: str = 'Empty'
  _customer_discount: float = 0
  _current_pdv_sale_code: int = int()
  _current_erp_sale_code: int = int()
  _current_nfce_number: int = int()
  _use_nfce_document: bool = True
  _current_sale_status: str = 'Empty'

  # Caculator.py PROPERTIES OF THE SALE::
  _products_for_sale: dict = dict()
  _group_prod_for_sale: dict = dict()
  _list_of_product_price: list = list()
  _final_sale_value: float = 0
  _sale_value_with_diff: float = 0
  _difference_from_value: float = 0
  _block_discount_for_promotion:bool = False

  # DataCentralizer.py PROPERTIES OF THE PROMOTION CONTROL ::
  _there_is_promotion_by_CPF: bool = False
  
  # OFFERS AND PROMOTIONS SUBPROCESS ::
  _prod_on_offer_controller: dict = dict()
  _prod_on_promotion_controller: dict = dict()
  _product_on_promotion_subdict: dict = dict()
  _produto_pesavel: dict = dict()

  # INTERNAL DATA SERIALIZATION ::
  _CnpjCpf_on_promotion_lint: list = list()
  _offer_controllers_storage: dict = dict()
  _promotion_controller_storage: dict = dict()
  _promotion_payment_controllers: dict = dict()
  _cpf_controller_storage: dict = dict()

  # STANDARD DATA BEHAVIOUR ::
  _cstat_check_out: bool = True
  _standard_product_code: int = int()
  _standard_customer_code: int = int()
  _default_customer_code: int = int()
  
  # STARTUP SETTINGS:
  _sangria_status_is_open: bool = False
  _sangria_counter_controller: bool = False
  _cancelling_sale_status: bool = False
    
  def __init__(self) -> None:
    return
  
  def __new__(cls):
    if cls._centralizer is None:
      cls._centralizer = super(DataCentralizer, cls).__new__(cls)
      return cls._centralizer
  
  # DataCentralizer.py SINGULAR PROPERTIES ::
  @classmethod
  def gett(cls, name) -> Any: return DataCentralizer.__getattribute__(cls, name)

  @classmethod
  def sett(cls, name, value): DataCentralizer.__setattr__(cls, name, value); return None


  @classmethod
  def prates_current_settings(cls, 
      __sttr:list[tuple[str, ...]] | dict = [('',)], __ope:str='get') -> dict|None:
    """
    \n<class> `DataCentralizer`
    \nMethod operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      if(not isinstance(__sttr, dict)):
        cls._prates_current_settings.update(__sttr)
        print("◾ @entity.setter:= Central._prates_current_settings has been successfully updated!")
      elif(isinstance(__sttr, dict)):
        cls._prates_current_settings = __sttr
        print("◾ @entity.setter:= Central._prates_current_settings has been successfully defined!")
    else:
      print('◽ @entity.getter:= Central._prates_current_settigns.__value() :: _countains(%s)' %list(cls._customers).__len__())
      return cls._prates_current_settings.copy()


  @classmethod
  def customers(cls,
    __sttr:list[tuple[str, ...]] | dict = [('',)], __ope:str='get', /, gt_log:bool=False, elem_key:str='') -> dict|None:
    """    
    \n<class> `DataCentralizer`   
    \n Method operators: `__ope`:
    \n* Positional-Only 'set' ⇒: `@attribute` =  `__sttr`
    \n* Positional-Only 'get' ⇒: `@attribute.__value__`
    \n* Positional Or Keyword 'gt_log' ⇒: @entity.getter.log `robot.html.log `
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      if(not isinstance(__sttr, dict)):
        cls._customers.update(__sttr)
        print("◾ @entity.setter:= Central.cls._customers has been successfully updated!")
      elif(isinstance(__sttr, dict)):
        cls._customers = __sttr
        print("◾ @entity.setter:= Central.cls._customers has been successfully defined!")
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      if(gt_log is True):
        charset = (lambda x: str(str(x)[:34] + '... }'))
        print('◽ @entity.getter:= Central._customers.__value(-1) :: %s, _countains(%s)' 
        %((charset(cls._customers.get(list(cls._customers).__getitem__(-1)))
           if ope.eq(elem_key, '') else charset(cls._customers.get(elem_key))), 
           list(cls._customers).__len__()))
      return cls._customers.copy()
  

  @classmethod
  def products(cls,
    __sttr:list[tuple[str, ...]] | dict = [('',)], __ope:str='get', /,
    gt_log:bool=False, elem_key:str='') -> dict|None:
    """    
    \n<class> `DataCentralizer`   
    \n Method operators: `__ope`:
    \n* Positional-Only 'set' ⇒: `@attribute` =  `__sttr`
    \n* Positional-Only 'get' ⇒: `@attribute.__value__`
    \n* Positional Or Keyword 'gt_log' ⇒: @entity.getter.log `robot.html.log `
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      if(not isinstance(__sttr, dict)):
        cls._products.update(__sttr)
        print("◾ @entity.setter:= Central._products has been successfully updated!")
      elif(isinstance(__sttr, dict)):
        cls._products = __sttr
        print("◾ @entity.setter:= Central._products has been successfully defined!")
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      if(gt_log is True):
        charset = (lambda x: str(str(x)[:34] + '... }'))
        print('%s %s, _countains(%s)' 
        %(('◽ @entity.getter:= Central._products.__value(-1) ::' 
           if ope.eq(elem_key, '') 
           else f'◽ @entity.getter:= Central._products.__value({elem_key}) ::'),
          (charset(cls._products.get(list(cls._products).__getitem__(-1)))
           if ope.eq(elem_key, '') else charset(cls._products.get(elem_key))),
           list(cls._products).__len__()))
      return cls._products.copy()


  @classmethod
  def company_internal_code(cls, __sttr:int=int(), __ope:str='get') -> int|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      if(ope.gt(__sttr, int())):
        cls._company_internal_code = __sttr
        print("◾ @entity.setter:= Central._company_internal_code ->: %s" %cls._company_internal_code)
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Central._company_internal_code.__value() :: %s' %cls._company_internal_code) 
      return cls._company_internal_code


  @classmethod
  def customer_code(cls, __sttr:int=int(), __ope:str='get') -> int|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      if(ope.gt(__sttr, int())):
        cls._customer_code = __sttr
        print("◾ @entity.setter:= Central._customer_code ->: %s" %cls._customer_code)
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Central._customer_code.__value() :: %s' %cls._customer_code) 
      return cls._customer_code


  @classmethod
  def current_cpf_cnpj(cls, __sttr:str='Empty', __ope:str='get') -> str|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr.lower() if __sttr is not None else 'Not Informed')
      cls._current_cpf_cnpj = __sttr
      print("◾ @entity.setter:= Central._current_cpf_cnpj ->: %s" %cls._current_cpf_cnpj)
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print("◽ @entity.getter:= Central._current_cpf_cnpj.__value() :: %s" %cls._current_cpf_cnpj) 
      return cls._current_cpf_cnpj


  @classmethod
  def customer_discount(cls, __sttr:float=0, __ope:str='get') -> float|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      cls._customer_discount = __sttr
      print("◾ @entity.setter:= Central.cls._customer_discount ->: %s" %cls._customer_discount)
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Central.cls._customer_discount.__value() :: %s' %cls._customer_discount) 
      return cls._customer_discount


  @classmethod
  def current_pdv_sale_code(cls, __sttr:int=int(), __ope:str='get') -> int|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      if(ope.gt(__sttr, int())):
        cls._current_pdv_sale_code = __sttr
        print("◾ @entity.setter:= Central._current_pdv_sale_code ->: %s" %cls._current_pdv_sale_code)
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Central._current_pdv_sale_code.__value() :: %s' %cls._current_pdv_sale_code) 
      return cls._current_pdv_sale_code


  @classmethod
  def current_erp_sale_code(cls, __sttr:int=int(), __ope:str='get') -> int|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      if(ope.gt(__sttr, int())):
        cls._current_erp_sale_code = __sttr
        print("◾ @entity.setter:= Central._current_erp_sale_code ->: %s" %cls._current_erp_sale_code)
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Central._current_erp_sale_code.__value() :: %s' %cls._current_erp_sale_code) 
      return cls._current_erp_sale_code


  @classmethod
  def current_nfce_number(cls, __sttr:int=int(), __ope:str='get') -> int|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      if(ope.gt(__sttr, int())):
        cls._current_nfce_number = __sttr
        print("◾ @entity.setter:= Central._current_nfce_number ->: %s" %cls._current_nfce_number)
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Central._current_nfce_number.__value() :: %s' %cls._current_nfce_number) 
      return cls._current_nfce_number


  @classmethod
  def use_nfce_document(cls, __sttr:bool=True, __ope:str='get') -> bool|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      cls._use_nfce_document = __sttr if(ope.ne(__sttr, cls._use_nfce_document)) else cls._use_nfce_document
      print("◾ @setter:= Central.cls._use_nfce_document ->: %s" %cls._use_nfce_document)
    elif(__ope.lower() not in ('set', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Central._use_nfce_document.__value() :: %s' %cls._use_nfce_document) 
      return cls._use_nfce_document


  @classmethod
  def current_sale_status(cls, __sttr:str='Empty', __ope:str='get') -> str|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr.lower())
      cls._current_sale_status = __sttr
      print("◾ @entity.setter:= Central._current_sale_status ->: %s" %cls._current_sale_status)
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print("◽ @entity.getter:= Central._current_sale_status.__value() :: %s" %cls._current_sale_status) 
      return cls._current_sale_status


  # DataCentralizer -> Caculator.py PROPERTIES OF THE SALE::
  @classmethod
  def products_for_sale(cls, 
    __sttr:list[tuple[str, ...]] | dict = [('',)], __ope:str='get', 
    gt_log:bool=False, elem_key:str='') -> dict|None:
    """    
    \n<class> `DataCentralizer`   
    \n Method operators: `__ope`:
    \n* Positional-Only 'set' ⇒: `@attribute` =  `__sttr`
    \n* Positional-Only 'clear' ⇒: @ttribute.clear()
    \n* Positional-Only 'get' ⇒: `@attribute.__value__`
    \n* Positional Or Keyword 'gt_log' ⇒: @entity.getter.log `robot.html.log `
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      if(not isinstance(__sttr, dict)):
        cls._products_for_sale.update(__sttr)
        print("◾ @entity.setter:= Central._products_for_sale has been successfully updated!")
      elif(isinstance(__sttr, dict)):
        cls._products_for_sale = __sttr
        print("◾ @entity.setter:= Central._products_for_sale has been successfully defined!")
    
    elif(ope.eq(__ope.lower(), 'clear')):
        cls._products_for_sale.clear()
        print("◾ @entity.setter:= Central._products_for_sale has been successfully cleared!")
    
    elif(__ope.lower() not in ('set', 'get', 'clear')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    
    else:
      if((gt_log is True) and (list(cls._products_for_sale).__len__() != int())):
        charset = (lambda x: str(str(x)[:34] + '... }'))
        print('◽ @entity.getter:= Central._products_for_sale.__value(-1) :: %s, _countains(%s)' 
        %((charset(cls._products_for_sale.get(list(cls._products_for_sale).__getitem__(-1)))
        if ope.eq(elem_key, '') else charset(cls._products_for_sale.get(elem_key))),
        list(cls._products_for_sale).__len__()))

      elif((gt_log is True) and (list(cls._products_for_sale).__len__() == int())):
        print('◽ @entity.getter:= Central._products_for_sale() is Empty')
      
      else:pass
      return cls._products_for_sale.copy()

  
  @classmethod
  def group_prod_for_sale(cls,
    __sttr:list[tuple[str, ...]] | dict = [('',)], __ope:str='get', gt_log:bool=False) -> dict|None:
    """    
    \n<class> `DataCentralizer`   
    \n Method operators: `__ope`:
    \n* Positional-Only 'set' ⇒: `@attribute` =  `__sttr`
    \n* Positional-Only 'clear' ⇒: @ttribute.clear()
    \n* Positional-Only 'get' ⇒: `@attribute.__value__`
    \n* Positional Or Keyword 'gt_log' ⇒: @entity.getter.log `robot.html.log `
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      if(not isinstance(__sttr, dict)):
        cls._group_prod_for_sale.update(__sttr)
        print("◾ @entity.setter:= Central._group_prod_for_sale has been successfully updated!")
      elif(isinstance(__sttr, dict)):
        cls._group_prod_for_sale = __sttr
        print("◾ @entity.setter:= Central._group_prod_for_sale has been successfully defined!")
    
    elif(ope.eq(__ope.lower(), 'clear')):
      cls._group_prod_for_sale.clear()
      print("◾ @entity.setter:= Central._group_prod_for_sale has been successfully cleared!")

    elif(__ope.lower() not in ('set', 'get', 'clear')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    
    else:
      if(gt_log is True):
        charset = (lambda x: str(str(x)[:34] + '... }'))
        print('◽ @entity.getter:= Central._group_prod_for_sale.__value(-1) :: %s, _countains(%s)' 
        %(charset(cls._group_prod_for_sale.get(list(cls._group_prod_for_sale).__getitem__(-1))), 
        list(cls._group_prod_for_sale).__len__()))
      return cls._group_prod_for_sale.copy()


  @classmethod
  def list_of_product_price(cls, __sttr:float=0.0, __ope:str='get', /, gt_log:bool=False) -> list|None:
    """    
    \n<class> `DataCentralizer`   
    \n Method operators: `__ope`:
    \n* Positional-Only 'set' ⇒: `@attribute` =  `__sttr`
    \n* Positional-Only 'clear' ⇒: @ttribute.clear()
    \n* Positional-Only 'get' ⇒: `@attribute.__value__`
    \n* Positional Or Keyword 'gt_log' ⇒: @entity.getter.log `robot.html.log `
    """
    if((__ope.lower() == 'set')): 
      ClassError.ReferenceNullException(__sttr)
      if(isinstance(__sttr, list)):
        cls._list_of_product_price = __sttr
        print("◾ @entity.setter:= Central._list_of_product_price has been successfully defined!")
      elif(isinstance(__sttr, float)):
        cls._list_of_product_price.append(__sttr)
        print("◾ @entity.setter:= Central._list_of_product_price has been successfully increased!")
    
    elif(ope.eq(__ope.lower(), 'clear')):
      cls._list_of_product_price.clear()
      print("◾ @entity.setter:= Central._list_of_product_price has been successfully cleared!")

    elif(__ope.lower() not in ('set', 'get', 'clear')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    
    else:
      if(gt_log is True):
        print('◽ @entity.getter:= Central._list_of_product_price.__value(-1) :: %s, _countains(%s)' 
        %(cls._list_of_product_price.__getitem__(-1), cls._list_of_product_price.__len__()))
      return cls._list_of_product_price


  @classmethod
  def final_sale_value(cls, __sttr:float=0.0, __ope:str='get') -> float|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      cls._final_sale_value = __sttr
      print("◾ @entity.setter:= Central.cls._final_sale_value ->: %s" %cls._final_sale_value)
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Central.cls._final_sale_value.__value() :: %s' %cls._final_sale_value)
      return cls._final_sale_value


  @classmethod
  def sale_value_with_diff(cls, __sttr:float=0.0, __ope:str='get') -> float|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      cls._sale_value_with_diff = __sttr
      print("◾ @entity.setter:= Central.cls._sale_value_with_diff ->: %s" %cls._sale_value_with_diff)
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Central.cls._sale_value_with_diff.__value() :: %s' %cls._sale_value_with_diff)
      return cls._sale_value_with_diff


  @classmethod
  def difference_from_value(cls, __sttr:float=0.0, __ope:str='get') -> float|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      cls._difference_from_value = __sttr
      print("◾ @entity.setter:= Central.cls._difference_from_value ->: %s" %cls._difference_from_value)
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Central.cls._difference_from_value.__value() :: %s' %cls._difference_from_value)
      return cls._difference_from_value


  @classmethod
  def block_discount_for_promotion(cls, __sttr:bool=True, __ope:str='get') -> bool|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    ClassError.ReferenceNullException(__sttr)
    if(ope.eq(__ope.lower(), 'set')):
      cls._block_discount_for_promotion = (__sttr 
                                           if(ope.ne(__sttr, cls._block_discount_for_promotion))
                                           else cls._block_discount_for_promotion)
      print("◾ @setter:= Central.cls._block_discount_for_promotion ->: %s" 
            %cls._block_discount_for_promotion)
    elif(__ope.lower() not in ('set', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Central._block_discount_for_promotion.__value() :: %s'
             %cls._block_discount_for_promotion)    
      return cls._block_discount_for_promotion


  # OFFERS AND PROMOTIONS SUBPROCESS ::
  @classmethod
  def there_is_promotion_by_CPF(cls, __sttr:bool=True, __ope:str='get') -> bool|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    ClassError.ReferenceNullException(__sttr)
    if(ope.eq(__ope.lower(), 'set')):
      cls._there_is_promotion_by_CPF = (__sttr 
                                           if(ope.ne(__sttr, cls._there_is_promotion_by_CPF))
                                           else cls._there_is_promotion_by_CPF)
      print("◾ @setter:= Central.cls._there_is_promotion_by_CPF ->: %s" 
            %cls._there_is_promotion_by_CPF)
    elif(__ope.lower() not in ('set', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Central._there_is_promotion_by_CPF.__value() :: %s'
             %cls._there_is_promotion_by_CPF)       
      return cls._there_is_promotion_by_CPF


  @classmethod
  def prod_on_offer_controller(cls, 
    __sttr:list[tuple[str, ...]] | dict = [('',)], __ope:str='get', /,
    gt_log:bool=False, elem_key:str='') -> dict|None:   
    """    
    \n<class> `DataCentralizer`   
    \n Method operators: `__ope`:
    \n* Positional-Only 'set' ⇒: `@attribute` =  `__sttr`
    \n* Positional-Only 'clear' ⇒: @ttribute.clear()
    \n* Positional-Only 'get' ⇒: `@attribute.__value__`
    \n* Positional Or Keyword 'gt_log' ⇒: @entity.getter.log `robot.html.log `
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr, entity='prod_on_offer_controller')
      if(not isinstance(__sttr, dict)):
        cls._prod_on_offer_controller.update(__sttr)
        print("◾ @entity.setter:= Central._prod_on_offer_controller has been successfully updated!")
      elif(isinstance(__sttr, dict)):
        cls._prod_on_offer_controller = __sttr
        print("◾ @entity.setter:= Central._prod_on_offer_controller has been successfully defined!")
    
    elif(ope.eq(__ope.lower(), 'clear')):
      cls._prod_on_offer_controller.clear()
      print("◾ @entity.setter:= Central._prod_on_offer_controller has been successfully cleared!")

    elif(__ope.lower() not in ('set', 'get', 'clear')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    
    else:
      if((gt_log is True) and (list(cls._prod_on_offer_controller).__len__() != int())):
        charset = (lambda x: str(str(x)[:34] + '... }'))
        print('◽ @entity.getter:= Central._prod_on_offer_controller.__value(-1) :: %s, _countains(%s)' 
        %((charset(cls._prod_on_offer_controller.get(list(cls._prod_on_offer_controller).__getitem__(-1)))
        if ope.eq(elem_key, '') else charset(cls._prod_on_offer_controller.get(elem_key))),
        list(cls._prod_on_offer_controller).__len__()))
      
      elif((gt_log is True) and (list(cls._prod_on_offer_controller).__len__() == int())):
        print('◽ @entity.getter:= Central._prod_on_offer_controller() is Empty')
      
      else: pass
      return cls._prod_on_offer_controller.copy()


  @classmethod
  def prod_on_promotion_controller(cls,  
    __sttr:list[tuple[str, ...]] |dict = [('',)], __ope:str='get', /,
    gt_log:bool=False, elem_key:str='') -> dict|None:
    """    
    \n<class> `DataCentralizer`   
    \n Method operators: `__ope`:
    \n* Positional-Only 'set' ⇒: `@attribute` =  `__sttr`
    \n* Positional-Only 'clear' ⇒: @ttribute.clear()
    \n* Positional-Only 'get' ⇒: `@attribute.__value__`
    \n* Positional Or Keyword 'gt_log' ⇒: @entity.getter.log `robot.html.log `
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr, entity='prod_on_promotion_controller')
      if(not isinstance(__sttr, dict)):
        cls._prod_on_promotion_controller.update(__sttr)
        print("◾ @entity.setter:= Central._prod_on_promotion_controller has been successfully updated!")
      elif(isinstance(__sttr, dict)):
        cls._prod_on_promotion_controller = __sttr
        print("◾ @entity.setter:= Central._prod_on_promotion_controller has been successfully defined!")
    
    elif(ope.eq(__ope.lower(), 'clear')):
      cls._prod_on_promotion_controller.clear()
      print("◾ @entity.setter:= Central._prod_on_promotion_controller has been successfully cleared!")
    
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    
    else:
      if((gt_log is True) and (list(cls._prod_on_promotion_controller).__len__() != int())):
        charset = (lambda x: str(str(x)[:34] + '... }'))
        print('◽ @entity.getter:= Central._prod_on_promotion_controller.__value(-1) :: %s, _countains(%s)'
        %((charset(cls._prod_on_promotion_controller.get(list(cls._prod_on_promotion_controller).__getitem__(-1)))
        if ope.eq(elem_key, '') else charset(cls._prod_on_promotion_controller.get(elem_key))),
        list(cls._prod_on_promotion_controller).__len__()))
      
      elif((gt_log is True) and (list(cls._prod_on_promotion_controller).__len__() == int())):
        print('◽ @entity.getter:= Central._prod_on_promotion_controller() is Empty')
      
      else: pass
      return cls._prod_on_promotion_controller.copy()

  
  @classmethod
  def product_on_promotion_subdict(cls,  
    __sttr:list[tuple[str, ...]] = [('',)], __ope:str='get', /, gt_log:bool=False) -> dict|None:
    """    
    \n<class> `DataCentralizer`   
    \n Method operators: `__ope`:
    \n* Positional-Only 'set' ⇒: `@attribute` =  `__sttr`
    \n* Positional-Only 'clear' ⇒: @ttribute.clear()
    \n* Positional-Only 'get' ⇒: `@attribute.__value__`
    \n* Positional Or Keyword 'gt_log' ⇒: @entity.getter.log `robot.html.log `
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      if(not isinstance(__sttr, dict)):
        cls._product_on_promotion_subdict.update(__sttr)
        print("◾ @entity.setter:= Central._product_on_promotion_subdict has been successfully updated!")
      elif(isinstance(__sttr, dict)):
        cls._product_on_promotion_subdict = __sttr
        print("◾ @entity.setter:= Central._product_on_promotion_subdict has been successfully defined!")
    
    elif(ope.eq(__ope.lower(), 'clear')):
      cls._product_on_promotion_subdict.clear()
      print("◾ @entity.setter:= Central._product_on_promotion_subdict has been successfully cleared!")

    elif(__ope.lower() not in ('set', 'get', 'clear')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    
    else:
      if((gt_log is True) and (list(cls._product_on_promotion_subdict).__len__() != int())):
        charset = (lambda x: str(str(x)[:34] + '... }'))
        print('◽ @entity.getter:= Central._product_on_promotion_subdict.__value(-1) :: %s, _countains(%s)'
        %(charset(cls._product_on_promotion_subdict.get(list(cls._product_on_promotion_subdict).__getitem__(-1))),
        list(cls._product_on_promotion_subdict).__len__()))
      
      elif((gt_log is True) and (list(cls._product_on_promotion_subdict).__len__() == int())):
        print('◽ @entity.getter:= Central._product_on_promotion_subdict() is Empty')
      
      else: pass
      return cls._product_on_promotion_subdict.copy()

  
  @classmethod
  def produto_pesavel(cls, __sttr:list[tuple[str, ...]] | dict = [('',)], __ope:str='get') -> dict|None:
    """    
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      if(not isinstance(__sttr, dict)):
        cls._produto_pesavel.update(__sttr)
        print("◾ @entity.setter:= Central._produto_pesavel has been successfully updated!")
      elif(isinstance(__sttr, dict)):
        cls._produto_pesavel = __sttr
        print("◾ @entity.setter:= Central._produto_pesavel has been successfully defined!")
    
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    
    else:
      print('◽ @entity.getter:= Central._produto_pesavel.__value() :: _count(%s)' 
            %(len(list(cls._produto_pesavel.keys())))) 
      return cls._produto_pesavel.copy()

  
  @classmethod
  def CnpjCpf_on_promotion_list(cls,
    __sttr:str|list='Empty', __ope:str='get', /, gt_log:bool=False) -> list|None:
    """
      CPF/CNPJ `sequence` has writen to control the promotion lauching for products on sale when those one
      were in a promotion for CPF/CNPJ
    """
    
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr.lower() if isinstance(__sttr, str) else __sttr)
      if(isinstance(__sttr, list)):
        cls._CnpjCpf_on_promotion_lint = __sttr
        print("◾ @entity.setter:= Central._CnpjCpf_on_promotion_dict has been successfully defined!")
      elif(isinstance(__sttr, str)): 
        cls._CnpjCpf_on_promotion_lint.append(__sttr)
        print("◾ @entity.setter:= Central._CnpjCpf_on_promotion_dict has been successfully increased!")
    
    elif(ope.eq(__ope.lower(), 'clear')):
      cls._CnpjCpf_on_promotion_lint.clear()
      print("◾ @entity.setter:= Central._CnpjCpf_on_promotion_dict has been successfully cleared!")

    elif(__ope.lower() not in ('set', 'get', 'clear')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    
    else:
      if(gt_log is True):
        print('◽ @entity.getter:= Central._CnpjCpf_on_promotion_dict.__value(-1) :: %s, _countains(%s)' 
        %(cls._CnpjCpf_on_promotion_lint.__getitem__(-1)), cls._CnpjCpf_on_promotion_lint.__len__())
      return cls._CnpjCpf_on_promotion_lint


  @classmethod
  def offer_controllers_storage(cls, 
    __sttr:list[tuple[str, ...]] | dict = [('',)], __ope:str='get', /,
    gt_log:bool=False, elem_key:str='') -> dict|None:
    """    
    \n<class> `DataCentralizer`   
    \n Method operators: `__ope`:
    \n* Positional-Only 'set' ⇒: `@attribute` =  `__sttr`
    \n* Positional-Only 'get' ⇒: `@attribute.__value__`
    \n* Positional Or Keyword 'gt_log' ⇒: @entity.getter.log `robot.html.log `
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      if(not isinstance(__sttr, dict)):
        cls._offer_controllers_storage.update(__sttr)
        print("◾ @entity.setter:= Central._offer_controllers_storage has been successfully updated!")
      elif(isinstance(__sttr, dict)):
        cls._offer_controllers_storage = __sttr
        print("◾ @entity.setter:= Central._offer_controllers_storage has been successfully defined!")
    
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    
    else:
      if((gt_log is True) and (list(cls._offer_controllers_storage).__len__() != int())):
        charset = (lambda x: str(str(x)[:34] + '... }'))
        print('◽ @entity.getter:= Central._offer_controllers_storage.__value(-1) :: %s, _countains(%s)' 
        %((charset(cls._offer_controllers_storage.get(list(cls._offer_controllers_storage).__getitem__(-1)))
        if ope.eq(elem_key, '') else charset(cls._offer_controllers_storage.get(elem_key))),
        list(cls._offer_controllers_storage).__len__()))
      
      elif((gt_log is True) and (list(cls._offer_controllers_storage).__len__() == int())):
        print('◽ @entity.getter:= Central._offer_controllers_storage() is Empty')
      
      else: pass
      return cls._offer_controllers_storage.copy()


  @classmethod
  def promotion_controller_storage(cls, 
    __sttr:list[tuple[str, ...]] | dict = [('',)], __ope:str='get', /,
    gt_log:bool=False, elem_key:str='') -> dict|None:
    """    
    \n<class> `DataCentralizer`   
    \n Method operators: `__ope`:
    \n* Positional-Only 'set' ⇒: `@attribute` =  `__sttr`
    \n* Positional-Only 'get' ⇒: `@attribute.__value__`
    \n* Positional Or Keyword 'gt_log' ⇒: @entity.getter.log `robot.html.log `
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr, entity='promotion_controller_storage')
      if(not isinstance(__sttr, dict)):
        cls._promotion_controller_storage.update(__sttr)
        print("◾ @entity.setter:= Central._promotion_controller_storage has been successfully updated!")
      elif(isinstance(__sttr, dict)):
        cls._promotion_controller_storage = __sttr
        print("◾ @entity.setter:= Central._promotion_controller_storage has been successfully defined!")
    
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    
    else:
      if((gt_log is True) and (list(cls._promotion_controller_storage).__len__() != int())):
        charset = (lambda x: str(str(x)[:34] + '... }'))
        print('◽ @entity.getter:= Central._promotion_controller_storage.__value(-1) :: %s, _countains(%s)' 
        %((charset(cls._promotion_controller_storage.get(list(cls._promotion_controller_storage).__getitem__(-1)))
        if ope.eq(elem_key, '') else charset(cls._promotion_controller_storage.get(elem_key))),
        list(cls._promotion_controller_storage).__len__()))
      
      elif((gt_log is True) and (list(cls._promotion_controller_storage).__len__() == int())):
        print('◽ @entity.getter:= Central._promotion_controller_storage() is Empty')
      
      else: pass
      return cls._promotion_controller_storage.copy()

  
  @classmethod
  def payment_controllers(cls,
    __sttr:list[tuple[str, ...]] | dict = [('',)], __ope:str='get', /, 
    gt_log:bool=False, elem_key:str='') -> dict|None:
    """    
    \n<class> `DataCentralizer`   
    \n Method operators: `__ope`:
    \n* Positional-Only 'set' ⇒: `@attribute` =  `__sttr`
    \n* Positional-Only 'get' ⇒: `@attribute.__value__`
    \n* Positional Or Keyword 'gt_log' ⇒: @entity.getter.log `robot.html.log `
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      if(not isinstance(__sttr, dict)):
        cls._promotion_payment_controllers.update(__sttr)
        print("◾ @entity.setter:= Central._promotion_payment_controllers has been successfully updated!")
      elif(isinstance(__sttr, dict)):
        cls._promotion_payment_controllers = __sttr
        print("◾ @entity.setter:= Central._promotion_payment_controllers has been successfully defined!")
    
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    
    else:
      if((gt_log is True) and (list(cls._promotion_payment_controllers).__len__() != int())):
        charset = (lambda x: str(str(x)[:34] + '... }'))
        print('◽ @entity.getter:= Central._promotion_payment_controllers.__value(-1) :: %s, _countains(%s)' 
        %((charset(cls._promotion_payment_controllers.get(list(cls._promotion_payment_controllers).__getitem__(-1)))
          if ope.eq(elem_key, '') else charset(cls._promotion_payment_controllers.get(elem_key))),
          list(cls._promotion_payment_controllers).__len__()))
      
      elif((gt_log is True) and (list(cls._promotion_payment_controllers).__len__() == int())):
        print('◽ @entity.getter:= Central._promotion_payment_controllers() is Empty')
      
      else: pass
      return cls._promotion_payment_controllers.copy()


  @classmethod
  def cpf_controller_storage(cls,
    __sttr:list[tuple[str, ...]] | dict = [('',)], __ope:str='get', /,
    gt_log:bool=False, elem_key:str='') -> dict|None:
    """    
    \n<class> `DataCentralizer`   
    \n Method operators: `__ope`:
    \n* Positional-Only 'set' ⇒: `@attribute` =  `__sttr`
    \n* Positional-Only 'get' ⇒: `@attribute.__value__`
    \n* Positional Or Keyword 'gt_log' ⇒: @entity.getter.log `robot.html.log `
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      if(not isinstance(__sttr, dict)):
        cls._cpf_controller_storage.update(__sttr)
        print("◾ @entity.setter:= Central._cpf_controller_storage has been successfully updated!")
      elif(isinstance(__sttr, dict)):
        cls._cpf_controller_storage = __sttr
        print("◾ @entity.setter:= Central._cpf_controller_storage has been successfully defined!")
    
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    
    else:
      if((gt_log is True) and (list(cls._cpf_controller_storage).__len__() != int())):
        charset = (lambda x: str(str(x)[:34] + '... }'))
        print('◽ @entity.getter:= Central._cpf_controller_storage.__value(-1) :: %s, _countains(%s)' 
        %((charset(cls._cpf_controller_storage.get(list(cls._cpf_controller_storage).__getitem__(-1)))
        if ope.eq(elem_key, '') else charset(cls._cpf_controller_storage.get(elem_key))),
          list(cls._cpf_controller_storage).__len__()))
      
      elif((gt_log is True) and (list(cls._cpf_controller_storage).__len__() == int())):
        print('◽ @entity.getter:= Central._cpf_controller_storage() is Empty')
      
      else: pass
      return cls._cpf_controller_storage.copy()


  @classmethod
  def cstat_check_out(cls, __sttr:bool=True, __ope:str='get') -> bool|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    ClassError.ReferenceNullException(__sttr)
    if(ope.eq(__ope.lower(), 'set')):
      cls._cstat_check_out = __sttr if(ope.ne(__sttr, cls._cstat_check_out)) else cls._cstat_check_out
      print("◾ @setter:= Central.cls._cstat_check_out ->: %s" %cls._cstat_check_out)
    elif(__ope.lower() not in ('set', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Central._cstat_check_out.__value() :: %s' %cls._cstat_check_out)      
      return cls._cstat_check_out

  
  @classmethod
  def standard_product_code(cls, __sttr:int=int(), __ope:str='get') -> int|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      if(ope.gt(__sttr, int())):
        cls._standard_product_code = __sttr
        print("◾ @entity.setter:= Central._standard_product_code ->: %s" %cls._standard_product_code)
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Central._standard_product_code.__value() :: %s' %cls._standard_product_code)
      return cls._standard_product_code

  
  @classmethod
  def standard_customer_code(cls, __sttr:int=int(), __ope:str='get') -> int|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      if(ope.gt(__sttr, int())):
        cls._standard_customer_code = __sttr
        print("◾ @entity.setter:= Central._standard_customer_code ->: %s" %cls._standard_customer_code)
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Central._standard_customer_code.__value() :: %s' %cls._standard_customer_code)
      return cls._standard_customer_code

  
  @classmethod
  def default_customer_code(cls, __sttr:int=int(), __ope:str='get', /, gt_log:bool=False) -> int|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      if(ope.gt(__sttr, int())):
        cls._default_customer_code = __sttr
        print("◾ @entity.setter:= Central._default_customer_code ->: %s" %cls._default_customer_code)
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      if(gt_log is True):
        print('◽ @entity.getter:= Central._default_customer_code.__value() :: %s' %cls._default_customer_code)
      return cls._default_customer_code

  
  @classmethod
  def sangria_status_is_open(cls, __sttr:bool=True, __ope:str='get') -> bool|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    ClassError.ReferenceNullException(__sttr)
    if(ope.eq(__ope.lower(), 'set')):
      cls._sangria_status_is_open = (__sttr 
                                     if(ope.ne(__sttr, cls._sangria_status_is_open)) 
                                     else cls._sangria_status_is_open)
      print("◾ @setter:= Central.cls._sangria_status_is_open ->: %s" 
            %cls._sangria_status_is_open)
    elif(__ope.lower() not in ('set', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Central._sangria_status_is_open.__value() :: %s' 
            %cls._sangria_status_is_open)     
      return cls._sangria_status_is_open


  @classmethod
  def sangria_counter_controller(cls, __sttr:bool=True, __ope:str='get') -> bool|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    ClassError.ReferenceNullException(__sttr)
    if(ope.eq(__ope.lower(), 'set')):
      cls._sangria_counter_controller = (__sttr 
                                     if(ope.ne(__sttr, cls._sangria_counter_controller)) 
                                     else cls._sangria_counter_controller)
      print("◾ @setter:= Central.cls._sangria_counter_controller ->: %s" 
            %cls._sangria_counter_controller)
    elif(__ope.lower() not in ('set', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Central._sangria_counter_controller.__value() :: %s' 
            %cls._sangria_counter_controller)     
      return cls._sangria_counter_controller


  @classmethod
  def cancelling_sale_status(cls, __sttr:bool=True, __ope:str='get') -> bool|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    ClassError.ReferenceNullException(__sttr)
    if(ope.eq(__ope.lower(), 'set')):
      cls._cancelling_sale_status = (__sttr 
                                     if(ope.ne(__sttr, cls._cancelling_sale_status)) 
                                     else cls._cancelling_sale_status)
      print("◾ @setter:= Central.cls._cancelling_sale_status ->: %s" 
            %cls._cancelling_sale_status)
    elif(__ope.lower() not in ('set', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Central._cancelling_sale_status.__value() :: %s' %cls._cancelling_sale_status)
    return cls._cancelling_sale_status


  @classmethod
  def recovery_db_contents(cls, __sttr:bool=True, __ope:str='get') -> bool|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    ClassError.ReferenceNullException(__sttr)
    if(ope.eq(__ope.lower(), 'set')):
      cls._save_db_contents = (__sttr 
                                     if(ope.ne(__sttr, cls._save_db_contents)) 
                                     else cls._save_db_contents)
      print("◾ @setter:= Central.cls._save_db_contents ->: %s" 
            %cls._save_db_contents)
    elif(__ope.lower() not in ('set', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Central._save_db_contents.__value() :: %s' %cls._save_db_contents)      
    return cls._save_db_contents
pass
#\\END CLASS ::





# DATA OF PAYMENTS METHOD ::
class DataPayment(object):
  _datapayment = None

   # DATA OF PAYMENTS METHOD ::
  _payment_ways: dict = dict()
  _card_codes: dict = dict()
  _card_taxes: dict = dict()
  _current_paymnt_on_use: str = ''
  _chq_serial_number: int = 0
  _cash_card_number: int = 0

  def __init__(self) -> None:
    pass

  def __new__(cls):
    if cls._datapayment is None:
      cls._datapayment = super(DataPayment, cls).__new__(cls)
      return cls._datapayment

  @classmethod
  def payment_ways(cls,
    __sttr:list[tuple[str, ...]] | dict = [('',)], __ope:str='get', gt_log:bool=False) -> dict|None:
    """
    \n<class> `DataPayment`
    \n Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      if(not isinstance(__sttr, dict)):
        cls._payment_ways.update(__sttr)
        print("◾ @entity.setter:= Payments._payment_ways has been successfully updated!")
      elif(isinstance(__sttr, dict)):
        cls._payment_ways = __sttr
        print("◾ @entity.setter:= Payments._payment_ways has been successfully defined!")
    
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    
    else:
      if(gt_log is True):
        charset = (lambda x: str(str(x)[:34] + '... }'))
        print('◽ @entity.getter:= Central._payment_ways.__value(-1) :: %s, _countains(%s)' 
        %(charset(cls._payment_ways.get(list(cls._payment_ways).__getitem__(-1))), 
          list(cls._payment_ways).__len__()))
      return cls._payment_ways.copy()

  
  @classmethod
  def card_codes(cls,
    __sttr:list[tuple[str, ...]] | dict = [('',)], __ope:str='get', gt_log:bool=False) -> dict|None:
    """
    \n<class> `DataCentralizer`
    \n Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      if(not isinstance(__sttr, dict)):
        cls._card_codes.update(__sttr)
        print("◾ @entity.setter:= Payments._card_codes has been successfully updated!")
      elif(isinstance(__sttr, dict)):
        cls._card_codes = __sttr
        print("◾ @entity.setter:= Payments._card_codes has been successfully defined!")
    
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    
    else:
      if(gt_log is True):
        charset = (lambda x: str(str(x)[:34] + '... }'))
        print('◽ @entity.getter:= Central._card_codes.__value(-1) :: %s, _countains(%s)' 
        %(charset(cls._card_codes.get(list(cls._card_codes).__getitem__(-1))), list(cls._card_codes).__len__()))
      return cls._card_codes.copy()


  @classmethod
  def card_taxes(cls, 
    __sttr:list[tuple[str, ...]] | dict = [('',)], __ope:str='get', gt_log:bool=False) -> dict|None:
    """
    \n<class> `DataCentralizer`
    \n Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      if(not isinstance(__sttr, dict)):
        cls._card_taxes.update(__sttr)
        print("◾ @entity.setter:= Payments._card_taxes has been successfully updated!")
      elif(isinstance(__sttr, dict)):
        cls._card_taxes = __sttr
        print("◾ @entity.setter:= Payments._card_taxes has been successfully defined!")
    
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    
    else:
      if(gt_log is True):
        charset = (lambda x: str(str(x)[:34] + '... }'))
        print('◽ @entity.getter:= Central._card_taxes.__value(-1) :: %s, _countains(%s)' 
        %(charset(cls._card_taxes.get(list(cls._card_taxes).__getitem__(-1))), list(cls._card_taxes).__len__())) 
      return cls._card_taxes.copy()

  
  @classmethod
  def current_paymnt_on_use(cls, __sttr:str='Empty', __ope:str='get') -> str|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr.lower())
      cls._current_paymnt_on_use = __sttr
      print("◾ @entity.setter:= Payment._current_paymnt_on_use ->: %s" %cls._current_paymnt_on_use)
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print("◽ @entity.getter:= Payments._current_paymnt_on_use.__value() :: %s" %cls._current_paymnt_on_use) 
      return cls._current_paymnt_on_use
    

  @classmethod
  def chq_serial_number(cls, __sttr:int=int(), __ope:str='get') -> int|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      if(ope.gt(__sttr, int())):
        cls._chq_serial_number = __sttr
        print("◾ @entity.setter:= Payments._chq_serial_number ->: %s" %cls._chq_serial_number)
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Payments._chq_serial_number.__value() :: %s' %cls._chq_serial_number)
      return cls._chq_serial_number


  @classmethod
  def cash_card_number(cls, __sttr:int=int(), __ope:str='get') -> int|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    ClassError.ReferenceNullException(__sttr)
    if(ope.eq(__ope.lower(), 'set')):
      if(ope.gt(__sttr, int())):
        cls._cash_card_number = __sttr
        print("◾ @entity.setter:= Payments._cash_card_number ->: %s" %cls._cash_card_number)
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Payments._cash_card_number.__value() :: %s' %cls._cash_card_number)
      return cls._cash_card_number
pass
#\\END CLASS ::





class CashierDataPaymnt(object):
  _cashierdata = None
  #----------------------------------------+
  # CASHIER PROPERTIES                     |
  #----------------------------------------+
  _cashier_code: int = int()
  _cashier_name: str = ''
  _cashier_open_code: int = int()
  #----------------------------------------+
  # CASHIER'S CONTENT                      |
  #----------------------------------------+
  _total_on_cashier: float = 0
  _total_sales_value: float = 0  
  _all_finished_sales: float = 0 
  _totEletrnc_payments: float = 0
  _qnt_sales: int = int()
  _uncompleted_sales: int = int()
  _totUncomp_sales_value: float = 0
  _canceled_sales: int = int()
  _totCance_sales_value: float = 0
  _qnt_sangria: int = int()
  _total_removed_values: float = 0
  _cashiers_event: int = int()
  _total_cashback_payments: float = 0
  _total_chq_payments: float  = 0
  _total_customer_payments: float = 0
  _total_credit_card_payments: float = 0
  _total_ticket_payments: float = 0
  _total_pix_payments: float = 0
  _total_bank_tranference: float = 0

  def __init__(self) -> None:
    pass

  def __new__(cls):
    if cls._cashierdata is None:
      cls._cashierdata = super(CashierDataPaymnt, cls).__new__(cls)
      return cls._cashierdata
  
  @staticmethod
  def check_for_value(value:object, entt:str): return ClassError.ReferenceNullException(value, entt)

  @classmethod
  def cashier_code(cls, __sttr:int=int(), __ope:str='get') -> int|None:
    """
    \n<class> `CashierDataPayment`
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    ClassError.ReferenceNullException(__sttr)
    if(ope.eq(__ope.lower(), 'set')):
      if(ope.gt(__sttr, int())):
        cls._cashier_code = __sttr
        print("◾ @entity.setter:= Cashier._pdv_cashier_code ->: %s" %cls._cashier_code)
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Cashier._pdv_cashier_code.__value() :: %s' %cls._cashier_code)
      return cls._cashier_code


  @classmethod
  def cashier_name(cls, __sttr:str='Empty', __ope:str='get') -> str|None:
    """
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr.lower())
      cls._cashier_name = __sttr
      print("◾ @entity.setter:= Cashier._cashier_name ->: %s" %cls._cashier_name)
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print("◽ @entity.getter:= Cashier._cashier_name.__value() :: %s" %cls._cashier_name) 
      return cls._cashier_name


  @classmethod
  def cashier_open_code(cls,__sttr:int=int(), __ope:str='get') -> int|None:
    """
    \n<class> `CashierDataPayment`
    \t Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      if(ope.gt(__sttr, int())):
        cls._cashier_open_code = __sttr
        print("◾ @entity.setter:= Cashier._cashier_open_code ->: %s" %cls._cashier_open_code)
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Cashier._cashier_open_code.__value() :: %s' %cls._cashier_open_code)
      return cls._cashier_open_code


  @classmethod
  def total_on_cashier(cls, __sttr:float=0, __ope:str='get') -> float:
    """
    \n<class> `CashierDataPayment`
    \nMethod operators: `__ope`
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'add' ⇒: `@attribute` += `__sttr`
    \n* 'sub' ⇒: `@attribute` -= `__sttr`
    \n* 'get' ⇒: `@attribute.__value`
    """
    #\\... Security calling method >>
    if __ope.lower() in ('set', 'add', 'sub'):
      CashierDataPaymnt.check_for_value(__sttr, '<Cashier.total_on_cashier>')
    
    if(__ope.lower() == 'set'):
      cls._total_on_cashier = __sttr
      print("\n▶🧾 @entity.setter:= Cashier.cls._total_on_cashier ->: %s" %cls._total_on_cashier)
    
    elif(__ope.lower() == 'add'): 
      cls._total_on_cashier += __sttr
      print("\n🧾🔼 @entity.setter.add:= Cashier.cls._total_on_cashier ->: %s" %cls._total_on_cashier)
    
    elif(__ope.lower() == 'sub'): 
      cls._total_on_cashier -= __sttr if((cls._total_on_cashier - __sttr) > float(0)) else cls._total_on_cashier
      print("\n🧾🔽 @entity.setter.sub:= Cashier.cls._total_on_cashier ->: %s" %cls._total_on_cashier)
    
    elif(__ope.lower() == 'get'):
      print("\n◀🧾 @entity.getter:= Cashier.cls._total_on_cashier ->: %s" %cls._total_on_cashier)
      return cls._total_on_cashier #\\... Escape from ::
    
    elif(__ope.lower() not in ('set', 'add', 'sub', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    return


  @classmethod
  def total_sales_value(cls, __sttr:float=0, __ope:str='get') -> float:
    """
    \n<class> `CashierDataPayment`
    \nMethod operators: `__ope`
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'add' ⇒: `@attribute` += `__sttr`
    \n* 'sub' ⇒: `@attribute` -= `__sttr`
    \n* 'get' ⇒: `@attribute.__value`
    """
    #\\... Security calling method >>
    if __ope.lower() in ('set', 'add', 'sub'):
      CashierDataPaymnt.check_for_value(__sttr, '<Cashier.total_sales_value>')
    
    if(__ope.lower() == 'set'):
      cls._total_sales_value = __sttr
      print("\n▶🧾 @entity.setter:= Cashier.cls._total_sales_value ->: %s" %cls._total_sales_value)
    
    elif(__ope.lower() == 'add'): 
      cls._total_sales_value += __sttr
      print("\n🧾🔼 @entity.setter.add:= Cashier.cls._total_sales_value ->: %s" %cls._total_sales_value)
    
    elif(__ope.lower() == 'sub'): 
      cls._total_sales_value -= __sttr if((cls._total_sales_value - __sttr) > float(0)) else cls._total_sales_value
      print("\n🧾🔽 @entity.setter.sub:= Cashier.cls._total_sales_value ->: %s" %cls._total_sales_value)
    
    elif(__ope.lower() == 'get'):
      print("\n◀🧾 @entity.getter:= Cashier.cls._total_sales_value ->: %s" %cls._total_sales_value)
      return cls._total_sales_value #\\... escape ::
    
    elif(__ope.lower() not in ('set', 'add', 'sub', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    return
  
  
  @classmethod
  def all_finished_sales(cls, __sttr:float=0, __ope:str='get') -> float:
    """
    \n<class> `CashierDataPayment`
    \nMethod operators: `__ope`
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'add' ⇒: `@attribute` += `__sttr`
    \n* 'sub' ⇒: `@attribute` -= `__sttr`
    \n* 'get' ⇒: `@attribute.__value`
    """
    #\\... Security calling method >>
    if __ope.lower() in ('set', 'add', 'sub'):
      CashierDataPaymnt.check_for_value(__sttr, '<Cashier.all_finished_sales>')
    
    if(__ope.lower() == 'set'):
      cls._all_finished_sales = __sttr
      print("\n▶🧾 @entitty.setter:= Cashier.cls._all_finished_sales ->: %s" %cls._all_finished_sales)
    
    elif(__ope.lower() == 'add'): 
      cls._all_finished_sales += __sttr
      print("\n🔼🧾 @entitty.setter.add:= Cashier.cls._all_finished_sales ->: %s" %cls._all_finished_sales)
    
    elif(__ope.lower() == 'sub'): 
      cls._all_finished_sales -= (__sttr 
                                  if((cls._all_finished_sales - __sttr) > float(0)) 
                                  else cls._all_finished_sales)
      print("\n🔽🧾 @entitty.setter.sub:= Cashier.cls._all_finished_sales ->: %s" %cls._all_finished_sales)
    
    elif(__ope.lower() == 'get'):
      print("\n◀🧾 @entity.getter:= Cashier.cls._all_finished_sales ->: %s" %cls._all_finished_sales)
      return cls._all_finished_sales #\\... Escape from ::
    
    elif(__ope.lower() not in ('set', 'add', 'sub', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    return

  
  @classmethod
  def total_eletronic_payments(cls, __sttr:float=0, __ope:str='get') -> float:
    """
    \n<class> `CashierDataPayment`
    \nMethod operators: `__ope`
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'add' ⇒: `@attribute` += `__sttr`
    \n* 'sub' ⇒: `@attribute` -= `__sttr`
    \n* 'get' ⇒: `@attribute.__value`
    """
    #\\... Security calling method >>
    if __ope.lower() in ('set', 'add', 'sub'):
      CashierDataPaymnt.check_for_value(__sttr, '<Cashier.total_eletronic_payments>')
    
    if(__ope.lower() == 'set'):
      cls._totEletrnc_payments = __sttr
      print("\n▶🧾 @entity.setter:= Cashier.cls._total_eletronic_payments ->: %s" %cls._totEletrnc_payments)
    
    elif(__ope.lower() == 'add'): 
      cls._totEletrnc_payments += __sttr
      print("\n🔼🧾 @entitty.setter.add:= Cashier.cls._total_eletronic_payments ->: %s" %cls._totEletrnc_payments)
    
    elif(__ope.lower() == 'sub'): 
      cls._totEletrnc_payments -= (__sttr 
                                   if((cls._totEletrnc_payments - __sttr) > float(0)) 
                                   else cls._totEletrnc_payments)
      print("\n🔽🧾 @entitty.setter.sub:= Cashier.cls._total_eletronic_payments ->: %s" %cls._totEletrnc_payments)
    
    elif(__ope.lower() == 'get'):
      print("\n◀🧾 @entity.getter:= Cashier.cls._total_eletronic_payments ->: %s" %cls._totEletrnc_payments)
      return cls._totEletrnc_payments #\\... Escape from ::
    
    elif(__ope.lower() not in ('set', 'add', 'sub', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    return
  
  
  @classmethod
  def qnt_sales(cls, __sttr:int=0, __ope:str='get') -> int:
    """
    \n<class> `CashierDataPayment`
    \nMethod operators: `__ope`
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'add' ⇒: `@attribute` += `__sttr`
    \n* 'sub' ⇒: `@attribute` -= `__sttr`
    \n* 'get' ⇒: `@attribute.__value`
    """
    #\\... Security calling method >>
    if __ope.lower() in ('set', 'add', 'sub'):
      CashierDataPaymnt.check_for_value(__sttr, '<Cashier.qnt_sales>')
    
    if(__ope.lower() == 'set'):
      cls._qnt_sales = __sttr
      print("\n▶🧾 @entity.setter:= Cashier.cls._qnt_sales ->: %s" %cls._qnt_sales)
    
    elif(__ope.lower() == 'add'):
      cls._qnt_sales += __sttr
      print("\n🔼🧾 @entity.setter.add:= Cashier.cls._qnt_sales ->: %s" %cls._qnt_sales)
    
    elif(__ope.lower() == 'sub'): 
      cls._qnt_sales -= __sttr if((cls._qnt_sales - __sttr) > int(0)) else cls._qnt_sales
      print("\n🔽🧾 @entity.setter.sub:= Cashier.cls._qnt_sales ->: %s" %cls._qnt_sales)
    
    elif(__ope.lower() == 'get'):
      print("\n🧾 @entity.getter:= Cashier.cls._qnt_sales ->: %s" %cls._qnt_sales)
      return cls._qnt_sales #\\... Escape from ::
    
    elif(__ope.lower() not in ('set', 'add', 'sub', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    return
  
  
  @classmethod
  def uncompleted_sales(cls, __sttr:int=0, __ope:str='get') -> int:
    """
    \n<class> `CashierDataPayment`
    \tMethod operators: `__ope`
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'add' ⇒: `@attribute` += `__sttr`
    \n* 'sub' ⇒: `@attribute` -= `__sttr`
    \n* 'get' ⇒: `@attribute.__value`
    """
    #\\... Security calling method >>
    if __ope.lower() in ('set', 'add', 'sub'):
      CashierDataPaymnt.check_for_value(__sttr, '<Cashier.uncompleted_sales>')

    if(__ope.lower() == 'set'):
      cls._uncompleted_sales = __sttr
      print("\n▶🧾 @entity.setter:= Cashier.cls._uncompleted_sales ->: %s" %cls._uncompleted_sales)
    
    elif(__ope.lower() == 'add'): 
      cls._uncompleted_sales += __sttr
      print("\n🔼🧾 @entity.setter.add:= Cashier.cls._uncompleted_sales ->: %s" %cls._uncompleted_sales)
    
    elif(__ope.lower() == 'sub'): 
      cls._uncompleted_sales -= __sttr if((cls._uncompleted_sales - __sttr) > int(0)) else cls._uncompleted_sales
      print("\n🔽🧾 @entity.setter.sub:= Cashier.cls._uncompleted_sales ->: %s" %cls._uncompleted_sales)
    
    elif(__ope.lower() == 'get'):
      print("\n◀🧾 @entity.getter:= Cashier.cls._uncompleted_sales ->: %s" %cls._uncompleted_sales)
      return cls._uncompleted_sales #\\... Escape from ::
    
    elif(__ope.lower() not in ('set', 'add', 'sub', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    return

  
  @classmethod
  def total_uncompleted_sales_value(cls, __sttr:float=0, __ope:str='get') -> int:
    """
    \n<class> `CashierDataPayment`
    \tMethod operators: `__ope`
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'add' ⇒: `@attribute` += `__sttr`
    \n* 'sub' ⇒: `@attribute` -= `__sttr`
    \n* 'get' ⇒: `@attribute.__value`
    """
    #\\... Security calling method >>
    if __ope.lower() in ('set', 'add', 'sub'):
      CashierDataPaymnt.check_for_value(__sttr, '<Cashier.totUncomp_sales_value>')
    
    if(__ope.lower() == 'set'):
      cls._totUncomp_sales_value = __sttr
      print("\n▶🧾 @entity.setter:= Cashier.cls._total_uncomp_sal... ->: %s" %cls._totUncomp_sales_value)
    
    elif(__ope.lower() == 'add'): 
      cls._totUncomp_sales_value += __sttr
      print("\n🔼🧾 @entity.setter.add:= Cashier.cls._total_uncomp_sal... ->: %s" %cls._totUncomp_sales_value)

    elif(__ope.lower() == 'sub'): 
      cls._totUncomp_sales_value -= (
        __sttr if((cls._totUncomp_sales_value - __sttr) > int(0)) else cls._totUncomp_sales_value)
      print("\n🔽🧾 @entity.setter.sub:= Cashier.cls._total_uncomp_sal... ->: %s" %cls._totUncomp_sales_value)
    
    elif(__ope.lower() == 'get'):
      print("\n◀🧾 @entity.getter:= Cashier.cls._total_uncomp_sal... ->: %s" %cls._totUncomp_sales_value)
      return cls._totUncomp_sales_value #\\... Escape from ::
    
    elif(__ope.lower() not in ('set', 'add', 'sub', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    return

  
  @classmethod
  def canceled_sales(cls, __sttr:int=0, __ope:str='get') -> int:
    """
    \n<class> CashierDataPayment
    \nMethod operators: `__ope`
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'add' ⇒: `@attribute` += `__sttr`
    \n* 'sub' ⇒: `@attribute` -= `__sttr`
    \n* 'get' ⇒: `@attribute.__value`
    """
    #\\... Security calling method >>
    if __ope.lower() in ('set', 'add', 'sub'):
      CashierDataPaymnt.check_for_value(__sttr, '<Cashier.canceled_sales>')

    if(__ope.lower() == 'set'):
      print("\n▶🧾 @entity.setter:= Cashier.cls._canceled_sales ->: %s" %cls._canceled_sales)
      cls._canceled_sales = __sttr
    
    elif(__ope.lower() == 'add'): 
      cls._canceled_sales += __sttr
      print("\n🔼🧾 @entity.setter.add:= Cashier.cls._canceled_sales ->: %s" %cls._canceled_sales)
    elif(__ope.lower() == 'sub'): 
      cls._canceled_sales -= __sttr if((cls._canceled_sales - __sttr) > int(0)) else cls._canceled_sales
      print("\n🔽🧾 @entity.setter.sub:= Cashier.cls._canceled_sales ->: %s" %cls._canceled_sales)
    
    elif(__ope.lower() == 'get'):
      print("\n❗🛒 @entity.getter:= Cashier.cls._canceled_sales ->: %s" %cls._canceled_sales)
      return cls._canceled_sales #\\... Escape from ::
    
    elif(__ope.lower() not in ('set', 'add', 'sub', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    return
  
  
  @classmethod
  def total_canceled_sales_value(cls, __sttr:float=0, __ope:str='get') -> int:
    """
    \n<calss> `CashierDataPayment`
    \tMethod operators: `__ope`
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'add' ⇒: `@attribute` += `__sttr`
    \n* 'sub' ⇒: `@attribute` -= `__sttr`
    \n* 'get' ⇒: `@attribute.__value`
    """
    #\\... Security calling method >>
    if __ope.lower() in ('set', 'add', 'sub'):
      CashierDataPaymnt.check_for_value(__sttr, '<Cashier.total_canceled_sales_value>')

    if(__ope.lower() == 'set'):
      cls._totCance_sales_value = __sttr
      print("\n▶🧾 @entity.setter:= Cashier.cls._totCance_sales_value ->: %s" %cls._totCance_sales_value)
    
    elif(__ope.lower() == 'add'): 
      cls._totCance_sales_value += __sttr
      print("\n🔼🧾 @entity.setter.add:= Cashier.cls._totCance_sales_value ->: %s" %cls._totCance_sales_value)
    
    elif(__ope.lower() == 'sub'): 
      cls._totCance_sales_value -= (__sttr
                                    if((cls._totCance_sales_value - __sttr) > int(0)) 
                                    else cls._totCance_sales_value)
      print("\n🔽🧾 @entity.setter.sub:= Cashier.cls._totCance_sales_value ->: %s" %cls._totCance_sales_value)
    
    elif(__ope.lower() == 'get'):
      print("\n◀🧾 @entity.getter:= Cashier.cls._totCance_sales_value ->: %s" %cls._totCance_sales_value)
      return cls._totCance_sales_value #\\... Escape from ::
    
    elif(__ope.lower() not in ('set', 'add', 'sub', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    return
  
  
  @classmethod
  def qnt_sangria(cls, __sttr:int=0, __ope:str='get') -> int:
    """
    \n<class> `CashierDataPayment`
    \tMethod operators: `__ope`
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'add' ⇒: `@attribute` += `__sttr`
    \n* 'sub' ⇒: `@attribute` -= `__sttr`
    \n* 'get' ⇒: `@attribute.__value`
    """
    #\\... Security calling method >>
    if __ope.lower() in ('set', 'add', 'sub'):
      CashierDataPaymnt.check_for_value(__sttr, '<Cashier.qnt_sangria>')

    if(__ope.lower() == 'set'):
      cls._qnt_sangria = __sttr
      print("\n▶🧾 @entity.setter:= Cashier.cls._qnt_sangria ->: %s" %cls._qnt_sangria)

    elif(__ope.lower() == 'add'): 
      cls._qnt_sangria += __sttr
      print("\n🔼🧾 @entity.setter.add:= Cashier.cls._qnt_sangria ->: %s" %cls._qnt_sangria)

    elif(__ope.lower() == 'sub'): 
      cls._qnt_sangria -= __sttr if((cls._qnt_sangria - __sttr) > int(0)) else cls._qnt_sangria
      print("\n🔽🧾 @entity.setter.sub:= Cashier.cls._qnt_sangria ->: %s" %cls._qnt_sangria)

    elif(__ope.lower() == 'get'):
      print("\n🧾 @entity.getter:= Cashier.cls._qnt_sangria ->: %s" %cls._qnt_sangria)
      return cls._qnt_sangria #\\... Escape from ::
    
    elif(__ope.lower() not in ('set', 'add', 'sub', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    return

  
  @classmethod
  def total_removed_values(cls, __sttr:float=0, __ope:str='get') -> int:
    """
    \n<class> `CashierDataPayment`
    \tMethod operators: `__ope`
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'add' ⇒: `@attribute` += `__sttr`
    \n* 'sub' ⇒: `@attribute` -= `__sttr`
    \n* 'get' ⇒: `@attribute.__value`
    """
    #\\... Security calling method >>
    if __ope.lower() in ('set', 'add', 'sub'):
      CashierDataPaymnt.check_for_value(__sttr, '<Cashier.total_removed_values>')

    if(__ope.lower() == 'set'):
      cls._total_removed_values = __sttr
      print("\n▶🧾 @entity.setter:= Cashier.cls._removed_values ->: %s" %cls._total_removed_values)

    elif(__ope.lower() == 'add'):
      cls._total_removed_values += __sttr
      print("\n🔼🧾 @entity.setter.add:= Cashier.cls._removed_values ->: %s" %cls._total_removed_values)

    elif(__ope.lower() == 'sub'): 
      cls._total_removed_values -= ( 
        __sttr if((cls._total_removed_values - __sttr) > int(0)) else cls._total_removed_values)
      print("\n🔽🧾 @entity.setter.sub:= Cashier.cls._removed_values ->: %s" %cls._total_removed_values)

    elif(__ope.lower() == 'get'):
      print("\n◀🧾 @entity.getter:= Cashier.cls._removed_values ->: %s" %cls._total_removed_values)
      return cls._total_removed_values #\\... Escape from ::
    
    elif(__ope.lower() not in ('set', 'add', 'sub', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    return

  
  @classmethod
  def cashiers_event(cls, __sttr:int=0, __ope:str='get') -> int:
    """
    \n<class> `CashierDataPayment`
    \tMethod operators: `__ope`
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'add' ⇒: `@attribute` += `__sttr`
    \n* 'sub' ⇒: `@attribute` -= `__sttr`
    \n* 'get' ⇒: `@attribute.__value`
    """
    #\\... Security calling method >>
    if __ope.lower() in ('set', 'add', 'sub'):
      CashierDataPaymnt.check_for_value(__sttr, '<Cashier.cashiers_event>')
    
    if(__ope.lower() == 'set'):
      cls._cashiers_event = __sttr
      print("\n▶🧾 @entity.setter:= Cashier.cls._cashiers_event ->: %s" %cls._cashiers_event)

    elif(__ope.lower() == 'add'): 
      cls._cashiers_event += __sttr
      print("\n🔼🧾 @entity.setter.add:= Cashier.cls._cashiers_event ->: %s" %cls._cashiers_event)

    elif(__ope.lower() == 'sub'):
      cls._cashiers_event -= __sttr if((cls._cashiers_event - __sttr) > int(0)) else cls._cashiers_event
      print("\n🔽🧾 @entity.setter.sub:= Cashier.cls._cashiers_event ->: %s" %cls._cashiers_event)

    elif(__ope.lower() == 'get'):
      print("\n◀🧾 @entity.getter:= Cashier.cls._cashiers_event ->: %s" %cls._cashiers_event)
      return cls._cashiers_event #\\... Escape from ::
    
    elif(__ope.lower() not in ('set', 'add', 'sub', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    return
  
  
  #--------------------------------------------------------------------------------------------------------------
  # CASHIER BREAKDOWN ::
  #--------------------------------------------------------------------------------------------------------------
  
  @classmethod
  def total_cashback_payments(cls, __sttr:float=0, __ope:str='get') -> int:
    """
    \n<class> `CashierDataPayment`
    \tMethod operators: `__ope`
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'add' ⇒: `@attribute` += `__sttr`
    \n* 'sub' ⇒: `@attribute` -= `__sttr`
    \n* 'get' ⇒: `@attribute.__value`
    """
    #\\... Security calling method >>
    if __ope.lower() in ('set', 'add', 'sub'):
      CashierDataPaymnt.check_for_value(__sttr, '<Cashier.total_cashback_payments>')

    if(__ope.lower() == 'set'):
      cls._total_cashback_payments = __sttr
      print("\n▶🧾 @entity.setter:= Cashier.cls._total_cashback_payments ->: %s" %cls._total_cashback_payments)

    elif(__ope.lower() == 'add'): 
      cls._total_cashback_payments += __sttr
      print("\n🔼🧾 @entity.setter.add:= Cashier.cls._total_cashback_payments ->: %s" %cls._total_cashback_payments)

    elif(__ope.lower() == 'sub'): 
      cls._total_cashback_payments -= (
        __sttr if((cls._total_cashback_payments - __sttr) > int(0)) else cls._total_cashback_payments)
      print("\n🔽🧾 @entity.setter.sub:= Cashier.cls._total_cashback_payments ->: %s" %cls._total_cashback_payments)

    elif(__ope.lower() == 'get'):
      print("\n🧾 @entity.getter:= Cashier.cls._total_cashback_payments ->: %s" %cls._total_cashback_payments)
      return cls._total_cashback_payments #\\... Escape from ::
    
    elif(__ope.lower() not in ('set', 'add', 'sub', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    return
  
  @classmethod
  def total_chq_payments(cls, __sttr:float=0, __ope:str='get') -> int:
    """
    \n<class> `CashierDataPayment`
    \tMethod operators: `__ope`
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'add' ⇒: `@attribute` += `__sttr`
    \n* 'sub' ⇒: `@attribute` -= `__sttr`
    \n* 'get' ⇒: `@attribute.__value`
    """
    #\\... Security calling method >>
    if __ope.lower() in ('set', 'add', 'sub'):
      CashierDataPaymnt.check_for_value(__sttr, '<Cashier.total_chq_payments>')

    if(__ope.lower() == 'set'):
      cls._total_chq_payments = __sttr
      print("\n▶🧾 @entity.setter:= Cashier.cls._total_chq_payments ->: %s" %cls._total_chq_payments)
    
    elif(__ope.lower() == 'add'): 
      cls._total_chq_payments += __sttr
      print("\n🔼🧾 @entity.setter.add:= Cashier.cls._total_chq_payments ->: %s" %cls._total_chq_payments)
    
    elif(__ope.lower() == 'sub'): 
      cls._total_chq_payments -= (
        __sttr if((cls._total_chq_payments - __sttr) > int(0)) else cls._total_chq_payments)
      print("\n🔽🧾 @entity.setter.sub:= Cashier.cls._total_chq_payments ->: %s" %cls._total_chq_payments)
    
    elif(__ope.lower() == 'get'):
      print("\n◀🧾 @entity.getter:= Cashier.cls._total_chq_payments ->: %s" %cls._total_chq_payments)
      return cls._total_chq_payments #\\... Escape from ::
    
    elif(__ope.lower() not in ('set', 'add', 'sub', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    return
  
  
  @classmethod
  def total_customer_payments(cls, __sttr:float=0, __ope:str='get') -> int:
    """
    \n<class> `CashierDataPayment`
    \tMethod operators: `__ope`
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'add' ⇒: `@attribute` += `__sttr`
    \n* 'sub' ⇒: `@attribute` -= `__sttr`
    \n* 'get' ⇒: `@attribute.__value`
    """
    #\\... Security calling method >>
    if __ope.lower() in ('set', 'add', 'sub'):
      CashierDataPaymnt.check_for_value(__sttr, '<Cashier.total_customer_payments>')
    
    if(__ope.lower() == 'set'):
      cls._total_customer_payments = __sttr
      print("\n▶🧾 @entity.setter:= Cashier.cls._total_customer_payments ->: %s" %cls._total_customer_payments)

    elif(__ope.lower() == 'add'): 
      cls._total_customer_payments += __sttr
      print("\n🔼🧾 @entity.setter.add:= Cashier.cls._total_customer_payments ->: %s" %cls._total_customer_payments)

    elif(__ope.lower() == 'sub'): 
      cls._total_customer_payments -= (
        __sttr if((cls._total_customer_payments - __sttr) > int(0)) else cls._total_customer_payments)
      print("\n🔽🧾 @entity.setter.sub:= Cashier.cls._total_customer_payments ->: %s" %cls._total_customer_payments)
      
    elif(__ope.lower() == 'get'):
      print("\n◀🧾 @entity.getter:= Cashier.cls._total_customer_payments ->: %s" %cls._total_customer_payments)
      return cls._total_customer_payments #\\... Escape from ::
    
    elif(__ope.lower() not in ('set', 'add', 'sub', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    return

 
  @classmethod
  def total_ticket_payments(cls, __sttr:float=0, __ope:str='get') -> int:
    """
    \n<class> `CashierDataPayment`
    \tMethod operators: `__ope`
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'add' ⇒: `@attribute` += `__sttr`
    \n* 'sub' ⇒: `@attribute` -= `__sttr`
    \n* 'get' ⇒: `@attribute.__value`
    """
    #\\... Security calling method >>
    if __ope.lower() in ('set', 'add', 'sub'):
      CashierDataPaymnt.check_for_value(__sttr, '<Cashier.total_ticket_payments>')

    if(__ope.lower() == 'set'):
      cls._total_ticket_payments = __sttr
      print("\n▶🧾 @entity.setter:= Cashier.cls._total_ticket_payments ->: %s" %cls._total_ticket_payments)

    elif(__ope.lower() == 'add'): 
      cls._total_ticket_payments += __sttr
      print("\n🔼🧾 @entity.setter.add:= Cashier.cls._total_ticket_payments ->: %s" %cls._total_ticket_payments)

    elif(__ope.lower() == 'sub'): 
      cls._total_ticket_payments -= (
        __sttr if((cls._total_ticket_payments - __sttr) > int(0)) else cls._total_ticket_payments)
      print("\n🔽🧾 @entity.setter.sub:= Cashier.cls._total_ticket_payments ->: %s" %cls._total_ticket_payments)
      
    elif(__ope.lower() == 'get'):
      print("\n\◀🧾 @entity.getter:= Cashier.cls._total_ticket_payments ->: %s" %cls._total_ticket_payments)
      return cls._total_ticket_payments #\\... escape ::
    
    elif(__ope.lower() not in ('set', 'add', 'sub', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    return
  
  
  @classmethod
  def total_credit_card_payments(cls, __sttr:float=0, __ope:str='get') -> int:
    """
    \n<class> `CashierDataPayment`
    \tMethod operators: `__ope`
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'add' ⇒: `@attribute` += `__sttr`
    \n* 'sub' ⇒: `@attribute` -= `__sttr`
    \n* 'get' ⇒: `@attribute.__value`
    """
    #\\... Security calling method >>
    if __ope.lower() in ('set', 'add', 'sub'):
      CashierDataPaymnt.check_for_value(__sttr, '<Cashier.total_credit_card_payments>')

    if(__ope.lower() == 'set'):
      cls._total_credit_card_payments = __sttr
      print("\n▶🧾 @entity.setter:= Cashier.cls._total_credit_card_payments ->: %s" %cls._total_credit_card_payments)

    elif(__ope.lower() == 'add'): 
      cls._total_credit_card_payments += __sttr
      print("\n🔼🧾 @entity.setter.add:= Cashier.cls._total_credit_card_payments ->: %s" %cls._total_credit_card_payments)

    elif(__ope.lower() == 'sub'): 
      cls._total_credit_card_payments -= (
        __sttr if((cls._total_credit_card_payments - __sttr) > int(0)) else cls._total_credit_card_payments)
      print("\n🔽🧾 @entity.setter.sub:= Cashier.cls._total_credit_card_payments ->: %s" %cls._total_credit_card_payments)
      
    elif(__ope.lower() == 'get'):
      print("\n◀🧾 @entity.getter:= Cashier.cls._total_credit_card_payments ->: %s" %cls._total_credit_card_payments)
      return cls._total_credit_card_payments #\\... Escape from ::
    
    elif(__ope.lower() not in ('set', 'add', 'sub', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    return
  
  
  @classmethod
  def total_pix_payments(cls, __sttr:float=0, __ope:str='get') -> int:
    """
    \n<class> `CashierDataPayment`
    \tMethod operators: `__ope`
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'add' ⇒: `@attribute` += `__sttr`
    \n* 'sub' ⇒: `@attribute` -= `__sttr`
    \n* 'get' ⇒: `@attribute.__value`
    """
    #\\... Security calling method >>
    if __ope.lower() in ('set', 'add', 'sub'):
      CashierDataPaymnt.check_for_value(__sttr, '<Cashier.total_pix_payments>')

    if(__ope.lower() == 'set'):
      cls._total_pix_payments = __sttr
      print("\n▶🧾 @entity.setter:= Cashier.cls._total_pix_payments ->: %s" %cls._total_pix_payments)

    elif(__ope.lower() == 'add'): 
      cls._total_pix_payments += __sttr
      print("\n🔼🧾 @entity.setter.add:= Cashier.cls._total_pix_payments ->: %s" %cls._total_pix_payments)

    elif(__ope.lower() == 'sub'): 
      cls._total_pix_payments -= (
        __sttr if((cls._total_pix_payments - __sttr) > int(0)) else cls._total_pix_payments)
      print("\n🔽🧾 @entity.setter.sub:= Cashier.cls._total_pix_payments ->: %s" %cls._total_pix_payments)
      
    elif(__ope.lower() == 'get'):
      print("\n◀🧾 @entity.getter:= Cashier.cls._total_pix_payments ->: %s" %cls._total_pix_payments)
      return cls._total_pix_payments #\\... Escape from ::
    
    elif(__ope.lower() not in ('set', 'add', 'sub', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    return
  
  
  @classmethod
  def total_bank_tranference(cls, __sttr:float=0, __ope:str='get') -> int:
    """
    \n<class> `CashierDataPayment`
    \tMethod operators: `__ope`
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'add' ⇒: `@attribute` += `__sttr`
    \n* 'sub' ⇒: `@attribute` -= `__sttr`
    \n* 'get' ⇒: `@attribute.__value`
    """
    #\\... Security calling method >>
    if __ope.lower() in ('set', 'add', 'sub'):
      CashierDataPaymnt.check_for_value(__sttr, '<Cashier.total_bank_tranference>')

    if(__ope.lower() == 'set'):
      cls._total_bank_tranference = __sttr
      print("\n🔼🧾 @entity.getter.add:= Cashier.cls._total_bank_tranference ->: %s" %cls._total_bank_tranference)
    
    elif(__ope.lower() == 'add'): 
      cls._total_bank_tranference += __sttr
      print("\n🔽🧾 @entity.getter.sub:= Cashier.cls._total_bank_tranference ->: %s" %cls._total_bank_tranference)
    
    elif(__ope.lower() == 'sub'):
      cls._total_bank_tranference -= (
        __sttr if((cls._total_bank_tranference - __sttr) > int(0)) else cls._total_bank_tranference)
      print("\n🔽🧾 @entity.getter.sub:= Cashier.cls._total_bank_tranference ->: %s" %cls._total_bank_tranference)
    
    elif(__ope.lower() == 'get'):
      print("\n◀🧾 @entity.getter:= Cashier.cls._total_bank_tranference ->: %s" %cls._total_bank_tranference)
      return cls._total_bank_tranference #\\... Escape from ::
  
    elif(__ope.lower() not in ('set', 'add', 'sub', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    return
  
#\\END CLASS ::
pass


class LocalStorage(object):
  """
  `LocalStorage` for conference and comparison of data moved during the execution of automated
  test cases. these properties can only be accessed for its  integrated accessor provided for 
  the decorator  python. that is a security  feature that ensures better methods for handling 
  these class properties.
  """
  _localStorage = None
  _restore_sale_properties = dict()
  _database_cashback: float = 0
  _db_cashier_code: int = 0
  _last_sale_code: list = list()
  _last_sale_value: list = list()
  _last_sale_difference: list = list()
  _last_sale_status: list = list()
  _last_fiscal_document: list = list()
  _last_customer_ident: list = list()
  _last_customer_code: list = list()
  _master_status: bool = True
  _cashier_conference: dict = dict()
  _cashier_adjustment: list = list()
  _products_dictionary = dict()          

  def __init__(cls) -> None:
    pass

  def __new__(cls):
    if cls._localStorage is None:
      cls._localStorage = super(LocalStorage, cls).__new__(cls)

  @classmethod
  def gett(cls, name) -> Any: return DataCentralizer.__getattribute__(cls, name)


  @classmethod
  def sett(cls, name, value): DataCentralizer.__setattr__(cls, name, value); return None


  @classmethod
  def restore_sale_properties(cls,  
    __sttr:list[tuple[str, ...]] | dict = [('',)], __ope:str='get') -> dict|None:
    """    
    \n<class> `LocalStorage.py`   
    \n Method operators: `__ope`:
    \n* Positional-Only 'set' ⇒: `@attribute` =  `__sttr`
    \n* Positional-Only 'clear' ⇒: @ttribute.clear()
    \n* Positional-Only 'get' ⇒: `@attribute.__value__`
    \n* Positional Or Keyword 'gt_log' ⇒: @entity.getter.log `robot.html.log `
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      if(not isinstance(__sttr, dict)):
        cls._restore_sale_properties.update(__sttr)
        print("◾ @entity.setter:= Storage._restore_sale_properties has been successfully updated!")
      elif(isinstance(__sttr, dict)):
        cls._restore_sale_properties = __sttr
        print("◾ @entity.setter:= Storage._restore_sale_properties has been successfully defined!")

    elif(ope.eq(__ope.lower(), 'clear')):
      cls._restore_sale_properties.clear()
      print("◾ @entity.setter:= Storage._restore_sale_properties has been successfully cleared!")

    elif(__ope.lower() not in ('set', 'get', 'clear')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope), '<def> restore_sale_properties'))

    else:
      print('◽ @entity.getter:= Storage._restore_sale_properties.__value() :: _count(%s)' 
            %(list(cls._cashier_conference.keys()).__len__()))
      return cls._restore_sale_properties


  @classmethod
  def database_cashback(cls, __sttr:float=0.0, __ope:str='get') -> float|None:
    """ 
    \n`<class>` `LocalStorage.py`   
    \n Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if(ope.eq(__ope.lower(), 'set')):
      ClassError.ReferenceNullException(__sttr)
      cls._database_cashback = __sttr
      print("◾ @entity.setter:= Storage.cls._final_sale_value ->: %s" %cls._database_cashback)
    elif(__ope.lower() not in ('set', 'get')):
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Storage.cls._database_cashback.__value() :: %s' %cls._database_cashback)
      return cls._database_cashback


  @classmethod
  def db_cashier_code(cls, __sttr:int=int(), __ope:str='get') -> int|None:
    """ 
    \n`<class>` `LocalStorage.py`   
    \n Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if((__ope.lower() == 'set')): 
      ClassError.ReferenceNullException(__sttr)
      cls._db_cashier_code = __sttr
    elif(__ope.lower() not in ('set', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Storage._db_cashier_code.__value() :: %s' %cls._db_cashier_code)
      return cls._db_cashier_code    


  @classmethod
  def last_sale_code(cls, __sttr:int=int(), __ope:str='get') -> list|None:
    """ 
    \n`<class>` `LocalStorage.py`   
    \n Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if((__ope.lower() == 'set')): 
      ClassError.ReferenceNullException(__sttr)
      cls._last_sale_code.append(__sttr)
    elif(__ope.lower() not in ('set', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Storage._last_sale_code.__value() :: _count(%s)' 
            %(len(cls._last_sale_code))) 
      return cls._last_sale_code


  @classmethod
  def last_sale_value(cls, __sttr:float=0.0, __ope:str='get') -> list|None:
    """ 
    \n`<class>` `LocalStorage.py`   
    \n Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    ClassError.ReferenceNullException(__sttr)
    if((__ope.lower() == 'set')): 
      cls._last_sale_value.append(__sttr)
    elif(__ope.lower() not in ('set', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Storage._last_sale_value.__value() :: _count(%s)' 
            %(len(cls._last_sale_value)))
      return cls._last_sale_value


  @classmethod
  def last_sale_difference(cls, __sttr:float=0.0, __ope:str='get') -> list|None:
    """ 
    \n`<class>` `LocalStorage.py`   
    \n Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    ClassError.ReferenceNullException(__sttr)
    if((__ope.lower() == 'set')): 
      cls._last_sale_difference.append(__sttr)
    elif(__ope.lower() not in ('set', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Storage._last_sale_difference.__value() :: _count(%s)' 
            %(len(cls._last_sale_difference)))
      return cls._last_sale_difference


  @classmethod
  def last_sale_status(cls, __sttr:str='Empty', __ope:str='get') -> list|None:
    """ 
    \n`<class>` `LocalStorage.py`   
    \n Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if((__ope.lower() == 'set')): 
      ClassError.ReferenceNullException(__sttr.lower())
      cls._last_sale_status.append(__sttr)
    elif(__ope.lower() not in ('set', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Storage._last_sale_status.__value() :: _count(%s)' 
            %(len(cls._last_sale_status)))
      return cls._last_sale_status


  @classmethod
  def last_fiscal_document(cls, __sttr:int=int(), __ope:str='get') -> list|None:
    """ 
    \n`<class>` `LocalStorage.py`   
    \n Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if((__ope.lower() == 'set')): 
      ClassError.ReferenceNullException(__sttr)
      cls._last_fiscal_document.append(__sttr)
    elif(__ope.lower() not in ('set', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Storage._last_fiscal_document.__value() :: _count(%s)' 
            %(len(cls._last_fiscal_document)))
      return cls._last_fiscal_document
  

  @classmethod
  def last_customer_ident(cls, __sttr:str='Empty', __ope:str='get') -> list|None:
    """ 
    \n`<class>` `LocalStorage.py`   
    \n Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if((__ope.lower() == 'set')): 
      ClassError.ReferenceNullException(__sttr.lower() if __sttr is not None else 'Not Informed')
      cls._last_customer_ident.append(__sttr)
    elif(__ope.lower() not in ('set', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Storage._last_customer_ident.__value() :: _count(%s)' 
      %cls._last_customer_ident.__len__())
      return cls._last_customer_ident


  @classmethod
  def last_customer_code(cls, __sttr:int=int(), __ope:str='get') -> list|None:
    """ 
    \n`<class>` `LocalStorage.py`   
    \n Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    if((__ope.lower() == 'set')): 
      ClassError.ReferenceNullException(__sttr)
      cls._last_customer_code.append(__sttr)
    elif(__ope.lower() not in ('set', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Storage._last_customer_code.__value() :: _count(%s)' 
            %(len(cls._last_customer_code)))
      return cls._last_customer_code


  @classmethod
  def master_status(cls, __sttr:bool=True, __ope:str='get') -> bool|None:
    """ 
    \n`<class>` `LocalStorage.py`   
    \n Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    ClassError.ReferenceNullException(__sttr)
    if(ope.eq(__ope.lower(), 'set')):
      cls._master_status = __sttr if(ope.ne(__sttr, cls._master_status)) else cls._master_status
      print("◾ @setter:= Storage.cls._master_status ->: %s" %cls._master_status)
    elif(__ope.lower() not in ('set', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Storage._master_status.__value() :: %s' %cls._master_status) 
      return cls._master_status


  @classmethod
  def cashier_conference(cls, 
    __sttr:list[tuple[str, ...]] | dict = [('',)], __ope:str='get') -> dict|None:
    """ 
    \n`<class>` `LocalStorage.py`   
    \n Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    ClassError.ReferenceNullException(__sttr)
    if(ope.eq(__ope.lower(), 'set')):
      if(not isinstance(__sttr, dict)):
        cls._cashier_conference.update(__sttr)
        print("◾ @entity.setter:= Storage._cashier_conference has been successfully updated!")
      elif(isinstance(__sttr, dict)):
        cls._cashier_conference = __sttr
        print("◾ @entity.setter:= Storage._cashier_conference has been successfully defined!")
    else:
      print('◽ @entity.getter:= Storage._cashier_conference.__value() :: _count(%s)' 
            %(len(list(cls._cashier_conference.keys()))))
      return cls._cashier_conference  
  

  @classmethod
  def cashier_adjustment(cls, __sttr:float=0.0, __ope:str='get') -> list|None:
    """ 
    \n`<class>` `LocalStorage.py`   
    \n Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    ClassError.ReferenceNullException(__sttr)
    if((__ope.lower() == 'set')): 
      cls._cashier_adjustment.append(__sttr)
    elif(__ope.lower() not in ('set', 'get')): 
      ClassError.ArgumentError(('__ope', __ope, type(__ope)))
    else:
      print('◽ @entity.getter:= Storage._cashier_adjustment.__value() :: _count(%s)' 
            %(len(cls._cashier_adjustment)))
      return cls._cashier_adjustment


  @classmethod
  def products_dictionary(cls,  
      __sttr:list[tuple[str, ...]] | dict = [('',)], __ope:str='get') -> dict|None:
    """ 
    \n`<class>` `LocalStorage.py`   
    \n Method operators: `__ope`:
    \n* 'set' ⇒: `@attribute` =  `__sttr`
    \n* 'get' ⇒: `@attribute.__value__`
    """
    ClassError.ReferenceNullException(__sttr)
    if(ope.eq(__ope.lower(), 'set')):
      if(not isinstance(__sttr, dict)):
        cls._products_dictionary.update(__sttr)
        print("◾ @entity.setter:= Storage._products_dictionary has been successfully updated!")
      elif(isinstance(__sttr, dict)):
        cls._products_dictionary = __sttr
        print("◾ @entity.setter:= Storage._products_dictionary has been successfully defined!")
    else:
      print('◽ @entity.getter:= Storage._products_dictionary.__value() :: _count(%s)' 
            %(len(list(cls._products_dictionary.keys()))))
      return cls._products_dictionary

#\\END CLASS