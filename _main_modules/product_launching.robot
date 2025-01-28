*** Settings ***
Documentation       This present structure is an internal module of product seletion for the
...                 sales run. Its code call the product windows on main layout and inserts all the
...                 products previous and available in the LIST_PRODUCTS on 'Variables.robot' script.

Resource            ../_structures/base.robot
Resource            ../_main_modules/cashier_controller.robot
# =======================================================================================================================//


*** Keywords ***
Forward The Product For Sale
    [Tags]    type_selector

    IF    ${use_product_grouping} == ${True}
        Product Grouping For Sale
    ELSE
        IF    ${product_sequence} == ${True}
            Enter A Custom Product Sequence
        ELSE IF    ${choose_prod_in_the_layout} != ${False}
            Use The Layout To Choose Products
        ELSE
            ${search_key}    DataHandler.Read System Settings    key=TECLADO_BUSCA    key_type=KEYBOARD
            Sikulilibrary.Press Special Key    ${search_key}
            base.Navigate On The Property Selector Up Bar
            Use The Product Search Window
        END
    END

# =======================================================================================================================//

Enter A Custom Product Sequence
    [Documentation]    This    Keyword    Perform    the    launching of one custom products sequence. A Custom
    ...    sequence    of    produts    can    be    builded    during the test    case startup also done through the
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
            cashier_controller.Send The Product Price To Cashier Controller Module    ${product_price}
            cashier_controller.Calculate The Current Sale Value Before Their Closing
            SikuliLibrary.Input Text    ${EMPTY}    ${prod_barcode}
            base.Please Wait a Moment    ${default_time/ 2}
            SikuliLibrary.Press Special Key    TAB

            # PRODUCT RECORD INSPECT ::
            base.Please Wait a Moment    ${0.3}
            ${adjust}    Check For An Invalid Product
            IF    ${adjust} == ${True}
                ${current_sale_value}    Calculator.Get The Current Sale Value
                DataHandler.Colored Log    mssg=► THE CURRENT SALE VALUE HAS BEEN ADJUSTED    level=INFO
                MySQLConnector.Database Log    mssg=• Sale Value: ${current_sale_value}    level=WARN
                DataHandler.Colored Log
                ...    mssg============================================================
                ...    level=NULL
                FOR    ${counter}    IN RANGE    ${0}    ${3}
                    base.Please Wait a Moment    ${0.25}
                    Builtin.Log To Console    .    no_newline=True
                END
                Builtin.Log To Console    ${\n}
            END

            IF    ${grid_product} != ${False}
                ${grid_product_on_sale}    Get How Many Grid Product Are Selling
                base.Check For Product Grid Selector    qt_grid_prod=${grid_product_on_sale}
            ELSE
                base.Check If Exists CPF Modal Box On Sreen
            END
        END
    EXCEPT
        Builtin.Log To Console    ${\n}Was not possible to perform the insertion custom product sequence!
        Builtin.Log To Console    There was a problem with the product picker! Check out if the sequence is not empty!
        Builtin.Fatal Error
    END

# =======================================================================================================================//

