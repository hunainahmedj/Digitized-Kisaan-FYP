from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager

from farm.models import Farm


class UserManager(BaseUserManager):

    def create_user(self, email, first_name, middle_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("Please provide a password for authentication")
        if not first_name:
            raise ValueError("First name is required")
        if not last_name:
            raise ValueError("Last name is required")
        email = self.normalize_email(email)
        user_obj = self.model(
            email=email, **extra_fields
        )

        user_obj.set_password(password)
        user_obj.first_name = first_name
        user_obj.middle_name = middle_name
        user_obj.last_name = last_name
        # user_obj.staff = False
        # user_obj.is_admin = is_admin
        # user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    # def create_staffuser(self, email, first_name, middle_name, last_name, password=None):
    #     user = self.create_user(
    #         email,
    #         first_name,
    #         middle_name,
    #         last_name,
    #         password = password,
    #         is_staff = True
    #     )
    #     return user

    def create_superuser(self, email, first_name, middle_name, last_name, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)


        user = self.create_user(
            email,
            first_name,
            middle_name,
            last_name,
            password = password,
            **extra_fields
        )
        return user

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    managed_farms = models.ManyToManyField(Farm)

    is_active = models.BooleanField(default=True)     # is the account active or not
    is_staff = models.BooleanField(default=True)     # is a staff or an admin

    USERNAME_FIELD = 'email'  # username and password are required by default

    REQUIRED_FIELDS = ['first_name', 'middle_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return "{} {} {}".format(self.first_name, self.middle_name, self.last_name)

    def get_email(self):
        return self.email

    def get_full_name(self):
        if self.middle_name != None:
            return f'{self.first_name} {self.middle_name} {self.last_name}'
        else:
            return f'{self.first_name} {self.last_name}'
        

    # @property
    # def staff(self):
    #     return self.is_staff
    #
    # @property
    # def is_admin(self):
    #     return self.is_admin
    #
    # @property
    # def active(self):
    #     return self.is_active

    # def has_perm(self, perm, obj=None):
    #     return True
    #
    # def has_module_perms(self, app_label):
    #     return True

