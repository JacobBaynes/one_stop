# PurplePages

## Description
PurplePages is a new version of the old milan/onecard application. It's purpose is to provide students with up to date information
about their Black Board account transactions, meal plan balances, and account balances. It also has a dining locations page that lists on campus locations where students, faculty, and staff can use their one card.

PurplePages is also meant to be a one stop shop for concierge, security, and IT users to quickly search for anyone in the HPU system.
Depending on the users status, they will have permissions to search users, view searched users Black Board transaction information, Active Directory information, and CCure clearance and account data.

This application has the potential to consume other applications used by HPU, such as singapore, and possibly incorporate more features specific to security and concierge users.

## Installation
To contribute to this application, you need Python, Django, and virtual environment, and a multitude of packages.

### 1. Create directory on your machine in a place of your choosing, cd into this folder, and Clone repo:
```
mkdir purple_pages
cd purple_pages
git clone https://github.com/hpuit/PurplePages.git
```

### 2. If you don't have Python
https://www.python.org/downloads/. Download the newest stable version

### 3. Create a virtual environment
```
# Windows
c:\> python -m venv venv
# or
c:\> c:\Python35\python -m venv c:\path\to\venv
# Unix
$ python3 -m venv ./venv
```

### 4. Activate virtual environment
```
# Windows
c:\> venv\Scripts\activate.bat
# Unix
$ source venv/bin/activate
```

### 5. Install dependencies
```
pip install -r requirements.txt
```

## Dependencies

#### Datatables.net
The Black Board Transactions table and the search users directory table are powered by Datatables.net. The requirements.txt file
should install djangorestframework-datatables.
- https://datatables.net/
- https://pypi.org/project/djangorestframework-datatables/

#### LDAP
The main authentication backend for PurplePages is django-auth-ldap which require python-ldap
- https://django-auth-ldap.readthedocs.io/en/latest/
- https://pypi.org/project/python-ldap/

## Database Settings

Contact Admin for settings.ini file to access credentials

settings.py uses python-decouple and dj-database-url to retrieve values from settings.ini
to populate django SECRET_KEY, user names, passwords, and ALLOWED_HOSTS
- https://pypi.org/project/python-decouple/
- https://github.com/kennethreitz/dj-database-url#id5

## Production
### Linux package dependencies

python-ldap
```
sudo apt-get install libsasl2-dev libldap2-dev libssl-dev
```
cx_Oracle
```
sudo apt-get install libaio1 
```
pillow
```
sudo apt-get install libjpeg8-dev
```
cx_Oracle installation (adjust for version installed):1
https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html#oracle-instant-client-zip-files

zip file location:
https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html

Follow odbc instructions for ubuntu:

https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15#ubuntu17

fill out /etc/odbc.ini file (need to use file for driver, not nice name, ie SQL Server Native Client 11):

```
[vprodsec002]
Description = vprodsec002
Driver = /opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.8.so.1.1
Server = tcp:vprodsec002.highpoint.edu,1433
Database = ACVSCore
UID = ccure_integration
PWD = <yourpassword>
```

you should be able to verify that the odbc connection will work by using the following command:
```
isql vprodsec002 ccure_integration <yourpassword>-v
```

### uwsgi
```
[uwsgi]
module = purple_pages.wsgi:application

plugin = python38
home = /srv/milan_2022/venv
virtualenv = /srv/milan_2022/venv

chmod-socket = 666
chown-socket = www-data:www-data
uid = www-data
gid = www-data

master = true
processes = 5
threads = 2

socket = /var/run/uwsgi/milan_2022.sock
#chmod-socket = 660
vacuum = true

die-on-term = true
logto = /var/log/uwsgi/milan_2022.log
```
