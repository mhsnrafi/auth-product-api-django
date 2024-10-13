from django.urls import path
from .views import ProductListView, ProductSearchView, ProductCreateView, ProductSelectView, ProductReportView

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),  # List products
    path('search/', ProductSearchView.as_view(), name='product-search'),  # Search products
    path('create/', ProductCreateView.as_view(), name='create-product'),  # Create products
    path('select/<int:product_id>/', ProductSelectView.as_view(), name='product-select'),  # Select product
    path('report/<int:product_id>/', ProductReportView.as_view(), name='product-report'),  # Report product
]
