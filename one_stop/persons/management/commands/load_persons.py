from django.core.management.base import BaseCommand, CommandError
from persons.models import Person
from django.contrib.auth.models import User
import json


# from: https://docs.djangoproject.com/en/3.2/howto/custom-management-commands/
class Command(BaseCommand):
    help = 'load users'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **options):
        # todo: add check for local directory -- make more secure/stable
        print(options['file'])
        # open our json file and parse
        try:
            self.stdout.write(self.style.NOTICE(
                'reading from file: "%s"' % options['file']))
            json_file = options['file']
            with open(json_file, 'r') as jf:
                json_data = jf.read()
            data = json.loads(json_data)

            # work with data
            for p in data:
                # create user
                user = User()
                if p['email'] == None:
                    continue
                else:
                    username = p['email'].split('@')
         
                user.first_name = p['fname']
                user.last_name = p['lname']
                user.username = username[0]
                user.email = p['email']
                user.save()

                # populate person data
                person = Person()
                person.user = user
                person.sys_ID = user.id
                person.uuid = p['id']
                person.classification = p['classification']
                person.dob = p['dob']
                person.ssn = p['ssn']
                person.fname = user.first_name
                person.lname = user.last_name
                person.phone = p['phone']
                person.email = p['email']
                person.mname = p['mname']
                person.campusbox = p['campusbox']
                person.campusroom = p['campusroom']
                person.current = p['current']
                person.preferred_name = p['preferred_name']
                person.position = p['position']
                person.stutype = p['stutype']
                person.class_level = p['class_level']
                person.cardnumber = p['cardnumber']
                person.housed = p['housed']
                person.save()

                # user = User()
                # username = p['fields']['email'].split('@')
                # user.first_name = p['fields']['fname']
                # user.last_name = p['fields']['lname']
                # user.username = username[0]
                # user.email = p['fields']['email']
                # user.save()

                # # populate person data
                # person = Person()
                # person.user = user
                # person.sys_ID = user.id
                # person.uuid = p['fields']['uuid']
                # person.classification = p['fields']['classification']
                # person.dob = p['fields']['dob']
                # person.fname = user.first_name
                # person.lname = user.last_name
                # person.phone = p['fields']['phone']
                # person.email = p['fields']['email']
                # person.mname = p['fields']['mname']
                # person.campusbox = p['fields']['campusbox']
                # person.campusroom = p['fields']['campusroom']
                # person.current = p['fields']['current']
                # person.preferred_name = p['fields']['preferred_name']
                # person.position = p['fields']['position']
                # person.stutype = p['fields']['stutype']
                # person.class_level = p['fields']['class_level']
                # person.cardnumber = p['fields']['cardnumber']
                # person.housed = p['fields']['housed']
                # person.save()

            # report success
            self.stdout.write(self.style.SUCCESS(
                'loaded users from "%s"' % options['file']))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                'error loading users from "%s"' % options['file']))
            print(e)
