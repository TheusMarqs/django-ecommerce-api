from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/', include('product.urls')),
    path('category/', include('category.urls')),
    path('order/', include('order.urls')),
    path('supplier/', include('supplier.urls')),
    path('auth/', include('authentication.urls')),
    path('token/verify', TokenVerifyView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
]
