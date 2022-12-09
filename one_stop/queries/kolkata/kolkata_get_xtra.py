from django.db import connections


def get_xtra_fields(uuid):
    with connections['kolkata'].cursor() as c:
        c.execute(
            """SELECT emp.DEPARTMENT, OFF_CAMPUS_EMAIL FROM idm_prod.dbo.CACHED_IDM_EMPLOYEES Emp WHERE ID = %s""", [uuid])
        extras = c.fetchone()
        if not extras:
            return 'None', 'None'
        else:
            dept = extras[0]
            off_campus_email = extras[1]
            return dept, off_campus_email
