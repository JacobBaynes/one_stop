from django.db import connections

from datetime import date
from queries.bbts.bbts_oracle_queries import dictfetchall


current_year = date.today().year


def get_stud_classes(uuid):
    with connections['kolkata'].cursor() as c:
        c.execute(
            """SELECT DISTINCT 
                    SPT_STUDENT_ACAD_CRED.STC_TERM "Term",
                    ODS_COURSE_SECTIONS.SEC_NAME "Course",
                    ODS_COURSE_SECTIONS.SEC_SHORT_TITLE "CourseName",
                    ODS_PERSON.FIRST_NAME +' '+ ODS_PERSON.LAST_NAME "Instructor",
                    ODS_COURSE_SECTIONS.SEC_MIN_CRED "CreditHours",
                    CASE WHEN ODS_COURSE_SECTION_MTG.CSM_MONDAY is not null
                    THEN 'M'
                    ELSE ''
                    END "M",
                    case when ODS_COURSE_SECTION_MTG.CSM_TUESDAY is not null
                    THEN 'T'
                    ELSE ''
                    END "T",
                    case when ODS_COURSE_SECTION_MTG.CSM_WEDNESDAY is not null
                    THEN 'W'
                    ELSE ''
                    END "W",
                    case when ODS_COURSE_SECTION_MTG.CSM_THURSDAY is not null
                    THEN 'TH'
                    ELSE ''
                    END "TH",
                    case when ODS_COURSE_SECTION_MTG.CSM_FRIDAY is not null
                    THEN 'F'
                    ELSE ''
                    END "F",
                    ltrim(right(convert(varchar,ODS_COURSE_SECTION_MTG.CSM_START_TIME,100),7)) "Start_Time",
                    ltrim(right(convert(varchar,ODS_COURSE_SECTION_MTG.CSM_END_TIME,100),7)) "End_Time",
                    ODS_COURSE_SECTION_MTG.BUILDING_DESC "Building",
                    ODS_COURSE_SECTION_MTG.CSM_ROOM "Classroom"
            FROM ( ( ods_prod.dbo.SPT_STUDENT_ACAD_CRED LEFT JOIN ( ods_prod.dbo.ODS_COURSE_SECTIONS LEFT JOIN ods_prod.dbo.ODS_COURSE_SEC_FACULTY on ods_prod.dbo.ODS_COURSE_SECTIONS.COURSE_SECTIONS_ID = ods_prod.dbo.ODS_COURSE_SEC_FACULTY.CSF_COURSE_SECTION ) on ods_prod.dbo.SPT_STUDENT_ACAD_CRED.STC_SCS_COURSE_SECTION = ods_prod.dbo.ODS_COURSE_SECTIONS.COURSE_SECTIONS_ID ) INNER JOIN ods_prod.dbo.ODS_COURSE_SECTION_MTG on ods_prod.dbo.ODS_COURSE_SECTIONS.COURSE_SECTIONS_ID = ods_prod.dbo.ODS_COURSE_SECTION_MTG.CSM_COURSE_SECTION ) LEFT JOIN ods_prod.dbo.ODS_PERSON on ods_prod.dbo.ODS_COURSE_SEC_FACULTY.CSF_FACULTY = ods_prod.dbo.ODS_PERSON.ID FULL OUTER JOIN ods_prod.dbo.H17_PREVIOUS_CURRENT_FUTURE_REPORTING_TERMS on ODS_COURSE_SECTIONS.SEC_REPORTING_TERM = ods_prod.dbo.H17_PREVIOUS_CURRENT_FUTURE_REPORTING_TERMS.CURRENT_TERM
            WHERE SPT_STUDENT_ACAD_CRED.STC_PERSON_ID = %s
                AND ODS_COURSE_SECTIONS.SEC_REPORTING_TERM = ods_prod.dbo.H17_PREVIOUS_CURRENT_FUTURE_REPORTING_TERMS.CURRENT_TERM
                AND ODS_COURSE_SECTIONS.SEC_CURRENT_STATUS = 'A'
                AND SPT_STUDENT_ACAD_CRED.STC_CURRENT_STATUS IN('A','N')
""", [uuid])
        dictionary = dictfetchall(c)
        if not dictionary:
            return 'None'
        else:
            return dictionary


