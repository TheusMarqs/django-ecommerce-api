from django.urls import path
from .views import CategoryCreate, CategoryUpdate, CategoryView, CategoryViewById

urlpatterns = [
    path('create', CategoryCreate.as_view()),
    path('', CategoryView.as_view()),
    path('update/<int:pk>', CategoryUpdate.as_view()),
    path('<int:pk>', CategoryViewById.as_view())
]
