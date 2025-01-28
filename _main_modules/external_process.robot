*** Settings ***
Resource        database.robot
Resource        ../_structures/base.robot
Resource        ../_main_modules/external_process.robot

#=======================================================================================================================//
*** Keywords ***
Accept The Cashiers Transference From PDV
    database.Set Data Inserts To Database    accpt_sangria=${True}
    #Open MyCommerce System
    #Check For Startup System Images    wait_time=${5}
    #base.Please Wait a Moment         ${default_time}
    #Accept Credit To The Cashier Amount

#=======================================================================================================================//
Open MyCommerce System
    ImageHorizonLibrary.Press Combination            KEY.WIN     KEY.R
    base.Please Wait a Moment        ${default_time / 4}
    SikuliLibrary.Input Text         ${EMPTY}    C:\\Visual Software\\MyCommerce\\myCommerce.exe
    SikuliLibrary.Press Special Key    ENTER
    SikuliLibrary.Wait Until Screen Contain    ${MYC_LOGIN}    ${10}
    SikuliLibrary.Double Click In    ${MYC_LOGIN}    ${MYC_LOGIN_BUTTON}
    base.Please Wait a Moment        ${default_time}
    SikuliLibrary.Input Text         ${EMPTY}    ${company_code}
    base.Please Wait a Moment        ${default_time / 2}
    SikuliLibrary.Press Special Key    TAB
    base.Please Wait a Moment        ${default_time / 2}
    SikuliLibrary.Input Text         ${EMPTY}    ${MYC_USER_ID}
    base.Please Wait a Moment        ${default_time / 2}
    SikuliLibrary.Press Special Key    TAB
    ${var}    Exists    ${MYC_INVALID_LOGIN}    ${1}
    IF    ${var} == ${True}
        SikuliLibrary.Press Special Key    ENTER
        base.Please Wait a Moment     ${1}
        SikuliLibrary.Press Special Key    UP
        base.Please Wait a Moment     ${default_time / 2}
    END
    SikuliLibrary.Input Text          ${EMPTY}    ${MYC_USER_PASSWORD}                
    base.Please Wait a Moment         ${0.3}
    SikuliLibrary.Press Special Key    TAB
    base.Please Wait a Moment         ${0.3}
    SikuliLibrary.Press Special Key    ENTER
    SikuliLibrary.Wait Until Screen Not Contain    ${MYC_LOGIN}    ${75}
    TRY
        SikuliLibrary.Wait For Image    ${MYC_TERMINAL_LIB}    ${MYC_INITIAL_LAYOUT}    ${3}
        SikuliLibrary.Click In    ${MYC_TERMINAL_LIB}    ${MYC_LIB_BTTN}
        Builtin.Log    ...    level=WARN
        DataHandler.Colored Log    mssg=${\n}The System Liberation Image has appeared on screen!    level=WARN
    EXCEPT
        DataHandler.Colored Log    mssg=${\n}THE MyComemrce ERP SYSTEM IS OPEN!    level=INFO
        base.Check For Company Liberation Satus
    END
    
#=======================================================================================================================//
Check For Startup System Images
    [Arguments]     ${wait_time}=${3}
    base.Please Wait a Moment    ${wait_time}
    ${var1}    SikuliLibrary.Exists    ${MYC_SYS_BACKUP}       ${default_time}
    ${var2}    SikuliLibrary.Exists    ${MYC_SCHEDULE}         ${default_time}
    ${var3}    SikuliLibrary.Exists    ${MYC_COMPANY_OFFER}    ${default_time}
    
    # STATEMENTS:
    IF    ${var1} == ${True}
        SikuliLIbrary.Click    ${MYC_SCHEDULE}
        base.Please Wait a Moment    ${0.3}
        ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.F
        
    ELSE IF    ${var2} == ${True}
        ${var3}    Set Variable    ${False}
        SikuliLIbrary.Click    ${MYC_SCHEDULE}
        base.Please Wait a Moment                ${0.3}
        ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.F

    ELSE IF    ${var3} == ${True}
        SikuliLIbrary.Click In    ${MYC_COMPANY_OFFER}    ${MYC_CLOSED_BUTTON}
    ELSE
        RETURN
    END

