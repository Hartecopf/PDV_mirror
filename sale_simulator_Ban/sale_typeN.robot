*** Settings ***
Documentation       This test case is performing a sale with multiple random products
...                 through Cash Payment Method.

Resource            ../_structures/base.robot
Resource            ../_payment_way/eletronic_transference.robot
Resource            ../_main_modules/product_launching.robot
Resource            ../_main_modules/database.robot
Resource            ../_main_modules/cancel_sale.robot
# ======================================================================================================//


*** Keywords ***
Executes One Sale Type BNC
    IF    ${pay_eletronic_transf} == ${True}
        DataHandler.Colored Log    
        ...    mssg=${\n}${\n}PERFORMING TEST CASE `BNC`...    level=INFO
        SikuliLibrary.Wait Until Screen Contain    ${SALE_LAYOUT_PDV}    ${5}
        product_launching.Forward The Product For Sale
        ${uncompleted_event}
        ...    eletronic_transference.Finalize It Using Eletronic Transference Payment Way
        IF    ${uncompleted_event} == ${True}
            Calculator.Clear Temporary Sale Modifiers
            DataHandler.Clear Temporary Sale Properties
            RETURN
        END
        base.Print NFC-e
        Finalize This Test Case Type BNC
        # CLEARING THE TEMPORARY LIST OF ITEMS IS REQUIRED AFTER THE COMPLETION OF EACH
        # TEST CASE PERFORMED BY THE SEQUENCE SCRIPT.
        Calculator.Clear Temporary Sale Modifiers
        DataHandler.Clear Temporary Sale Properties
        IF    ${CANCEL_SALE} == ${True}
            ${var}    cancel_sale.Check For The Cancel Event Recursion
            IF    ${var} == ${True}
                To Perform The Canceling Sale Event    TRANSFER
            END
        END
    END

# ======================================================================================================//

Finalize This Test Case Type BNC
    TRY
        base.Please Wait a Moment    ${DEFAULT_TIME / 2}
        SikuliLibrary.Screen Should Not Contain    ${DGT_CERT_NOT_FOUND}
        SikuliLibrary.Wait Until Screen Contain    ${SALE_LAYOUT_PDV}    ${5}
        database.Check Results Aigainst ERP Database    vendas
        database.Check Results Aigainst ERP Database    notassaidas    anim=${False}
    EXCEPT
        ${var}    SikuliLibrary.Exists    ${DGT_CERT_NOT_FOUND}
        IF    ${var} == ${True}
            Builtin.Log    ...    level=ERROR
            DataHandler.Colored Log
            ...    mssg=${\n}DIGITAL CERTIFICATE NOT FOUND! CHECK THE SETTINGS.${\n}    level=ERROR
            SikuliLibrary.Press Special Key    ENTER
        ELSE
            Builtin.Log    ${\n}    console=True
            Builtin.Log    ...    level=ERROR
            DataHandler.Colored Log
            ...    mssg=${\n}UNPOSSIBLE TO COMPLETE THE OPERATION!${\n}    level=ERROR
            SikuliLibrary.Press Special Key    ENTER
        END
    END
    database.Check Results Aigainst ERP Database    ontrolecaixa    anim=${False}
    base.Please Wait a Moment    ${0.5}

# =================================================================================================-End//
