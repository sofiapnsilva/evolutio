from django.test import TestCase, Client
from django.urls import reverse
from .models import Order, Delivery, DeliveryProduct, Product
from datetime import datetime

class OrdersAndDeliveriesByBrandTest(TestCase):
    def setUp(self):
        # Create brand, order, and product
        self.product = Product.objects.create(name="Product A")

        self.order = Order.objects.create(
            brand_id=1,
            customer_name="John Doe",
            reference="#123",
            order_date=datetime.strptime("2022-01-01 12:00:00", "%Y-%m-%d %H:%M:%S"),
            price_total=100.00
        )

        self.delivery = Delivery.objects.create(order=self.order, shipped=True)
        self.delivery_product1 = DeliveryProduct.objects.create(
            delivery=self.delivery,
            product=self.product,
            quantity=5
        )

        self.order2 = Order.objects.create(
            brand_id=2,
            customer_name="Joana Doe",
            reference="#125",
            order_date=datetime.strptime("2022-01-01 12:00:00", "%Y-%m-%d %H:%M:%S"),
            price_total=100.00
        )

        self.delivery2 = Delivery.objects.create(order=self.order, shipped=True)
        self.delivery_product2 = DeliveryProduct.objects.create(
            delivery=self.delivery2,
            product=self.product,
            quantity=3
        )

        self.order3 = Order.objects.create(
            brand_id=2,
            customer_name="James Doe",
            reference="#12556",
            order_date=datetime.strptime("2022-01-01 12:00:00", "%Y-%m-%d %H:%M:%S"),
            price_total=990.00
        )

        self.delivery3 = Delivery.objects.create(order=self.order, shipped=False)
        self.delivery_product3 = DeliveryProduct.objects.create(
            delivery=self.delivery3,
            product=self.product,
            quantity=2
        )

    
    def test_orders_and_deliveries_by_brand(self):
        client = Client()

        url = reverse('orders_and_deliveries_by_brand')

        # Make a valid GET request
        response = client.get(url, {'brand': 1})

        # Check that the response has a 200 status code (positive)
        self.assertEqual(response.status_code, 200)

        # Parse the response JSON
        data = response.json()

        # Check specific fields
        order_data = data['orders'][0]
        self.assertIn('id', order_data)
        self.assertEqual(order_data['id'], self.order.id)

        self.assertIn('brand_id', order_data)
        self.assertEqual(order_data['brand_id'], self.order.brand_id)

        self.assertIn('customer_name', order_data)
        self.assertEqual(order_data['customer_name'], self.order.customer_name)

        self.assertIn('reference', order_data)
        self.assertEqual(order_data['reference'], self.order.reference)

        self.assertIn('order_date', order_data)
        self.assertTrue(order_data['order_date'].startswith(str(self.order.order_date.date())))

        self.assertIn('price_total', order_data)
        self.assertEqual(float(order_data['price_total']), float(str(self.order.price_total)))

        self.assertIn('deliveries', order_data)
        self.assertIsInstance(order_data['deliveries'], list)
        self.assertEqual(len(order_data['deliveries']), 3)

        # Make a GET request without the brand parameter
        response = client.get(url)

        # Check that the response has a 400 status code (error)
        self.assertEqual(response.status_code, 400)

        data = response.json()

        # Check that the expected error message is present in the response
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Brand ID is required')

        # Make a GET request with a non-integer brand parameter
        response = client.get(url, {'brand': 'invalid'})

        # Check that the response has a 400 status code
        self.assertEqual(response.status_code, 400)

        # Parse the response JSON
        data = response.json()

        # Check that the expected error message is present in the response
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Invalid value for brand ID. It must be an integer.')

        # Make a GET request with a non-existing brand
        response = client.get(url, {'brand': 999})

        # Check that the response has a 400 status code
        self.assertEqual(response.status_code, 404)

        # Parse the response JSON
        data = response.json()

        # Check that the expected key 'error' is present in the response
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'No orders found for the given brand ID.')

        # Clean up created objects after the test
        self.order.delete()
        self.delivery.delete()
        self.product.delete()


    def test_shipped_products_by_id(self):
        client = Client()

        url = reverse('shipped_products')

        # Make a GET request with an existing order ID
        response = client.get(url, {'id': self.order.id})

        # Check that the response has a 200 status code (positive)
        self.assertEqual(response.status_code, 200)

        # Parse the response JSON
        data = response.json()

        # Check that the expected key 'shipped_products' is present in the response
        self.assertIn('shipped_products', data)
        self.assertIsInstance(data['shipped_products'], list)

        # Check if the product quantities are correct
        self.assertEqual(len(data['shipped_products']), 1)
        self.assertEqual(data['shipped_products'][0]['product_name'], 'Product A')
        self.assertEqual(data['shipped_products'][0]['quantity'], 8) 

        # Make a GET request with a non-existing order ID
        response = client.get(url, {'id': 999})

        # Check that the response has a 404 status code
        self.assertEqual(response.status_code, 404)

        # Parse the response JSON
        data = response.json()

        # Check that the expected key 'error' is present in the response
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Order not found')

        # Make a GET request with a non-integer order ID
        response = client.get(url, {'id': 'invalid'})

        # Check that the response has a 400 status code
        self.assertEqual(response.status_code, 400)

        # Parse the response JSON
        data = response.json()

        # Check that the expected key 'error' is present in the response
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Invalid value for id parameter. It must be an integer.')

        # Clean up created objects after the test
        self.order.delete()
        self.delivery.delete()
        self.product.delete()
        self.order2.delete()
        self.delivery2.delete()
        self.order3.delete()
        self.delivery3.delete()


    def test_shipped_products_by_reference(self):
        client = Client()

        url = reverse('shipped_products')

        # Make a GET request with an existing order reference
        response = client.get(url, {'reference': '#123'})

        # Check that the response has a 200 status code (positive)
        self.assertEqual(response.status_code, 200)

        # Parse the response JSON
        data = response.json()

        # Check that the expected key 'shipped_products' is present in the response
        self.assertIn('shipped_products', data)
        self.assertIsInstance(data['shipped_products'], list)

        # Check if the product quantities are correct
        self.assertEqual(len(data['shipped_products']), 1)
        self.assertEqual(data['shipped_products'][0]['product_name'], 'Product A')
        self.assertEqual(data['shipped_products'][0]['quantity'], 8)
        
        # Make a GET request with a non-existing order reference
        response = client.get(url, {'reference': 'nonexistent'})

        # Check that the response has a 404 status code
        self.assertEqual(response.status_code, 404)

        # Parse the response JSON
        data = response.json()

        # Check that the expected key 'error' is present in the response
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Order not found')

        # Clean up created objects after the test
        self.order.delete()
        self.delivery.delete()
        self.product.delete()
        self.order2.delete()
        self.delivery2.delete()
        self.order3.delete()
        self.delivery3.delete()
