from django.contrib import admin
from . import models

# from restapi.models import UserProfile,ProfileFeedItem
# Register your models here.

admin.site.register(models.UserProfile)
admin.site.register(models.ProfileFeedItem)