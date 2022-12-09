from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import (
    post_save
)


@receiver(post_save, sender=User)
def user_created_handler(sender, instance, created, *args, **kwargs):

    if created:
        print(instance.username, 'Was created')

    else:
        print(instance.username, 'Was just saved')


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sys_ID = models.AutoField(primary_key=True)
    classification = models.CharField(max_length=25, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    mname = models.CharField(
        'Middle Name', max_length=50, blank=True, null=True)
    dob = models.DateField('Date of Birth', null=True)
    ssn = models.CharField('SSN Last Four', max_length=4,
                           blank=True, null=True)
    campusbox = models.CharField(
        'Campus Box', max_length=25, null=True, blank=True)
    campusroom = models.CharField(
        'Campus Room', max_length=100, null=True, blank=True)
    created_at = models.DateField(null=True, blank=True)
    current = models.CharField(max_length=40)
    preferred_name = models.CharField(max_length=40, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    stutype = models.CharField(
        'Student Type', max_length=40, blank=True, null=True)
    class_level = models.CharField(max_length=40, null=True)
    cardnumber = models.IntegerField('Card Number', null=True)
    housed = models.IntegerField(blank=True)
    uuid = models.IntegerField('HPU ID')

    class Meta:
        permissions = [
            ("view_ssn", "Can view ssn number"),
            ("security", "Can view security staff features"),
            ("help_desk", "Can view help desk staff features"),
            ("concierge", "Can view concierge staff features")
        ]

    def __str__(self):
        return self.user.first_name
