from rest_framework.renderers import JSONRenderer


class ProfileJSONRenderer(JSONRenderer):
    object_label = 'profile'
    pagination_object_label = 'profiles'
    pagination_count_label = 'profilesCount'