from datetime import date
import requests

from rest_framework import viewsets
from .serializers import PersonSerializer
from django.shortcuts import render
from .models import Person
from queries.bbts.bbts_oracle_queries import dining_dollar_balance, general_account_balance, magic_meal_balance, meal_plan, meals_left, meals_reset_on, passport_gen_acc_trans
from queries.ccure.ccure_queries import ccure_data, get_door_access
from queries.active_dir.ad_data import get_ad_data
from queries.kolkata.kolkata_get_xtra import get_xtra_fields
from queries.kolkata.kolkata_get_address import get_address
from queries.kolkata.kolkata_get_schedule import get_stud_classes, get_faculty_classes
from queries.starrez.starrez_booking import star_rez_get_booking

# user_proile view renders template with context data
# pertaining to the currently logged in user


def user_detail(request, sys_ID=None):
    if sys_ID != None:
        person = Person.objects.get(sys_ID=sys_ID)
        person = fix_uuid(person)
        uuid = person.uuid

        if person.dob == date(1900, 1, 1):
            person.dob = "None"

        # Query for Black Board transactions and balances
        bbts_mm_bal = magic_meal_balance(uuid)
        bbts_gen_acc_trans = get_time_stamp(passport_gen_acc_trans(uuid))
        bbts_gen_acc_bal = general_account_balance(uuid)
        bbts_dd_bal = dining_dollar_balance(uuid)
        bbts_meal_plan = meal_plan(uuid)
        bbts_meals_left = meals_left(uuid)
        bbts_meal_reset = meals_reset_on(uuid)
        # Get CCure clearance data for user
        ccure = ccure_data(str(uuid))
        doors = get_door_access(str(uuid))
        # Get Active Directroy Data for
        ad_info = get_ad_data(person.user.username)
        # Get Department info for user
        dept, off_campus_email = get_xtra_fields(uuid)
        address = get_address(uuid)
        if person.classification != 'Faculty' and person.classification != 'Adjunct' and person.classification != 'Staff':
            classes = get_stud_classes(uuid)
        else:
            classes = get_faculty_classes(uuid)
        starrez_booking = star_rez_get_booking(uuid)

        context = {
            'person': person,
            'bbts_mm_bal': bbts_mm_bal,
            'bbts_gen_acc_trans': bbts_gen_acc_trans,
            'bbts_gen_acc_bal': bbts_gen_acc_bal,
            'bbts_dd_bal': bbts_dd_bal,
            'bbts_meal_plan': bbts_meal_plan,
            'bbts_meals_left': bbts_meals_left,
            'bbts_meal_reset': bbts_meal_reset,
            'ccure': ccure,
            'doors': doors,
            'ad_info': ad_info,
            'dept': dept,
            'off_campus_email': off_campus_email,
            'address': address,
            'classes': classes,
            'sr_booking': starrez_booking
        }

    else:
        # Get currently logged in user
        u = request.user
        # Get currently logged in users persons record from vista
        person = Person.objects.get(user_id=u.id)
        # zero fill uuid to get correct format for pulling profile images
        person = fix_uuid(person)
        uuid = u.person.uuid

        if person.dob == date(1900, 1, 1):
            person.dob = "None"

    # Query for transactions and balances
        bbts_mm_bal = magic_meal_balance(uuid)
        bbts_gen_acc_trans = get_time_stamp(passport_gen_acc_trans(uuid))
        bbts_gen_acc_bal = general_account_balance(uuid)
        bbts_dd_bal = dining_dollar_balance(uuid)
        bbts_meal_plan = meal_plan(uuid)
        bbts_meals_left = meals_left(uuid)
        bbts_meal_reset = meals_reset_on(uuid)
        # Get CCure clearance data for user
        ccure = ccure_data(str(uuid))
        doors = get_door_access(str(uuid))
        # Get Active Directroy Data for
        ad_info = get_ad_data(person.user.username)
        # Get Department info for user
        dept, off_campus_email = get_xtra_fields(uuid)
        address = get_address(uuid)

        if person.classification != 'Faculty':
            classes = get_stud_classes(uuid)
        else:
            classes = get_faculty_classes(uuid)
        starrez_booking = star_rez_get_booking(uuid)

        context = {
            'u': u,
            'person': person,
            'bbts_mm_bal': bbts_mm_bal,
            'bbts_gen_acc_trans': bbts_gen_acc_trans,
            'bbts_gen_acc_bal': bbts_gen_acc_bal,
            'bbts_dd_bal': bbts_dd_bal,
            'bbts_meal_plan': bbts_meal_plan,
            'bbts_meals_left': bbts_meals_left,
            'bbts_meal_reset': bbts_meal_reset,
            'ccure': ccure,
            'doors': doors,
            'ad_info': ad_info,
            'dept': dept,
            'off_campus_email': off_campus_email,
            'address': get_address,
            'classes': classes,
            'sr_booking': starrez_booking
        }

    return render(request, 'persons/user_profile.html', context)


# fix_uuid attempts to pad the front of a user or persons uuid with zeros until
# a status code of 200 is returned.  This is supposed to fix the uuid for pulling
# person images from colleague
def fix_uuid(person):
    uuid = person.uuid
    uuid = str(uuid)
    payload = {'id': uuid}
    res = requests.get(
        "https://vprodlbapi001.highpoint.edu/image.asp", params=payload)
    if res.status_code != 200:
        while res.status_code != 200 and len(uuid) < 7:
            uuid = "0" + uuid
            person.uuid = uuid
            payload = {'id': uuid}
            res = requests.get(
                "https://vprodlbapi001.highpoint.edu/image.asp", params=payload)
        return person
    return person


def get_time_stamp(list):
    if list != 'None':
        for dt in list:
            trans_date = dt["DateTime"]
            trans_date_ts = int(round(trans_date.timestamp())*1000)
            dt["JS_TimeStamp"] = trans_date_ts
    return list


def directory(request):
    return render(request, 'persons/directory.html')


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


# test view is for trying out new template features on a blank view
def test(request):
    u = request.user
    # Get currently logged in users persons record from vista
    person = Person.objects.get(user_id=u.id)
    person = fix_uuid(person)
    uuid = int(u.person.uuid)

    # Query for transactions, balance, and general account info
    bbts_mm_bal = magic_meal_balance(uuid)
    bbts_gen_acc_trans = passport_gen_acc_trans(uuid)
    bbts_gen_acc_bal = general_account_balance(uuid)
    bbts_dd_bal = dining_dollar_balance(uuid)
    bbts_meal_plan = meal_plan(uuid)
    bbts_meals_left = meals_left(uuid)
    bbts_meal_reset = meals_reset_on(uuid)

    context = {
        'u': u,
        'person': person,
        'bbts_mm_bal': bbts_mm_bal,
        'bbts_gen_acc_trans': bbts_gen_acc_trans,
        'bbts_gen_acc_bal': bbts_gen_acc_bal,
        'bbts_dd_bal': bbts_dd_bal,
        'bbts_meal_plan': bbts_meal_plan,
        'bbts_meals_left': bbts_meals_left,
        'bbts_meal_reset': bbts_meal_reset
    }
    return render(request, 'test/test.html', context)
