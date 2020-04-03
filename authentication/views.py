from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer
#renders help format return json to client
from .renderers import UserJSONRenderer

class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    # Set serializer class
    serializer_class = RegistrationSerializer
    # Set UserJSONRenderer as renderer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get('user', {})

        #validate by RegistrationSerializer
        serializer = self.serializer_class(data=user)
        #raise_exception true to handle and return JSON format ValidationErrors to client
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)