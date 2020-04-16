#pip install PyJWT
import jwt

from datetime import datetime, timedelta

from django.conf import settings

# custom base authen default of django
#document to custom https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#substituting-a-custom-user-model
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models

# from core.models import TimestampedModel

#class UserManager to override BaseUserManager from django.
class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free. 

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, name, email, image=None, password=None):
        #add validate username password.
        if name is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')
        user = self.model(name=name, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        if image:
            avatar = Image(user=user)
            avatar.file = image['file']
            avatar.save()

        return user

    def create_superuser(self, name, email, password):
    #   """
    #   Create and return a `User` with superuser powers.

    #   Superuser powers means that this use is an admin that can do anything
    #   they want.
    #   """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(name, email, password)
        user.is_superuser = True
        user.save()

        return user

#Override User of Django AbstractBaseUser
class User(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(db_index=True, max_length=255)

    email = models.EmailField(db_index=True, unique=True)

    

    # followings = models.ManyToManyField(
    #     'self',
    #     related_name='followed_by',
    #     symmetrical=False
    # )

    #setting field use to authen.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.email

    @property
    def token(self):
        #create token by _generate_jwt_token
        return self._generate_jwt_token()

    def get_full_name(self):
        #method default of user, return first name and lastname field. custom to return username.
        return self.name

    def get_short_name(self):
        #like get_full_name
        return self.name

    def _generate_jwt_token(self):
        #Create jwt token with 60 days of expiration
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

   

class Image(models.Model):
    user = models.OneToOneField(User, models.DO_NOTHING)
    file = models.ImageField(upload_to='images/')