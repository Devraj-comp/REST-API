from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.conf import settings

# Create your models here.

class UserProfileManager(BaseUserManager):
    """manager for user profiles"""

    def create_user(self,email,name,password=None):
        """create a new userprofile"""
        if not email:
            raise ValueError("users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,name,password):
        """create and save a new super user"""
        user = self.create_user(email,name,password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser,PermissionsMixin):
    """database model for users in the system"""

    email = models.EmailField(max_length=256,unique=True)
    name = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """retrieve full name of user"""
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        """return string representation of our users"""

        return self.email

class ProfileFeedItem(models.Model):
    """profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )
    status_text = models.CharField(max_length=256)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """return the model as a string"""
        return self.status_text