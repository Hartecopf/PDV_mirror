*** Settings ***
Resource    ../_structures/base.robot
# ================================================================================================================================//

*** Keywords ***

Check Results Aigainst FireBird Localhost
    [Arguments]    ${query_type}=table name
    MySQLConnector.Get Firebird Query Results    ${False}    table=${query_type}

Check Results Aigainst ERP Database
    [Arguments]
    ...    ${query_type}=table name
    ...    ${anim}=${True}

    # INNER CONTROL FOR QUERIES LOOP!
    ${internal_counter}    Builtin.Set Variable    ${1}
    IF    ${anim} == ${True}
        Connection Console Animation
        MySQLConnector.Show Connection
    ELSE
        Retisences
    END    #\\ END IF/ELSE

    ${var_ok}    MySQLConnector.Get Query Results    table=${query_type}
    IF    ${var_ok} == ${False}
        WHILE    ${internal_counter} < ${10}
            ${internal_counter}    Calculator.Addition Operation    ${internal_counter}    ${1}
            MySQLConnector.Database Log
            ...    mssg=${\n}⏳ Waiting for Data Synchronization... ${internal_counter - 1}/10
            ...    level=INFO
            base.Please Wait a Moment    ${0.25}
            Timer Five Seconds
            Builtin.Log    ${\n}    console=True
            base.Please Wait a Moment    ${0.25}
            ${var_ok}    MySQLConnector.Get Query Results    table=${query_type}
            
            IF    ${var_ok} == ${True}
                BREAK
            ELSE IF    ${internal_counter} >= ${10}
                MySQLConnector.Allowed Loop Time Has Been Exceeded
                MySQLConnector.Database Record Incomplete
                BREAK
            END    #\\ END IF/ELSE IF
        END    #\\ END WHILE
    END    #\\ END IF


Connection Console Animation
    MySQLConnector.Database Log    mssg=${\n}${\n}Establishing conection...    level=INFO
    base.Please Wait a Moment    ${0.25}
    FOR    ${counter}    IN RANGE    ${0}    ${25}
        base.Please Wait a Moment    ${0.025}
        Builtin.Log To Console    ▮    no_newline=True
    END    #\\ END FOR
    MySQLConnector.Database Log    mssg=${\n}${\n}Querying Database...    level=INFO
    base.Please Wait a Moment    ${0.25}
    FOR    ${counter}    IN RANGE    ${0}    ${39}
        base.Please Wait a Moment    ${0.077}
        Builtin.Log To Console    ▮    no_newline=True
    END    #\\ END FOR


Retisences
    FOR    ${counter}    IN RANGE    ${0}    ${3}
        base.Please Wait a Moment    ${0.25}
        Builtin.Log To Console    •    no_newline=True
    END    #\\ END FOR
    RETURN


Timer Five Seconds
    FOR    ${counter}    IN RANGE    ${0}    ${10}
        base.Please Wait a Moment    ${0.50}
        Builtin.Log To Console    •      no_newline=True
    END    #\\ END FOR
    RETURN


Timer Custom Seconds
    [Arguments]    ${delimiter}=${10}    ${message}=None
    IF    '${message}' != 'None'
    ...    MySQLConnector.Database Log    ${\n}${\n}${message}    level=INFO
    FOR    ${counter}    IN RANGE    ${0}    ${delimiter}
        base.Please Wait a Moment    ${0.50}
        Builtin.Log To Console    ◼      no_newline=True
    END    #\\ END FOR
    RETURN


Set Data Inserts To Database
    [Arguments]   
    ...    ${accpt_sangria}=${False}
    ...    ${create_custom_user}=${False}
    ...    ${create_custom_prod}=${False}
    ...    ${create_custom_promotion}=${False}
    ...    ${create_custom_offers}=${False}
    ...    ${adjust_payment_way}=${False}
    
    MySQLConnector.Set Query Inserts    accept_sangria=${accpt_sangria}
    RETURN