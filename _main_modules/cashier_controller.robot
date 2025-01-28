*** Settings ***
Documentation       This script has been created for calculating sales made in automated cases.
...                 Runned like a module, it is constantly used to verify the veracity of the values calculated
...                 for the pdv. The value of each product is available in the 'variables.robot' script.

Resource            ../_structures/base.robot
Resource            ../_main_modules/external_process.robot
Resource            database.robot
Library             DateTime
# =========================================================================================================================//


*** Keywords ***
Send The Product Price To Cashier Controller Module
    [Documentation]    This keyword controls the entry of the product's price in the CURRENT_SALE
    ...    _LIST_ variable. This    is used    to    storage in real time all the products inserted in
    ...    the current sale during its execution process. Upon completion of this step, the
    ...    CURRENT_SALE is sent to the PriceManager.py Library to complete its course.
    [Arguments]    ${price_element}=${None}

    Calculator.Add Amount To The Current Sale    ${price_element}

# =========================================================================================================================//

Adjust The Current Sale Value
    [Documentation]    Use this keyword to adjust the current sale value or remove an amount from
    ...    list object of products prices has computed to the sale matching or the cashier closement.
    [Arguments]    ${last_event}=${True}    ${adjustment}=${0}
    Calculator.Remove Amount From Current Sale    last=${last_event}    amount=${adjustment}

# =========================================================================================================================//

Calculate The Current Sale Value Before Their Closing
    [Documentation]    This keyword Calculates the value of the current running sale. All products and their
    ...    prices are calculated in this step, but possible discounts are not yet included in this process.
    ...    This keyword is necessary to control the entry and exit of products into the sale, showing all
    ...    stages    of the process in the syten console.
    [Arguments]    ${show_logger}=${True}

    IF    ${show_logger} == ${True}
        Builtin.Log To Console    -----------------------------------------------------------
        Calculator.Show The Current Sale Value
        Builtin.Log To Console    -----------------------------------------------------------${\n}
    END

# =========================================================================================================================//

Replace The Pricing Table IF Necessary
    [Documentation]    This keyword is the function that controls the replacement of pricing tables. The
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
                # ->    'varejo' is the products property will    be used in the replacement.
                # This    keyword will trow an    Exception if the customer record isn't
                # a valid    signature. The replacement of the price list only be done
                # if    the customer's registration    is in the database and its status
                # be 'ATIVA'.
                ...    check_customer=${CHECK_CUSTOMER_RECORD}

                # When replacing the default price table with another one, it is necessary to apply the new
                # ... updated prices of each product to the items entered for sale ::
            END
        EXCEPT
            Builtin.Log To Console    ${EMPTY}
        END
    ELSE
        DataHandler.Colored Log
        ...    mssg=${\n}PRICE LIST REPLACEMENT UNAVAILABLE FOR THIS TEST CASE!${\n}
        ...    level=INFO
    END

# =========================================================================================================================//

Calculate The Final Value Of The Current Sale
    [Documentation]    This keyword is the first component of the calculator module. Calculating and
    ...    comparing the final value of the sale with the information in the database is the desired
    ...    performance of this structure! Your resolutions are called whenever a product is entered
    ...    into the current sale. Later in this process, this keyword will apply the correponding calculate
    ...    method imported from the PriceManager.py which means that different Keywords Method can be used
    ...    according to the values of the parameters this keyword.
    [Arguments]    ${calc_difference}=${False}
    Replace The Pricing Table IF Necessary
    ${ok}    Calculator.Calculate The Final Sale Value    compute_difference=${calc_difference}
    IF    ${ok} == ${False}
        base.Please Wait a Moment    ${DEFAULT_TIME / 2}
        Builtin.Log To Console    ${\n}
        DataHandler.Colored Log
        ...    mssg=SOME PROGRAMMATIC CONDITION IS BLOCKING THE SALE FINALIZATION!
        ...    level=WARN
        DataHandler.Colored Log
        ...    mssg=LIKELY THIS PAYMENT METHOD HAS BLOCKED THE DISCOUNT PERCENTAGE.
        ...    level=INFO
        DataHandler.Colored Log
        ...    mssg=A DISCOUNT LIBERATION iS NECESSARY IN THIS CASE.${\n}
        ...    level=INFO
        SikuliLIbrary.Screen Should Contain    ${DISCOUNT_LIBERATION}
        base.Run This Keyword If Discount Release Image To Appears
        Calculator.Calculate The Final Sale Value    compute_difference=${calc_difference}
    END

