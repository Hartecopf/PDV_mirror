*** Settings ***
Documentation       This script is one adaptation for the PRATES test cases automation
...                 project. It will perform a sales paerson simulator during the sale finalization
...                 trougth Cashback Payment Method that it is the more simple way to pay an sale.

Resource            ../_structures/base.robot
Resource            ../_structures/variables.robot
Resource            ../_main_modules/cashier_controller.robot
Resource            ../_main_modules/cancel_sale.robot
# ====================================================================================================//


*** Keywords ***
Finalize The Sale With Cashback Payment Way
    [Documentation]    Finalize the sale proccess and print the NFC-e fiscal document.

    TRY
        ${key_letter}    DataHandler.Set Payment Way    paymnt_way=DIN
        IF    ${use_client_selection} == ${True}
            base.Enter CPF Code Manually
        ELSE
            base.Use Default Data To Client Code
        END
        DataHandler.Replace Products On Offer
        DataHandler.Replace Products On Promotion
        cashier_controller.Calculate The Final Value Of The Current Sale    
        ...    ${use_difference}
        Builtin.Log To Console    
        ...    ${\n}Payment: Cashback${\n}Shortcut default: ${key_letter}
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
        # Cumpute the amount between the final sale value and its difference returned
        # for the <def> Set_And_Calc_Difference... ->: tuple from <library> Calculator.py
        IF    ${use_difference} == ${True}
            ${qnt}    Calculator.Get Values From Cashierr    cashback=${True}
            ${diff}    Calculator.Get Difference Has Computed From Final Sale Value    dff=${True}
            IF    ${qnt} > ${diff}
                ${value}    Calculator.Get Difference Has Computed From Final Sale Value
                base.Please Wait a Moment    ${default_time}
                SikuliLIbrary.Input Text    ${EMPTY}    ${value}
            END
        END
        ImageHorizonLibrary.Press Combination    KEY.ALT    ${key_letter}
        base.Run This Keyword If Discount Release Image To Appears
        base.Run This Keyword To Report A Sale Note
        cashier_controller.Price Manager Cashier Controller
        ...    keep_on_cashier=${True}    add_to_total=${True}    cashback=${True}
    EXCEPT
        SikuliLibrary.Capture Screen
        Builtin.Log    ${\n}    console=${True}
        Builtin.Log    
        ...    ${\n}It Was not possible to finalize the sale using the Cashback payment way!    
        ...    level=WARN
        DataHandler.Set Master Status    status=${False}
    END
    RETURN    ${None}

# ====================================================================================================//END
