from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Product, ProductReport
from .serializers import ProductSerializer
from django.core.exceptions import ObjectDoesNotExist



class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if request.user.is_authenticated:
            products = Product.objects.all()  # Or filter if needed
            return render(request, 'dashboard.html', {
                'products': products,
                'user_email': request.user.email
            })
        else:
            return redirect('login')

# Admin users can create products
class ProductCreateView(APIView):
     # Ensure only authenticated users can create products

    def get(self, request, format=None):
        return render(request, 'create_product.html')

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('dashboard')
        return render(request, 'create_product.html', {'form_errors': serializer.errors})

    def post(self, request, format=None):
        # Handle product creation logic
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('dashboard')  # Redirect to dashboard after successful creation
        return render(request, 'create_product.html', {'form_errors': serializer.errors})

# View for fetching the logged-in user's email and the product list
class ProductListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        products = Product.objects.all()
        return render(request, 'dashboard.html', {'products': products, 'user_email': request.user.email})


# Search functionality for products with sorting options
# Search functionality for products with sorting options
class ProductSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
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
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id, format=None):
        try:
            product = Product.objects.get(id=product_id)
            product.selected_by = request.user
            product.save()

            # After successfully selecting the product, redirect or render a success page
            return redirect('dashboard')  # You can redirect to the dashboard or render a success template

        except Product.DoesNotExist:
            # If the product is not found, render an error page
            return render(request, 'product_error.html', {'error': 'Product not found'})




class ProductSelectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id, format=None):
        # Get the product by ID
        product = get_object_or_404(Product, id=product_id)

        # Check if the product is already selected by another user
        if product.selected_by and product.selected_by != request.user:
            return Response({'error': 'Product already selected by another user.'}, status=status.HTTP_400_BAD_REQUEST)

        # Mark the product as selected by the current user
        product.selected_by = request.user
        product.save()

        # Optionally redirect to the dashboard page to refresh the UI
        if request.accepted_renderer.format == 'html':
            return redirect('dashboard')

        # For JSON response (API-based interaction)
        return Response({'status': 'Product selected successfully'}, status=status.HTTP_200_OK)

    def get(self, request, product_id, format=None):
        # Handle GET requests to render a page (if needed)
        product = get_object_or_404(Product, id=product_id)
        return render(request, 'product_detail.html', {'product': product})

# Report a product with a reason
class ProductReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id, format=None):
        reason = request.data.get('reason')
        try:
            product = Product.objects.get(id=product_id)
            ProductReport.objects.create(product=product, reported_by=request.user, reason=reason)
            return redirect('dashboard')
        except Product.DoesNotExist:
            return render(request, 'dashboard.html', {'error': 'Product not found'})


