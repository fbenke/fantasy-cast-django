from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import SignupSerializer


class Signup(APIView):

    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)


class Signin(ObtainAuthToken):

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {'token': token.key, 'email': user.email,
             'user_id': user.pk, 'username': user.username}
        )


class Signout(APIView):

    def post(self, request):

        if request.auth is not None:
            request.auth.delete()

        return Response()
