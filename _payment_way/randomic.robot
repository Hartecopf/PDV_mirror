*** Settings ***
Documentation    This script makes the choice of any payment method, which
...          will be executed for the test case that calls this properties
Resource    ../_structures/base.robot
Resource    ../_structures/variables.robot
Resource    cashback.robot
Resource    chq_payment.robot
Resource    customer_credit.robot
Resource    pix.robot
Resource    credit_card.robot

#==================================================================================//
*** Keywords ***
Makes The Choice Of The Payment Method
    [Documentation]    Once the choice is made, the script of this payment 
    ...    method will be executed.
    [Arguments]    ${randomic_mode}=${False}    ${payment_way}=default
    
    IF    ${payment_way} == DIN
        Log To Console    The sale will be finalized with the cashback payment mmethod!
        cashback.Finalize The Sale With Cashback Payment Way
        RETURN
    ELSE IF    ${payment_way} == CHQ
        Log To Console    The sale will be finalized with the CHQ payment way!
        chq_payment.Finalize The Sale On CHQ Payment Way
        RETURN
    ELSE IF    ${payment_way} == CRE
        Log To Console    The sale will be finalized with the customer credit payment method!
        customer_credit.Finalize The Sale With Customer Credit
        RETURN
    ELSE IF    ${payment_way} == TEF
        Log To Console    The sale will be finalized with the TEF Credit Card payment method!
        credit_card.Credits Card Payment Method Internal Structure
        RETURN
    ELSE IF     ${payment_way} == CRT
        Log To Console    It Yet has not implemented!
        Log To Console    The Cashbach Payment way has selected by default!
        cashback.Finalize The Sale With Cashback Payment Way
        RETURN
    ELSE IF     ${payment_way} == PIX
        Log To Console    It Yet has not implemented!
        Log To Console    The Cashbach Payment way has selected by default!
        cashback.Finalize The Sale With Cashback Payment Way
        RETURN
    ELSE
        Log To Console    ${\n}No valid value has informed to finalize this sale!
        Log To Console    Because of this, the randomic mode has activated for this case!
        ${randomic_mode}    Set Variable    ${True}
    END   

    #=====================================================================================================
    IF        ${randomic_mode} != ${False}
        # Dictionary
        ${payment_methods}    Create Dictionary
        ...    cashback=Finalize The Sale With Cashback Way                                # [0]
        ...    chq_way=Finalize The Sale On CHQ Payment Way                                # [1]
        ...    customer_credit=Finalize The Sale With Customer Credit To Client            # [2]
        ...    tef_card=Finalize This Sale Using The Credits Card Payment Method           # [3]
        ...    tranference=Finalize The Sale With Eletronic Transference Payment Way       # [4]
        # List of the dicitionaries value
        ${list_methods}    Create List
        ...    ${payment_methods.cashback}            # [0] 
        ...    ${payment_methods.chq_way}             # [1]
        ...    ${payment_methods.customer_credit}     # [2]  
        ...    ${payment_methods.tef_card}            # [3]
        ...    ${payment_methods.tranference}         # [4]
        # Systematic resolution
        ${list_length}    Calculator.Get Length Base Zero    ${list_methods}
        ${randomic_indexer}    Random Int    min=${0}    max=${list_length}    step=${1}    
        Log To Console    ${list_methods}[${randomic_indexer}] was chosen like the payment mathod used!

        Run Keyword    ${list_methods}[${randomic_indexer}]
        RETURN
    END

#=========================================================================================================