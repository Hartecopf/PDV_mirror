*** Settings ***
Documentation    Debug File
Library          OperatingSystem
Library          ../_custom_libraries/DataHandler.py
Library          ../_custom_libraries/MySQLConnector.py
Library          ../_custom_libraries/Calculator.py
Variables        ../_custom_libraries/input/Config_Bkp.yaml
Resource    ../_main_modules/product_launching.robot
# =========================================================================================================//
*** Test Cases ***
Debug Libraries
    Load Data Libraries
    Single Sale Event
    [Teardown]
    ...    Run Keyword And Warn On Failure    
    ...    DataHandler.Show Project Relatory

*** Keywords ***
Console Animation For Synchronization Time
    [Arguments]    
    ...    ${anim_time}=${0}    
    ...    ${pollingInterval}=${0.25}    
    ...    ${msge}=${\n}Wait For Synchronization...
    MySQLConnector.Database Log    mssg=${\n}${\n}${msge}    level=INFO
    Builtin.Sleep   ${0.25}
    FOR    ${counter}    IN RANGE    ${0}    ${anim_time}
        Builtin.Sleep    ${pollingInterval}
        Builtin.Log To Console    ▮    no_newline=True
    END
    # PyAutoGI Debug @Keyword
    ${instructions}    Builtin.Create Dictionary
    ...    type=keyboard    function=press_key    key=space
    DataHandler.Machine Instructions    instruct=${instructions}
# =========================================================================================================//

Load Data Libraries
    DataHandler.Load Storage Path
    Console Animation For Synchronization Time
    ...    ${32}    pollingInterval=${0.05}    msge=🔠 Checking for Project Settings...
    DataHandler.Check For The Project Settings Integrity
    DataHandler.Colored Log    ${\n}🔄 Wait for the loading to finishing...    level=INFO2
    Builtin.Import Variables    ${EXECDIR}/../_custom_libraries/input/Config_Bkp.yaml
    Builtin.Sleep    ${0.3}
    MySQLConnector.Show FireBird Connection Status
    IF    ${data_recovery} == ${False} 
        DataHandler.Colored Log    ${\n}💬 Loading Keyboard Instruction...    level=INFO
        DataHandler.Load Keyboard Instruction
        DataHandler.Colored Log    ${\n}🔧 Loading PDV System Settings...    level=INFO
        DataHandler.Load PDV System Settings
    END
    DataHandler.Colored Log    ${\n}📥 Recording Project Folder...    level=INFO
    Builtin.Sleep    ${0.3}
    OperatingSystem.Directory Should Exist    path=../resources/elements
    OperatingSystem.Count Files In Directory    path=../resources/elements
    DataHandler.Colored Log    ${\n}📡 Creating a MySQL Conenction...    level=INFO
    Builtin.Sleep    ${0.5}
    # DATA LIBRARIES BEHAVIOUR ::
    MySQLConnector.Create Connection To Database    ${use_new_connect}
    MySQLConnector.Show Internal Data
    MySQLConnector.Load Custom Settings
    MySQLConnector.Load System Versions
    MySQLConnector.Show MySQL Connection Status
    DataHandler.Colored Log    ${\n}💱 Loading payment methods...    level=INFO
    DataHandler.Create Payment Mapping
    DataHandler.Colored Log    ${\n}👨 Loading customer dataschema...    level=INFO
    DataHandler.Create Custommer Mapping
    DataHandler.Colored Log    ${\n}🛒 Loading product dataschema...    level=INFO
    DataHandler.Create Product Mapping
    DataHandler.Colored Log    ${\n}💰 Loading cashier's content...    level=INFO
    DataHandler.Reset Cashier Output File
    #DataHandler.Cashier Auto Adjustment
    DataHandler.Load Cashier Contents
    DataHandler.Initial Info
# =========================================================================================================//

