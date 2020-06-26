from django.contrib import admin

# Register your models here.
from authentication.models import User, Image

admin.site.register(User)
admin.site.register(Image)