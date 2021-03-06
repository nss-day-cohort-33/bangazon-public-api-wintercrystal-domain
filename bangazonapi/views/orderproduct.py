"""
   Author: Daniel Krusch
   Purpose: To convert order products data to json
   Methods: GET, DELETE, POST
"""

"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import OrderProduct, Order, Product, Customer
from .product import ProductSerializer
from .order import OrderSerializer
import datetime


class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    product = ProductSerializer(many=False)
    class Meta:
        model = OrderProduct
        url = serializers.HyperlinkedIdentityField(
            view_name='orderproduct',
            lookup_field='id'
        )
        fields = ('id', 'url', 'order', 'product', 'quantity')
        depth = 2

class OrderProducts(ViewSet):
    """Park Areas for Kennywood Amusement Park"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized product category instance
        """
        new_order_product = OrderProduct()
        new_order_product.product = Product.objects.get(pk=request.data["product"])
        # new_order_product.order = request.data["order_id"]
        # new_order_product.product = request.data["product_id"]
        new_order_product.quantity = request.data["quantity"]
        customer = Customer.objects.get(user=request.auth.user)
        try:
            neworder = Order.objects.get(customer=customer, payment_type__isnull=True)
        except Order.DoesNotExist:
            neworder = Order()
            neworder.created_date = datetime.date.today()
            neworder.customer = customer
            neworder.save()


        new_order_product.order = neworder
        new_order_product.save()
        # if order.payment_type is not "NULL":
        #     ordered_items = order.invoiceline.all()

        #     for oi in ordered_items:
        #         ordered_products.add(oi.product)

        #     products = list(ordered_products)

        #     for p in products:
        #         num_sold = p.item.filter(order=order).count()
        #         p.quantity = p.new_inventory(num_sold)
        #         p.save()

        serializer = OrderProductSerializer(new_order_product, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            order_product = OrderProduct.objects.get(pk=pk)
            serializer = OrderProductSerializer(order_product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area ItineraryItem

        Returns:
            Response -- Empty body with 204 status code
        """
        new_order_product = OrderProduct.objects.get(pk=pk)
        new_order_product.quantity = request.data["quantity"]
        new_order_product.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park are

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            order_product = OrderProduct.objects.get(pk=pk)
            order_product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except order_product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to park OrderProducts resource

        Returns:
            Response -- JSON serialized list of park OrderProducts
        """
        OrderProducts = OrderProduct.objects.all()
        # ordered_products = set()

        # Support filtering OrderProducts by area id
        # area = self.request.query_params.get('area', None)
        # if area is not None:
        #     OrderProducts = OrderProducts.filter(area__id=area)
        productId = self.request.query_params.get('product_id', None)
        order = self.request.query_params.get('order_id', None)
        if order is not None:
            OrderProducts = OrderProducts.filter(order__id=order)
            # if productId is None:
            #     for op in OrderProducts:
            #         ordered_products.add(op.product)

            #     product_items = list(ordered_products)

            #     for p in product_items:
            #         num = p.item.filter(order__id=order).count()
            #         p.new_cart(num)
            #         p.save()

        if productId is not None:
            OrderProducts = OrderProducts.filter(product__id=productId)

        serializer = OrderProductSerializer(
            OrderProducts, many=True, context={'request': request})
        return Response(serializer.data)
