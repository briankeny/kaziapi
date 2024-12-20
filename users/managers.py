from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def get_mobile_number(self, user):
        return str(user.mobile_number)

    def create_user(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)

        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(mobile_number, password, **extra_fields)

    










