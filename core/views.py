from dj_rest_auth.views import LoginView
from rest_framework.response import Response
from dj_rest_auth.registration.views import RegisterView
from django.contrib.auth import login, authenticate

class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            user = self.get_user(request)
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                # Adicione outros campos que você deseja retornar
            }
            response.data.update({'user': user_data})
        
        return response
    
    def get_user(self, request):
        return request.user

from dj_rest_auth.views import LoginView
from rest_framework.response import Response
from dj_rest_auth.registration.views import RegisterView
from rest_framework.authtoken.models import Token

class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            user = self.get_user(request)
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                # Adicione outros campos que você deseja retornar
            }
            response.data.update({'user': user_data})
        
        return response
    
    def get_user(self, request):
        return request.user

class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        if response.status_code == 204:
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
        
        return Response({}, status=204)