Use The Product Search Window
    [Documentation]
    ...    This keyword is that runs the loop times to choose    the    product    and    insert it in the search bar.
    ...    When all products is entered on sale, this keyword will send an confirmation to 'cashier_controller
    ...    script confirming the    process finalization. The cashier's movement    is executed so that payment is
    ...    confirmed    for the pament method    has chosen. But for that it happen, an confirmation is necessary.
    ...    Look the subsequent stantement:
    [Arguments]    ${LOOP_TIMES}=${QNT_PROD_FOR_SALE}
    Builtin.Log To Console    The Chosen Products will be inserted through the Product Search Window!
    IF    ${RANDOMIZE_QNT_PRODUCT} == ${True}
        ${LOOP_TIMES}    Random Int    min=${1}    max=${QNT_MAX_PROD_FOR_SALE}    step=${1}
    END
    Builtin.Log To Console    Quantity of Products in this sale: ${LOOP_TIMES}
    Builtin.Log To Console    Here starts the products choice for this sale.
    Builtin.Log To Console    ${EMPTY}
    FOR    ${counter}    IN RANGE    ${0}    ${LOOP_TIMES}
        IF    ${USE_DEFAULT_PRODUCT} == ${False}
            ${prod_property}    DataHandler.Product Controller
            ...    _get=${False}    randomize_get=${True}
            ...    _id=${FILTER_BY_CODE}    barcode=${FILTER_BY_BARCODE}
            ...    reference=${FILTER_BY_REFE}    description=${FILTER_BY_DESC}
        ELSE
            ${prod_property}    Builtin.Set Variable    ${STANDARD_PRODUCT}
        END

        ${product_name}    DataHandler.Product Controller
        ...    _key=${prod_property}    _get=${True}
        ...    _find=${True}    description=${True}

        ${prod_code}    DataHandler.Product Controller
        ...    _key=${prod_property}    _get=${True}
        ...    _find=${True}    _id=${True}

        ${prod_barcode}    DataHandler.Product Controller
        ...    _key=${prod_property}    _get=${True}
        ...    _find=${True}    _id=${True}

        Builtin.Log To Console    ${\n}Prod. Name: ${product_name}
        Builtin.Log To Console    Prod. Code: ${prod_code}
        Builtin.Log To Console    Prod. Barcode: ${prod_barcode}

        ${product_price}    DataHandler.Product Controller
        ...    _key=${prod_property}    _get=${True}
        ...    _find=${True}    price_T1=${True}

        ${grid_product}    DataHandler.Product Controller
        ...    _key=${prod_property}    _get=${True}
        ...    _find=${True}    is_grid=${True}

        Builtin.Log To Console    Grid Product: ${grid_product}
        cashier_controller.Send The Product Price To Cashier Controller Module    ${product_price}
        cashier_controller.Calculate The Current Sale Value Before Their Closing
        base.Please Wait a Moment    ${DEFAULT_TIME}
        SikuliLibrary.Input Text    ${EMPTY}    ${prod_property}
        base.Please Wait a Moment    ${DEFAULT_TIME / 2}
        SikuliLIbrary.Press Special Key    ENTER
        base.Please Wait a Moment    ${DEFAULT_TIME / 2}
        SikuliLIbrary.Press Special Key    INSERT
        base.Please Wait a Moment    ${DEFAULT_TIME / 2}
        SikuliLIbrary.Press Special Key    ENTER
        base.Please Wait a Moment    ${DEFAULT_TIME / 2}
    END
    ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.S
    base.Please Wait a Moment    ${default_time + 0.5}
    SikuliLibrary.Screen Should Not Contain    ${INVALID_PRODUCT}
    ${grid_product_on_sale}    DataHandler.Get How Many Grid Product Are Selling
    base.Check If Exists CPF Modal Box On Sreen
    IF    ${grid_product_on_sale} != ${0}
        base.Check For Product Grid Selector    qt_grid_prod=${grid_product_on_sale}
    END

# =======================================================================================================================//

Use The Layout To Choose Products
    [Documentation]    This structure    execute    the    launching    of produts for sale using the system's
    ...    inital layout and    also the product properties provided as boolean settings to the function
    ...    parameters. In Addition, this keyword has the chacacteristic of using only the barcode as a
    ...    search filter during launch of the chosen product or standard product.
    [Arguments]    ${LOOP_TIMES}=${QNT_PROD_FOR_SALE}

    Builtin.Log To Console    The Chosen Products will be entered through the PDV Initial Layout Screen!
    IF    ${RANDOMIZE_QNT_PRODUCT} == ${True}
        ${LOOP_TIMES}    Random Int    min=${1}    max=${QNT_MAX_PROD_FOR_SALE}    step=${1}
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
        cashier_controller.Send The Product Price To Cashier Controller Module    ${product_price}
        cashier_controller.Calculate The Current Sale Value Before Their Closing
        SikuliLibrary.Input Text    ${EMPTY}    ${prod_barcode}
        base.Please Wait a Moment    ${DEFAULT_TIME / 2}
        SikuliLIbrary.Press Special Key    TAB

        # PRODUCT RECORD INSPECT ::
        base.Please Wait a Moment    ${0.3}
        ${adjust}    Check For An Invalid Product
        IF    ${adjust} == ${True}
            ${current_sale_value}    Calculator.Get The Current Sale Value
            DataHandler.Colored Log    mssg=► THE CURRENT SALE VALUE HAS BEEN ADJUSTED    level=INFO
            MySQLConnector.Database Log    mssg=• Sale Value: ${current_sale_value}    level=WARN
            DataHandler.Colored Log
            ...    mssg============================================================
            ...    level=NULL
            FOR    ${counter}    IN RANGE    ${0}    ${3}
                base.Please Wait a Moment    ${0.25}
                Builtin.Log To Console    .    no_newline=True
            END
            Builtin.Log To Console    ${\n}
        END

        IF    ${grid_product} != ${False}
            base.Check For Product Grid Selector
        ELSE
            base.Check If Exists CPF Modal Box On Sreen
        END
    END

# =======================================================================================================================//

