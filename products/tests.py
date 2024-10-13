from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User
from products.models import Product, ProductReport


class ProductTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass123', name='Test User', tc=True)
        self.client.login(email='testuser@example.com', password='testpass123')
        self.product = Product.objects.create(
            name="Product 1", description="A test product", price=10.00, available_stock=100
        )

    def test_get_products(self):
        url = reverse('product-list')
        response = self.client.get(url)

        # Check if the response is an HTML page or JSON response
        if response.headers['Content-Type'] == 'application/json':
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(len(response.json()) > 0)
        else:
            self.assertContains(response, "Product 1")

    def test_search_products(self):
        url = reverse('product-search') + '?query=Product'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Product 1', str(response.data))

    def test_create_product(self):
        url = reverse('create-product')
        data = {
            'name': 'Product 2',
            'description': 'Another test product',
            'price': 20.00,
            'available_stock': 50
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(Product.objects.filter(name='Product 2').exists())

    def test_create_product_invalid(self):
        """
        Test that creating a product with invalid data fails.
        """
        url = reverse('create-product')
        data = {
            'name': '',  # Invalid: Name is required
            'description': 'Another test product',
            'price': 20.00,
            'available_stock': 50
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "This field may not be blank.")  # Adjusted to match the actual message

    def test_select_product(self):
        url = reverse('product-select', kwargs={'product_id': self.product.id})
        response = self.client.post(url)
        self.product.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.product.selected_by, self.user)

    def test_select_already_selected_product(self):
        another_user = User.objects.create_user(
            email='otheruser@example.com', password='testpass123', name='Another User', tc=True
        )
        self.product.selected_by = another_user
        self.product.save()

        url = reverse('product-select', kwargs={'product_id': self.product.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Product already selected by another user.', str(response.data))

    def test_report_product(self):
        url = reverse('product-report', kwargs={'product_id': self.product.id})
        data = {'reason': 'Defective'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(ProductReport.objects.filter(reason='Defective').exists())

    def test_report_non_existent_product(self):
        """
        Test that reporting a non-existent product returns a 404 error.
        """
        url = reverse('product-report', kwargs={'product_id': 999})  # Non-existent product ID
        data = {'reason': 'Defective'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Expecting 404 status for non-existent product
