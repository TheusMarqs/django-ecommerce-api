from django.urls import path
from .views import OrderCreate, OrderDelete, OrderUpdate, OrderView, OrderViewById

urlpatterns = [
    path('create', OrderCreate.as_view()),
    path('', OrderView.as_view()),
    path('update/<int:pk>', OrderUpdate.as_view()),
    path('<int:pk>', OrderViewById.as_view()),
    path('delete/<int:pk>', OrderDelete.as_view()),
]
