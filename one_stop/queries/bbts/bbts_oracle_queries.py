from django.db import connections
import cx_Oracle
from decouple import config

cx_Oracle.init_oracle_client(lib_dir=config(r'LIB_DIR'))

########## Queries for Black Board Transactions Data ################


def passport_card_num(uuid):
    with connections['bbts'].cursor() as c:
        c.execute("""SELECT  substr(customer.defaultcardnum,14,9) "PassportCardNumber"
                    FROM   CUSTOMER
                    WHERE substr(customer.custnum,16,7) = %s""", [uuid])
    return


# Magic Meal Balance for Period 4
def magic_meal_balance(uuid):
    with connections['bbts'].cursor() as c:
        c.execute("""select
                    CUSTOMERBOARDPLANUSAGESTATUS.SEMQTRBALANCE "MagicMealBalance"
                    from ENVISION.CUSTOMERBOARDPLANUSAGESTATUS CUSTOMERBOARDPLANUSAGESTATUS,
                    ENVISION.CUSTOMER CUSTOMER
                    where ( CUSTOMERBOARDPLANUSAGESTATUS.CUSTOMERID = CUSTOMER.CUST_ID (+) )
                    and substr(customer.custnum,16,7) = %s
                    and CUSTOMERBOARDPLANUSAGESTATUS.BOARDPLANID IN (110)
                    UNION
                    select
                    CUSTOMERBOARDPLANUSAGESTATUS.WEEKBALANCE "MagicMealBalance"
                    from ENVISION.CUSTOMERBOARDPLANUSAGESTATUS CUSTOMERBOARDPLANUSAGESTATUS,
                    ENVISION.CUSTOMER CUSTOMER
                    where ( CUSTOMERBOARDPLANUSAGESTATUS.CUSTOMERID = CUSTOMER.CUST_ID (+) )
                    and substr(customer.custnum,16,7) = %s
                    and CUSTOMERBOARDPLANUSAGESTATUS.BOARDPLANID IN (122,97,93)
                    UNION
                    select
                    CUSTOMERBOARDPLANUSAGESTATUS.PERIOD4BALANCE "MagicMealBalance"
                    from ENVISION.CUSTOMERBOARDPLANUSAGESTATUS CUSTOMERBOARDPLANUSAGESTATUS,
                    ENVISION.CUSTOMER CUSTOMER
                    where ( CUSTOMERBOARDPLANUSAGESTATUS.CUSTOMERID = CUSTOMER.CUST_ID (+) )
                    and substr(customer.custnum,16,7) = %s
                    and CUSTOMERBOARDPLANUSAGESTATUS.BOARDPLANID IN (94,95,96,99,100,101)
                    and CUSTOMERBOARDPLANUSAGESTATUS.PERIOD4BALANCE <= CUSTOMERBOARDPLANUSAGESTATUS.WEEKBALANCE
                    UNION
                    select
                    CUSTOMERBOARDPLANUSAGESTATUS.WEEKBALANCE "MagicMealBalance"
                    from ENVISION.CUSTOMERBOARDPLANUSAGESTATUS CUSTOMERBOARDPLANUSAGESTATUS,
                    ENVISION.CUSTOMER CUSTOMER
                    where ( CUSTOMERBOARDPLANUSAGESTATUS.CUSTOMERID = CUSTOMER.CUST_ID (+) )
                    and substr(customer.custnum,16,7) = %s
                    and CUSTOMERBOARDPLANUSAGESTATUS.BOARDPLANID IN (94,95,96,99,100,101)
                    and CUSTOMERBOARDPLANUSAGESTATUS.PERIOD4BALANCE > CUSTOMERBOARDPLANUSAGESTATUS.WEEKBALANCE""", [uuid, uuid, uuid, uuid])
        dictionary = dictfetchall(c)
        if not dictionary:
            return 'None'
        else:
            dictionary = dictionary[0]
            return dictionary


