from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


ROLE_CHOICES = (
    ('', '---------'),
    (1, 'RECRUITER'),
    (2, 'HR_MANAGER'),
    (3, 'TEAM_MANAGER'),
    (4, 'CORDINATOR'),
    (5, 'BUSINESS_PARTNER'),
    (6, 'PARTNER'),
    (0, 'OTHERS')
)


# class Role(models.Model):
#   id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)
#
#   def __str__(self):
#       return self.get_id_display()


class User(AbstractUser):
    CANDIDATE = 1
    CUSTOMER = 2
    EMPLOYEE = 3
    USER_TYPE_CHOICES = (
        (CANDIDATE, 'CANDIDATE'),
        (CUSTOMER, 'CUSTOMER'),
        (EMPLOYEE, 'EMPLOYEE')
    )
    user_type = models.PositiveSmallIntegerField(null=True, blank=True, choices=USER_TYPE_CHOICES)
    # roles = models.ManyToManyField(Role)
    roles = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=0)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username + " _ " + self.first_name
