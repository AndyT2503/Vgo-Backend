from django.db import models
from profile.models import TimestampedModel

class Status(TimestampedModel):

    #url cua post
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    #profile tao status
    profile = models.ForeignKey('profile.Profile', on_delete=models.CASCADE, related_name='statuses')
    title = models.CharField(max_length = 100)
    image = models.URLField(blank=True, null=True)
    content = models.TextField()

    def __str__(self):
        return (self.title, self.content)