Product Grouping For Sale
    [Documentation]    This keyword is the most recent implementations to the module 'various_product.robot'.
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

            cashier_controller.Send The Product Price To Cashier Controller Module    price_element=${product_price}
            cashier_controller.Calculate The Current Sale Value Before Their Closing    show_logger=${False}
        END
    ELSE
        Builtin.Log To Console    The Chosen Products will be entered through the PDV Initial Layout Screen!
        IF    ${RANDOMIZE_QNT_PRODUCT} == ${True}
            ${LOOP_TIMES}    FakerLibrary.Random Int    min=${1}    max=${QNT_MAX_PROD_FOR_SALE}    step=${1}
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

            cashier_controller.Send The Product Price To Cashier Controller Module    price_element=${product_price}
            cashier_controller.Calculate The Current Sale Value Before Their Closing    show_logger=${False}
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
        base.Please Wait a Moment    ${DEFAULT_TIME / 2}
        ${current_sale_value}    Calculator.Addition Operation    ${current_sale_value}    ${prod_total}
        ${items_on_sale}    Calculator.Addition Operation    ${items_on_sale}    ${prod_quantity}
        DataHandler.Show Table Message    ${current_sale_value}    ${items_on_sale}

        # PRODUCT LAUNCHING ::
        IF    ${prod_quantity} > ${1}
            SikuliLibrary.Input Text    ${EMPTY}    ${prod_quantity}
            base.Please Wait a Moment    ${DEFAULT_TIME / 2}
            ${qnt_key}    DataHandler.Read System Settings    key=TECLADO_QUANTIDADE    key_type=KEYBOARD
            ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.${qnt_key}
            base.Please Wait a Moment    ${DEFAULT_TIME / 2}
            SikuliLibrary.Input Text    ${EMPTY}    ${prod_barcode}
            base.Please Wait a Moment    ${DEFAULT_TIME / 2}
            SikuliLibrary.Press Special Key    TAB
        ELSE
            base.Please Wait a Moment    ${DEFAULT_TIME / 2}
            SikuliLibrary.Input Text    ${EMPTY}    ${prod_barcode}
            SikuliLibrary.Press Special Key    TAB
        END

        # PRODUCT RECORD INSPECT ::
        base.Please Wait a Moment    ${0.3}
        ${adjust}    Check For An Invalid Product
        ...    last=${False}    product_code=${prod_code}    prod_total_value=${prod_total}
        IF    ${adjust} == ${True}
            ${calc}    Calculator.Subtraction Operator    ${current_sale_value}    ${prod_total}
            DataHandler.Colored Log    mssg=► THE CURRENT SALE VALUE HAS BEEN ADJUSTED    level=INFO
            MySQLConnector.Database Log    mssg=• Sale Value: ${calc}    level=WARN
            DataHandler.Colored Log
            ...    mssg============================================================
            ...    level=NULL
            ${current_sale_value}    Builtin.Set Variable    ${calc}
            FOR    ${counter}    IN RANGE    ${0}    ${3}
                base.Please Wait a Moment    ${0.25}
                Builtin.Log To Console    .    no_newline=True
            END
            Builtin.Log To Console    ${\n}${\n}
        END

        # CUSTOMER INSERTING ::
        IF    ${grid_product} != ${False}
            base.Check For Product Grid Selector
            MySQLConnector.Database Log    mssg=-----------------------------------------------------------    level=INFO
        ELSE
            ${cstm}    DataHandler.Read System Settings    key=NFPAULISTA_HABILITADO    key_type=FUNCTION
            IF    ${cstm} == ${True}    base.Check If Exists CPF Modal Box On Sreen
        END
    END

# =====================================================================================================================//

Check For An Invalid Product
    [Documentation]
    ...    This Keyword check if exists any other image else PDV Initial Layout.
    ...    During the products lauching on barcode up bar, it's possible that one
    ...    product informed be an invalid product record. That action will raise
    ...    an unexpected event on system main screen. Assegures the replacemnet of
    ...    this product is the objective from this keyword.
    [Arguments]
    ...    ${last}=${True}
    ...    ${product_code}=${0}
    ...    ${prod_total_value}=${0}

    base.Please Wait a Moment    ${default_time}
    ${var}    Exists    ${INVALID_PRODUCT}
    IF    ${var} == ${True}
        SikuliLibrary.Capture Screen
        DataHandler.Remove Product From Sale    
        ...    last_prod=${last}    code=${product_code}
        FOR    ${counter}    IN RANGE    ${2}
            SikuliLibrary.Press Special Key    ESC
            base.Please Wait a Moment    ${0.35}
        END
        cashier_controller.Adjust The Current Sale Value    
        ...    last_event=${last}    adjustment=${prod_total_value}
        RETURN    ${True}
    ELSE
        RETURN    ${False}
    END

# ==================================================================================================================//END
