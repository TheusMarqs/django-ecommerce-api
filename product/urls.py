from django.urls import path
from .views import ProductCreate, ProductView, ProductUpdate, ProductViewById, ProductDelete, ProductViewByCode

urlpatterns = [
    path('create', ProductCreate.as_view()),
    path('update/<int:pk>', ProductUpdate.as_view()),
    path('<int:pk>', ProductViewById.as_view()),
    path('', ProductView.as_view()),
    path('delete/<int:pk>', ProductDelete.as_view()),
    path('code', ProductViewByCode.as_view())
]