# =========================================================================================================================//

Price Manager Cashier Controller
    [Documentation]    This keyword call the cashier method from the PriceManager Library. This method
    ...    performing the cashier controll in accordance    with the parameters provided to the module.
    ...    This keyword is called only by the payment method scripts and no other. For more information
    ...    look the _main_modules diretory. All payment methods scripts are there. It's important to know
    ...    that this structure is the main method of this keyword. The cashiers controller method in the
    ...    PriceManager Library will only work if this keyword also works correctly.
    [Arguments]
    ...    ${keep_on_cashier}=${False}
    ...    ${add_to_total}=${False}
    ...    ${is_customer_payment}=${False}
    ...    ${is_eletronic_payment}=${False}
    ...    ${cashback}=${False}
    ...    ${chq}=${False}
    ...    ${credit_card}=${False}
    ...    ${pix_pay}=${False}
    ...    ${transference}=${False}

    Calculator.Cashier Controller
    ...    ${keep_on_cashier}
    ...    ${add_to_total}
    ...    ${is_customer_payment}
    ...    ${is_eletronic_payment}
    ...    cashback=${cashback}
    ...    chq_pay=${chq}
    ...    card_pay=${credit_card}
    ...    pix_pay=${pix_pay}
    ...    bank=${transference}

    Calculator.Sales Counter    add=${True}
    Calculator.Cashier Breakdown

# =========================================================================================================================//