def get_faculty_classes(uuid):
    with connections['kolkata_ods'].cursor() as c:
        c.execute('''
                  select
    distinct SPT_STUDENT_ACAD_CRED.STC_TERM "Term",
    ODS_COURSE_SECTIONS.SEC_NAME "Course",
    ODS_COURSE_SECTIONS.SEC_SHORT_TITLE "CourseName",
    ODS_COURSE_SECTIONS.SEC_MIN_CRED "CreditHours",
    case
        when ODS_COURSE_SECTION_MTG.CSM_MONDAY is not null then 'M'
        else ''
    end "M",
    case
        when ODS_COURSE_SECTION_MTG.CSM_TUESDAY is not null then 'T'
        else ''
    end "T",
    case
        when ODS_COURSE_SECTION_MTG.CSM_WEDNESDAY is not null then 'W'
        else ''
    end "W",
    case
        when ODS_COURSE_SECTION_MTG.CSM_THURSDAY is not null then 'TH'
        else ''
    end "TH",
    case
        when ODS_COURSE_SECTION_MTG.CSM_FRIDAY is not null then 'F'
        else ''
    end "F",
    ltrim(
        right(
            convert(
                varchar,
                ODS_COURSE_SECTION_MTG.CSM_START_TIME,
                100
            ),
            7
        )
    ) "Start_Time",
    ltrim(
        right(
            convert(
                varchar,
                ODS_COURSE_SECTION_MTG.CSM_END_TIME,
                100
            ),
            7
        )
    ) "End_Time",
    ODS_COURSE_SECTION_MTG.BUILDING_DESC "Building",
    ODS_COURSE_SECTION_MTG.CSM_ROOM "Classroom"
from
    SPT_STUDENT_ACAD_CRED SPT_STUDENT_ACAD_CRED
    inner join (
        (
            (
                ODS_COURSE_SECTIONS ODS_COURSE_SECTIONS
                inner join ODS_COURSE_SEC_FACULTY ODS_COURSE_SEC_FACULTY on ODS_COURSE_SECTIONS.COURSE_SECTIONS_ID = ODS_COURSE_SEC_FACULTY.CSF_COURSE_SECTION
            )
            left join ODS_COURSE_SECTION_MTG ODS_COURSE_SECTION_MTG on ODS_COURSE_SECTIONS.COURSE_SECTIONS_ID = ODS_COURSE_SECTION_MTG.CSM_COURSE_SECTION
        )
        inner join ODS_PERSON ODS_PERSON on ODS_COURSE_SEC_FACULTY.CSF_FACULTY = ODS_PERSON.ID
    ) on SPT_STUDENT_ACAD_CRED.STC_SCS_COURSE_SECTION = ODS_COURSE_SECTIONS.COURSE_SECTIONS_ID
    FULL OUTER JOIN ods_prod.dbo.H17_PREVIOUS_CURRENT_FUTURE_REPORTING_TERMS on ODS_COURSE_SECTIONS.SEC_REPORTING_TERM = ods_prod.dbo.H17_PREVIOUS_CURRENT_FUTURE_REPORTING_TERMS.CURRENT_TERM
where
    ODS_PERSON.ID = %s
    and SPT_STUDENT_ACAD_CRED.STC_REPORTING_TERM = ods_prod.dbo.H17_PREVIOUS_CURRENT_FUTURE_REPORTING_TERMS.CURRENT_TERM
    and ODS_COURSE_SECTIONS.SEC_CURRENT_STATUS = 'A'
    and SPT_STUDENT_ACAD_CRED.STC_CURRENT_STATUS IN('A', 'N')
    and ODS_COURSE_SECTION_MTG.CSM_END_TIME IS NOT NULL

                  ''', [uuid])

        dictionary = dictfetchall(c)
        if not dictionary:
            return 'None'
        else:
            return dictionary
