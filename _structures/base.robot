*** Settings ***
Documentation       This is a test case's base script to MyCommercePDV System and its Automation Test Cases.
...                 This structure    works    as    an    aggregator of all components and import files used during the execution
...                 of test cases. This script is the driving force for the execution of the test cases and is responsible
...                 for applying each component according to the need for executing the test cases.
...
...                 This structure works as an aggregator    of all components and import files used during the execution of
...                 test cases.    This    script    is the driving force for the execution of the test cases and is responsible
...                 for applying each component according to the need for executing the test cases.

# =========================================================================================================//
Library             Process
Library             DateTime
Library             Collections
Library             FakerLibrary
Library             OperatingSystem
Library             ImageHorizonLibrary
Library             SikuliLibrary    mode=NEW
Library             ../_custom_libraries/DataHandler.py
Library             ../_custom_libraries/MySQLConnector.py
Library             ../_custom_libraries/Calculator.py
Library             ../_custom_libraries/ExternalPrograms.py
Variables           ../_custom_libraries/input/Config_Bkp.yaml
Resource            variables.robot
Resource            ../_main_modules/cashier_controller.robot
Resource            ../_main_modules/cancel_sale.robot
Resource            ../_main_modules/external_process.robot
# =========================================================================================================//

*** Keywords ***
Load Data Libraries
    [Documentation]    This keyword is the first process to be runned. Your job is
    ...    to add all components and variables from the local directory    to this
    ...    test case and so start the subsequent instructions.

    DataHandler.Load Storage Path
    Console Animation For Synchronization Time
    ...    ${32}    pollingInterval=${0.05}    msge=🔠 Checking for Project Settings...
    DataHandler.Check For The Project Settings Integrity
    DataHandler.Colored Log    ${\n}🔄 Wait for the loading to finishing...    level=INFO2
    Builtin.Import Variables    ${EXECDIR}/../_custom_libraries/input/Config_Bkp.yaml
    Please Wait a Moment    ${0.3}
    MySQLConnector.Show FireBird Connection Status
    IF    ${data_recovery} == ${False} 
        DataHandler.Colored Log    ${\n}💬 Loading Keyboard Instruction...    level=INFO
        DataHandler.Load Keyboard Instruction
        DataHandler.Colored Log    ${\n}🔧 Loading PDV System Settings...    level=INFO
        DataHandler.Load PDV System Settings
    END
    DataHandler.Colored Log    ${\n}📥 Recording Project Folder...    level=INFO
    Please Wait a Moment    ${0.3}
    OperatingSystem.Directory Should Exist    path=../resources/elements
    OperatingSystem.Count Files In Directory    path=../resources/elements
    SikuliLIbrary.Add Image Path    path=../resources/elements
    DataHandler.Colored Log    ${\n}📡 Creating a MySQL Conenction...    level=INFO
    Please Wait a Moment    ${0.5}
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
    DataHandler.Console Line     
    ...    space=${59} 
    ...    char==
    ...    cmd=return
    ...    title=${True}
    ...    msg=PDV SYSTEM INFO
    ExternalPrograms.PDV Info
    DataHandler.Console Line     
    ...    space=${59}
    ...    char==
    ...    break_line=${True}
    ...    to_the_end=${True}
    ...    cmd=return
    
    IF    ${DATA_DEBUG} == ${True}    End Test


Check If The System Has Already Been Started
    [Documentation]
    ...    This Keyword will check out if the login screen will appears. If True, it
    ...    will does not execute this next stantement structure.

    TRY
        SikuliLibrary.Screen Should Contain    ${SALE_LAYOUT_PDV}
        SikuliLIbrary.Click    ${PDV_ICON}
        # That Master Keyword from <base.robot> also check for possibles uncompleted cashier events
        # as also as cashier 'sangria' or cashiers transference...
        database.Check Results Aigainst ERP Database    sangria_incomp    anim=${False}
        # If there's an uncompleted cashier event type sangria the Calculator's respective @keywords
        # will do a cashier adjustment according to the cashier's amount found on erp database. 
        ${var}    Calculator.Check For Uncompleted Cashiers Event Type Sangria
        IF    ${var} != ${0}    cashier_controller.Cancel Cashier Event Type Sangria
        Calculator.Check For The Cashier Events Type Sangria
        RETURN    ${True}
    EXCEPT
        Fatal Error Triggered
        RETURN    ${False}
    END


Open System
    [Arguments]    ${cmmd}=C:\\Visual Software\\MyCommerce\\PDV\\MyCommercePDV.exe
    ImageHorizonLibrary.Press Combination    KEY.WIN    KEY.R
    Please Wait a Moment    ${DEFAULT_TIME / 4}
    SikuliLibrary.Input Text    ${EMPTY}    ${cmmd}
    SikuliLibrary.Press Special Key    ENTER


Check For Login Screen
    TRY
        SikuliLibrary.Wait For Image    
        ...    ${LOGIN_SCREEN}    ${EMPTY}    ${startup_time}
        RETURN    ${True}
    EXCEPT
        Builtin.Log    ...    level=Error
        DataHandler.Colored Log
        ...    ${\n}The time out was happenend and the system it did'nt start!${\n}
        ...    level=ERROR
        RETURN    ${False}
    END