Forward The Products For Sale
    [Documentation]    
    ...    It   performs the launching of produts for sale using the system's initial layout and also 
    ...    the product properties provided as boolean settings to the function parameters. In Addition,
    ...    this keyword has the chacacteristic of using only the barcode as a search filter during launch
    ...    of the chosen product or standard product.
    [Arguments]    ${LOOP_TIMES}=${QNT_PROD_FOR_SALE}

    Builtin.Log To Console    
    ...    The Chosen Products will be entered through the PDV Initial Layout Screen!
    IF    ${RANDOMIZE_QNT_PRODUCT} == ${True}
        ${LOOP_TIMES}    DataHandler.Random Interger    imax=${QNT_MAX_PROD_FOR_SALE}
    END

    Builtin.Log To Console    Quantity of Products in this sale: ${LOOP_TIMES}
    Builtin.Log To Console    Here starts the products choice for this sale.
    FOR    ${counter}    IN RANGE    ${0}    ${LOOP_TIMES}
        IF    ${USE_DEFAULT_PRODUCT} == ${False}
            ${prod_code}    DataHandler.Product Controller
            ...    _get=${False}    randomize_get=${True}
            ...    _id=${True}
        ELSE
            ${prod_code}    Builtin.Set Variable    ${STANDARD_PRODUCT}
        END

        ${product_name}    DataHandler.Product Controller
        ...    _key=${prod_code}    _get=${True}
        ...    _find=${True}    description=${True}

        ${prod_barcode}    DataHandler.Product Controller
        ...    _key=${prod_code}    _get=${True}
        ...    _find=${True}    barcode=${True}

        Builtin.Log To Console    ${\n}Prod. Name: ${product_name}
        Builtin.Log To Console    Prod. Code: ${prod_code}
        Builtin.Log To Console    Prod. Barcode: ${prod_barcode}

        ${product_price}    DataHandler.Product Controller
        ...    _key=${prod_code}    _get=${True}
        ...    _find=${True}    price_T1=${True}

        ${grid_product}    DataHandler.Product Controller
        ...    _key=${prod_code}    _get=${True}
        ...    _find=${True}    is_grid=${True}

        Builtin.Log To Console    Grid Product: ${grid_product}
        Calculator.Add Amount To The Current Sale    ${product_price}
        Builtin.Log To Console    -----------------------------------------------------------
        Calculator.Show The Current Sale Value
        Builtin.Log To Console    -----------------------------------------------------------${\n}
    END
# =========================================================================================================//

Enter A Custom Sequence of Products
    [Documentation]    
    ...    This    Keyword    Perform    the    launching of one custom products sequence. A Custom
    ...    sequence  of produts can be builded during the test    case startup also done through the
    ...    PRATES interactive module. A Fatal Error Sentence will be triggered if the sequence is empty.
    
    ${products_seq}    DataHandler.Interpreter Of Sequences    sequence=@{custom_prod_sequence}    
    Builtin.Log To Console    Was choosen a custom sequence of product to insert on sale!
    Builtin.Log To Console    Products sequence: @{products_seq}
    Builtin.Log To Console    ${EMPTY}
    TRY
        FOR    ${index}    ${element}    IN ENUMERATE    @{products_seq}
            ${prod_barcode}    DataHandler.Product Controller
            ...    _key=${element}    _get=${True}
            ...    _find=${True}    barcode=${True}

            ${product_name}    DataHandler.Product Controller
            ...    _key=${element}    _get=${True}
            ...    _find=${True}    description=${True}

            Builtin.Log To Console    ${\n}Prod. Name: ${product_name}
            Builtin.Log To Console    Prod. Code: ${element}
            Builtin.Log To Console    Prod. Barcode: ${prod_barcode}

            ${product_price}    DataHandler.Product Controller
            ...    _key=${element}    _get=${True}
            ...    _find=${True}    price_T1=${True}

            ${grid_product}    DataHandler.Product Controller
            ...    _key=${element}    _get=${True}
            ...    _find=${True}    is_grid=${True}

            Builtin.Log To Console    Grid Product: ${grid_product}
            Calculator.Add Amount To The Current Sale    ${product_price}
            Builtin.Log To Console    -----------------------------------------------------------
            Calculator.Show The Current Sale Value
            Builtin.Log To Console    -----------------------------------------------------------${\n}
        END
    EXCEPT
        Builtin.Log To Console    ${\n}Was not possible to perform the insertion custom product sequence!
        Builtin.Log To Console    There was a problem with the product picker! Check out if the sequence is not empty!
        Builtin.Fatal Error
    END
# =========================================================================================================//

