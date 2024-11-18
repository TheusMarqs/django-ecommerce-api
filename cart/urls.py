from django.urls import path
from .views import CartCreate, CartDelete, CartUpdate, CartView, CartViewById

urlpatterns = [
    path('create', CartCreate.as_view()),
    path('', CartView.as_view()),
    path('update/<int:pk>', CartUpdate.as_view()),
    path('<int:pk>', CartViewById.as_view()),
    path('delete/<int:pk>', CartDelete.as_view()),
]
