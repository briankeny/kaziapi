from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def get_username(self, user):
        return str(user.public_service_no)

    def create_user(self, public_service_no, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)

        if not public_service_no:
            raise ValueError('The Public Service Number must be set')

        user = self.model(public_service_no=public_service_no, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, public_service_no, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(public_service_no, password, **extra_fields)

    










