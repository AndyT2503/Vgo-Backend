from django.db import models

class TimestampedModel(models.Model):
    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

        # By default, any model that inherits from `TimestampedModel` should
        # be ordered in reverse-chronological order. We can override this on a
        # per-model basis as needed, but reverse-chronological is a good
        # default ordering for most models.
        ordering = ['-created_at', '-updated_at']


class Profile(TimestampedModel):
    # As mentioned, there is an inherent relationship between the Profile and
    # User models. By creating a one-to-one relationship between the two, we
    # are formalizing this relationship. Every user will have one -- and only
    # one -- related Profile model.
    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE
    )
    #Each user profile will have a field where they can tell other users
    #something about themselves.
    bio = models.TextField(blank=True, null=True)

    image = models.URLField(blank=True, null=True)

    # This is an example of a Many-To-Many relationship where both sides of the
    # relationship are of the same model. In this case, the model is `Profile`.
    # As mentioned in the text, this relationship will be one-way. Just because
    # you are following mean does not mean that I am following you. This is
    # what `symmetrical=False` does for us.
    follows = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False
    )

    favorites = models.ManyToManyField('status.Status', related_name='favorited_by')


    def __str__(self):
        return self.user.name

    #Hàm thêm xóa follow
    def follow(self, profile):
        """Follow `profile` if we're not already following `profile`."""
        self.follows.add(profile)

    def unfollow(self, profile):
        """Unfollow `profile` if we're already following `profile`."""
        self.follows.remove(profile)

    def is_following(self, profile):
        """Returns True if we're following `profile`; False otherwise."""
        return self.follows.filter(pk=profile.pk).exists()

    def is_followed_by(self, profile):
        """Returns True if `profile` is following us; False otherwise."""
        return self.followed_by.filter(pk=profile.pk).exists()


    #Hàm thêm xóa Favorite
    def favorite(self, status):
        self.favorites.add(status)
    
    def unfavorite(self, status):
        self.favorites.remove(status)
    


    
    