Product Grouping For Sale
    [Documentation]    
    ...    This keyword is the most recent implementations to the module 'various_product.robot'.
    ...    Its incumbence is to organize the product grouping for the sales building together its
    ...    properties. In a different way from another launghing types, that method requires the previously
    ...    sales creations before to make the product grouping. Some promotions and offers are impacted for
    ...    this resource in the sales process building.
    [Arguments]    ${LOOP_TIMES}=${QNT_PROD_FOR_SALE}

    ${current_sale_value}    Builtin.Set Variable    ${0}
    ${items_on_sale}    Builtin.Set Variable    ${0}

    IF    ${PRODUCT_SEQUENCE} == ${True}
        ${prod_sequence}    DataHandler.Interpreter Of Sequences    sequence=@{custom_prod_sequence}
        Builtin.Log To Console    Was choosen a custom sequence of product to insert on sale!
        Builtin.Log To Console    Products sequence: @{prod_sequence}${\n}
        Builtin.Log To Console    ${EMPTY}
        FOR    ${index}    ${element}    IN ENUMERATE    @{prod_sequence}
            ${prod_barcode}    Product Controller
            ...    _key=${element}    _get=${True}
            ...    _find=${True}    barcode=${True}

            ${product_price}    DataHandler.Product Controller
            ...    _key=${element}    _get=${True}
            ...    _find=${True}    price_T1=${True}    attr_logger=${False}

            ${grid_product}    DataHandler.Product Controller
            ...    _key=${element}    _get=${True}
            ...    _find=${True}    is_grid=${True}

            Calculator.Add Amount To The Current Sale    ${product_price}
        END
    ELSE
        Builtin.Log To Console    The Chosen Products will be entered through the PDV Initial Layout Screen!
        IF    ${RANDOMIZE_QNT_PRODUCT} == ${True}
            ${LOOP_TIMES}    DataHandler.Random Interger    imin=${1}    imax=${QNT_MAX_PROD_FOR_SALE}
        END

        Builtin.Log To Console    Quantity of Products in this sale: ${LOOP_TIMES}${\n}
        FOR    ${counter}    IN RANGE    ${0}    ${LOOP_TIMES}
            # BUILDING THE SALE...
            IF    ${USE_DEFAULT_PRODUCT} == ${False}
                ${prod_code}    DataHandler.Product Controller
                ...    _get=${False}    randomize_get=${True}
                ...    _id=${True}
            ELSE
                ${prod_code}    Builtin.Set Variable    ${STANDARD_PRODUCT}
            END

            ${product_price}    DataHandler.Product Controller
            ...    _key=${prod_code}    _get=${True}
            ...    _find=${True}    price_T1=${True}    attr_logger=${False}

            ${grid_product}    DataHandler.Product Controller
            ...    _key=${prod_code}    _get=${True}
            ...    _find=${True}    is_grid=${True}

            Calculator.Add Amount To The Current Sale    ${product_price}
        END
    END
    DataHandler.Replace Products On Offer
    MySQLConnector.Database Log    mssg=-----------------------------------------------------------    level=INFO
    DataHandler.Colored Log    mssg=PRODUCT GROUNPING FOR CURRENT SALE...    level=INFO
    DataHandler.Colored Log    mssg=Here starts the products choice for this sale.    level=NULL
    MySQLConnector.Database Log    mssg=-----------------------------------------------------------${\n}    level=INFO
    ${elements_qnt}    DataHandler.Set Group Products For Sale
    FOR    ${counter}    IN RANGE    ${0}    ${elements_qnt}
        Builtin.Log    Current <var>: counter -> ${counter}
        # tuple ↴
        ${temp_var}    DataHandler.Get Group of Products For Sale    ${counter}

        # EXTRACTING VALUES FROM INTERNAL @PROPERTY python <dict>: Centralizer.group_prod_for_sale...
        ${prod_quantity}    Builtin.Set Variable    ${temp_var}[${0}]
        ${prod_code}    Builtin.Set Variable    ${temp_var}[${1}]
        ${prod_barcode}    Builtin.Set Variable    ${temp_var}[${2}]
        ${prod_total}    Builtin.Set Variable    ${temp_var}[${3}]
        ${prod_status}    Builtin.Set Variable    ${temp_var}[${4}]

        # GET THE PRODUCT NAME FROM INTERNAL @PROPERTY pytthon <dict>: self.products ...
        ${product_name}    DataHandler.Product Controller
        ...    _key=${prod_code}    _get=${True}
        ...    _find=${True}    description=${True}

        ${grid_product}    DataHandler.Product Controller
        ...    _key=${prod_code}    _get=${True}
        ...    _find=${True}    is_grid=${True}
        ...    build_sale=${False}

        # CONSOLE LOG:
        Builtin.Log To Console    Prod. Name: ${product_name}
        Builtin.Log To Console    Prod. Code: ${prod_code}
        Builtin.Log To Console    Prod. Barcode: ${prod_barcode}
        Builtin.Log To Console    Quantity: ${prod_quantity}
        IF    ${prod_status} == ${False}
            DataHandler.Colored Log    This product is on offer!    level=DEBUG
            MySQLConnector.Database Log    Total Value: ${prod_total}    level=INFO
        ELSE
            DataHandler.Colored Log    Total Value: ${prod_total}    level=WARN
        END
        Builtin.Log To Console    Grid Product: ${grid_product}${\n}
        ${current_sale_value}    Calculator.Addition Operation    ${current_sale_value}    ${prod_total}
        ${items_on_sale}    Calculator.Addition Operation    ${items_on_sale}    ${prod_quantity}
        DataHandler.Show Table Message    ${current_sale_value}    ${items_on_sale}
    END
