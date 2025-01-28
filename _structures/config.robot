*** Settings ***
Documentation     :: THIS DOCUMENT IS THE ROBOT  TEST CASE CONFIGURATIONS FILE. ALL CONTROL DATA AND THEIR CORRESPONDING
...    INFORMATION ARE HERE. THESE DATA  HAS  BEEN  WRITTEN  ACCORDING  TO  THE HIERARCHICAL FUNCTIONAL COMPONENTS OF
...    THE TEST CASES STRUCTURE. BEFORE CONFIGURING  ANY CHANGES TO THIS SEQUENCE, MAKE SURE THAT WHAT YOU ARE GOING 
...    TO DO IS IN ACCORDANCE  WITH THE FUNCTIONALITY AND BEHAVIOR OF THE TEST CASE ::

*** Comments *** 

::                                                     WARNING                                                         
                                                      ---------
THIS DATA SEQUENCE MUST BE USED WHEN THE USER WANTS TO PERFORM A SPECIFIC TEST CASE USING CUSTOM DATA. MORE SPECIFICALLY,
THIS SEQUENCE  OF AUTOMATION SYSTEM CONFIGURATIONS IS EXECUTED WHEN WE WISH TO USE ANOTHER DATABASE AND  ITS INFORMATION. 
CHANGING OR ADDING VALUES TO THESE VARIABLES CAUSE A DIRECT IMPACT ON THE BEHAVIOR OF THE AUTOMATION SYSTEM, CHANGING ALL 
ITS CLAUSES AND DECLARATIONS.  ::
#																														
#=========================================================================================================================
# Database Settings									[AUTOUPDATE]		     											01
#-------------------------------------------------------------------------------------------------------------------------
*** Variables ***     

#" INTERNAL DATA ::
${DATA_DEBUG}			  ${True}

#" DO YOU WANT TO USE A NEW CONNECTION TO SERVER ? 
${USE_NEW_CONNECT}		  ${False}

#" CUSTOM DATABASE ON ERP SERVER ::
${SERVER_USER}            root
${SERVER_PASSWRD}         vssql
${HOST_SERVER}            10.1.1.220
${PORT}					  3306
${DATABASE_NAME}          scanntech


# WHO WILL MOVEMENT THIS DATABASE CONNECTION ?
${USER_CODE_ID}           ${3781}
${USER_NAME}              ROBOT
${TERMINAL_PC}            CQP-MATHEUS-165


# WHAT'S THE CASHIER SETTINGS TO PDV SYSTEM ?
${CASHIER_CODE}			  ${118}
${CASHIER_NAME}		      NEW CASHIER


#" USE THESE SETTINGS BELLOW TO ACTIVE THE DOWNLOAD OF NEW DATA FROM DATABASE GIVEN ABOVE ::
${GET_DATA_FROM_DB}	      ${False}	 # -> This option has filters to download data from the database!
${LIMIT_FOR_CUST}	      ${20}
${LIMIT_FOR_PROD}		  ${30}
${RANDOMIZE_CHOICE}		  ${False}	 # -> Use it to randomly choose from the range of database records.
${SET_NEW_DATA}           ${False}   # -> This option has no filters of any kind!
${USE_PDV_PRICE}		  ${True}    # -> This variable controls the downloading of product prices from
									 #"   the database. It is very important because this is what defines
									 #"   which product price the automation system will use during the
									 #"   test case execution. This means that we can choose between SaleT1
									 #"   and SalePDV elements
									 
# IF {SET_NEW_DATA} IS TRUE, YOU MUST INFORM WHAT DATA WILL BE DOWNLOADED FROM THE DATABASE CONNECTION 
# CUSTOM SEQUENCE OF PRODUCTS REGISTER TO BE USED.
@{SEQUENCE_OF_PRODUCTS}   
...		${91449}

# CUSTOM SEQUENCE OF CUSTOMERS RECORD TO BE USED.
@{SEQUENCE_OF_CUSTOMERS}
...     ${3742}

#=========================================================================================================================
# Update Data Libraries (only to <scanntech>)																			02
#-------------------------------------------------------------------------------------------------------------------------
#" This configuration is what controls the automatic update of the internal data structure, but this feature works
#" only for the default database <scannntech>. Other data structures require new data sets or custom data sequence.
${AUTO_UPDATE_OF_DATA}          ${True}
	
