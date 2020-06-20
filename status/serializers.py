from rest_framework import serializers
from profile.serializers import ProfileSerializer
from .models import Status, Comment

class StatusSerializer(serializers.ModelSerializer):

    author = ProfileSerializer(read_only=True)
    slug = serializers.SlugField(required=False)
    image = serializers.SerializerMethodField()
    #Thời điểm khởi tạo
    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')
    class Meta:
        models = Status
        fields = ('author', 'slug', 'title', 'image','location', 'content', 'createdAt', 'updatedAt',)

    def get_image(self, obj):
        if obj.image:
            return obj.image
    def create(self, validated_data):
        author= self.context.get('author', None)

        status = Status.objects.create(author=author, **validated_data)

        return status

    def get_created_at(self, instance):
        return instance.created_at.isoformat()
    
    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()


class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(required=False)

    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'body',
            'createdAt',
            'updatedAt',
        )

    def create(self, validated_data):
        status = self.context['status']
        author = self.context['author']

        return Comment.objects.create(
            author=author, status=status, **validated_data
        )

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()

