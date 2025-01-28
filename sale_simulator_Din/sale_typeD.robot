*** Settings ***
Documentation       This test case is performing a sale with multiple random products
...                 through Cash Payment Method.

Resource            ../_structures/base.robot
Resource            ../_payment_way/cashback.robot
Resource            ../_main_modules/product_launching.robot
Resource            ../_main_modules/database.robot
# ======================================================================================================//

*** Keywords ***
Executes One Sale Type DIN
    IF    ${pay_cashback} == ${True}
        DataHandler.Colored Log    
        ...    mssg=${\n}${\n}PERFORMING TEST CASE `DIN`...    level=INFO
        SikuliLibrary.Wait Until Screen Contain    ${SALE_LAYOUT_PDV}   ${DEFAULT_TIME * 5}
        product_launching.Forward The Product For Sale
        ${uncompleted_event}    cashback.Finalize The Sale With Cashback Payment Way
        IF    ${uncompleted_event} == ${True}
            Calculator.Clear Temporary Sale Modifiers
            DataHandler.Clear Temporary Sale Properties
            RETURN
        END
        base.Print NFC-e
        Finalize This Test Case Type DIN
        Calculator.Clear Temporary Sale Modifiers
        DataHandler.Clear Temporary Sale Properties
        IF    ${CANCEL_SALE} == ${True}
            ${var}    cancel_sale.Check For The Cancel Event Recursion
            IF    ${var} == ${True}    
            ...    cancel_sale.To Perform The Canceling Sale Event    CASH
        END
    END

# ======================================================================================================//

Finalize This Test Case Type DIN
    TRY
        base.Please Wait a Moment    ${DEFAULT_TIME / 2}
        SikuliLibrary.Screen Should Not Contain    ${DGT_CERT_NOT_FOUND}
        SikuliLibrary.Wait Until Screen Contain    ${SALE_LAYOUT_PDV}    ${30}
        database.Check Results Aigainst FireBird Localhost    vendas
        database.Check Results Aigainst ERP Database    vendas
        database.Check Results Aigainst ERP Database    notassaidas    anim=${False}
    EXCEPT
        base.Looking For Screen Error Images After Sales Finishment
    END
    ExternalPrograms.Call External Program    fiscalcheckup
    database.Timer Custom Seconds    delimiter=${20}    message=Loading to Finising...
    database.Check Results Aigainst ERP Database    contasareceber    anim=${False}
    database.Check Results Aigainst ERP Database    caixamovimentosformas    anim=${False}
    database.Check Results Aigainst ERP Database    controlecaixa    anim=${False}
    base.Please Wait a Moment    ${default_time}

# =================================================================================================-End//