Execute A Cashier Movement Type Sangria
    [Documentation]    It Performs an remotion from cashier amount acoording to the settings file.
    ${cashier_value}    Calculator.Get The Values On Cashier    compare_results=${True}
    IF    ${cashier_value} >= ${MINIMUN_NECESSARY}
        ${result}    base.Perform The Recursion Event    probability=${SANGRIA_RECURSION}
        IF    ${result} == ${True}
            Builtin.Log To Console    ${\n}
            Builtin.Log    ...    level=WARN
            DataHandler.Colored Log
            ...    mssg=${\n}An extraction of the cashier amount is being performed...
            ...    level=WARN
            # WHENEVER THE SELECTION TYPE IS 'CHECK', WILL BE NECESSARY TO CONFIRM THE
            # VALUE TO BE EXTRACTED FROM CASHIER AMOUNT ACCORDING TO THE TYPE HAS CHOSEN.
            # IT HASN'T MADE AN ESPECIF SELECTION BY CUSTOMER CODE OR SERIAL CODE FOR CHECK.
            # WHEN THE USER BE USING THE 'CHECK' AS TYPE SELECTION TO THIS EVENT, ALL AMOUNT
            # ON CASHIER AVAILABLE TO THIS PAYMENT METHOD WILL BE TRANFERED TO THE MAIN CASHIER
            # IN THE ERP SYTEM (MyCommerce).

            # EXECUTING THE EVENT...
            SikuliLibrary.Press Special Key    F11
            base.Please Wait a Moment    ${DEFAULT_TIME}
            SikuliLibrary.Press Special Key    NUM6
            SikuliLibrary.Wait Until Screen Contain    ${SANGRIA_WINDOW}    ${ALERT_IMAGE_TIME}
            ${type_event}    Builtin.Set Variable    CASH
            ${amount_to_be_removed}    Set Variable    ${value_extracted}
            base.Please Wait a Moment    ${0.5}
            TRY
                IF    ${CHECK_EVENT} == ${True}
                    SikuliLibrary.Press Special Key    DOWN
                    base.Please Wait a Moment    ${0.5}
                    SikuliLibrary.Press Special Key    ENTER
                    base.Please Wait a Moment    ${default_time}
                    SikuliLibrary.Screen Should Contain    ${CHECK_GRID_FOR_SNG}
                    SikuliLibrary.Press Special Key    ENTER
                    base.Please Wait a Moment    ${0.5}
                    ImageHorizonLibrary.Press Combination    KEY.SHIFT    KEY.TAB
                    ${type_event}    Builtin.Set Variable    CHECK
                    ${amount_to_be_removed}    Calculator.Get Values From Cashierr    check=${True}
                ELSE
                    SikuliLibrary.Press Special Key    TAB
                END
                # Security Clause...
                ${clause}    Calculator.Remotion From Cashier Amount
                ...    ${amount_to_be_removed}    ${type_event}    just_check=${True}
                IF    ${clause} == ${False}
                    DataHandler.Colored Log    mssg=${\n}This Cashiers Event has been cancelled!    level=WARN
                    base.Please Wait a Moment    ${DEFAULT_TIME / 2}
                    SikuliLibrary.Press Special Key    ESC
                    RETURN    # End this process
                END
            EXCEPT
                Builtin.Log To Console    ${\n}
                Builtin.Log    ...    level=ERROR
                DataHandler.Colored Log    mssg=${\n}UNPOSSIBLE TO REALIZE AN EVENT TYPE: 'Sangria'    level=ERROR
                DataHandler.Colored Log    mssg=The execution of the event type didn't works!    level=WARN
                DataHandler.Colored Log    mssg=It Likely an unexpected iamage has apeeared on    level=WARN
                DataHandler.Colored Log    mssg=screen or an wished image has not found.    level=WARN
                DataHandler.Colored Log    mssg=Check for the file <../test_sequence/log.htm>    level=NULL
                base.Please Wait a Moment    ${default_time / 2}
                FOR    ${counter}    IN RANGE    ${0}    ${2}
                    Log    ${counter}
                    base.Please Wait a Moment    ${0.3}
                    SikuliLibrary.Press Special Key    ESC
                END
                RETURN    # End this process
            END
            DataHandler.Colored Log    mssg=${\n}Event type: SANGRIA${\n}Feature: ${type_event}    level=INFO
            DataHandler.Colored Log    mssg=Value: ${amount_to_be_removed}    level=INFO
            base.Please Wait a Moment    ${0.5}
            SikuliLibrary.Input Text    ${EMPTY}    ${MYC_CASHIER_CODE}
            SikuliLibrary.Press Special Key    TAB
            base.Please Wait a Moment    ${0.5}
            IF    ${check_event} == ${False}
                SikuliLibrary.Input Text    ${EMPTY}    ${VALUE_EXTRACTED}
                SikuliLIbrary.Press Special Key    TAB
                base.Please Wait a Moment    ${0.5}
                SikuliLIbrary.Press Special Key    ENTER
            ELSE
                base.Please Wait a Moment    ${0.5}
                SikuliLibrary.Press Special Key    ENTER
            END
            # CHECKING FOR PPOSSIBLE PROBLEMS IN THIS STEP....
            ${var1}    SikuliLibrary.Exists    ${UNSUFICIENT_AMOUNT}    ${default_time}
            ${var2}    SikuliLibrary.Exists    ${CONFIRM_EVENT}    ${default_time}
            IF    ${var1} == ${True}
                Builtin.Log To Console    ${\n}
                Builtin.Log    ...    level=WARN
                DataHandler.Colored Log    mssg=${\n}UNPOSSIBLE TO REALIZE AN EVENT TYPE: 'Sangria'    level=WARN
                DataHandler.Colored Log    mssg=There is not enougth amount on cashier!    level=WARN
                DataHandler.Colored Log
                ...    mssg=Check the automated cashiers audict. There is a difference
                ...    level=ERROR
                DataHandler.Colored Log
                ...    mssg=between the system cashier amount and the values in <../output/data_output.yaml>
                ...    level=ERROR
                SikuliLibrary.Press Special Key    ESC
                Fatal Error Triggered
                RETURN
            ELSE IF    ${var2} == ${True}
                SikuliLibrary.Screen Should Contain    ${CONFIRM_EVENT}
                SikuliLibrary.Input Text    ${EMPTY}    ${MASTER_PASSWORD}
                base.Please Wait a Moment    ${0.5}
                SikuliLibrary.Press Special Key    ENTER
            END
            # TRY ACCEPT THE TRANSFERENCE FROM PDV CASHIER TO THE MAIN CASHIER ON ERP SYSTEM...
            # OBS: This process will be results in a event cancelling wheter there is a performing issue!
            TRY
                base.Console Animation For Synchronization Time    anim_time=${synchronization_time}
                external_process.Accept The Cashiers Transference From PDV
            EXCEPT
                Builtin.Log To Console    ${\n}
                Builtin.Log    ...    level=ERROR
                DataHandler.Colored Log    mssg=${\n}It doesn't works!    level=ERROR
                DataHandler.Colored Log
                ...    mssg=Unpossible to complete the cashier's event type "Sangria".
                ...    level=ERROR
                DataHandler.Colored Log    mssg=This cashier's movement process will be canceled.    level=WARN
                # IF THE MyComemrce Sysrtem IS OPERN, WILL BE NECESSARY TO CLOSE THE APPLICATION...
                ${var3}    Exists    ${SALE_LAYOUT_PDV}
                IF    ${var3} == ${False}
                    FOR    ${counter}    IN RANGE    ${1}    ${3}
                        Builtin.Log    ${counter}
                        SikuliLibrary.Press Special Key    ESC
                        base.Please Wait a Moment    ${0.3}
                    END
                    # CLOSE MyCommerce System Process
                    ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.F4
                    base.Please Wait a Moment    ${2}
                    ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.N
                END
                Cancel Cashier Event Type Sangria
                RETURN
            ELSE
                Calculator.Remotion From Cashier Amount    ${amount_to_be_removed}    ${type_event}
                Builtin.Log To Console    ${\n}
                database.Check Results Aigainst ERP Database    sangriacaixa
            END
        END
    END