# =========================================================================================================//

Replace The Pricing Table IF Necessary
    [Documentation]    
    ...    This keyword is the function that controls the replacement of pricing tables. The
    ...    default value for    PRICING_TABLE_LIMIT    is R$100 Brazilian Cash. Whenever, if the final value
    ...    of    the sale exceeds R$100, the list price is replaced    by the second option. In this case it
    ...    is price_Tn -> any other table set up int the internal data structure!

    IF    ${REPLACE_PRICING_TABLE} == ${True}
        TRY
            ${sum_prices}    Calculator.Get The Current Sale Value
            IF    ${sum_prices} > ${PRICING_TABLE_LIMIT}
                DataHandler.Colored Log
                ...    mssg=${\n}THE FINAL VALUE OF THE SALE EXCEEDED THE MAXIMUM VALUE FOR LIST NUMBER 1.
                ...    level=INFO
                DataHandler.Colored Log
                ...    mssg=As a result of this, there was an exchange of price lists :: 1 -> VAREJO 3
                ...    level=NULL
                ${new_prod_prices}    DataHandler.Replace Product Properties
                ...    replace=${True}
                ...    price_Tn=${PRICING_LIST_NAME}
                ...    check_customer=${CHECK_CUSTOMER_RECORD}
            END
        EXCEPT
            Builtin.Log To Console    ${EMPTY}
        END
    ELSE
        DataHandler.Colored Log
        ...    mssg=${\n}PRICE LIST REPLACEMENT UNAVAILABLE FOR THIS TEST CASE!${\n}
        ...    level=INFO
    END

# =========================================================================================================//
Get Payment Way
    [Documentation]
    ...    It Returns the first true payment clause assigned on Config.yaml file.
    IF    ${pay_cashback} == ${True}    
        RETURN    DIN
    ELSE IF    ${pay_check} == ${True}   
        RETURN    CHQ
    ELSE IF   ${pay_customer_credit} == ${True}   
        RETURN    CRE
    ELSE IF   ${pay_credit_card} == ${True}
        RETURN    ${type_card}
    ELSE IF    ${pay_eletronic_transf} == ${True}
        RETURN    BNC
    END

# =========================================================================================================//
Single Sale Event
    ${payment}    Get Payment Way
    # Available Payment types:
    # DIN, CHQ, CRT, CRE, PIX, BNC, VLE, TEF
    DataHandler.Colored Log    
        ...    mssg=${\n}${\n}PERFORMING TEST CASE `${payment}`...    level=INFO
    
    IF    ${use_product_grouping} == ${True}
        Product Grouping For Sale
    ELSE IF    ${product_sequence} == ${True}
        Enter A Custom Sequence of Products
    ELSE
        Forward The Products For Sale
    END
    ${key_letter}    DataHandler.Set Payment Way    paymnt_way=${payment}
    DataHandler.Store The Customer Code Or CPF/CNPJ    code_id=${1}    cpf_cnpj=SET
    DataHandler.Replace Products On Offer
    DataHandler.Replace Products On Promotion
    Replace The Pricing Table IF Necessary
    Calculator.Calculate The Final Sale Value    compute_difference=${use_difference}
    Builtin.Log To Console    ${\n}Payment Shortcut Key: ${key_letter}
    # Cumpute the amount between the final sale value and its difference returned
    # for the <def> Set_And_Calc_Difference... ->: tuple from <library> Calculator.py
    IF    ${use_difference} == ${True}
        ${qnt}    Calculator.Get Values From Cashierr    cashback=${True}
        ${diff}    Calculator.Get Difference Has Computed From Final Sale Value    dff=${True}
        IF    ${qnt} > ${diff}
            ${value}    Calculator.Get Difference Has Computed From Final Sale Value
            Builtin.Log To Console    Computed Difference: ${value}
        END
    END
    # SALE'S BREAKDOWN ::
    Calculator.Cashier Controller
    ...    keep_on_cashier=${True}    add_to_total=${True}    cashback=${True}
    Calculator.Sales Counter    add=${True}
    Calculator.Cashier Breakdown
    Calculator.Clear Temporary Sale Modifiers
    DataHandler.Clear Temporary Sale Properties
# =========================================================================================================//