User Login
    [Documentation]    Login Process: Into the User's data automatically
    SikuliLibrary.Screen Should Contain    ${LOGIN_SCREEN}
    SikuliLibrary.Input Text    ${EMPTY}    ${PDV_USER_ID}
    SikuliLibrary.Press Special Key    TAB
    SikuliLIbrary.Input Text    ${EMPTY}    ${PDV_USER_PASSWORD}
    SikuliLibrary.Press Special Key    ENTER
    Builtin.Log To Console    ${\n}These next data were entered in the system login
    Builtin.Log To Console    User: ${PDV_USER_ID} Password: ${PDV_USER_PASSWORD}${\n}


Check The Terminal Liberation Status
    [Documentation]    Run the System Terminal Liberation when existly.
    ${existis_image}    SikuliLibrary.Exists    ${PC_LIBERATION}    ${ALERT_IMAGE_TIME}
    IF    ${existis_image} != ${False}
        SikuliLibrary.Press Special Key    ENTER
        SikuliLibrary.Wait Until Screen Contain    ${CONFIRM_LIBERATION}    ${DEFAULT_TIME * 5}
        SikuliLibrary.Capture Screen
        Builtin.Log    ...    level=WARN
        DataHandler.Colored Log
        ...    mssg=${\n}An Alert Message Box about system liberation was triggered on the screen!${\n}
        ...    level=WARN
        SikuliLibrary.Press Special Key    ENTER
    ELSE
        DataHandler.Colored Log    mssg=${\n}Machine MAC released for system use!${\n}    level=INFO
    END


Check For Company Liberation Satus
    ${existis_image}    SikuliLibrary.Exists    ${COMPANY_LIBERATION}    ${ALERT_IMAGE_TIME}
    IF    ${existis_image} == ${True}
        Builtin.Log    ${\n}The PDV System has not been released for use!    level=ERROR
        DataHandler.Colored Log    mssg=${\n}Check system settings in the SIA.${\n}    level=ERROR
        Builtin.Log To Console    ${EMPTY}
        SikuliLibrary.Input Text    ${EMPTY}    ${ACCESS_CODE}
        ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.G
        Please Wait a Moment    ${0.5}
        SikuliLibrary.Press Special Key    ENTER
    ELSE
        RETURN
    END


Check The Library Error
    [Documentation]    Condition structure that verifier if there are error images on the screen:
    ${wanted_images}    Builtin.Create List    ${LIB_ALERT}    ${LIB_ALERT_2}    ${DLL_ERROR}
    ${not_wanted_for_this_case}    Builtin.Create List    ${LOGIN_SCREEN}    ${SALE_LAYOUT_PDV}
    TRY
        SikuliLibrary.Wait For Multiple Images
        ...    ${DEFAULT_TIME * 5}    ${1}
        ...    ${wanted_images}    ${not_wanted_for_this_case}
    EXCEPT
        Builtin.Log To Console    The Library Compatibility DLL Status OK!
    ELSE
        Builtin.Log    ...    level=ERROR
        DataHandler.Colored Log
        ...    mssg=${\n}An alert message about Local Libraries was triggered on screen.
        ...    level=ERROR
        DataHandler.Colored Log    mssg=The Library compatibility or the dlls is not OK!    level=ERROR
        DataHandler.Colored Log    mssg=Check the description on the screenshots.${\n}    level=WARN
        SikuliLibrary.Capture Screen
        Fatal Error Triggered
    END


Check The System Automation Error
    [Documentation]    Condition structure that verifiers if there are error images on the screen:
    ${exists_auto_error}    SikuliLibrary.Exists    ${AUTOMATION_ERROR}    ${ALERT_IMAGE_TIME}
    IF    ${exists_auto_error} != ${False}
        Builtin.Log    ...    level=ERROR
        DataHandler.Colored Log
        ...    mssg=${\n}Message Box of the 'Automation Error' appeared on screen!
        ...    level=ERROR
        DataHandler.Colored Log
        ...    mssg=Because of this inconsistence this test case was finalized!${\n}
        ...    level=WARN
        SikuliLibrary.Capture Screen
        SikuliLibrary.Press Special Key    ENTER
        End Test
    ELSE
        Builtin.Log To Console    Automation System Process OK!
    END


Check The System Class Status
    ${existis_image}    SikuliLibrary.Exists    ${CLASS_NOT_SUPPORTED}    ${ALERT_IMAGE_TIME}
    IF    ${existis_image} != ${False}
        SikuliLibrary.Capture Screen
        SikuliLibrary.Press Special Key    ENTER
        Builtin.Log    ...    level=WARN
        DataHandler.Colored Log
        ...    mssg=${\n}One Alert Message Box about system's class was triggered on the screen!${\n}
        ...    level=WARN
        Fatal Error Triggered
    ELSE
        Builtin.Log To Console    System Classes are correct and available for use!
    END


Check If The System Already Can Used To Execute One Sale
    [Documentation]
    ...    This Keyword will check if the login screen will appears. If True it
    ...    will does not execute this next stantement structure.

    TRY
        SikuliLibrary.Wait For Image    ${SALE_LAYOUT_PDV}    ${EMPTY}    ${5}
    EXCEPT
        Check If Exist NFC's Errors
        Check If Exist CQP Alert Messages
        RETURN
    END


