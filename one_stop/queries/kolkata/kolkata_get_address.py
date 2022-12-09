from django.db import connections

from datetime import date
from queries.bbts.bbts_oracle_queries import dictfetchall


current_year = date.today().year


def get_address(uuid):
    str_uuid = str(uuid)
    with connections['kolkata_ods'].cursor() as c:
        c.execute(
            """
            SELECT DISTINCT ODS_PERSON.ID,
    ODS_ADDRESS.ADDRESS_LINE_1,
    ODS_ADDRESS.ADDRESS_LINE_2,
    ODS_ADDRESS.CITY,
    ODS_ADDRESS.STATE,
    ODS_ADDRESS.ZIP,
    (
       CASE
       WHEN ODS_ADDRESS.COUNTRY_DESC = 'United States of America'
          THEN NULL
       ELSE ODS_ADDRESS.COUNTRY_DESC
       END
       ),

    (
       SELECT PHONE COLLATE SQL_Latin1_General_CP1_CI_AS
    FROM idm_prod.dbo.CACHED_IDM_STUDENTS
    WHERE ID COLLATE SQL_Latin1_General_CP1_CI_AS =ODS_PERSON.ID
       )
FROM ( ODS_PERSON LEFT JOIN ODS_ADDRESS on ODS_PERSON.PREFERRED_ADDRESS = ODS_ADDRESS.ADDRESS_ID )
CROSS JOIN H17_PREVIOUS_CURRENT_FUTURE_REPORTING_TERMS
WHERE ODS_PERSON.ID IN
       (SELECT DISTINCT STC_PERSON_ID
    FROM SPT_STUDENT_ACAD_CRED
    WHERE STC_REPORTING_TERM IN (H17_PREVIOUS_CURRENT_FUTURE_REPORTING_TERMS.CURRENT_TERM)
        AND STC_CURRENT_STATUS IN ('A','N') )
    AND ODS_PERSON.ID = %s
""", [str_uuid])
        dictionary = dictfetchall(c)
        if not dictionary:
            return 'None'
        else:
            return dictionary[0]
