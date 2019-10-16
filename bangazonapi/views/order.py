"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Order, Payment, Customer

'''
auther: Tyler Carpenter
purpose: Allow a user to communicate with the Bangazon database to GET PUT POST and DELETE entries.
methods: all
'''

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for order

    Arguments:
        serializers
    """


    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order',
            lookup_field='id'
        )
        fields = ('id', 'url', 'created_date', 'payment_type', "customer")
        depth = 1


class Orders(ViewSet):
    """Park Areas for Kennywood Amusement Park"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized ParkArea instance
        """
        neworder = Order()
        neworder.created_date = request.data["created_date"]
        customer = Customer.objects.get(id=request.data["customer_id"])
        neworder.customer = customer
        neworder.save()

        serializer = OrderSerializer(neworder, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for order

        Returns:
            Response -- JSON serialized order
        """
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area

        Returns:
            Response -- Empty body with 204 status code
        """
        ordered_products = set()
        order = Order.objects.get(pk=pk)
        payment = Payment.objects.get(pk=request.data["payment_type"])
        order.payment_type = payment
        order.save()
        if order.payment_type is not "NULL":
            ordered_items = order.invoiceline.all()

            for oi in ordered_items:
                ordered_products.add(oi.product)

            products = list(ordered_products)

            for p in products:
                num_sold = p.item.filter(order=order).count()
                p.quantity = p.new_inventory(num_sold)
                p.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park are

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            order = Order.objects.get(pk=pk)
            order.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to park areas resource

        Returns:
            Response -- JSON serialized list of park areas
        """
        orders = Order.objects.all()

        customer = self.request.query_params.get('customer_id', None)
        complete = self.request.query_params.get('complete', None)
        payment = self.request.query_params.get('payment_id', None)
        if customer is not None:
            if complete == "1":
                orders = orders.filter(customer__id=customer, payment_type__id__isnull=True)
            if complete == "0":
                orders = orders.filter(customer__id=customer, payment_type__id__isnull=False)

        if payment is not None:
            orders = orders.filter(payment_type__id=payment)

        if complete is not None and customer is None:
            complete_bool = bool(complete)
            orders = orders.filter(payment_type__id__isnull=complete_bool)

        serializer = OrderSerializer(
            orders, many=True, context={'request': request})
        return Response(serializer.data)
