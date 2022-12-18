from django.db import models

from accounts.models import Group


class PrivilegeManager(models.Manager):

    def get_queryset(self):
        return super(PrivilegeManager, self).get_queryset().filter(

        )
