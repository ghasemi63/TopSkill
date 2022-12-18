from django.db import models

from accounts.models import Group


class PositionManager(models.Manager):

    def get_queryset(self):
        return super(PositionManager, self).get_queryset().filter(

        )
