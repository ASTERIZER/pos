# urls.py

from django.urls import path
from .views import item_list, item_detail, generate_bill, add_item

urlpatterns = [
    path('items/', item_list),
    path('items/<int:pk>/', item_detail),
    path('generate-bill/', generate_bill),
    path('add-item/', add_item),
]
