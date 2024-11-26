from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from authentication.models import BlacklistedToken

class UserRegister(APIView):
    def post(self, request):
        try:
            data = JSONParser().parse(request)

            # Verifica se o email já está em uso
            if User.objects.filter(email=data['email']).exists():
                return Response({'error': 'Este e-mail já está em uso.'}, status=status.HTTP_400_BAD_REQUEST)

            user = User(
                email=data['email'],
                username=data['username'],
                first_name=data['first_name'],
                last_name=data['last_name'],
            )
            user.set_password(data['password'])
            user.save()

            # Gera o token JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            return Response({
                'message': 'Usuário criado com sucesso',
                'access_token': access_token,
                'refresh_token': str(refresh),
                'username': user.username,
                'user_id': user.id,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
            
            # response.set_cookie(
            #     key='refresh_token',
            #     value=str(refresh),
            #     httponly=False,
            #     secure=False,
            #     samesite='Strict',
            # )
            
            # response.set_cookie(
            #     key='access_token',
            #     value=access_token,
            #     secure=False,
            #     httponly=True,  # Impede acesso via JavaScript
            #     # secure=True,  # Apenas via HTTPS
            #     samesite='Strict',  # Evita CSRF em outros sites
            #     max_age=3600,  # Tempo de expiração (1 hora)
            # )
            
            # response.set_cookie(
            #     key='username',
            #     value=user.username,
            #     secure=False,
            #     httponly=True, 
            #     # secure=True,
            #     samesite='Strict',
            #     max_age=3600,
            # )
            
            # response.set_cookie(
            #     key='email',
            #     value=user.email,
            #     httponly=True, 
            #     # secure=True,
            #     secure=False,
            #     samesite='Strict',
            #     max_age=3600,
            # )
            
            # response.set_cookie(
            #     key='id',
            #     value=user.id,
            #     httponly=True, 
            #     # secure=True,
            #     # samesite='Strict',
            #     secure=False,
            #     samesite='Strict',
            #     max_age=3600,
            # )
            
            
        except Exception as e:
            return Response({'error': 'Erro desconhecido: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def http_method_not_allowed(self, request):
        return Response({
            'detail': 'Method not allowed'
        },  status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
class UserLogin(APIView):
    def post(self, request):
        data = JSONParser().parse(request)

        # Autenticar o usuário
        user = authenticate(username=data['username'], password=data['password'])
        
        if user is not None:
            # Gerar os novos tokens JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Se você tiver algum lugar para armazenar o refresh_token, pode salvar aqui

            # Retornar a resposta com os tokens e informações do usuário
            username = user.username
            user_id = user.id
            email = user.email
            is_superuser = user.is_superuser
            

            return Response({
                'message': 'Login bem-sucedido',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'username': username,
                'user_id': user_id,
                'email': email,
                'is_superuser': is_superuser
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

    def http_method_not_allowed(self, request):
        return Response({
            'detail': 'Method not allowed'
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]

            # Adicionar o token à blacklist personalizada
            BlacklistedToken.objects.create(
                token=str(refresh_token),
                expires_at=BlacklistedToken.calculate_expiration()
            )
            return Response({"detail": "Logout realizado com sucesso."})
        except Exception as e:
            return Response({"detail": "Erro ao realizar logout: " + str(e)}, status=400)

        
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        if BlacklistedToken.objects.filter(token=refresh_token).exists():
            raise InvalidToken("Token inválido ou já utilizado.")
        return super().post(request, *args, **kwargs)