*** Settings ***
Documentation       This Module is running one siple sale with various products chosen from
...                 MASTER_LIST and finlize this process as customer credit payment method.

Resource            ../_structures/base.robot
Resource            ../_payment_way/customer_credit.robot
Resource            ../_main_modules/product_launching.robot
Resource            ../_main_modules/database.robot
Resource            ../_main_modules/cancel_sale.robot
# ======================================================================================================//


*** Keywords ***
Executes One Sale Type CRE
    IF    ${pay_customer_credit} == ${True}
        IF    ${RANDOMIZE_CPF_CODE} == ${False}
            DataHandler.Colored Log    
            ...    mssg=${\n}${\n}PERFORMING TEST CASE `CRE`...    level=INFO
            SikuliLIbrary.Wait Until Screen Contain    ${SALE_LAYOUT_PDV}    ${5}
            product_launching.Forward The Product For Sale
            ${var}    Finalize The Sale With Customer Credit
            IF    ${var} == ${False}    RETURN
            base.Print NFC-e
            Finalize This Test Case Type CRE
            # CLEARING THE TEMPORARY LIST OF ITEMS IS REQUIRED AFTER THE COMPLETION OF EACH
            # TEST CASE PERFORMED BY THE SEQUENCE SCRIPT.
            Calculator.Clear Temporary Sale Modifiers
            DataHandler.Clear Temporary Sale Properties
        ELSE
            Builtin.Log To Console    ${\n}
            Builtin.Log    ...    level=WARN
            DataHandler.Colored Log    mssg=${\n}${\n}TEST CASE ``P``...    level=INFO
            DataHandler.Colored Log    mssg=This Payment Method is unvaliable to the current Test Case behavior!    level=WARN
            DataHandler.Colored Log    mssg=It's unposible to perform a Customer Payment Way when the client    level=WARN
            DataHandler.Colored Log    mssg=doesn't exists or has not subscripted in the ERP database.    level=WARN
            DataHandler.Colored Log    mssg=Check for the Settings of the Test Case in execution.    level=NULL
            RETURN
        END
    END

# ======================================================================================================//

Finalize This Test Case Type CRE
    TRY
        base.Please Wait a Moment    ${DEFAULT_TIME / 2}
        SikuliLibrary.Screen Should Not Contain    ${DGT_CERT_NOT_FOUND}
        SikuliLibrary.Wait Until Screen Contain    ${SALE_LAYOUT_PDV}    ${30}
        database.Check Results Aigainst FireBird Localhost    vendas
        database.Check Results Aigainst ERP Database    vendas
        database.Check Results Aigainst ERP Database    notassaidas       anim=${False}
    EXCEPT
        base.Looking For Screen Error Images After Sales Finishment
    END
    ExternalPrograms.Call External Program    fiscalcheckup
    database.Timer Custom Seconds    delimiter=${20}    message=Loading to Finising...
    database.Check Results Aigainst ERP Database    contasareceber    anim=${False}
    #database.Check Results Aigainst ERP Database    controlecaixa    anim=${False}
    base.Please Wait a Moment    ${default_time}

# ==================================================================================================-End//
