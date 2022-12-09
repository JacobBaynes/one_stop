import uuid
from django.db import connections
from collections import Counter

from queries.bbts.bbts_oracle_queries import dictfetchall


def ccure_data(uuid):
    with connections['ccure'].cursor() as c:
        c.execute("""SELECT p_udf.BBCardNumber_, 
                            p.Disabled,
                            c.Name as Clearances,
                            cre.CardNumber,
                            b.Name AS BadgeLayoutName
                    FROM Access.PersonnelUDF AS p_udf
                    INNER JOIN Access.Personnel AS p ON p_udf.ObjectID=p.ObjectID
                    INNER JOIN Access.PersonnelClearancePair as pc_pair ON p_udf.ObjectID=pc_pair.PersonnelId
                    INNER JOIN Access.Credential AS cre ON p_udf.ObjectID=cre.PersonnelId
                    INNER JOIN Access.Clearance AS c ON pc_pair.ClearanceID=c.ObjectID
                    INNER JOIN Access.BadgeLayout AS b ON cre.BadgeLayoutId=b.ObjectID
                    WHERE NOT c.Name LIKE 'CC_%%' AND p_udf.Student_ID__ = %s""", [uuid])
        dictionary = dictfetchall(c)
        if not dictionary:
            return 'None'
        else:
            dict = get_muliple_values(dictionary)
            return dict


def get_door_access(uuid):
    with connections['ccure'].cursor() as c:
        c.execute("""SELECT a.MessageType
                        ,a.MessageUTC
                        ,p.Name
                        ,d.Name as Door
                        ,pudf.Student_ID__
                    FROM ACVSUJournal_00010039.dbo.ACVSUJournalLog AS a
                    INNER JOIN ACVSCore.Access.Personnel AS p ON a.ObjectIdentity1 = p.GUID
                    INNER JOIN ACVSCore.Access.Door AS d ON a.ObjectIdentity2 = d.GUID
                    INNER JOIN ACVSCore.Access.PersonnelUDF AS pudf ON p.ObjectID = pudf.ObjectID
                    WHERE MessageType IN ('CardAdmitted', 'CardRejected')
                    AND pudf.Student_ID__ = %s
                    ORDER BY a.MessageUTC DESC""", [uuid])
        dictionary = dictfetchall(c)
        if not dictionary:
            return 'None'
        else:
            return dictionary


def get_muliple_values(dict):
    clearances = []
    card_nums = []
    badge_layouts = []

    for c in dict:
        clearances.append(c["Clearances"])

    for n in dict:
        card_nums.append(n["CardNumber"])

    for b in dict:
        badge_layouts.append(b["BadgeLayoutName"])

    counter = Counter(clearances)
    clear_list = sorted(counter)

    counter = Counter(card_nums)
    card_list = sorted(counter)

    counter = Counter(badge_layouts)
    badge_list = sorted(counter)

    record = dict[0]

    record["Clearances"] = clear_list
    record["CardNumber"] = card_list
    record["BadgeLayoutName"] = badge_list

    return record
