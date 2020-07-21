from  django.urls import path
from .views import (
    ExpenseListAPIView, ExpenseDetailAPIView)

urlpatterns = [
    path('', ExpenseListAPIView.as_view(), name='expenses'),
    path('<int:id>', ExpenseDetailAPIView.as_view(), name='expense')
]