#=======================================================================================================================//
Accept Credit To The Cashier Amount
    TRY
        Screen Should Not Contain       ${MYC_SCHEDULE}
    EXCEPT     
        Check For Startup System Images    wait_time=${4}
    ELSE
        SikuliLibrary.Press Special Key             ESC
        base.Please Wait a Moment                   ${default_time}
        SikuliLibrary.Press Special Key             F12
        Check For MyCommerce Cashier
        base.Please Wait a Moment                   ${alert_image_time}
        ImageHorizonLibrary.Press Combination       KEY.ALT    KEY.T
        SikuliLibrary.Wait Until Screen Contain     ${MYC_CASHIER_IMG}    ${ALERT_IMAGE_TIME}
        base.Please Wait a Moment                   ${ALERT_IMAGE_TIME}
        SikuliLIbrary.Click In                      ${MYC_CASHIER_IMG}    ${MYC_SANGRIA_BTTN}
        base.Please Wait a Moment                   ${ALERT_IMAGE_TIME}
        SikuliLibrary.Press Special Key             ENTER
        base.Please Wait a Moment                   ${DEFAULT_TIME / 2}
        ImageHorizonLibrary.Press Combination       KEY.ALT    KEY.S
        base.Please Wait a Moment                   ${DEFAULT_TIME / 2}
        ImageHorizonLibrary.Press Combination       KEY.ALT    KEY.F4
        base.Please Wait a Moment                   ${alert_image_time}    
        ImageHorizonLibrary.Press Combination       KEY.ALT    KEY.N
        base.Please Wait a Moment                   ${default_time}
        SikuliLibrary.Screen Should Contain         ${SALE_LAYOUT_PDV}
        SikuliLIbrary.Click                         ${PDV_ICON}
    END

#=======================================================================================================================//
Check For MyCommerce Cashier
    TRY
        base.Please Wait a Moment    ${3}
        SikuliLibrary.Screen Should Not Contain    ${MYC_CASHIER_CLOSED}
    EXCEPT
        SikuliLibrary.Press Special Key    ENTER
        SikuliLibrary.Wait Until Screen Contain    ${MYC_OPEN_CASHIER}    ${5}
        SikuliLibrary.Click In       ${MYC_OPEN_CASHIER}    ${MYC_UP_SEARCH_BAR}
        base.Please Wait a Moment    ${0.3}
        SikuliLIbrary.Input Text     ${EMPTY}    ${myc_cashier_name}
        base.Please Wait a Moment    ${0.5}
        SikuliLibrary.Press Special Key          ENTER
        base.Please Wait a Moment    ${0.5}
        ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.E
        base.Please Wait a Moment    ${alert_image_time}
        ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.C
        base.Please Wait a Moment    ${5}
        SikuliLibrary.Click In       ${MYC_CSHR_DOWNGRID}    ${MYC_DOWNGRID_BUTTON}
        base.Please Wait a Moment    ${default_time}
        #ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.F4
        Builtin.Log To Console    ${\n}
        Builtin.Log    ...           level=WARN
        Builtin.Log To Console    ${\n}Searching for available Transferences...
        #Builtin.Log To Console       ${\n}Like the System's Cashier was closed it's necessay reopen the system!
        #base.Please Wait a Moment    ${default_time}
        #Reopen The MyCommerce System
        SikuliLibrary.Press Special Key    F12
    ELSE
        RETURN
    END

#=======================================================================================================================//
Reopen The MyCommerce System
    ImageHorizonLibrary.Press Combination      KEY.WIN     KEY.R
    base.Please Wait a Moment         ${default_time / 4}
    SikuliLibrary.Input Text     ${EMPTY}      C:\\Visual Software\\MyCommerce\\myCommerce.exe
    SikuliLibrary.Press Special Key            ENTER
    SikuliLibrary.Wait Until Screen Contain    ${MYC_LOGIN}    ${10}
    SikuliLibrary.Double Click In    ${MYC_LOGIN}    ${MYC_LOGIN_BUTTON}
    base.Please Wait a Moment        ${default_time}
    SikuliLibrary.Input Text         ${EMPTY}    ${company_code}
    base.Please Wait a Moment        ${default_time / 2}
    SikuliLibrary.Press Special Key            TAB
    base.Please Wait a Moment         ${default_time / 2}
    SikuliLibrary.Input Text          ${EMPTY}    ${MYC_USER_ID}
    base.Please Wait a Moment         ${default_time / 2}
    SikuliLibrary.Press Special Key            TAB
    base.Please Wait a Moment         ${0.3}
    SikuliLibrary.Press Special Key            ENTER
    SikuliLibrary.Wait Until Screen Not Contain    ${MYC_LOGIN}    ${60}
    Check For Startup System Images

#====================================================================================================================END//