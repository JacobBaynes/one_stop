import ldap
from decouple import config


def get_ad_data(cn):
    server = config('AD_SERVER')
    binddn = config('BIND_DN')
    pw = config('AD_PWD')
    base_dn = 'OU=Active,OU=Campus,dc=highpoint,dc=edu'
    filtering = '(cn={})'.format(cn)
    attrs = ['userAccountControl', 'lockoutTime', 'memberof']
    encoding = "utf-8"

    try:
        l = ldap.initialize(server, bytes_mode=False)
        l.simple_bind_s(binddn, pw)
    except ldap.SERVER_DOWN as e:
        print(e)
    else:
        results = l.search_s(base_dn, ldap.SCOPE_SUBTREE, filtering, attrs)

    try:
        results = results[0]
        dn = results[0]

    except IndexError as e:
        print(e, "- User has no active directory data")
        return 'None'

    try:
        disabled = results[1]['userAccountControl'][0]
        status = int(str(disabled, encoding))
        if status != 512:
            status = 'Yes'
        else:
            status = 'No'
    except KeyError as e:
        print(e, "- User doesn't have disabled attribute")
        disabled = "No"

    try:
        lock = results[1]['lockoutTime'][0]
        locked = int(str(lock, encoding))
        if locked > 0:
            locked = 'Yes'
        else:
            locked = 'No'
    except KeyError as e:
        print(e, "- User doesn't have locked attribute")
        locked = "No"

    try:
        groups = []

        for group in results[1]['memberOf']:
            group = group.decode('utf-8').split(',')
            cn = group[0]
            groups.append(cn)
    except KeyError as e:
        print(e, "User is not in any AD Groups")
        groups = 'None'

    data = [dn, status, locked, groups]

    return data
