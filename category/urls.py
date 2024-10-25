from django.urls import path
from .views import CategoryCreate, CategoryUpdate, CategoryView, CategoryViewById, CategoryDelete

urlpatterns = [
    path('create', CategoryCreate.as_view()),
    path('', CategoryView.as_view()),
    path('update/<int:pk>', CategoryUpdate.as_view()),
    path('<int:pk>', CategoryViewById.as_view()),
    path('delete/<int:pk>', CategoryDelete.as_view()),
]