Check If Exist NFC's Errors
    [Documentation]
    ...    Condition structure that verifiers if there are error images of Fiscal Document on the screen:
    ${list_nfc_erros}    Builtin.Create List
    ...    ${NFC_e_STATUS_ALERT}    ${NFC_e_STATUS_ERROR}
    ...    ${CQP_ALERT_MESSAGE}    ${NFC_e_STATUS_SSL}
    ${considers_NFC_ok}    Builtin.Create List
    ...    ${LOGIN_SCREEN}    ${SALE_LAYOUT_PDV}
    TRY
        SikuliLibrary.Wait For Multiple Images
        ...    ${DEFAULT_TIME * 5}    ${1}
        ...    ${list_nfc_erros}    ${considers_NFC_ok}
        Builtin.Log    ...    level=ERROR
        DataHandler.Colored Log    mssg=${\n}The NFC-e Satus is not correct!    level=ERROR
        DataHandler.Colored Log
        ...    mssg=Check the NFC-e settings on the system and runs this test case again!${\n}
        ...    level=WARN
        SikuliLibrary.Capture Screen
        SikuliLibrary.Press Special Key    ENTER
    EXCEPT
        Builtin.Log To Console    NFC-e Status OK!
    END


Check If Exist CQP Alert Messages
    [Documentation]
    ...    Conditional structure that checks for error images on the screen:
    ${list_possible_errors}    Builtin.Create List    ${CQP_ALERT_MESSAGE}    ${EMPTY}
    ${list_system_ok}    Builtin.Create List    ${SALE_LAYOUT_PDV}    ${LAST_SALE_IS_OPEN}
    TRY
        SikuliLibrary.Wait For Multiple Images
        ...    ${DEFAULT_TIME * 5}    ${1}
        ...    ${list_possible_errors}    ${list_system_ok}
        ${confirm}    SikuliLibrary.Exists    ${CQP_ALERT_MESSAGE}    ${ALERT_IMAGE_TIME}
        IF    ${confirm} == ${True}
            Builtin.Log    ...    level=WARN
            DataHandler.Colored Log
            ...    mssg=${\n}An Alert Message Box about CQP has triggered on screen.
            ...    level=ERROR
            DataHandler.Colored Log    mssg=Check the CQP settings on the system!${\n}    level=WARN
            SikuliLibrary.Capture Screen
            SikuliLibrary.Press Special Key    ENTER
        END
    EXCEPT
        Builtin.Log To Console    CQP Settings Status OK!
    END


Check For Cashier Operational Status
    [Documentation]
    ...    This Keyword will verifier if the cashier is open or close during the systems
    ...    initialization. Esta Keyword fará a abertura do caixa com todos os valores = 0;
    ${is_exists}    SikuliLibrary.Exists    ${CASHIER_OPENING}    ${ALERT_IMAGE_TIME}
    IF    ${is_exists} != ${False}
        SikuliLibrary.Press Special Key    NUM1
        SikuliLibrary.Wait Until Screen Contain    ${CONFIRM_OPEN}    ${10}
        SikuliLibrary.Capture Screen
        ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.C
        ${DATETIME_OPEN}    DateTime.Get Current Date    exclude_millis=${True}
        SikuliLibrary.Wait Until Screen Not Contain    ${CONFIRM_OPEN}    ${60}
        Builtin.Log To Console    The cashier has closed and so has opened!
        Builtin.Log To Console    Cashier has been opened at: ${DATETIME_OPEN}
        MySQLConnector.Check For Cashier Open Code
        DataHandler.Reset Cashier Output File
        DataHandler.Load Cashier Contents
    ELSE
        Builtin.Log To Console    The Cashier is open!
    END
    # That Master Keyword from <base.robot> also check for possibles uncompleted cashier events
    # which as cashier 'sangria' or cashiers transference...
    database.Check Results Aigainst ERP Database    sangria_incomp
    ${var}    Calculator.Check For Uncompleted Cashiers Event Type Sangria
    IF    ${var} != ${0}    cashier_controller.Cancel Cashier Event Type Sangria
    Calculator.Check For The Cashier Events Type Sangria

# =========================================================================================================//

Checks If The Last Sale Is Open
    [Documentation]    It Verifiers if the last sale yet is open and clos it.
    TRY
        SikuliLibrary.Wait For Image    ${LAST_SALE_IS_OPEN}    ${SALE_LAYOUT_PDV}    ${DEFAULT_TIME}
        SikuliLibrary.Press Special Key    ENTER
        Please Wait a Moment    ${DEFAULT_TIME / 2}
        SikuliLibrary.Capture Screen
        Builtin.Log    ...    level=WARN
        DataHandler.Colored Log    mssg=${\n}The system found an open sale!    level=WARN
        Builtin.Log To Console    ${EMPTY}
    EXCEPT
        RETURN
    END

# =========================================================================================================//

Enter CPF Code Manually
    [Documentation]    If the CPF code window does not appear on the screen to confirm and insert the customer
    ...    code during launching the product for sale, this window must be opened by pressing the shortcut 'Y'
    ...    during the sale completion.
    
    ${automathic_insertion}    DataHandler.Read System Settings    
    ...    key=NFPAULISTA_HABILITADO    key_type=FUNCTION
    
    IF    ${automathic_insertion} == ${False}
        Please Wait a Moment    ${DEFAULT_TIME / 2}
        ${cpf_nf_key}    DataHandler.Read System Settings    
        ...    key=TECLADO_CPFNF    key_type=KEYBOARD
        ImageHorizonLibrary.Press Combination    
        ...    KEY.ALT    KEY.${cpf_nf_key}
        SikuliLibrary.Wait Until Screen Contain    
        ...    ${CPF_CLIENT_WINDOW}    ${5}
        Check If Exists CPF Modal Box On Sreen
    END

# =========================================================================================================//