# Transaction History Passport General Account
def passport_gen_acc_trans(uuid):
    with connections['bbts'].cursor() as c:
        c.execute("""SELECT udf_functions.UDF_TDatetimeToOracleDateTime(boardtransactions.actualdatetime) "DateTime" ,
                    packreportingfuncs.GetDomainValueText('POS Name',pos.pos_id) "Location" ,
                    'Meal Plan' "Account",
                    packreportingfuncs.GetDomainValueText('Board Meal Type',boardtransactions.boardmt_id) "Type",
                    NULL "Amount",
                    to_char(boardtransactions.countused ) "MealsUsed"
                    FROM   BOARDTRANSACTIONS, POS, PROFITCENTER, MERCHANT, CUSTOMER  WHERE   BOARDTRANSACTIONS.POS_ID = POS.POS_ID   AND
                    POS.PROFITCENTER_ID = PROFITCENTER.PROFITCENTER_ID   AND PROFITCENTER.MERCHANT_ID = MERCHANT.MERCHANT_ID   AND BOARDTRANSACTIONS.CUST_ID = CUSTOMER.CUST_ID
                    AND  (  customer.custnum =  '000000000000000' + %s  )   AND  MERCHANT.MERCHANT_ID = (1)
                    AND ( udf_functions.UDF_TDatetimeToOracleDateTime (boardtransactions.actualdatetime) < SYSDATE)
                    UNION
                    (
                    SELECT
                    udf_functions.UDF_TDatetimeToOracleDateTime (v_report_sv_transaction.datetime) "DateTime" ,
                    packreportingfuncs.GetDomainValueText('POS Name',v_report_sv_transaction.pos_id) "Location",
                    packreportingfuncs.GetDomainValueText('SV Account Type Name',v_report_sv_transaction.sv_account_type_id) "Account" ,
                    packreportingfuncs.GetDomainValueText('Sv Transaction Types',v_report_sv_transaction.SVTransactionType) "Type",
                    to_char(ABS(packreportingfuncs.ConvertMilliDollartoDollar(v_report_sv_transaction.amount)),'9999.99') "Amount",
                    NULL "MealsUsed"
                    FROM   V_REPORT_SV_TRANSACTION, CUSTOMER, POS  WHERE   V_REPORT_SV_TRANSACTION.CUST_ID = CUSTOMER.CUST_ID (+)
                    AND V_REPORT_SV_TRANSACTION.POS_ID = POS.POS_ID
                    AND  ( udf_functions.UDF_TDatetimeToOracleDateTime (v_report_sv_transaction.datetime) < SYSDATE
                    and  customer.custnum =  '000000000000000' + %s  and v_report_sv_transaction.IsSuccess = ('T') )
                    ) Order By "DateTime" desc""", [uuid, uuid])
        dictionary = dictfetchall(c)
        if not dictionary:
            return 'None'
        else:
            # print(dictionary)
            return dictionary


# Passport General Account balance
def general_account_balance(uuid):
    with connections['bbts'].cursor() as c:
        c.execute("""SELECT
                    to_char(packreportingfuncs.ConvertMilliDollartoDollar(sv_account.balance),'99999.99') "General_Balance"
                    FROM   customer_sv_account, sv_account, customer
                    WHERE   SV_ACCOUNT.SV_ACCOUNT_ID = CUSTOMER_SV_ACCOUNT.SV_ACCOUNT_ID   AND
                    CUSTOMER_SV_ACCOUNT.CUST_ID = CUSTOMER.CUST_ID    AND
                    (  substr(customer.custnum,16,7) = %s  and  sv_account.sv_account_type_id IN (1)  )""", [uuid])
        dictionary = dictfetchall(c)
        if not dictionary:
            return 'None'
        else:
            dictionary = dictionary[0]
            dictionary["General_Balance"] = float(
                dictionary["General_Balance"])
            return dictionary


# Passport Dining dollar balance
def dining_dollar_balance(uuid):
    with connections['bbts'].cursor() as c:
        c.execute("""SELECT
                    to_char(packreportingfuncs.ConvertMilliDollartoDollar(sv_account.balance),'99999.99') "Dining_Dollar_Balance"
                    FROM   customer_sv_account, sv_account, customer
                    WHERE   SV_ACCOUNT.SV_ACCOUNT_ID = CUSTOMER_SV_ACCOUNT.SV_ACCOUNT_ID   AND
                    CUSTOMER_SV_ACCOUNT.CUST_ID = CUSTOMER.CUST_ID    AND
                    (  substr(customer.custnum,16,7) = %s  and  sv_account.sv_account_type_id IN (2)  )""", [uuid])
        dictionary = dictfetchall(c)
        if not dictionary:
            return 'None'
        else:
            dictionary = dictionary[0]
            dictionary["Dining_Dollar_Balance"] = float(
                dictionary["Dining_Dollar_Balance"])
            return dictionary


