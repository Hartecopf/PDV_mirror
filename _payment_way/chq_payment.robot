*** Settings ***
Documentation       This script is one adaptation for the PRATES test cases automation
...    project. It will perform a sales paerson simulator during the sale finalization
...    trougth CHQ Payment Method that it is the singular payment war for the sale. 
Resource        ../_structures/base.robot
Resource        ../_structures/variables.robot
Resource        ../_main_modules/cashier_controller.robot
Resource        ../_main_modules/cancel_sale.robot

#=========================================================================================================//
*** Keywords ***
#{CHQ PAYMENT METHOD}
Finalize The Sale On CHQ Payment Way
    [Documentation]       Finalize the sale proccess and print the NFC-e fiscal document. 

    TRY
        ${key_letter}    DataHandler.Set Payment Way    paymnt_way=CHQ
        IF    ${USE_CLIENT_SELECTION} == ${True}
            base.Enter CPF Code Manually
        ELSE
            base.Use Default Data To Client Code
        END
        DataHandler.Replace Products On Offer
        DataHandler.Replace Products On Promotion
        cashier_controller.Calculate The Final Value Of The Current Sale
        Builtin.Log To Console    
        ...    ${\n}Payment: CQH${\n}Shortcut default: ${key_letter}
        SikuliLibrary.Press Special Key    SPACE
        base.Run This Keyword If The Pricing Table Window To Appears
        IF    ${force_recalc} == ${True}
            base.Force Recalc
        END
        SikuliLibrary.Wait Until Screen Contain    
        ...    ${PAYMENT_SCREEN}    ${DEFAULT_TIME * 5}
        ${use_dav}    DataHandler.Read System Settings    
        ...    key=OPCOES_IMPRIMEDAV    key_type=FUNCTION
        ${equivalence}    DataHandler.Check For Equivalence    
        ...    ${use_dav}    ${print_dav}
        IF    ${equivalence} == ${True}
            base.Please Wait a Moment    ${default_time}
            SikuliLibrary.Press Special Key    F11
            base.Please Wait a Moment    ${default_time}
            SikuliLibrary.Press Special Key    NUM9
        END
        IF    ${UNCOMPLETE_SALE} == ${True}
            ${var}    cancel_sale.Check For The Uncompleted Event Rcursion
            IF    ${var} == ${True}
                cancel_sale.Uncompleted Sale Event
                RETURN    ${var}
            END
        END  
        ImageHorizonLibrary.Press Combination    KEY.ALT    ${key_letter}
        base.Run This Keyword If Discount Release Image To Appears
        ${client_chosen}    base.Get The Customer Data Record
        Finalize This Sale With CHQ Payment Method    client_code=${client_chosen}
        base.Run This Keyword If Finance Liberation Image To Appears
        ${error}    SikuliLibrary.Exists    ${CHQ_EXISTILY}    ${2}
        IF    ${error} != ${False}
            Builtin.Log To Console    ${\n}
            Builtin.Log    ...    level=WARN
            DataHandler.Colored Log    ${\n}CHQ Code has already subscripted!    level=WARN
            SikuliLibrary.Press Special Key    ENTER
            base.Please Wait a Moment    ${0.5}
            SikuliLibrary.Press Special Key    ESC
            base.Please Wait a Moment    ${0.5}
            ImageHorizonLibrary.Press Combination    KEY.ALT    ${key_letter}
            base.Run This Keyword If Discount Release Image To Appears
            Finalize This Sale With CHQ Payment Method    client_code=${PATTERN_CLIENT_CODE}
            base.Run This Keyword If Finance Liberation Image To Appears
        END
        base.Run This Keyword To Report A Sale Note
        cashier_controller.Price Manager Cashier Controller    
        ...    keep_on_cashier=${True}    add_to_total=${True}    chq=${True}
    EXCEPT
        Capture Screen
        Builtin.Log To Console    ${\n}
        Builtin.Log    ...        level=WARN
        DataHandler.Colored Log    
        ...    ${\n}Was not possible to finalize the sale using the CQH payment method!    
        ...    level=WARN
        DataHandler.Set Master Status    status=${False}
    END
    RETURN    ${None}
    
#==========================================================================================================//
Randomic CHQ Number
    [Documentation]    It Defines randomicaly what will be the value to CHQ_NUMBER.
    ${CHQ_NUMBER}    FakerLibrary.Random Number    digits=${5}  
    Builtin.Log To Console    
    ...    This is the random value has generated for CHQ_NUMBER: ${CHQ_NUMBER}    
    RETURN    ${CHQ_NUMBER}