#=========================================================================================================================
# User Interface Controllers For Auatomations System Behaviour															03
#-------------------------------------------------------------------------------------------------------------------------
${WIN_COMMAND}                 C:\\Visual Software\\MyCommerce\\PDV\\MyCommercePDV.exe
${SYSTEM_NAME}                 MyCommercePDV      # Font System Name of the application.
${PDV_USER_ID}                 ${54}              # Users System data Loging: ID
${PDV_USER_PASSWORD}           ${1}               # Users System data Loging: Password
${MASTER_PASSWORD}             ${321}             # Master password valid for any operation.
${PATTERN_CLIENT_CODE}         ${3742}            # Patter numerical code of identification for customers.
${MYC_USER_ID}				   ${3757}			  # User data Login to the MyCommerce ERP System
${MYC_USER_PASSWORD}		   ${1}				  # Passwrod data Login to the MyCommerce ERP System 		  
${PATTERN_CLIENT_CPF}          95022559099        # Default Customer CPF code registered on ERP server in <scanntech> Dtb.
${ACCESS_CODE}                 103521261563       # Inner Company Code to release the system usage.
${CLOSE_SYSTEM}				   ${False}		      # Use this control to close the PDV system to end of test case.


#=========================================================================================================================
# User Interface Controllers For Customer Properties																	04
#-------------------------------------------------------------------------------------------------------------------------
${USE_CLIENT_SELECTION}		   ${True}			#" DO YOU WISH TO UTILIZE ESPECIFIC CUSTOMERS IN YOUR TEST CASE SEQUENCE?
${USE_DEFAULT_CLIENT}          ${False}         # Use it to set up an patter to the customer selectiong during the sale.
${DEFAULT_CLIENT_CODE}         ${3743}          # If the clause above is TRUE, inform what's the pattern customer code.
${USE_CNPJ_CODE}			   ${True}
${USE_CPF_CODE}			   	   ${False}
${AUTOMATHIC_ISERTION}         ${False}         # Confirm the insertion of the CPF code during product launching.
${USE_CLIENT_SEARCH_WIN}	   ${False}			
${FILTER_BY_SOCIAL_NAME}	   ${False}
${FILTER_BY_CLIENT_CODE}	   ${False}
${FILTER_BY_CNPJ_CPF}		   ${False}

#" DO YOU WANT TO USE A RANDOM GENERATION FOR THE CPF CODE ?
${RANDOMIZE_CPF_CODE}          ${False}

#" DO YOU WANT TO USE A SPECIFIC SEQUENCE OF CUSTOMER CODES ?
${CUSTOMER_SEQUENCE}		   ${True}
@{CUSTOM_CLIENT_SEQUENCE}
	...		${3760}
	...		${3776}
	...		${3742}
	...		${3743}

	
#" CUSTOMER CREDIT PAYMENT WAY :: 
${RAND_CLIENT_CODE_PAYMENT}    ${False}
${CONFIRM_CUSTOMER_CPF}        ${True}      #" It's TRUE by default. This is used to confirm the CPF code printed to NFC.
${CREDIT_MONTHS}               ${1}         #" It is always ONE month by default. This variable is used to inform how many
                                            #" months will be launched for the payment of a sale of the credit type.


#==========================================================================================================================
# Controllers of the Fiscal Document and Tax Document																	 05
#--------------------------------------------------------------------------------------------------------------------------
${CONFIRM_PRINT_NFC}           ${True}     #" Use it to confirm the appearance of the message box to printing the NFC-e
${PRINT_NFC_BUTTON}            NUM1        #" It's FALSE by default. This is used to confirm the NFC print. Press 1 or 2
${PRINT_PIX_DOCMNT}			   ${False}
${PRINT_PIX_BUTTON}            NUM1        #" 'NUM1' to confirm printing or 'NUM2' to reject. It's  always NUM1 by default
${CSTAT_CHECK_OUT}	           ${False}


#==========================================================================================================================
# Controller of the Product Selector																					 06
#--------------------------------------------------------------------------------------------------------------------------
# if (the user wants to randomize the element: 'QNT_PROD_FOR_SALE'):
${RANDOMIZE_QNT_PRODUCT}       ${True}
${QNT_MAX_PROD_FOR_SALE}       ${20}          # It controls the maximum quantity of products can be launched for sale.
${QNT_PROD_FOR_SALE}           ${5}           # If 'RANDOMIZE_QTD_PRODUCT_FOR_SALE' is 'FALSE' this variable will be used.


#:: DURING THE LAUNCH OF THE PRODUCT FOR CURRENT SALE, THE SYSTEM NEEDS TO FIND THE PRODUCT BY ITS SERIAL CODE. AUTOMATION 
#   SUPPORTS  ONLY THOSE POSSIBILITIES  BELOW. BUT PAY ATTENTION! THE SELECTION OF PRODUCTS FROM THE INITIAL LAYOUT OF THE 
#   SYSTEM ONLY ACCEPTS THE BAR CODE OF THE PRODUCT AS A SEARCH PARAMETER! ::											 