Check If Exists CPF Modal Box On Sreen
    [Arguments]    
    ...    ${cnpjCpf_code}=${PATTERN_CLIENT_CPF}
    
    [Documentation]    
    ...    It Runs    the    subsequent    section if the Client's CPF Code window to appear on scrren.
    ...    This keyword captures the customer's CPF code from the customer's internal Dictionary and enter it
    ...    in this windows of the PDV system. The Keyword 'Customer Controller' is a multifunctional resource
    ...    that can be user to get one customer property and with itself, execute a look-up in the dictionary
    ...    searching any    other property    of them. For exemple, from the CPF code, we can find out which 
    ...    name belongs to this code, in addition any other customer property, if exist.

    ${exists}    SikuliLibrary.Exists    ${CPF_CLIENT_WINDOW}    ${DEFAULT_TIME}
    IF    ${exists} != ${False}
        Builtin.Log To Console    Client's CPF Code windows has appeared on screen!

        IF    ${RANDOMIZE_CPF_CODE} == ${True}
            ${cnpjCpf_code}    DataHandler.CPF Code Generator    area_code=${9}
            Builtin.Log To Console    ${cnpjCpf_code} This is the CPF Code generated randomicaly!${\n}
            DataHandler.Store The Customer Code Or CPF/CNPJ    cpf_cnpj=${cnpjCpf_code}    is_random=${True}
            SikuliLibrary.Input Text    ${EMPTY}    ${cnpjCpf_code}
            Please Wait a Moment    ${DEFAULT_TIME / 4}
            SikuliLibrary.Press Special Key    ENTER
        ELSE
            IF    ${use_default_client} == ${True}
                ${cnpjCpf_code}    DataHandler.Customer Controller
                ...    _key=${default_client_code}    
                ...    _find=${True}
                ...    _get=${True}    
                ...    cnpj=${USE_CNPJ_CODE}    
                ...    cpf=${USE_CPF_CODE}

            ELSE IF    ${CUSTOMER_SEQUENCE} == ${True}
                
                # GET AN ESPECIFIC CUSTOMER CODE FROM CUSTORMER CUSTOM SEQUENCE
                ${counter}    DataHandler.Internal Counter
                ...    counter=${1}    type_list=${True}    obj=${CUSTOM_CLIENT_SEQUENCE}

                ${cnpjCpf_code}    DataHandler.Customer Controller
                ...    _key=${CUSTOM_CLIENT_SEQUENCE}[${counter}]    _get=${True}
                ...    _find=${True}    cnpj=${USE_CNPJ_CODE}    cpf=${USE_CPF_CODE}
            ELSE
                # GET THE RANDOM CPF CODE FROM CUSTOMER DICTIONARY
                ${cnpjCpf_code}    DataHandler.Customer Controller
                ...    _get=${False}    randomize_get=${True}
                ...    cnpj=${USE_CNPJ_CODE}    cpf=${USE_CPF_CODE}
            END

            # GET THE PROPERTIES OF THE CUSTOMER'S REGISTRATION WHERE THE
            # ${cpf_code} IS FOUND WITH THEM:
            ${customer_code}    DataHandler.Customer Controller
            ...    _key=${cnpjCpf_code}    _get=${True}
            ...    _find=${True}    _id=${True}

            ${customer_name}    DataHandler.Customer Controller
            ...    _key=${cnpjCpf_code}    _get=${True}
            ...    _find=${True}    name=${True}

            ${customer_discount}    DataHandler.Customer Controller
            ...    _key=${cnpjCpf_code}    _get=${True}
            ...    _find=${True}    custom_discount=${True}

            ${customer_status}    DataHandler.Customer Controller
            ...    _key=${customer_code}    _get=${True}
            ...    _find=${True}    status=${True}

            ${record_type}    DataHandler.Customer Controller
            ...    _key=${customer_code}    _get=${True}
            ...    _find=${True}    record_type=${True}

            DataHandler.Store The Customer Discount    
            ...    ${customer_discount}

            DataHandler.Store The Customer Code Or CPF/CNPJ    
            ...    code_id=${customer_code}    
            ...    cpf_cnpj=${cnpjCpf_code}

            IF    ${USE_CLIENT_SEARCH_WIN} == ${True}
                Use Customer Searching Windows
            ELSE
                SikuliLibrary.Input Text    ${EMPTY}    ${cnpjCpf_code}
            END

            Please Wait a Moment    ${DEFAULT_TIME / 4}
            Builtin.Log To Console    Was entered the code: ${cnpjCpf_code} in the System Box.
            Builtin.Log To Console    Here are the Customers Information:
            Builtin.Log To Console    ${\n}Name: ${customer_name}${\n}Custom Discount: ${customer_discount}
            Builtin.Log To Console    Customer Internal Code: ${customer_code}
            Builtin.Log To Console    This customer subscription is: ${customer_status}
            Builtin.Log To Console    Customer Record Type: ${record_type}${\n}
            Sikulilibrary.Press Special Key    ENTER
        END
        Check If The CPF Code Is An Invalid Serial    ${cnpjCpf_code}
    ELSE
        RETURN
    END

# =========================================================================================================//

