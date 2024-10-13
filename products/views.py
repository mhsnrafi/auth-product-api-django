from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Product, ProductReport
from .serializers import ProductSerializer
from django.core.exceptions import ObjectDoesNotExist

class DashboardView(APIView):
    """
    Displays the dashboard with a list of products for authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Renders the dashboard page with a list of products.

        Args:
        - request: The HTTP request object.

        Returns:
        - Rendered dashboard.html template with product data.
        """
        products = Product.objects.all()
        return render(request, 'dashboard.html', {'products': products, 'user_email': request.user.email})


class ProductCreateView(APIView):
    """
    Allows authenticated users to create new products.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Renders the product creation form for GET requests.

        Args:
        - request: The HTTP request object.

        Returns:
        - Rendered create_product.html template.
        """
        return render(request, 'create_product.html')

    def post(self, request, format=None):
        """
        Handles product creation for POST requests.

        Args:
        - request: The HTTP request object with product data.

        Returns:
        - Redirects to the dashboard after successful creation, or renders form with errors.
        """
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('dashboard')
        return render(request, 'create_product.html', {'form_errors': serializer.errors})

class ProductListView(APIView):
    """
    Lists all products for authenticated users.
    """
    def get(self, request, format=None):
        """
        Renders the product list in the dashboard for GET requests.

        Args:
        - request: The HTTP request object.

        Returns:
        - Rendered dashboard.html template with product data.
        """
        products = Product.objects.all()
        return render(request, 'dashboard.html', {'products': products, 'user_email': request.user.email})



class ProductSearchView(APIView):
    """
    Provides search functionality for products with sorting options.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Handles product search based on a query and sorts by specified fields.

        Args:
        - request: The HTTP request object with search and sorting data.

        Returns:
        - JSON response with filtered and sorted product data.
        """
        search_query = request.GET.get('query', '')
        sort_field = request.GET.get('sort_field', 'name')
        sort_direction = request.GET.get('sort_direction', 'asc')

        if sort_direction == 'desc':
            sort_field = f'-{sort_field}'

        products = Product.objects.filter(name__icontains=search_query).order_by(sort_field)
        data = list(products.values('id', 'name', 'description', 'price', 'available_stock'))
        return Response(data, status=status.HTTP_200_OK)

# Mark a product as selected by the user
class ProductSelectView(APIView):
    """
    Allows users to select a product.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id, format=None):
        """
        Handles product selection for authenticated users.

        Args:
        - request: The HTTP request object.
        - product_id: The ID of the product to be selected.

        Returns:
        - JSON response or redirect to dashboard if successful, or error message.
        """
        product = get_object_or_404(Product, id=product_id)

        if product.selected_by and product.selected_by != request.user:
            return Response({'error': 'Product already selected by another user.'}, status=status.HTTP_400_BAD_REQUEST)

        product.selected_by = request.user
        product.save()
        return Response({'status': 'Product selected successfully'}, status=status.HTTP_200_OK)

class ProductReportView(APIView):
    """
    Allows users to report a product with a reason.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id, format=None):
        """
        Handles product reporting by authenticated users.

        Args:
        - request: The HTTP request object with the report reason.
        - product_id: The ID of the product being reported.

        Returns:
        - Redirects to dashboard or renders an error page.
        """
        product = get_object_or_404(Product, id=product_id)
        reason = request.data.get('reason')
        ProductReport.objects.create(product=product, reported_by=request.user, reason=reason)
        return redirect('dashboard')
