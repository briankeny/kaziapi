import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import pre_save
from .permissions import add_User_To_Group
from .models import (User)


# Add Employee To Groups and update Their Permissions
@receiver(pre_save,sender =User)
def update_Employee_Group(sender, instance,**kwargs):
    try:
        user = instance
        account_type = user.objects.get('account_type',None)
        groups = add_User_To_Group(account_type)
        instance.groups.set(groups)
    except Exception as e:
        pass
 