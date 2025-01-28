*** Settings ***
Documentation     Performing the sequence of test cases ::
Resource          ../_structures/base.robot
Resource          ../sale_simulator_Din/sale_typeD.robot
Resource          ../sale_simulator_Chq/sale_typeC.robot
Resource          ../sale_simulator_Cre/sale_typeP.robot
Resource          ../sale_simulator_Crd/sale_typeK.robot
Resource          ../sale_simulator_Ban/sale_typeN.robot
Resource          ../sale_simulator_Pix/sale_type_T.robot
Resource          ../_main_modules/cashier_controller.robot
Suite Setup       Run Keyword    Start Sikuli Process
Suite Teardown    SikuliLibrary.Stop Remote Server

#============================================================================================//
*** Test Cases ***
Main Executable
    base.Load Data Libraries
    ${system_ok}    base.Check If The System Has Already Been Started
    IF    ${system_ok} == ${True}
        Perform Test Sequences
    ELSE
        base.Open System
        Startupr Steps
    END
    [Teardown]
    ...    Run Keyword And Warn On Failure    DataHandler.Show Project Relatory
    

#============================================================================================//
*** Keywords ***
Startupr Steps
    [Tags]    seq_testCase
    Check For Startup Issues
    base.User Login
    base.Check If The System Already Can Used To Execute One Sale
    base.Check For Cashier Operational Status
    base.Checks If The Last Sale Is Open
    Perform Test Sequences                                       

#============================================================================================// 
Check For Startup Issues
    [Tags]    first-step  
    [Documentation]    This step in the process will call onpening the system and check out for
    ...     errors during startup. Some  startup issues are worked here in such a way that when
    ...     onse of them apeear on screen, this test case will be finished.
    ${system_ok}    base.Check For Login Screen
    IF    ${system_ok} == ${False}
        Builtin.Log    ...    level=WARN
        DataHandler.Colored Log    
        ...    mssg=${\n}System was not started!${\n}Verifying the possible problems...    
        ...    level=WARN
        DataHandler.Colored Log    mssg=${\n}Initializing debug mode...                                        level=INFO
        SikuliLibrary.Capture Screen
        Find The Problem That Occurred During The System Startup
    ELSE
        RETURN
    END
     
#============================================================================================//
Find The Problem That Occurred During The System Startup
    [Tags]    check_problems
    [Documentation]    This Keyword will be run if the sysem is not started. There
    ...    are many reasons why the system cannot sart. This subsequent structure will
    ...    verify what happened and wich problem appeared on the screen.
    base.Check The Terminal Liberation Status
    base.Check For Company Liberation Satus
    base.Check The Library Error
    base.Check If Exist NFC's Errors
    base.Check The System Automation Error
    base.Check The System Class Status

#============================================================================================//
Perform Test Sequences
    Set Local Variable    ${local_loop_times}    ${0}
    WHILE    ${local_loop_times} < ${repeat_cycle_times}
        Builtin.Run Keyword    sale_typeD.Executes One Sale Type DIN
        Builtin.Run Keyword    sale_typeC.Executes One Sale Type CHQ
        Builtin.Run Keyword    sale_typeP.Executes One Sale Type CRE
        Builtin.Run Keyword    sale_typeK.Executes One Sale Type CRT
        Builtin.Run Keyword    sale_typeN.Executes One Sale Type BNC
        Builtin.Run Keyword    sale_type_T.Executes One Sale Type PIX
        ${local_loop_times}    Calculator.Addition Operation    
        ...    ${local_loop_times}    ${1}
        IF    ${sangria} == ${True}    
        ...    cashier_controller.Execute A Cashier Movement Type Sangria
        Calculator.Show Data Output    ${local_loop_times}
    END

#========================================================================================-End//
    