from django.urls import path
from .views import CartCreate, CartDelete, CartUpdate, CartView, CartViewById, CartItemView

urlpatterns = [
    path('create', CartCreate.as_view()),
    path('', CartView.as_view(), name='cart'),
    path('item', CartItemView.as_view(), name='cart-item'),
    path('update/<int:pk>', CartUpdate.as_view()),
    path('<int:pk>', CartViewById.as_view()),
    path('delete/<int:pk>', CartDelete.as_view()),
]
