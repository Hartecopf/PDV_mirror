*** Settings ***
Documentation       This test case is performing a sale with multiple random products
...                 through Credits Card Payment Method.

Resource            ../_structures/base.robot
Resource            ../_payment_way/credit_card.robot
Resource            ../_main_modules/product_launching.robot
Resource            ../_main_modules/database.robot
# ======================================================================================================//

*** Keywords ***
Executes One Sale Type CRT
    IF    ${pay_credit_card} == ${True}
        DataHandler.Colored Log    
        ...    mssg=${\n}${\n}PERFORMING TEST CASE `${type_card}`...    level=INFO
        SikuliLIbrary.Wait Until Screen Contain    ${SALE_LAYOUT_PDV}    ${5}
        product_launching.Forward The Product For Sale
        ${status}    credit_card.Finalize The Sale With Card Payment Way
        IF    ${status} == ${True}
            Calculator.Clear Temporary Sale Modifiers
            DataHandler.Clear Temporary Sale Properties
            RETURN
        END
        base.Print NFC-e
        Finalize This Test Case Type CRT    ${status}
        # CLEARING THE TEMPORARY LIST OF ITEMS IS REQUIRED AFTER THE COMPLETION OF EACH
        # TEST CASE PERFORMED BY THE SEQUENCE SCRIPT.
        Calculator.Clear Temporary Sale Modifiers
        DataHandler.Clear Temporary Sale Properties
        IF    ${CANCEL_SALE} == ${True}
            ${var}    cancel_sale.Check For The Cancel Event Recursion
            IF    ${status} == ${None}
                Builtin.Run Keyword If    ${var} == ${True}    
                ...    To Perform The Canceling Sale Event    CARD
            ELSE IF    ${status} == ${False}
                Builtin.Run Keyword If    ${var} == ${True}    
                ...    To Perform The Canceling Sale Event    CASH
            END
        END 
    END

# ======================================================================================================//

Finalize This Test Case Type CRT
    [Arguments]    ${all_ok}=CRT
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
    IF    ${all_ok} ==${None}
    ...    database.Check Results Aigainst ERP Database    
    ...    cartaomovimento    anim=${False}
    database.Timer Custom Seconds    delimiter=${20}    message=Loading to Finising...
    database.Check Results Aigainst ERP Database    contasareceber    anim=${False}
    database.Check Results Aigainst ERP Database    controlecaixa    anim=${False}
    base.Please Wait a Moment    ${default_time}

# =================================================================================================-End//
