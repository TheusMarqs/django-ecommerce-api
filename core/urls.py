from django.contrib import admin
from django.urls import include, path
from authentication.views import CustomLoginView, CustomRegisterView, CustomLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/', include('product.urls')),
    path('category/', include('category.urls')),
    path('order/', include('order.urls')),
    path('supplier/', include('supplier.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/loginn/', CustomLoginView.as_view(), name='rest_loginn'),
    path('auth/registrationn/', CustomRegisterView.as_view(), name='rest_registrationn'),
    path('auth/logoutt/', CustomLogoutView.as_view())

]