Use Customer Searching Windows
    [Documentation]    
    ...    This keyword uses the client search window to find the client to use in the current
    ...    test case. It is important to know that this keyword will only work if it is called 
    ...    after the client properties have been stored by @keyword: "Check if CPF window exists"

    ${client_code}    DataHandler.Get The Customer Identification    code_id=${True}
    ${search_key}    DataHandler.Read System Settings    key=TECLADO_BUSCA    key_type=KEYBOARD
    Sikulilibrary.Press Special Key    ${search_key}
    Please Wait a Moment    ${default_time + 0.5}
    Set Default To Search Bar
    Please Wait a Moment    ${0.5}
    
    #\\... SET UP FOR ARGUMENTS AS FILTER PARAMETERS ::
    Builtin.Log To Console    Using just customers who's "Ativos" as record status
    ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.S
    SikuliLIbrary.Input Text   ${EMPTY}    text=ativos
    Please Wait a Moment    ${0.5}
    
    #\\... GET RECORD TYPE ::
    ${RECD_TYPE}=    DataHandler.Customer Controller
        ...    _key=${client_code}    _get=${True}    
        ...    _find=${True}    record_type=${True}
    
    #\\... METHOD CLAUSES FOR AVAILABLE RECORD TYPES ::
    ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.T
    Please Wait a Moment    ${0.5}
    IF    "${RECD_TYPE}" == "C"
        SikuliLIbrary.Input Text    ${EMPTY}    text=clientes
    
    ELSE IF    "${RECD_TYPE}" == "A"
        SikuliLIbrary.Input Text    ${EMPTY}    text=ambos
    
    ELSE IF    "${RECD_TYPE}" == "F"
        SikuliLIbrary.Input Text    ${EMPTY}    text=todos
    
    ELSE IF    "${RECD_TYPE}" == "T"
        SikuliLIbrary.Input Text    ${EMPTY}    text=todos

    ELSE IF    "${RECD_TYPE}" == "E"
        SikuliLIbrary.Input Text    ${EMPTY}    text=funcionarios

    ELSE IF    "${RECD_TYPE}" == "D"
        SikuliLIbrary.Input Text    ${EMPTY}    text=todos

    ELSE IF    "${RECD_TYPE}" == "V"
        SikuliLIbrary.Input Text    ${EMPTY}    text=vendedores
    
    ELSE IF    "${RECD_TYPE}" == "M"
        SikuliLIbrary.Input Text    ${EMPTY}    text=contatos
    END
    Please Wait a Moment    ${0.5}
    ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.C

    #\\... METHOD CLAUSES FOR AVAILABLE FILTERS ON LOOING FOR ::
    Please Wait a Moment    ${0.5}
    IF    ${FILTER_BY_SOCIAL_NAME} == ${True}
        #\\... THEN ::
        Builtin.Log To Console    Using "Razão Social" as filter argument on Customer Searching Windows
        SikuliLibrary.Input Text    ${EMPTY}    text=razão
        ${argument}    DataHandler.Customer Controller
        ...    _key=${client_code}    _get=${True}    
        ...    _find=${True}    name=${True}
    
    ELSE IF    ${FILTER_BY_CLIENT_CODE} == ${True}
        #\\... THEN ::
        Builtin.Log To Console    Using "Código" as filter argument on Customer Searching Windows
        ${argument}    Builtin.Set Variable    ${client_code}
        SikuliLibrary.Input Text    ${EMPTY}    text=Código

    ELSE IF    ${FILTER_BY_CNPJ_CPF} == ${True}
        #\\... THEN ::
        Builtin.Log To Console    Using "CNPJ/CPF" as filter argument on Customer Searching Windows
        ${argument}    DataHandler.Get The Customer Identification    cpf_cnpj=${True}
        SikuliLibrary.Input Text    ${EMPTY}    text=CNPJ
    END
    #\\... END METHOD

    Please Wait a Moment    ${0.5}
    ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.P
    Please Wait a Moment    ${0.3}
    SikuliLibrary.Input Text    ${EMPTY}    text=${argument}
    Please Wait a Moment    ${DEFAULT_TIME / 2}
    SikuliLibrary.Capture Screen
    ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.E
    RETURN

# =========================================================================================================//

Use Default Data To Client Code
    DataHandler.Store The Customer Code Or CPF/CNPJ    code_id=${1}    cpf_cnpj=SET

# =========================================================================================================//

Get The Customer Data Record
    [Documentation]    It is what sort numbers by random choices to client code.
    IF    ${RAND_CLIENT_CODE_PAYMENT} == ${True}
        ${randomic_client_code}    DataHandler.Customer Controller
        ...    _get=${False}    randomize_get=${True}    _id=${True}

        ${customer_name}    DataHandler.Customer Controller
        ...    _key=${randomic_client_code}    _get=${True}
        ...    _find=${True}    name=${True}

        ${customer_discount}    DataHandler.Customer Controller
        ...    _key=${randomic_client_code}    _get=${True}
        ...    _find=${True}    custom_discount=${True}

        ${customer_status}    DataHandler.Customer Controller
        ...    _key=${randomic_client_code}    _get=${True}
        ...    _find=${True}    status=${True}

        Builtin.Log To Console    ${\n}An new customer code has been chosen for this payment method!
        Builtin.Log To Console    This is the random clinet code has chosen: ${randomic_client_code}
        Builtin.Log To Console    ${\n}Name: ${customer_name}${\n}Custom Discount: ${customer_discount}
        Builtin.Log To Console    This customer subscription is: ${customer_status}${\n}
        RETURN    ${randomic_client_code}
    ELSE
        ${client_code_on_use}    DataHandler.Get The Customer Identification    code_id=${True}
        Builtin.Log To Console    ${client_code_on_use} Customer Code in use!
        RETURN    ${client_code_on_use}
    END

# =========================================================================================================//

