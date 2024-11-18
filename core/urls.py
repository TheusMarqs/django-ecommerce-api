from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/', include('product.urls')),
    path('category/', include('category.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('supplier/', include('supplier.urls')),
    path('auth/', include('authentication.urls')),
    path('token/verify', TokenVerifyView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
