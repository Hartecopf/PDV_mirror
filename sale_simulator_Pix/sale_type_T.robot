*** Settings ***
Documentation       This test case is performing a sale with multiple random products
...                 through Cash Payment Method.

Resource            ../_structures/base.robot
Resource            ../_payment_way/pix.robot
Resource            ../_main_modules/product_launching.robot
Resource            ../_main_modules/database.robot
Resource            ../_main_modules/cancel_sale.robot
# ======================================================================================================//

*** Keywords ***
Executes One Sale Type PIX
    [Documentation]
    ...    This Keywords is a simulator of the sales person to PDV Cashier.
    ...    It's the initial process to run this test case.
    IF    ${pay_pix_code} == ${True}
        DataHandler.Colored Log    
        ...    mssg=${\n}${\n}PERFORMING TEST CASE 'PIX'...    level=INFO
        SikuliLIbrary.Wait Until Screen Contain    ${SALE_LAYOUT_PDV}    ${5}
        product_launching.Forward The Product For Sale
        ${status}    Finalize The Sale With PIX Payment Way
        IF    ${status} == ${True}
            Calculator.Clear Temporary Sale Modifiers
            DataHandler.Clear Temporary Sale Properties
            RETURN
        END
        base.Print NFC-e
        Print PIX
        Finalize This Test Case Type PIX    ${status}
        # CLEARING THE TEMPORARY LIST OF ITEMS IS REQUIRED AFTER THE COMPLETION OF EACH
        # TEST CASE PERFORMED BY THE SEQUENCE SCRIPT.
        Calculator.Clear Temporary Sale Modifiers
        DataHandler.Clear Temporary Sale Properties
        IF    ${CANCEL_SALE} == ${True}
            ${var}    cancel_sale.Check For The Cancel Event Recursion
            IF    ${status} == ${None}
                IF    ${var} == ${True}
                ...    cancel_sale.To Perform The Canceling Sale Event    PIX
            ELSE IF    ${status} == ${False}
                IF    ${var} == ${True}    
                ...    cancel_sale.To Perform The Canceling Sale Event    CASH
            END
        END
    END

# ======================================================================================================//

Finalize This Test Case Type PIX
    [Arguments]    ${all_ok}=PIX
    TRY
        base.Please Wait a Moment    ${DEFAULT_TIME / 2}
        SikuliLibrary.Screen Should Not Contain    ${DGT_CERT_NOT_FOUND}
        SikuliLIbrary.Wait Until Screen Contain    ${SALE_LAYOUT_PDV}    ${5}
        database.Check Results Aigainst ERP Database    vendas
        database.Check Results Aigainst ERP Database    notassaidas    anim=${False}
        # The PIX Conference aigainst database should be done wheter only there is 
        # sucess  in  their  sale process computering. If there isn't, it means the 
        # process has not been successfully!
        IF    ${all_ok} == ${None}
            database.Check Results Aigainst ERP Database    pixmovimento    anim=${False}
        END
    EXCEPT
        ${var}    SikuliLibrary.Exists    ${DGT_CERT_NOT_FOUND}
        IF    ${var} == ${True}
            Builtin.Log To Console    ${\n}
            Builtin.Log    ...    level=ERROR
            DataHandler.Colored Log    
            ...    mssg=${\n}DIGITAL CERTIFICATE NOT FOUND! CHECK THE SETTINGS.${\n}    
            ...    level=ERROR
            SikuliLibrary.Press Special Key    ENTER
        ELSE
            Builtin.Log To Console    ${\n}
            Builtin.Log    ...    level=ERROR
            DataHandler.Colored Log    
            ...    mssg=${\n}UNPOSSIBLE TO COMPLETE THE OPERATION!    
            ...    level=ERROR
            SikuliLIbrary.Press Special Key    ENTER
        END
    END
    database.Check Results Aigainst ERP Database    controlecaixa    anim=${False}
    base.Please Wait a Moment    ${0.5}

# =================================================================================================-End//

Print PIX
    # Get System Settings for document issue confirmation...
    ${print_pix}    DataHandler.Read System Settings    
    ...    key=OPCOES_IMPRESSAOPIX    key_type=FUNCTION
    IF    ${print_pix} == ${True}
        IF    ${print_pix_docmnt} == ${True}
            ${confirm_btt}    DataHandler.Read System Settings    
            ...    key=TECLADO_MSG_YES    key_type=KEYBBOARD
            base.Please Wait a Moment    ${alert_image_time}
            SikuliLibrary.Screen Should Contain    ${PRINT_PIX_IMG}
            SikuliLibrary.Press Special Key    ${confirm_btt}
        ELSE IF    ${print_pix_docmnt} == ${False}
            ${refiuse_btt}    DataHandler.Read System Settings    
            ...    key=TECLADO_MSG_NO    key_type=KEYBBOARD
            base.Please Wait a Moment    ${alert_image_time}
            SikuliLibrary.Screen Should Contain    ${PRINT_PIX_IMG}
            SikuliLibrary.Press Special Key    ${refiuse_btt}
        END
    END