# =========================================================================================================================//

Cancel Cashier Event Type Sangria
    SikuliLibrary.Wait Until Screen Contain    ${SALE_LAYOUT_PDV}    ${5}
    SikuliLibrary.Press Special Key    F11
    base.Please Wait a Moment    ${default_time}
    ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.E
    SikuliLibrary.Wait Until Screen Contain    ${CANCEL_CASHIERS_SNG}    ${5}
    SikuliLibrary.Input Text    ${EMPTY}    ${master_password}
    base.Please Wait a Moment    ${0.3}
    ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.C
    SikuliLibrary.Wait Until Screen Contain    ${CANCELLING_GRID}    ${alert_image_time}
    FOR    ${counter}    IN RANGE    ${0}    ${5}
        SikuliLibrary.Press Special Key    DOWN
        base.Please Wait a Moment    ${0.3}
    END
    base.Please Wait a Moment    ${0.5}
    SikuliLibrary.Press Special Key    NUM1
    SikuliLibrary.Wait Until Screen Contain    ${CANCEL_CASHIERS_SNG}    ${alert_image_time}
    SikuliLibrary.Input Text    ${EMPTY}    ${master_password}
    base.Please Wait a Moment    ${0.3}
    ImageHorizonLibrary.Press Combination    KEY.ALT    KEY.C
