from django.contrib import admin
from django.urls import include, path
from .views import CustomLoginView, CustomRegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/', include('product.urls')),
    path('category/', include('category.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/loginn/', CustomLoginView.as_view(), name='rest_loginn'),
    path('auth/registrationn/', CustomRegisterView.as_view(), name='rest_registrationn'),

]
