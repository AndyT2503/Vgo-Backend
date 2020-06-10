from rest_framework import serializers
from profile.serializers import ProfileSerializer
from .models import Status

class StatusSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer(read_only=True)
    slug = serializers.SlugField(required=False)
    
    #Thời điểm khởi tạo
    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')
    class Meta:
        models = Status
        fields = ('profile', 'slug', 'title', 'content', 'createdAt', 'updatedAt',)

    def create(self, validated_data):
        profile= self.context.get('profile', None)

        status = Status.objects.create(profile=profile, **validated_data)

        return status

    def get_created_at(self, instance):
        return instance.created_at.isoformat()
    
    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()