Check If The CPF Code Is An Invalid Serial
    [Arguments]    ${refused_cpf_code}
    Please Wait a Moment    ${default_time}
    ${var}    Exists    ${INVALID_CPF_CODE}    ${DEFAULT_TIME}
    IF    ${var} == ${True}
        Builtin.Log    ...    level=ERROR
        DataHandler.Colored Log    mssg=${\n}The CPF Code has informed is not valid!${\n}    level=ERROR
        Please Wait a Moment    ${DEFAULT_TIME / 2}
        SikuliLibrary.Press Special Key    ENTER
        SikuliLibrary.Input Text    ${EMPTY}    ${PATTERN_CLIENT_CPF}
        ${customer_discount}    DataHandler.Customer Controller
        ...    _key=${PATTERN_CLIENT_CODE}    _get=${True}
        ...    _find=${True}    custom_discount=${True}
        DataHandler.Store The Customer Discount    ${customer_discount}
        DataHandler.Store The Customer Code Or CPF/CNPJ
        ...    code_id=${PATTERN_CLIENT_CODE}    cpf_cnpj=${PATTERN_CLIENT_CPF}
        Builtin.Log To Console    ${\n}Because for it the patter client code has been informed to sale!
        Builtin.Log To Console    Standard CPF/CNPJ as begining a valid code: ${PATTERN_CLIENT_CPF}
        Builtin.Log To Console    Refiused Code Generated: ${refused_cpf_code}${\n}
        SikuliLibrary.Press Special Key    ENTER
    ELSE
        RETURN
    END

# =========================================================================================================//

Navigate On The Property Selector Up Bar
    [Documentation]    This keyword was created to select the Product Property chosen by the system tester
    ...    as 'Mode Enabled' for the system checkbox in the top bar of the product property picker.

    Builtin.Run Keyword    Set Default To Search Bar
    ${key}    Builtin.Set Variable    ${False}
    IF    ${FILTER_BY_CODE} == ${True}
        ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.P
        RETURN
    ELSE IF    ${FILTER_BY_BARCODE} == ${True}
        ${max}    Builtin.Set Variable    ${1}
    ELSE IF    ${FILTER_BY_REFE} == ${True}
        ${max}    Builtin.Set Variable    ${2}
    ELSE IF    ${FILTER_BY_DESC} == ${True}
        ${max}    Builtin.Set Variable    ${3}
    END

    FOR    ${counter}    IN RANGE    ${0}    ${max}
        Please Wait a Moment    ${0.3}
        IF    ${key} == ${True}
            SikuliLibrary.Press Special Key    UP
        ELSE
            SikuliLibrary.Press Special Key    DOWN
        END
    END
    ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.P
    RETURN

# ======================================================================================================//

Set Default To Search Bar
    Please Wait a Moment    ${DEFAULT_TIME}
    ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.C
    FOR    ${counter}    IN RANGE    ${0}    ${6}
        SikuliLibrary.Press Special Key    UP
    END

# =========================================================================================================//

Check For Product Grid Selector
    [Arguments]    
    ...    ${qt_grid_prod}=${1}
    
    [Documentation]    
    ...    This keyword verifer if the image of the Product Grid Selector will appear on screen.
    ...    That condition will    make the selection of a grid product in accordance to the options 
    ...    available for this. Its  controll is done by itneral structure of FakerClass.py into 
    ...    'cls.produts' dict. 'self._qtd_grid_prod_on_sale' is a control variable that inform to this 
    ...    Keyword if exists a grid products on salse and than what mus be done. 'qt_grid_prod' notice 
    ...    to this Keyword how much grid products there are in the sale producr's list. For each grid 
    ...    item, it is necesary to press ENTER once more.

    TRY
        Please Wait a Moment    ${ALERT_IMAGE_TIME}
        SikuliLibrary.Screen Should Contain    ${GRID_OF_PRODUCT}
        FOR    ${counter}    IN RANGE    ${0}    ${qt_grid_prod}
            Builtin.Log To Console    The Chosen product is an item of grid!
            Builtin.Log To Console    No specific category was chosen in this case!
            Please Wait a Moment    ${DEFAULT_TIME / 2}
            SikuliLibrary.Press Special Key    ENTER
            Check If Exists CPF Modal Box On Sreen
        END
    EXCEPT
        Builtin.Log To Console    ${\n}
        Builtin.Log    ...    level=ERROR
        DataHandler.Colored Log    mssg=${\n}The Grid Product Image has not appeared on screen!    level=ERROR
        Fail
    END

# =========================================================================================================//

Run This Keyword If The Pricing Table Window To Appears
    [Documentation]    This Keyword cheksfor Pricing Table Window on screen of the PDV layout.

    ${exist}    SikuliLibrary.Exists    ${PRICING_TABLE}    ${DEFAULT_TIME}
    IF    ${exist} != ${False}    SikuliLibrary.Press Special Key    ENTER

# =========================================================================================================//

Force Recalc
    Builtin.Log To Console    ${\n}
    Builtin.Log    ...    level=WARN
    DataHandler.Colored Log    ${\n}Forcing recalc of the final sale value...    level=WARN
    ${value}    Calculator.Get The Final Sale Value After Data Processing
    DataHandler.Colored Log    The final result of the sales value must to ${value}!${\n}    level=WARN
    base.Please Wait a Moment    ${default_time}
    SikuliLibrary.Press Special Key    ESC
    base.Please Wait a Moment    ${alert_image_time}
    # ${subtotal_key}    DataHandler.Read System Settings    key=TECLADO_BUSCA    key_type=KEYBOARD
    SikuliLibrary.Press Special Key    SPACE
    base.Run This Keyword If The Pricing Table Window To Appears

