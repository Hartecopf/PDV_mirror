*** Settings ***
Documentation       This test case runs a sale with various products through CQH payment
...                 method. Its resolution is same to sale_various_products_typeD.robot

Resource            ../_structures/base.robot
Resource            ../_payment_way/chq_payment.robot
Resource            ../_main_modules/product_launching.robot
Resource            ../_main_modules/database.robot
# ======================================================================================================//


*** Keywords ***
Executes One Sale Type CHQ
    [Documentation]
    ...    This Keywords is a simulator of the sales person to PDV Cashier.
    ...    It's the initial process to run this test case.
    IF    ${pay_check} == ${True}
        DataHandler.Colored Log    
        ...    mssg=${\n}${\n}PERFORMING TEST CASE `CHQ`...    level=INFO
        SikuliLibrary.Wait Until Screen Contain    ${SALE_LAYOUT_PDV}    ${DEFAULT_TIME * 5}
        product_launching.Forward The Product For Sale
        ${uncompleted_event}    chq_payment.Finalize The Sale On CHQ Payment Way
        IF    ${uncompleted_event} == ${True}
            Calculator.Clear Temporary Sale Modifiers
            DataHandler.Clear Temporary Sale Properties
            RETURN
        END
        base.Print NFC-e
        Finalize This Test Case Type CHQ
        Calculator.Clear Temporary Sale Modifiers
        DataHandler.Clear Temporary Sale Properties
        IF    ${CANCEL_SALE} == ${True}
            ${var}    cancel_sale.Check For The Cancel Event Recursion
            IF    ${var} == ${True}
            ...    cancel_sale.To Perform The Canceling Sale Event    CHECK
        END
    END

# ======================================================================================================//

Finalize This Test Case Type CHQ
    TRY
        base.Please Wait a Moment    ${DEFAULT_TIME / 2}
        SikuliLibrary.Screen Should Not Contain    
        ...    ${DGT_CERT_NOT_FOUND}
        SikuliLIbrary.Wait Until Screen Contain
        ...    ${SALE_LAYOUT_PDV}
        ...    ${DEFAULT_TIME * 5}
        database.Check Results Aigainst FireBird Localhost    vendas
        database.Check Results Aigainst ERP Database          vendas
        database.Check Results Aigainst ERP Database          notassaidas    anim=${False}
        database.Check Results Aigainst ERP Database          chequest       anim=${False}
    EXCEPT
        base.Looking For Screen Error Images After Sales Finishment
    END
    ExternalPrograms.Call External Program    fiscalcheckup
    database.Timer Custom Seconds    delimiter=${20}    message=Loading to Finising...
    database.Check Results Aigainst ERP Database    contasareceber    anim=${False}
    database.Check Results Aigainst ERP Database    caixamovimentosformas    anim=${False}
    database.Check Results Aigainst ERP Database    controlecaixa    anim=${False}
    base.Please Wait a Moment    ${0.5}

# ==================================================================================================-End//
