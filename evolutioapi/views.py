from django.http import JsonResponse
from .models import Order, Delivery, DeliveryProduct
from collections import Counter

def orders_and_deliveries_by_brand(request):
    brand_id = request.GET.get('brand')

    # Check if brand_id is present in the request
    if brand_id is None:
        return JsonResponse({'error': 'Brand ID is required'}, status=400)

    # Validate that brand_id is a valid integer
    try:
        brand_id = int(brand_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid value for brand ID. It must be an integer.'}, status=400)

    # Fetch orders for the given brand_id
    orders = Order.objects.filter(brand_id=brand_id)

    # Check if any orders are found
    if not orders:
        return JsonResponse({'message': 'No orders found for the given brand ID.'}, status=404)

    orders_data = []

    for order in orders:
        deliveries_data = []
        deliveries = order.delivery_set.all()

    for order in orders:
        deliveries_data = []
        deliveries = order.delivery_set.all()

        for delivery in deliveries:
            products_data = []
            delivery_products = DeliveryProduct.objects.filter(delivery=delivery)

            for delivery_product in delivery_products:
                product_data = {
                    'product_name': delivery_product.product.name,
                    'quantity': delivery_product.quantity,
                }
                products_data.append(product_data)

            # Convert datetime to string without timezone offset
            delivery_data = {
                'id': delivery.id,
                'order_id': delivery.order.id,
                'shipped': delivery.shipped,
                'products': products_data,
            }
            deliveries_data.append(delivery_data)

        # Convert datetime to string without timezone offset
        order_data = {
            'id': order.id,
            'brand_id': order.brand_id,
            'customer_name': order.customer_name,
            'reference': order.reference,
            'order_date': order.order_date.strftime("%Y-%m-%d %H:%M:%S.%f"),
            'price_total': str(order.price_total),
            'deliveries': deliveries_data,
        }
        orders_data.append(order_data)

    return JsonResponse({'orders': orders_data})


def shipped_products(request):
    order_id = request.GET.get('id')
    reference = request.GET.get('reference')

    # Check if either id or reference parameter is provided
    if not order_id and not reference:
        return JsonResponse({'error': 'id or reference parameter is required'}, status=400)

    try:
        # Try to get the order based on id or reference
        if order_id:
            order_id_int = int(order_id)
            order = Order.objects.get(id=order_id_int)

        elif reference:
            order = Order.objects.get(reference=reference)

    except ValueError:
        return JsonResponse({'error': 'Invalid value for id parameter. It must be an integer.'}, status=400)
    
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)

    try:
        # Retrieve delivered products for the given order
        deliveries = Delivery.objects.filter(order=order, shipped=True)
        
        # Count quantities
        shipped_products_counter = Counter()
        
        for delivery in deliveries:
            delivery_products = DeliveryProduct.objects.filter(delivery=delivery)
            
            for delivery_product in delivery_products:
                shipped_products_counter[delivery_product.product.name] += delivery_product.quantity

    except Exception as e:
        return JsonResponse({'error': f'Error processing delivery products: {str(e)}'}, status=500)

    # Convert Counter object to a list
    result = [{'product_name': key, 'quantity': value} for key, value in shipped_products_counter.items()]

    return JsonResponse({'shipped_products': result})