# =========================================================================================================//

Run This Keyword If Discount Release Image To Appears
    [Documentation]    This keyword was created to execute this conditional treatment for Discount
    ...    Liberation Image always when it appears on the screen.

    ${is_exists}    SikuliLibrary.Exists    ${DISCOUNT_LIBERATION}    ${ALERT_IMAGE_TIME}
    IF    ${is_exists} != ${False}
        Please Wait a Moment    ${DEFAULT_TIME / 2}
        SikuliLibrary.Input Text    ${EMPTY}    ${MASTER_PASSWORD}
        SikuliLibrary.Press Special Key    ENTER
        Builtin.Log    ${\n}Discount Release has been solicited to cashier operator!    level=WARN
        Builtin.Log To Console    ${EMPTY}
    END

# =========================================================================================================//

Run This Keyword If Finance Liberation Image To Appears
    [Documentation]    This keyword was created to perform this conditional treatment for Finances
    ...    Liberation Image always when it appears on the screen.
    Please Wait a Moment    ${2.5}
    ${is_exists}    SikuliLibrary.Exists    ${FINANCES_LIBERATION}
    IF    ${is_exists} == ${True}
        Please Wait a Moment    ${DEFAULT_TIME}
        SikuliLibrary.Input Text    ${EMPTY}    ${MASTER_PASSWORD}
        Please Wait a Moment    ${DEFAULT_TIME / 2}
        ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.C
        Builtin.Log    ${\n}    console=${True}
        Builtin.Log    ${\n}Finance Liberation has been solicited to cashier operator!    level=WARN
        Builtin.Log To Console    ${EMPTY}
    END

# =========================================================================================================//

Run This Keyword To Report A Sale Note
    [Documentation]
    ...    This keyword will inform to the process that this operation is being performed by
    ...    Robot Framework Technology. This operation is absolutely recommended.
    ${is_exists}    SikuliLibrary.Exists    ${SALE_OBS}    ${ALERT_IMAGE_TIME}
    IF    ${is_exists} != ${False}
        Please Wait a Moment    ${DEFAULT_TIME / 2}
        SikuliLibrary.Input Text    ${EMPTY}    ${ROBOT_OPERATOR}
        Please Wait a Moment    ${DEFAULT_TIME / 2}
        ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.C
        Builtin.Log To Console    User operator identification has been solicited to cashier operator!
        Builtin.Log To Console    OBS: The user identification is recommended according system default!
    END

# =========================================================================================================//

To Close PDV Cashier
    [Documentation]
    ...    This keyword will close the PDV Cashier. Its execution will make with the system be finalized.
    TRY
        SikuliLibrary.Wait Until Screen Contain    ${SALE_LAYOUT_PDV}    ${DEFAULT_TIME * 5}
        ${menu}    DataHandler.Read System Settings    key=TECLADO_MENU    key_type=KEYBOARD
        SikuliLibrary.Press Special Key    ${menu}
        Please Wait a Moment    ${DEFAULT_TIME / 2}
        SikuliLibrary.Press Special Key    NUM1
        ${tickets}    SikuliLibrary.Exists    ${TICKET_IS_OPEN}    ${default_time}
        # SikuliLibrary.Wait For Image    ${TICKET_IS_OPEN}    ${EMPTY}    ${DEFAULT_TIME * 5}
        IF    ${tickets} == ${True}
            SikuliLibrary.Capture Screen
            SikuliLibrary.Press Special Key    ENTER
        END
        Please Wait a Moment    ${DEFAULT_TIME / 2}
        SikuliLibrary.Capture Screen
        SikuliLibrary.Wait For Image    ${CHECK_CASHIER_VALUES}    ${EMPTY}    ${DEFAULT_TIME * 5}
        SikuliLibrary.Press Special Key    NUM1
        Please Wait a Moment    ${DEFAULT_TIME}
        SikuliLibrary.Press Special Key    NUM1
        Please Wait a Moment    ${DEFAULT_TIME / 2}
        ${duplicatas}    SikuliLibrary.Exists    ${CHECK_CUSTOMER_VALUES}    ${ALERT_IMAGE_TIME}
        IF    ${duplicatas} == ${True}
            FOR    ${counter}    IN RANGE    ${2}
                SikuliLibrary.Press Special Key    NUM1
                Please Wait a Moment    ${DEFAULT_TIME / 5}
            END
        END
        ${DATETIME_CLOSE}    DateTime.Get Current Date    exclude_millis=${True}
        Builtin.Log To Console    The Cashier has been closed at: ${DATETIME_CLOSE}
    EXCEPT
        Builtin.Log To Console    ${\n}
        Builtin.Log    ...    level=ERROR
        DataHandler.Colored Log    mssg=${\n}Was not possible to locke the cashier!${\n}    level=ERROR
        Builtin.Fail
        RETURN
    END

# =========================================================================================================//

