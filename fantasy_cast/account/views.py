from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import SignupSerializer, AuthTokenSerializer


class Signup(APIView):

    serializer_class = SignupSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Signin(APIView):

    serializer_class = AuthTokenSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            authenticated_user = serializer.validated_data.get('user')
            token, created = Token.objects.get_or_create(
                user=authenticated_user)
            return Response({'token': token.key})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
