*** Settings ***
Documentation       This script is one adaptation for the PRATES test cases automation
...                 project. It will perform a sales paerson simulator during the sale finalization
...                 trougth Customer Credit that it is the particular payment way of the client.

Resource            ../_structures/base.robot
Resource            ../_structures/variables.robot
Resource            ../_main_modules/cashier_controller.robot
# ====================================================================================================//


*** Keywords ***
Finalize The Sale With Customer Credit
    TRY
        ${key_letter}    DataHandler.Set Payment Way    paymnt_way=CRE
        IF    ${USE_CLIENT_SELECTION} == ${True}
            base.Enter CPF Code Manually
        ELSE
            base.Use Default Data To Client Code
        END
        DataHandler.Replace Products On Offer
        DataHandler.Replace Products On Promotion
        cashier_controller.Calculate The Final Value Of The Current Sale
        Builtin.Log To Console    
        ...    ${\n}Payment: Custommer Credit${\n}Shortcut default: ${key_letter}${\n}
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
        ImageHorizonLibrary.Press Combination    KEY.ALT    ${key_letter}
        Custommer Credit Function
        base.Run This Keyword To Report A Sale Note
        cashier_controller.Price Manager Cashier Controller
        ...    keep_on_cashier=${False}    is_customer_payment=${True}
    EXCEPT
        SikuliLibrary.Capture Screen
        Builtin.Log    ...    level=WARN
        DataHandler.Colored Log
        ...    mssg=${\n}It was not possible to finalize the sale using the Customer Credit!
        ...    level=WARN
        DataHandler.Colored Log    
        ...    mssg=Check for the html log and html report to understand what happened!    
        ...    level=NULL
        DataHandler.Set Master Status    status=${False}
        cancel_sale.Uncompleted Sale Event
        Calculator.Clear Temporary Sale Modifiers
        DataHandler.Clear Temporary Sale Properties
        RETURN    ${False}
    END

# ====================================================================================================//

Custommer Credit Function
    [Documentation]    This keyword is a part of the resolution that perfomr the Customer Credit Payment Wayt.
    ...    Its incumbence is execute the payment process according to necessary steps to do it.
    ${credit_status}    Set Variable    ${None}
    ${client_chosen}    base.Get The Customer Data Record

    IF    ${client_chosen} != ${1}    # -> Default Client Code type: 'C'
        ${credit_status}    DataHandler.Customer Controller
        ...    _key=${client_chosen}    _get=${True}
        ...    _find=${True}    is_blocked=${True}
    END
    SikuliLibrary.Wait Until Screen Contain    ${CUSTOMER_PAYMENT}    ${30}
    SikuliLibrary.Input Text    ${EMPTY}    ${client_chosen}
    base.Please Wait a Moment    ${0.3}
    SikuliLIbrary.Press Special Key    TAB
    # This variable contains the customer credit status. It can be 'is blocked' or 'is free'.
    IF    ${credit_status} == ${True}
        base.Please Wait a Moment    ${default_time}
        SikuliLibrary.Screen Should Contain    ${CUSTOMER_IS_BLOCKED}
        Builtin.Log To Console    ${None}
        Builtin.Log    ...    level=WARN
        DataHandler.Colored Log    
        ...    ${\n}This Customer Credit is blocked on ERP manager system!    
        ...    level=WARN
        base.Please Wait a Moment    ${1}
        SikuliLibrary.Press Special Key    ESC
        customer_credit.Internal Console Animation
        Replace The Customer Code And Sale Properties
        base.Please Wait a Moment    ${1}
        ${cpf_nf_key}    DataHandler.Read System Settings    
        ...    key=TECLADO_CPFNF    key_type=KEYBOARD
        ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.${cpf_nf_key}
        SikuliLibrary.Wait Until Screen Contain    ${CPF_CLIENT_WINDOW}    ${5}
        SikuliLibrary.Input Text    ${EMPTY}    ${pattern_client_cpf}
        base.Please Wait a Moment    ${0.5}
        SikuliLibrary.Press Special Key    ENTER
        base.Please Wait a Moment    ${0.5}
        ${key_letter}    DataHandler.Set Payment Way    paymnt_way=CRE
        ImageHorizonLibrary.Press Combination    KEY.ALT    ${key_letter}
        base.Please Wait a Moment    ${DEFAULT_TIME}
        SikuliLibrary.Input Text    ${EMPTY}    ${PATTERN_CLIENT_CODE}
        base.Please Wait a Moment    ${0.3}
        SikuliLibrary.Press Special Key    TAB
    END
    Check For Customer Code Issues    ${client_chosen}
    base.Run This Keyword If Finance Liberation Image To Appears
    base.Please Wait a Moment    ${DEFAULT_TIME / 2}
    SikuliLibrary.Input Text    ${EMPTY}    ${CREDIT_MONTHS}
    FOR    ${counter}    IN RANGE    ${2}
        base.Please Wait a Moment    ${DEFAULT_TIME / 2}
        SikuliLibrary.Press Special Key    TAB
    END
    SikuliLibrary.Capture Screen
    ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.I
    Pass The CPF To NFC-e On Message Box Confirmation    confirm=${CONFIRM_CUSTOMER_CPF}

