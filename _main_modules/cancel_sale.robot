*** Settings ***
Documentation       ... will be wwriten

Resource            ../_structures/base.robot
Resource            database.robot
# =========================================================================================================//


*** Keywords ***
Check For The Cancel Event Recursion
    ${var}    base.Perform The Recursion Event
    RETURN    ${var}

# =========================================================================================================//

Check For The Uncompleted Event Rcursion
    ${var}    base.Perform The Recursion Event
    RETURN    ${var}

# =========================================================================================================//

To Perform The Canceling Sale Event
    [Arguments]    ${paymnt_type}
    Builtin.Log To Console    ${\n}
    Builtin.Log    ...    level=WARN
    DataHandler.Colored Log    mssg=${\n}This sale process will be canceled!    level=WARN
    DataHandler.Colored Log    mssg=The Cancelling DataHandler has been contemplated.    level=INFO
    ${cancel_key}    DataHandler.Read System Settings    key=TECLADO_CANCELACUPOM    key_type=KEYBOARD
    SikuliLibrary.Press Special Key    ${cancel_key}
    SikuliLibrary.Wait Until Screen Contain    ${CANCELLING_LAYOUT}    ${5}
    SikuliLibrary.Input Text    ${EMPTY}    ${MASTER_PASSWORD}
    SikuliLibrary.Capture Screen
    SikuliLibrary.Press Special Key    ENTER
    ${var}    SikuliLibrary.Exists    ${CANCELL_PROBLEM}    ${ALERT_IMAGE_TIME}
    IF    ${var} == ${True}
        DataHandler.Colored Log    mssg=${\n}The cancel sale process has failed!    level=ERROR
        DataHandler.Colored Log    mssg=Likelly the tax document has retruned some issues problem.    level=WARN
        DataHandler.Colored Log    mssg=For more information check for the file///..html.log.    level=WARN
        SikuliLibrary.Press Special Key    ENTER
        Perform The Console Animation    anim_time=${28}    # -> (28* 0.25mls) = 7 seconds
        RETURN
    END
    SikuliLibrary.Wait Until Screen Contain    ${CASHIER_IS_FREE}    ${CANCELATIONS_TIME}
    Calculator.Remotion From Cashier Amount    event_type=cancelling    payment_type=${paymnt_type}
    #database.Check Results Aigainst ERP Database    check_for_sale=${False}    cancelling_sale=${True}
    Perform The Console Animation    anim_time=${28}    # -> (28* 0.25mls) = 7 seconds

# =========================================================================================================//

Perform The Console Animation
    [Arguments]    ${anim_time}=${0}    ${pollingInterval}=${0.25}
    MySQLConnector.Database Log    
    ...    mssg=${\n}${\n}Wait For Synchronization...    level=INFO
    base.Please Wait a Moment    ${0.25}
    FOR    ${counter}    IN RANGE    ${0}    ${anim_time}
        base.Please Wait a Moment    ${pollingInterval}
        Builtin.Log To Console    ▮    no_newline=True
    END
    Builtin.Log To Console    ${\n}

# =========================================================================================================//

Uncompleted Sale Event
    base.Please Wait a Moment    ${DEFAULT_TIME}
    Builtin.Log To Console    ${\n}
    Builtin.Log    ...    level=WARN
    DataHandler.Colored Log    
    ...    mssg=${\n}This sale process will not be finished!    
    ...    level=WARN
    base.Please Wait a Moment    ${DEFAULT_TIME}
    SikuliLibrary.Press Special Key    ESC
    SikuliLibrary.Wait Until Screen Contain    ${SALE_LAYOUT_PDV}    ${5}
    base.Cancel Sale Process
    Perform The Console Animation    ${cancelations_time}    ${0.10}
    database.Check Results Aigainst ERP Database    vendaincompleta     anim=${False}

# =====================================================================================================//END
