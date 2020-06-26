from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from vgo.apps.core.models import TimestampedModel

def upload_location(instance, filename, **kwargs):
	file_path = 'post/{author_id}/{title}-{filename}'.format(
			author_id=str(instance.author.id), title=str(instance.title), filename=filename
		) 
	return file_path

class Post(TimestampedModel):
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    title = models.CharField(db_index=True, max_length=255)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    point = models.IntegerField(default=1, validators=[MaxValueValidator(10),
            MinValueValidator(1)])
    
    location = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField()
    body = models.TextField()
    #geolocation = map_fields.GeoLocationField(max_length=100, null=True, blank=True)

    # Every post must have an author. This will answer questions like "Who
    # gets credit for writing this post?" and "Who can edit this post?".
    # Unlike the `User` <-> `Profile` relationship, this is a simple foreign
    # key (or one-to-many) relationship. In this case, one `Profile` can have
    # many `Post`s.
    author = models.ForeignKey(
        'authentication.User', on_delete=models.CASCADE, related_name='posts'
    )

    def __str__(self):
        return self.title

class Comment(TimestampedModel):
    body = models.TextField()

    post = models.ForeignKey(
        'post.Post', related_name='comments', on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        'authentication.User', related_name='comments', on_delete=models.CASCADE
    )



                              
