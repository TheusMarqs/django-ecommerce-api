from dj_rest_auth.views import LoginView
from rest_framework.response import Response

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
