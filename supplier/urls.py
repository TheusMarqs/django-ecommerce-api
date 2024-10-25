from django.urls import path
from .views import SupplierCreate, SupplierDelete, SupplierUpdate, SupplierView, SupplierViewById

urlpatterns = [
    path('create', SupplierCreate.as_view()),
    path('', SupplierView.as_view()),
    path('update/<int:pk>', SupplierUpdate.as_view()),
    path('<int:pk>', SupplierViewById.as_view()),
    path('delete/<int:pk>', SupplierDelete.as_view()),
]
