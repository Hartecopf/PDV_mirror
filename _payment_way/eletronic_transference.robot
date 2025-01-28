*** Settings ***
Documentation       This script is one adaptation for the PRATES test cases automation
...    project. It will perform a sales paerson simulator during the sale finalization
...    trougth Cashback Payment Method that it is the more simple way to pay an sale.
Resource        ../_structures/base.robot
Resource        ../_structures/variables.robot
Resource        ../_main_modules/cashier_controller.robot
Resource        ../_main_modules/cancel_sale.robot

#====================================================================================================//
*** Keywords ***
#{ELETRONIC TRANFERENCE TO USER ACCOUNT}
Finalize It Using Eletronic Transference Payment Way
    TRY
        ${key_letter}    DataHandler.Set Payment Way    paymnt_way=BNC
        IF    ${USE_CLIENT_SELECTION} == ${True}
            base.Enter CPF Code Manually
        ELSE
            base.Use Default Data To Client Code
        END
        DataHandler.Replace Products On Offer
        DataHandler.Replace Products On Promotion
        cashier_controller.Calculate The Final Value Of The Current Sale
        Builtin.Log To Console    
        ...    ${\n}Payment: Eletronic Transference${\n}Shortcut default: ${key_letter}
        SikuliLibrary.Press Special Key    SPACE
        base.Run This Keyword If The Pricing Table Window To Appears
        IF    ${force_recalc} == ${True}    base.Force Recalc
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
        base.Run This Keyword If Finance Liberation Image To Appears
        base.Run This Keyword To Report A Sale Note
        cashier_controller.Price Manager Cashier Controller    
        ...    add_to_total=${True}    is_eletronic_payment=${True}    transference=${True}
    EXCEPT
        SikuliLibrary.Capture Screen
        Builtin.Log To Console    ${\n}
        Builtin.Log    ...    level=WARN
        DataHandler.Colored Log    
        ...    ${\n}It Was not possible to finalize the sale using the Eletr. Transf. Payment Way!    
        ...    level=WARN
        Set Master Status    status=${False}
    END
 
#====================================================================================================//
