*** Settings ***
Documentation       This script is one adaptation for the PRATES test cases automation
...    project. It will perform a sales paerson simulator during the sale finalization
...    trougth Customer Credit that it is the particular payment way of the client. 
Resource        ../_structures/base.robot
Resource        ../_structures/variables.robot
Resource        ../_main_modules/cashier_controller.robot
Resource        ../_main_modules/cancel_sale.robot

#===================================================================================================================//
*** Keywords ***
Finalize The Sale With Card Payment Way 
    [Documentation]       Finalize the sale proccess and print the NFC-e fiscal document. 

    ${key_letter}    Set Payment Way    paymnt_way=${type_card}
    IF    ${USE_CLIENT_SELECTION} == ${True}
        base.Enter CPF Code Manually
    ELSE
        base.Use Default Data To Client Code
    END
    DataHandler.Replace Products On Offer
    DataHandler.Replace Products On Promotion
    cashier_controller.Calculate The Final Value Of The Current Sale
    Builtin.Log To Console   
    ...    ${\n}Payment: Credit Card${\n}Shortcut default: ${key_letter}
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
    ${status}    Credits Card Payment Method Internal Structure
    base.Run This Keyword If Finance Liberation Image To Appears
    base.Run This Keyword To Report A Sale Note
    RETURN    ${status}

#===================================================================================================================//

Randomic Number To Cash Card CV
    [Documentation]    It Defines randomicaly what will be the value to CHQ_NUMBER.
    ${cards_number}    FakerLibrary.Random Number    digits=${3}  
    Builtin.Log To Console    
    ...    The random value has generated for Cards Number it is: ${cards_number}
    RETURN    ${cards_number}

#===================================================================================================================//
Credits Card Payment Method Internal Structure
    [Documentation]    This Keyword get a element from credits card LIST and parse it as
    ...    an interactive object to the internal payment structure of the PDV system.
    TRY
        SikuliLibrary.Wait Until Screen Contain    ${CARDS_PAY_LAYOUT}    ${ALERT_IMAGE_TIME + 1}
        ${choices}    DataHandler.Get Card Codes For Payment
        Builtin.Log To Console    Card Choice: ${choices}
        SikuliLibrary.Input Text    ${EMPTY}    ${choices}[${0}]
        base.Please Wait a Moment    ${0.5}
        SikuliLibrary.Press Special Key    TAB
        base.Please Wait a Moment    ${0.5}
        SikuliLibrary.Input Text    ${EMPTY}    ${choices}[${1}]
        SikuliLibrary.Press Special Key    TAB
        base.Please Wait a Moment    ${0.5}
        SikuliLibrary.Screen Should Not Contain    ${CARD_NOT_FOUND}
        ${random_card_cv}    Randomic Number To Cash Card CV
        SikuliLibrary.Input Text    ${EMPTY}    ${random_card_cv}
        base.Please Wait a Moment    ${0.5}
        SikuliLibrary.Press Special Key    TAB
        SikuliLibrary.Input Text    ${EMPTY}    ${CREDIT_MONTHS}
        base.Please Wait a Moment    ${0.5}
        SikuliLibrary.Press Special Key    TAB
        SikuliLibrary.Press Special Key    ENTER
        Calculator.Check For Card Taxes Or Debits    ${choices}[${0}]    ${choices}[${1}]
        base.Please Wait a Moment    ${0.5}
    EXCEPT
        Builtin.Log To Console    ${\n}
        Builtin.Log    ...    level=ERROR
        DataHandler.Colored Log    mssg=${\n}It was not possible to complete this step of the process.    level=ERROR
        DataHandler.Colored Log    mssg=There was a problem during the finalization of the sale with TEF payment way.    level=WARN
        DataHandler.Colored Log    mssg=It is likely that the card code could not be found.    level=WARN
        Report The Problem But Continue The Process
        RETURN    ${False}
    ELSE
        Builtin.Log To Console    The sale process has been completed successfully!
        cashier_controller.Price Manager Cashier Controller    
        ...    add_to_total=${True}    is_eletronic_payment=${True}    credit_card=${True}
        RETURN    ${None}
    END

#===================================================================================================================//
Report The Problem But Continue The Process
    [Documentation]    This keyword will be called whenever something happens. A single problem can occur during the
    ...    finalization of the sale with the TEF Credit Card. This occurrence is considered through this structure.
    
    SikuliLibrary.Capture Screen
    SikuliLibrary.Press Special Key    ENTER
    Builtin.Log To Console    Check the screenshot!
    Builtin.Log To Console    ${\n}Like the TEF Credit Card payment didn't work, this
    Builtin.Log To Console    will be finished with the standard payment method!${\n}
    base.Please Wait a Moment    ${DEFAULT_TIME / 4}
    SikuliLibrary.Press Special Key    ESC
    ${key_letter}    DataHandler.Set Payment Way    paymnt_way=DIN
    DataHandler.Colored Log    mssg=${\n}RECALCULATING...    level=WARN
    base.Please Wait a Moment    ${0.25}
    FOR    ${counter}    IN RANGE    ${0}    ${25}
        base.Please Wait a Moment    ${0.025}
        Builtin.Log To Console    ▮    no_newline=True
    END
    Builtin.Log To Console    ${\n}
    ImageHorizonLibrary.Press Combination    KEY.ALT    ${key_letter}
    Calculator.Restore The Sale Properties
    DataHandler.Replace Products On Offer
    DataHandler.Replace Products On Promotion
    cashier_controller.Calculate The Final Value Of The Current Sale
    base.Run This Keyword If Discount Release Image To Appears
    base.Run This Keyword To Report A Sale Note
    cashier_controller.Price Manager Cashier Controller
    ...    keep_on_cashier=${True}    add_to_total=${True}    cashback=${True}

#===================================================================================================================//