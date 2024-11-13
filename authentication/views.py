from dj_rest_auth.views import LoginView
from rest_framework.response import Response
from dj_rest_auth.registration.views import RegisterView
from django.contrib.auth import login, authenticate
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from dj_rest_auth.views import LoginView
from rest_framework.response import Response
from dj_rest_auth.registration.views import RegisterView
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken


class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Verifica se a autenticação foi bem-sucedida
        if response.status_code == 200:
            # Obtém o usuário autenticado
            user = self.get_user_from_response(response)

            # Tenta obter um refresh token existente
            refresh_token = self.get_existing_refresh_token(user)

            if refresh_token:
                # Se já existir um token na blacklist, busca o token válido
                response.data['refresh'] = str(refresh_token)
            

        return response

    def get_user_from_response(self, response):
        user_id = response.data.get('user', {}).get('pk')
        User = get_user_model()
        return User.objects.get(pk=user_id)

    def get_existing_refresh_token(self, user):
        try:
            # Verifica se existe um token outstanding (não blacklistado)
            token = OutstandingToken.objects.filter(user=user).first()
            return token
        except OutstandingToken.DoesNotExist:
            return None

class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        username = request.data.get('username')
        password = request.data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)  # Autentica o usuário
        
        token, created = Token.objects.get_or_create(user=user)
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            # Adicione outros campos que você deseja retornar
        }
        return Response({
            'token': token.key,
            'user': user_data
        }, status=201)
        
    
class CustomLogoutView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                # Coloca o refresh token na blacklist
                token = RefreshToken(refresh_token)
                token.blacklist()

            # Apaga os cookies de acesso e refresh tokens
            response = Response({"message": "Logout realizado com sucesso."}, status=status.HTTP_204_NO_CONTENT)
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response

        except Exception as e:
            return Response({"error": "Falha ao realizar logout."}, status=status.HTTP_400_BAD_REQUEST)