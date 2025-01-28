*** Settings ***
Documentation       This script is one adaptation for the PRATES test cases automation
...    project. It will perform a sales person simulator during the sale finalization
...    trougth Payment Method by Instant Electronic Transfer that it is the more simple 
...    way to pay an sale.
Resource        ../_structures/base.robot
Resource        ../_main_modules/cashier_controller.robot
Resource        ../_main_modules/cancel_sale.robot

#====================================================================================================//
*** Keywords ***
#{CASH/MONEY PAYMENT WAY}
Finalize The Sale With PIX Payment Way
    TRY
        ${key_letter}    DataHandler.Set Payment Way    paymnt_way=PIX
        IF    ${USE_CLIENT_SELECTION} == ${True}
            base.Enter CPF Code Manually
        ELSE
            base.Use Default Data To Client Code
        END
        DataHandler.Replace Products On Offer
        DataHandler.Replace Products On Promotion
        cashier_controller.Calculate The Final Value Of The Current Sale
        Builtin.Log To Console    
        ...    ${\n}Payment: PIX${\n}Shortcut default: ${key_letter}
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
        base.Run This Keyword If Discount Release Image To Appears
        base.Run This Keyword To Report A Sale Note
        base.Please Wait a Moment    ${ALERT_IMAGE_TIME + 1}
        SikuliLibrary.Screen Should Not Contain    ${PIX_ERROR_CPF}
        SikuliLibrary.Screen Should Not Contain    ${PIX_ERROR_CPF_2}
        SikuliLibrary.Screen Should Not Contain    ${PIX_ERROR_CPF_3}
        SikuliLibrary.Screen Should Not Contain    ${PIX_ERROR_JASON}
        ${timer_pix}    DataHandler.Read System Settings
        ...    key=CAIXA_TIMERPIX    key_type=FUNCTION
        base.Please Wait a Moment    ${timer_pix + 1}
        SikuliLibrary.Screen Should Contain    ${PIX_PAYMENT}
        SikuliLibrary.Press Special Key    ENTER
        ${var}    SikuliLibrary.Exists    ${PIX_PAYMENT}    ${2}
        IF    ${var} == ${True}    ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.T
        ${var}    SikuliLibrary.Exists    ${PRINT_PIX_IMG}    ${5}
        # READ AND GET THE PRINT PIX DOCUMENT EVENT FROM CONFIGPDV.yaml FILE...
        IF    ${var} == ${True}
            IF    ${print_pix_docmnt} == ${True}
                ${print_bttn}    DataHandler.Read System Settings
                ...    key=TECLADO_MSG_YES    key_type=KEYBOARD
            ELSE
                ${print_bttn}    DataHandler.Read System Settings
                ...    key=TECLADO_MSG_NO    key_type=KEYBOARD
            END
            SikuliLibrary.Press Special Key    ${print_bttn}
        END
        cashier_controller.Price Manager Cashier Controller    
        ...    add_to_total=${True}    is_eletronic_payment=${True}    pix_pay=${True}
        RETURN    ${None}
    EXCEPT
        SikuliLibrary.Capture Screen
        Builtin.Log To Console    ${EMPTY}
        Builtin.Log    ...    level=ERROR
        DataHandler.Colored Log    mssg=${\n}It was not possible to finalize the sale using the PIX!    level=ERROR
        DataHandler.Colored Log    mssg=Check the screenshot capture for understanding what happened.     level=ERROR
        DataHandler.Colored Log    mssg=SUGESTION: Check for the 'PIX_TIME_OUT' in -dir ../config.robot    level=WARN
        SikuliLibrary.Press Special Key    ENTER
        Builtin.Log To Console    ${\n}Like the PIX payment ways didn't work, this sale
        Builtin.Log To Console    will be finished with the standard payment method!${\n}
        base.Please Wait a Moment    ${DEFAULT_TIME / 4}
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
        RETURN    ${False}
    END    
 
#====================================================================================================//