# ====================================================================================================//

Check For Customer Code Issues
    [Documentation]    This keyword will verify if the client code that was informed is a valid value or
    ...    not valid value    for this system solution. The zero number is the patter numeric value on list
    ...    of the possibility. It is one interger indexer. Check the 'variables.robot' to more informations.
    [Arguments]    ${code_chosen}=${0}

    ${var}    Identifier What Is The Occurence    ${code_chosen}
    IF    ${var} == ${True}    RETURN
    base.Please Wait a Moment    ${default_time}
    ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.Y
    SikuliLibrary.Wait Until Screen Contain    ${CPF_CLIENT_WINDOW}    ${alert_image_time}
    SikuliLibrary.Input Text    ${EMPTY}    ${pattern_client_code}
    # ------------------------REPLACEMENT--------------------------
    Internal Console Animation
    Replace The Customer Code And Sale Properties
    # ---------------------------------------------------------//END
    SikuliLibrary.Press Special Key    ENTER
    base.Please Wait a Moment    ${DEFAULT_TIME}
    ${key_letter}    DataHandler.Set Payment Way    paymnt_way=CRE
    ImageHorizonLibrary.Press Combination    KEY.ALT    ${key_letter}
    SikuliLibrary.Wait Until Screen Contain    ${CUSTOMER_PAYMENT}    ${30}
    SikuliLibrary.Input Text    ${EMPTY}    ${pattern_client_code}
    base.Please Wait a Moment    ${0.3}
    SikuliLibrary.Press Special Key    TAB
    # ↴ This Keyword is being called again to assegure the success to the customer code in usage.
    ${var}    Identifier What Is The Occurence    ${pattern_client_code}
    IF    ${var} == ${False}
        base.Please Wait a Moment    ${DEFAULT_TIME}
        DataHandler.Colored Log    NO CUSTOMER CODE IN USE LOOKS BE A VALID CLIENT RECORD!    level=ERROR
        DataHandler.Colored Log    THE PRATES PROJECT DO NOT WORK WITH INVALID ELEMENTS OR DATAS.    level=ERROR
        DataHandler.Colored Log    THIS SALE EVENT WILL NOT BE FINHISHED AS Customer Credit Payment Way.${\n}    level=ERROR
        DataHandler.Raise Exception
    END
    base.Please Wait a Moment    ${DEFAULT_TIME / 2}
    Builtin.Log To Console    ${\n}In the second time has been entered the customer code: ${PATTERN_CLIENT_CODE}!
    Builtin.Log To Console    This client code was chosen as Standard Numeric Value in this case!

# ====================================================================================================//

Identifier What Is The Occurence
    [Arguments]    ${client_code}
    base.Please Wait a Moment    ${alert_image_time}
    ${var}    SikuliLibrary.Exists    ${CLIENT_NOT_FOUND}
    ${var_2}    SikuliLibrary.Exists    ${INCOMP_SUBSCRIPTION}
    ${var_3}    SikuliLibrary.Exists    ${INVALID_CLIENT_CODE}
    
    base.Please Wait a Moment    ${0.5}
    IF    ${var} == ${True}
        SikuliLibrary.Capture Screen
        SikuliLibrary.Press Special Key    ENTER
        base.Please Wait a Moment    ${default_time}
        Builtin.Log To Console    ${\n}
        Builtin.Log    ...    level=WARN
        DataHandler.Colored Log    mssg=${\n}The client code ${client_code} has not been found!    level=WARN
        base.Please Wait a Moment    ${default_time}
        SikuliLibrary.Press Special Key    ESC
    ELSE IF    ${var_2} == ${True}
        SikuliLibrary.Capture Screen
        ${keyboard_key}    DataHandler.Read System Settings    key=TECLADO_MSG_NO    key_type=KEYBOARD
        SikuliLibrary.Press Special Key    ${keyboard_key}
        base.Please Wait a Moment    ${default_time}
        Builtin.Log To Console    ${\n}
        Builtin.Log    ...    level=WARN
        DataHandler.Colored Log    
        ...    mssg=${\n}Uncompleted record for this customer code: ${client_code}!    level=WARN
        base.Please Wait a Moment    ${default_time}
        SikuliLibrary.Press Special Key    ESC
        RETURN    ${False}
    ELSE IF    ${var_3} == ${True}
        SikuliLibrary.Capture Screen
        SikuliLibrary.Press Special Key    ENTER
        base.Please Wait a Moment    ${default_time}
        Builtin.Log To Console    ${\n}
        Builtin.Log    ...    level=WARN
        DataHandler.Colored Log    mssg=${\n}Invalid Client Code: ${client_code}!    level=WARN
        base.Please Wait a Moment    ${default_time}
        SikuliLibrary.Press Special Key    ESC
    ELSE
        RETURN    ${True}
    END