Print NFC-e
    [Documentation]    Asks you about to print the NFC-e fiscal document!
    ...    1 for true and 2 for false according the systems argument.
    # CONSIDERS TO ${PRINT_NFC_e} A variables.robot PROPERTY. IT'S CAN BE ONLY TRUE OR FALSE.

    ${print_fiscal_doc}    DataHandler.Read System Settings    key=NFCE_SOLICITAIMPRESSAONFCE    key_type=FUNCTION
    ${use_dav}             DataHandler.Read System Settings    key=OPCOES_IMPRIMEDAV    key_type=FUNCTION
    ${equivalence}         DataHandler.Check For Equivalence    ${use_dav}    ${print_dav}
    ${confirm_btt}         DataHandler.Read System Settings    key=TECLADO_MSG_YES    key_type=KEYBOARD
    IF    ${print_fiscal_doc} == ${True}
        IF    ${equivalence} == ${False}
            TRY
                SikuliLibrary.Wait For Image    ${PRINT_NFC_e}    ${CONFIRM_DAV_PRINT}    ${10}
                SikuliLibrary.Press Special Key    ${confirm_btt}
            EXCEPT
                Builtin.Log To Console    ${\n}
                Builtin.Log    ...    level=ERROR
                DataHandler.Colored Log
                ...    ${\n}THERE WAS A ISSUE WITH THE FISCAL DOCUMENT PRINTING.    level=ERROR
                SikuliLibrary.Capture Screen
                Builtin.Log To Console    ${\n}
                FOR    ${counter}    IN RANGE    ${0}    ${5}
                    Please Wait a Moment    ${DEFAULT_TIME / 2}
                    SikuliLibrary.Press Special Key    ENTER
                END
            END
        ELSE IF    ${equivalence} == ${True}
            SikuliLibrary.Wait For Image    ${CONFIRM_DAV_PRINT}    ${PRINT_NFC_e}    ${10}
            SikuliLibrary.Press Special Key    ${confirm_btt}
        END
    ELSE
        RETURN
    END

# =========================================================================================================//

Looking For Screen Error Images After Sales Finishment
    ${var}    SikuliLibrary.Exists    ${DGT_CERT_NOT_FOUND}
    IF    ${var} == ${True}
        Builtin.Log To Console    ${\n}
        Builtin.Log    ...    level=ERROR
        DataHandler.Colored Log    
        ...    mssg=${\n}DIGITAL CERTIFICATE NOT FOUND! CHECK THE SETTINGS.    
        ...    level=ERROR
        SikuliLibrary.Press Special Key    ENTER
    ELSE
        Builtin.Log To Console    ${\n}
        Builtin.Log    ...    level=ERROR
        DataHandler.Colored Log    
        ...    mssg=${\n}UNPOSSIBLE TO COMPLETE THE OPERATION!${\n}    level=ERROR
        SikuliLibrary.Press Special Key    ENTER
    END

# =========================================================================================================//

Perform The Recursion Event
    [Arguments]    ${probability}=${RECURSION}
    ${result}    DataHandler.Recursion   ${probability}
    RETURN    ${result}

# =========================================================================================================//

Please Wait a Moment
    [Documentation]    Quick pause in system operations.
    [Arguments]    ${time}
    Builtin.Sleep    ${time}

# =========================================================================================================//

Console Animation For Synchronization Time
    [Arguments]    ${anim_time}=${0}    ${pollingInterval}=${0.25}    ${msge}=${\n}Wait For Synchronization...
    MySQLConnector.Database Log    mssg=${\n}${\n}${msge}    level=INFO
    Please Wait a Moment    ${0.25}
    FOR    ${counter}    IN RANGE    ${0}    ${anim_time}
        Please Wait a Moment    ${pollingInterval}
        Builtin.Log To Console    ▮    no_newline=True
    END

# =========================================================================================================//

Cancel Sale Process
    [Documentation]    This test case is used to cancel sale in progress.
    ${cancel_key}    DataHandler.Read System Settings    key=TECLADO_CANCELACUPOM    key_type=KEYBOARD
    SikuliLibrary.Press Special Key    ${cancel_key}
    SikuliLibrary.Wait Until Screen Contain    ${CANCELLING_LAYOUT}    ${ALERT_IMAGE_TIME}
    SikuliLibrary.Input Text    ${EMPTY}    ${MASTER_PASSWORD}
    SikuliLibrary.Capture Screen
    SikuliLibrary.Press Special Key    ENTER
    Calculator.Cashier Controller    keep_on_cashier=${False}    uncomplete_event=${True}

# =========================================================================================================//

Close PDV System
    [Documentation]    Close Apllication and Finalize this test Case
    IF    ${CLOSE_SYSTEM} == ${True}
        SikuliLibrary.Wait Until Screen Contain    ${SALE_LAYOUT_PDV}    ${5}
        SikuliLibrary.Press Special Key    F4
        Please Wait a Moment    ${DEFAULT_TIME / 3}
        SikuliLibrary.Press Special Key    NUM1
    END

# =========================================================================================================//

End Test
    SikuliLibrary.Press Special Key    ESC
    #SikuliLibrary.Close Application    MyCommercePDV
    Builtin.Fatal Error
    SikuliLibrary.Stop Remote Server

# =========================================================================================================//

Fatal Error Triggered
    [Documentation]
    ...    This function will be dispered on the screen always fatal error triggered
    SikuliLibrary.Capture Screen
    Builtin.Log To Console    ${\n}
    Builtin.Log    ...    level=ERROR
    DataHandler.Colored Log    mssg=${\n}A Fatal Error was triggered on the screen    level=ERROR
    DataHandler.Colored Log    mssg=Performative Test Sequence has crashed!${\n}    level=WARN
    Builtin.Fatal Error
    Builtin.Fail    msg=This test case was not finalized correctly!
    End Test

# =========================================================================================================//

Get Test Case Status
    ${status}    Get Master Status
    IF    ${status} == ${False}
        Builtin.Run Keyword    Fatal Error
    ELSE
        Builtin.Run Keyword    Close PDV System
    END

# =========================================================================================================//