# MeaL Plan
def meal_plan(uuid):
    with connections['bbts'].cursor() as c:
        c.execute("""SELECT
                    packreportingfuncs.GetDomainValueText('Board Plan Name',customerboard.boardplan_id) "MealPlan"
                    FROM   CUSTOMER, CUSTOMERBOARD
                    WHERE   CUSTOMER.CUST_ID = CUSTOMERBOARD.CUST_ID (+)    AND  (  substr(customer.custnum,16,7) = %s  )""", [uuid])
        dictionary = dictfetchall(c)
        if not dictionary:
            return 'None'
        else:
            dictionary = dictionary[0]
            return dictionary


# Meals left week
def meals_left(uuid):
    with connections['bbts'].cursor() as c:
        c.execute("""select
           
                    CUSTOMERBOARDPLANUSAGESTATUS.WEEKBALANCE "MealsLeft"
                    
                    from ENVISION.CUSTOMERBOARDPLANUSAGESTATUS CUSTOMERBOARDPLANUSAGESTATUS,
                    ENVISION.CUSTOMER CUSTOMER
                    where ( CUSTOMERBOARDPLANUSAGESTATUS.CUSTOMERID = CUSTOMER.CUST_ID (+) )
                    and ( substr(customer.custnum,16,7) = %s
                    and CUSTOMERBOARDPLANUSAGESTATUS.BOARDPLANID IN (100,101,93,94,95,96,97,98,99,122))
                    UNION

                    select

                    CUSTOMERBOARDPLANUSAGESTATUS.SEMQTRBALANCE "MealsLeft"

                    from ENVISION.CUSTOMERBOARDPLANUSAGESTATUS CUSTOMERBOARDPLANUSAGESTATUS,
                    ENVISION.CUSTOMER CUSTOMER
                    where ( CUSTOMERBOARDPLANUSAGESTATUS.CUSTOMERID = CUSTOMER.CUST_ID (+) )
                    and ( substr(customer.custnum,16,7) = %s
                    and CUSTOMERBOARDPLANUSAGESTATUS.BOARDPLANID =110)""", [uuid, uuid])
        dictionary = dictfetchall(c)
        if not dictionary:
            return 'None'
        else:
            dictionary = dictionary[0]
            return dictionary

# Meal count resets on:


def meals_reset_on(uuid):
    with connections['bbts'].cursor() as c:
        c.execute("""select
                    'End of Semester' "MealsReset"
                    from ENVISION.CUSTOMERBOARDPLANUSAGESTATUS CUSTOMERBOARDPLANUSAGESTATUS,
                    ENVISION.CUSTOMER CUSTOMER
                    where ( CUSTOMERBOARDPLANUSAGESTATUS.CUSTOMERID = CUSTOMER.CUST_ID (+) )
                    and substr(customer.custnum,16,7) = %s
                    and CUSTOMERBOARDPLANUSAGESTATUS.BOARDPLANID IN (110)
                    UNION
                    select
                    'On Sunday' "MealsReset"
                    from ENVISION.CUSTOMERBOARDPLANUSAGESTATUS CUSTOMERBOARDPLANUSAGESTATUS,
                    ENVISION.CUSTOMER CUSTOMER
                    where ( CUSTOMERBOARDPLANUSAGESTATUS.CUSTOMERID = CUSTOMER.CUST_ID (+) )
                    and substr(customer.custnum,16,7) = %s
                    and CUSTOMERBOARDPLANUSAGESTATUS.BOARDPLANID IN (122,97,93,94,95,96,99,100,101)""", [uuid, uuid])
        dictionary = dictfetchall(c)
        if not dictionary:
            return 'None'
        else:
            dictionary = dictionary[0]
            return dictionary


# dictfetchall() takes in a cursor list object, iterates over each cols and rows and zips
# them into a dictionary and returns the dictionary to the sql function is was called from
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