# ====================================================================================================//

Pass The CPF To NFC-e On Message Box Confirmation
    [Documentation]    This Keyword will insert the CPF code in the fiscal document NFC-e if
    ...    the confirmation is True.
    [Arguments]    ${confirm}=${True}

    TRY
        SikuliLibrary.Wait For Image    ${CPF_IN_THE_NFC}    ${PRINT_NFC_e}    ${ALERT_IMAGE_TIME}
        IF    ${confirm} == ${True}
            ${keyboard_key}    DataHandler.Read System Settings    key=TECLADO_MSG_YES    key_type=KEYBOARD
            SikuliLibrary.Press Special Key    ${keyboard_key}
            Builtin.Log To Console    The CPF modal window has appeared on screen to confirm the client code.
            Builtin.Log To Console    The CPF code confirmation to NFC-e fiscal document has been acepted!
        ELSE IF    ${confirm} == ${False}
            ${keyboard_key}    DataHandler.Read System Settings    key=TECLADO_MSG_NO    key_type=KEYBOARD
            SikuliLibrary.Press Special Key    ${keyboard_key}
            Builtin.Log To Console    The CPF modal window has appeared on screen to confirm the client conde.
            Builtin.Log To Console    The CPF code confirmation to NFC-e fiscal document has not been acepted!
        ELSE
            Builtin.Log    ${\n}    console=True
            Builtin.Log    ${\n}${confirm} :: It's not a valid argummet for this structure!    level=WARN
            SikuliLibrary.Press Special Key    ESC
        END
    EXCEPT
        Builtin.Log To Console    ${\n}Was not possible to confirm the Client on fiscal document NFC-e!
        Builtin.Log To Console    Check the system settings to verify if the parameter is actived!
    END

# ====================================================================================================//

Replace The Customer Code And Sale Properties
    ${cnpjCpf_code}    DataHandler.Customer Controller
    ...    _key=${pattern_client_code}    _get=${True}
    ...    _find=${True}    cnpj=${USE_CNPJ_CODE}    cpf=${USE_CPF_CODE}

    ${customer_name}    DataHandler.Customer Controller
    ...    _key=${cnpjCpf_code}    _get=${True}
    ...    _find=${True}    name=${True}

    ${customer_discount}    DataHandler.Customer Controller
    ...    _key=${cnpjCpf_code}    _get=${True}
    ...    _find=${True}    custom_discount=${True}

    DataHandler.Store The Customer Discount    ${customer_discount}
    DataHandler.Store The Customer Code Or CPF/CNPJ    code_id=${pattern_client_code}    cpf_cnpj=${cnpjCpf_code}

    Builtin.Log To Console    Was storage the code: ${cnpjCpf_code} in the Data Library
    Builtin.Log To Console    Here are the Customers Information:
    Builtin.Log To Console    ${\n}Name: ${customer_name}${\n}Custom Discount: ${customer_discount}
    Builtin.Log To Console    Customer Internal Code: ${pattern_client_code}${\n}

    Calculator.Restore The Sale Properties
    DataHandler.Replace Products On Offer
    DataHandler.Replace Products On Promotion
    cashier_controller.Calculate The Final Value Of The Current Sale

# ====================================================================================================//

Internal Console Animation
    DataHandler.Colored Log    mssg=${\n}RECALCULATING...    level=WARN
    base.Please Wait a Moment    ${0.25}
    FOR    ${counter}    IN RANGE    ${0}    ${25}
        base.Please Wait a Moment    ${0.025}
        Builtin.Log To Console    ▮    no_newline=True
    END
    Builtin.Log To Console    ${\n}

# =================================================================================================//END