${USE_PRODUCT_GROUPING}			${True}
${CHOOSE_PROD_IN_THE_LAYOUT}    ${False}
${FILTER_BY_CODE}               ${False}   #" FALSE by default. It's used to set up this product property as a search filter
${FILTER_BY_BARCODE}            ${True}    #" TRUE by default. It's used to set up this product property as a search filter
${FILTER_BY_REFE}               ${False}   #" FALSE by default. It's used to set up this product property as a search filter
${FILTER_BY_DESC}               ${False}   #" FALSE by default. It's used to set up this product property as a search filter
${USE_DEFAULT_PRODUCT}          ${False}   #" FALSE by default. Use it to set up a patter product to be used in the test cases
${STANDARD_PRODUCT}             ${11943}   # If the sentence above is TRUE, notice the what the produc code: <ID>
${PRODUCT_SEQUENCE}             ${False}   # This variable to turn possible to apply a custom sequence of produts for sale.
@{CUSTOM_PROD_SEQUENCE}                    # If the clause above is TRUE, is necessary set up what the sequence to be used!    
...		${11943}
...		${28788}
...		${1060}
...		${28788}
...		${28788}
...		${1060}
...		${1060}


#==========================================================================================================================
# Pricing Table controllers																								 07
#--------------------------------------------------------------------------------------------------------------------------
${REPLACE_PRICING_TABLE}        ${False}   # Use it whether there is an available pricing list to replacement of the products.
${CHECK_CUSTOMER_RECORD}        ${False}   # This clause controls the replacement of products according to the customer record.
${PRICING_TABLE_LIMIT}          ${50}      # Limit for replacement of products on sale. !CHECK UP PRICING TABLE RECORD ON DTB¡
${PRICING_LIST_CODE_ID}         ${3}
${PRICING_LIST_NAME}			VAREJO


#==========================================================================================================================
# Payment Way Settings																				                     08
#--------------------------------------------------------------------------------------------------------------------------
${PAY_CASHBACK}                 ${True}
${PAY_CHECK}                    ${True}
${PAY_CUSTOMER_CREDIT}          ${False}
${PAY_CREDIT_CARD}              ${False}
${PAY_ELETRONIC_TRANSF}         ${False}
${PAY_PIX_CODE}                 ${True}
${PIX_TIME_OUT}                 ${10}
${PATTERN_PAYMENT_METHOD}        DIN       #" Select what the patter payment way. (CHQ, CRE, TEF, CRT and PIX)


#==========================================================================================================================
# Sales Approach					  [SALES CANCELLATIONS AND UNCOMPLETED SALES]										 09
#--------------------------------------------------------------------------------------------------------------------------
${UNCOMPLETE_SALE}				${True}
${CANCEL_SALE}					${True}   #" Use it to use the calnceling option for sales simulator.
${RECURSION}					${0}	  #" Set the of probability as a recursion percentange.
									      # -> The 'ReCuRsIoN' variable is a mathmatical delimiter to set up a probability
										  # margin of application to the canceling resource. 
										  

#==========================================================================================================================
#													  [SANGRIA]												     		 10

#:: OBS >> The cashier must be open in the MyCommerce ERP system. Wheter the cashier is closed, the event type "Sangria" 
# will not be performed. That functional condition is verifiered against database on usage. Ignore it isn't an option!! ::
#--------------------------------------------------------------------------------------------------------------------------
${SANGRIA}					   ${False}	 # Cashier Movement type "Sangria"
${CASH_EVENT}				   ${True}	 # Remotion from cashier amount type "Cashback"
${CHECK_EVENT}				   ${False}  # Remotion from cashier amount type "Check" 
${MINIMUN_NECESSARY}		   ${300}	 # Total of the general amount avaliable in the cashiers values.
${VALUE_EXTRACTED}			   ${150}	 # It's represents the total value to be removed from cashier amount.
${MYC_CASHIER_CODE}			   ${111}	 # The cashier code has opened in the MyCommerce ERP system.
${SANGRIA_RECURSION}		   ${50}     # Probability to perform an event type "Sangria".


#==========================================================================================================================
# Automations System Process Controllers																			     11
#--------------------------------------------------------------------------------------------------------------------------
#" HOW MUCH TIMES YOU WANT REPEAT THE TEST CASE'S SEQUENCE ?
${REPEAT_CYCLE_TIMES}           ${1}

${DEFAULT_TIME}                 ${1}          # One second by default. 
${ALERT_IMAGE_TIME}             ${3}		  # Two seconds by default.
${CANCELATIONS_TIME}		    ${15}

#" DO YOU WANT APPLY DISCOUNT TO PRODUCTS ON OFFER OR PROMOTIONS ?
${DISCOUNT_TO_MODIFIERS}	    ${False}
#==========================================================================================================================

	