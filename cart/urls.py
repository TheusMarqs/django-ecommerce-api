from django.urls import path
from .views import CartClean, CartView, CartViewById, CartItemCreate, CartItemDelete

urlpatterns = [
    path('', CartView.as_view()),
    path('item/create', CartItemCreate.as_view()),
    path('item/delete', CartItemDelete.as_view()),
    path('<int:pk>', CartViewById.as_view()),
    path('delete', CartClean.as_view()),
]
