from rest_framework.renderers import JSONRenderer
import json
from profile.renderers import ConduitJSONRenderer

class StatusJSONRenderer(ConduitJSONRenderer):
    object_label = 'status'
    pagination_object_label = 'statuses'
    pagination_count_label = 'statusesCount'