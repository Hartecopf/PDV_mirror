# SETTINGS OF THIS CLASS :::

import logging
import coloredlogs
from robot.api import logger as log
from robot.api.deco import library, keyword
from time import strftime as st, localtime as lt


def logger1(loggerOne= logging.getLogger(name='OptionOne')) -> logging.Logger:
    """
    Colors:
       * `debug`= 'white'
       * `info`= 'green'
       * `warning`= 'yellow'
       * `error`= 'bold_red'
       * `critical`= 'red'
    """
    coloredlogs.install(
        level=logging.DEBUG, logger=loggerOne, 
            fmt='%(message)s',
            datefmt=str(st('%H:%M:%S', lt())), 
            style='%',
            level_styles=dict(
            debug=dict(color='white'),
            info=dict(color='green'),
            warning=dict(color='yellow'),
            error=dict(color='red', bold=True),
            critical=dict(color='red'),
                    ),
            field_styles=dict(
            name=dict(color='white'),
            asctime=dict(color='white'),
        funcName=dict(color='white'),
    lineno=dict(color='white'),))
    loggerOne.propagate = False
    return loggerOne

def logger2(loggerTwo= logging.getLogger(name='Optiontwo')) -> logging.Logger:
    """
    Colors:
       * `debug`= 'bold_green'
       * `info`= 'bold_magenta'
       * `warning`= 'bold_yellow'
       * `error`= 'bold_red'
       * `critical`= 'red'
    """
    coloredlogs.install(
        level=logging.DEBUG, logger=loggerTwo, 
            fmt='%(message)s',
            datefmt=str(st('%H:%M:%S', lt())), 
            style='%',
            level_styles=dict(
            debug=dict(color='green', bold=True),
            info=dict(color='magenta', bold=True),
            warning=dict(color='yellow', bold=True),
            error=dict(color='red', bold=True),
            critical=dict(color='red'),
                    ),
            field_styles=dict(
            name=dict(color='white'),
            asctime=dict(color='white'),
        funcName=dict(color='white'),
    lineno=dict(color='white'),))
    loggerTwo.propagate = False
    return loggerTwo

def logger3(loggerThree= logging.getLogger(name='OptionThree'))-> logging.Logger:
    """
    Colors:
       * `debug`= 'white'
       * `info`= 'bold_cyan'
       * `warning`= 'bold_yellow'
       * `error`= 'bold_red'
       * `critical`= 'red'
    """
    coloredlogs.install(
        level=logging.DEBUG, logger=loggerThree, 
            fmt='%(message)s',
            datefmt=str(st('%H:%M:%S', lt())), 
            style='%',
            level_styles=dict(
            debug=dict(color='white'),
            info=dict(color='cyan', bold=True),
            warning=dict(color='yellow', bold=True),
            error=dict(color='red', bold=True),
            critical=dict(color='red'),
                    ),
            field_styles=dict(
            name=dict(color='white'),
            asctime=dict(color='white'),
        funcName=dict(color='white'),
    lineno=dict(color='white'),))
    loggerThree.propagate = False
    return loggerThree

def logger4(loggerFour= logging.getLogger(name='OptionFour')) -> logging.Logger:
    """
    Colors:
       * `debug`= 'bold_green'
       * `info`= 'bold_cyan'
       * `warning`= 'bold_yellow'
       * `error`= 'bold_red'
       * `critical`= 'white'
    """
    coloredlogs.install(level=logging.DEBUG, logger=loggerFour, 
        fmt='%(message)s',
            datefmt=str(st('%H:%M:%S', lt())), 
            style='%',
            level_styles=dict(
            debug=dict(color='green', bold=True),
            info=dict(color='cyan', bold=True),
            warning=dict(color='yellow', bold=True),
            error=dict(color='red', bold=True),
            critical=dict(color='white'),
                    ),
            field_styles=dict(
            name=dict(color='white'),
            asctime=dict(color='white'),
        funcName=dict(color='white'),
    lineno=dict(color='white'),))
    loggerFour.propagate = False
    return loggerFour

def logger5(loggerFive= logging.getLogger(name='OptionFive')) -> logging.Logger:
    """
    Colors:
       * `debug`= 'green'
       * `info`= 'cyan'
       * `warning`= 'yellow'
       * `error`= 'red'
       * `critical`= 'magenta'
    """
    coloredlogs.install(level=logging.DEBUG, logger=loggerFive, 
        fmt='%(message)s',
            datefmt=str(st('%H:%M:%S', lt())), 
            style='%',
            level_styles=dict(
            debug=dict(color='green'),
            info=dict(color='cyan'),
            warning=dict(color='yellow'),
            error=dict(color='red'),
            critical=dict(color='magenta', bold=True),
                    ),
            field_styles=dict(
            name=dict(color='white'),
            asctime=dict(color='white'),
        funcName=dict(color='white'),
    lineno=dict(color='white'),))
    loggerFive.propagate = False
    return loggerFive

def logger6(loggerSix= logging.getLogger(name='OptionSix')) -> logging.Logger:
    """
    Colors:
       * `debug`= 'green'
       * `info`= 'cyan'
       * `warning`= 'yellow'
       * `error`= 'bold_red'
       * `critical`= white
    """    
    coloredlogs.install(level=logging.DEBUG, logger=loggerSix, 
        fmt='%(message)s',
        datefmt=str(st('%H:%M:%S', lt())), 
        style='%',
        level_styles=dict(
        debug=dict(color='green'),
        info=dict(color='cyan'),
        warning=dict(color='yellow'),
        error=dict(color='red', bold=True),
        critical=dict(color='white'),
                ),
        field_styles=dict(
        name=dict(color='white'),
        asctime=dict(color='white'),
    funcName=dict(color='white'),
    lineno=dict(color='white'),))
    loggerSix.propagate = False
    return loggerSix

def t_status(status:bool, upbar:bool=False):
    green = logger5(); white = logger1(); boldred = logger2()
    if(status is True):
        if(upbar is True):
            white.debug(msg='==============================================================================')
        green.debug(    msg='TEST CASE STATUS:                                                     | PASS |')
        white.debug(    msg='==============================================================================\n')
        return
    elif(status is False):
        if(upbar is True):
            white.debug(msg='==============================================================================')
        boldred.error(  msg='TEST CASE STATUS:                                                     | FAIL |')
        white.debug(    msg='==============================================================================\n')
        return
    else:
        log.info('\n', also_console=True); log.error('❌ Invalid argument value!')
        boldred.error("\nOnly options 'True' and 'False' are possible arguments")
        raise ValueError()


@library(scope='GLOBAL', version='1.0', auto_keywords=False, doc_format='reST')
class ColorText:
    def __init__(self)-> None:
        pass

    @keyword(name='Colored Custom Message')
    def Colored_Custom_Message(self,
            mssg: str = 'Write here your message!', 
            level: str = 'EX: DEBUG | INFO | WARN | ERROR | CRITICAL',
            option_log: str = 'OptionOne | OptionTwo...',
            new_line: bool = False):
        
        enable_lvels = {'DEBUG':10, 'INFO':20, 'WARN':30, 'ERROR':40, 'CRITICAL':50}
        logger = logging.getLogger(option_log)

        if(level in enable_lvels.keys()):
            broke_line:str = '\n' if new_line is True else ''
            logger.log(level=enable_lvels.__getitem__(level), msg='%s%s' %(mssg, broke_line))    
        else:
            log.info('\n', also_console=True); log.error('❌ Unknow values!')
            logger = logging.getLogger('OptionTwo')
            logger.error('[ValueError]: Invalid level argument or logger name!')
            raise ValueError()
        return