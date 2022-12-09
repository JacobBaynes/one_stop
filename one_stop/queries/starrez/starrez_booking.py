from requests.auth import HTTPBasicAuth
import requests
from decouple import config


def star_rez_get_booking(uuid):
    '''
    Send API GET request with STARQL query.
    :return Dataframe df:
    '''

    # See StarRez API Guide for info on how to create STARQL queries: https://support.starrez.com/hc/en-us/articles/360056850292-StarRez-REST-2-0-Web-Services-API-Guide?auth_token=eyJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2lkIjo1NzU2NDksInVzZXJfaWQiOjEwNDI2MTE5MjMsInRpY2tldF9pZCI6MzAzNDIzLCJjaGFubmVsX2lkIjo2MywidHlwZSI6IlNFQVJDSCIsImV4cCI6MTY0NjM0MzEwNH0.WNdErQECjDM2e3yMi70IVI_-kYazcN7Rqws_zAAyUUE&source=search
    query = '''
SELECT
    RoomLocation.Description AS Building,
    RoomSpace.Description AS RoomSpace,
    RoomType.Description AS RoomType,
    Entry.ID1 AS ID,
    TermSession.Description as Term,
    Booking.BookingID
From
    Booking
    INNER JOIN RoomType ON Booking.RoomTypeID = RoomType.RoomTypeID
    INNER JOIN Entry ON Booking.EntryID = Entry.EntryID
    INNER JOIN RoomSpace ON Booking.RoomSpaceID = RoomSpace.RoomSpaceID
    INNER JOIN EntryDetail ON Entry.EntryID = EntryDetail.EntryID
    INNER JOIN RoomBase ON RoomSpace.RoomBaseID = RoomBase.RoomBaseID
    INNER JOIN RoomLocation ON RoomBase.RoomLocationID = RoomLocation.RoomLocationID
    INNER JOIN TermSession on Booking.TermSessionID = TermSession.TermSessionID
WHERE
    (
        (
            Booking.CheckInDate <= DATETIME
            AND ADD(Booking.CheckOutDate, 20, hours) >= DATETIME
            AND EntryDetail.ClassificationID >= 1
            AND Booking.EntryStatusEnum IN (5, 2)
        )
        OR (
            Booking.CheckInDate <= ADD(DATETIME, 7, days)
            AND EntryDetail.ClassificationID >= 1
            AND Booking.EntryStatusEnum IN (5, 2)
        )
        )
''' + f" AND Entry.ID1 = '{uuid}'"

    try:
        header = {
            "accept": "application/json"
        }
        params = {
            "q": query
        }
        # Send API request and get JSON representation of data
        send_request = requests.get(url=config('SR_API_URL') + '/query',
                                    auth=HTTPBasicAuth(username=config('SR_USERNAME'),
                                                       password=config('SR_PASS')),  # StarRez password is a token created in StarRezWeb account
                                    headers=header,
                                    params=params)
    except Exception as e:
        # log any errors from API call
        print(f'{e}')
    response = send_request.json()
    if len(response):
        return response
    else:
        return 'None'


# star_rez_get_booking('1833024')