#==========================================================================================================//
Pass The CHQ Number Using Its Randomic Intergers
    [Documentation]    
    ...    This Keyword choices randomicaly the CHQ number and applies it in the subscription dialog box
    ${the_number_chosen}    Randomic CHQ Number
    DataHandler.Store The CHQ Serial Number     number=${the_number_chosen}
    SikuliLibrary.Input Text    ${EMPTY}    ${the_number_chosen}
    SikuliLibrary.Press Special Key    TAB
    base.Please Wait a Moment    ${0.3}
    SikuliLibrary.Press Special Key    HOME
    base.Please Wait a Moment    ${0.3}
    SikuliLibrary.Press Special KEY    ADD
    base.Please Wait a Moment    ${0.3}
    SikuliLibrary.Press Special Key    TAB

#==========================================================================================================//
Finalize This Sale With CHQ Payment Method
    [Documentation]    It is the module that will finalize the sale using CHQ payment method.
    [Arguments]    ${client_code}=${0}

    # This loops structure inserts all components from ${CHQ_COMPONENTS} in ${CHQ_PAYMENT_WAY} 
    # fields. ${CHQ_PAYMENT_WAY} is a modal screen that appears during payment method layout.
    
    TRY
        SikuliLibrary.Wait Until Screen Contain   ${CHQ_PAYMENT_WAY}    ${DEFAULT_TIME * 2}
        SikuliLibrary.Press Special Key    TAB
        Builtin.Log To Console    In this step, the payment method solution is started using the CHQ!
        Builtin.Log To Console    Look at the CHQ datas that were entered on modal window of the payment!
        FOR    ${counter}    ${index_element}   IN ENUMERATE     @{CHQ_COMPONENTS}    start=${0}
            base.Please Wait a Moment    ${0.5}
            Builtin.Log To Console    
            ...    Step ${counter}: The element value has returned from CHQ List is: ${index_element}     
            SikuliLibrary.Input Text    ${EMPTY}    ${index_element}
            SikuliLibrary.Press Special Key    TAB
        END
        Pass The CHQ Number Using Its Randomic Intergers
        base.Please Wait a Moment   ${0.5}
        # This subsequent loop search the 'TEST' mode in [Origem] dialog modal box will appear on screen.
        FOR    ${counter}    IN RANGE    ${0}     ${3}    # start | end
            base.Please Wait a Moment    ${0.3}
            SikuliLibrary.Press Special Key    DOWN
        END
        SikuliLibrary.Press Special Key     ENTER
        SikuliLibrary.Input Text     ${EMPTY}    ${CHQ_DESCRIPTION}
        base.Please Wait a Moment    ${0.5}
        SikuliLibrary.Press Special Key     TAB
        SikuliLibrary.Input Text     ${EMPTY}    ${client_code}
        SikuliLibrary.Press Special Key     TAB
        ${var}     SikuliLibrary.Exists    ${INVALID_CUSTOM_CODE}    ${2}
        ${var2}    SikuliLibrary.Exists    ${CHQ_CRE_DEPARTMENT}     ${2}
        ${var3}    SikuliLibrary.Exists    ${CPF_CNPJ_NOT_FOUND}     ${2}
        IF    ${var} == ${True}
            SikuliLibrary.Press Special Key    ENTER
            base.Please Wait a Moment    ${0.5}
            SikuliLibrary.Input Text     ${EMPTY}    ${PATTERN_CLIENT_CODE}
            base.Please Wait a Moment    ${0.5}
            SikuliLibrary.Press Special Key    TAB
            base.Please Wait a Moment    ${0.5}
        ELSE IF    ${var2} == ${True}
            SikuliLibrary.Press Special Key    ENTER
            Builtin.Log To Console    ${\n}
            Builtin.Log    ...    level=WARN
            DataHandler.Colored Log    
            ...    ${\n}The System has reported an observation about this customer code!    level=WARN
            DataHandler.Colored Log    Customer Code: ${client_code}    level=WARN
            base.Run This Keyword If Finance Liberation Image To Appears
            base.Please Wait a Moment    ${0.5}
            SikuliLibrary.Press Special Key    ENTER
        ELSE IF    ${var3} == ${True}
            SikuliLibrary.Press Special Key    ENTER
            Builtin.Log To Console    ${\n}
            Builtin.Log    ...    level=WARN
            DataHandler.Colored Log    
            ...    mssg=${\n}Customer Code or Identification has not found!    level=WARN
            base.Please Wait a Moment    ${0.5}
            SikuliLibrary.Input Text     ${EMPTY}    ${PATTERN_CLIENT_CODE}
            base.Please Wait a Moment    ${0.3}
            SikuliLibrary.Press Special Key    TAB
        END
        base.Run This Keyword If Finance Liberation Image To Appears
        ImageHorizonLibrary.Press Combination     KEY.ALT    KEY.I
    EXCEPT
        SikuliLibrary.Capture Screen
        Builtin.Log To Console    ${\n}
        Builtin.Log    ...    level=WARN
        DataHandler.Colored Log    ${\n}It was not possible to finalize this sale using the CHQ payment method!   level=WARN
        DataHandler.Colored Log    $There was a problem during the finalization of the sale with CHQ payment way.    level=WARN
    END

 
#==========================================================================================================//