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
from bangazonapi.models import OrderProduct, Order, Product


class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    class Meta:
        model = OrderProduct
        url = serializers.HyperlinkedIdentityField(
            view_name='orderproduct',
            lookup_field='id'
        )
        fields = ('id', 'url', 'order_id', 'product_id', 'quantity')

class OrderProducts(ViewSet):
    """Park Areas for Kennywood Amusement Park"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized product category instance
        """
        new_order_product = OrderProduct()
        new_order_product.order = Order.objects.get(pk=request.data["order_id"])
        new_order_product.product = Product.objects.get(pk=request.data["product_id"])
        # new_order_product.order = request.data["order_id"]
        # new_order_product.product = request.data["product_id"]
        new_order_product.quantity = request.data["quantity"]
        new_order_product.save()

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

        # Support filtering OrderProducts by area id
        # area = self.request.query_params.get('area', None)
        # if area is not None:
        #     OrderProducts = OrderProducts.filter(area__id=area)
        product = self.request.query_params.get('product_id', None)
        order = self.request.query_params.get('order_id', None)
        if order is not None:
            OrderProducts = OrderProducts.filter(order__id=order)
        if product is not None:
            OrderProducts = OrderProducts.filter(product__id=product)

        serializer = OrderProductSerializer(
            OrderProducts, many=True, context={'request': request})
        return Response(serializer.data)
