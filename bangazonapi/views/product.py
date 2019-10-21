
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Product
from bangazonapi.models import Customer
from bangazonapi.models import ProductCategory
from bangazonapi.models import OrderProduct
from bangazonapi.models import Order
from .customer import CustomerSerializer


# Author: Danny Barker
# Purpose: Allow a user to communicate with the Bangazon database to GET PUT
# POST and DELETE entries.
# Methods: GET PUT(id) POST DELETE

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for product

    Arguments:
        serializers
    """
    customer = CustomerSerializer(many=False)
    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'price', 'description', 'quantity', 'created_date', 'location', 'number_sold', 'customer', 'image', 'product_category', 'avg_rating')
        depth = 2


class Products(ViewSet):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Product instance
        """
        new_product = Product()
        new_product.name = request.data["name"]
        new_product.price = request.data["price"]
        new_product.description = request.data["description"]
        new_product.quantity = request.data["quantity"]
        new_product.created_date = request.data["created_date"]
        new_product.location = request.data["location"]

        customer = Customer.objects.get(user=request.auth.user)
        new_product.customer = customer

        product_category = ProductCategory.objects.get(pk=request.data["product_category_id"])
        new_product.product_category = product_category

        new_product.save()

        serializer = ProductSerializer(new_product, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single product
        Returns:
            Response -- JSON serialized product instance
        """
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, context={'request': request})

            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a product attraction

        Returns:
            Response -- Empty body with 204 status code
        """
        product = Product.objects.get(pk=pk)
        product.quantity = request.data["quantity"]
        product.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single product

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            product = Product.objects.get(pk=pk)
            product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def list(self, request):
        """Handle GET requests to product resource

        Returns:
            Response -- JSON serialized list of product
        """

        # products = Product.objects.all()
        products = Product.objects.all()


        # Support filtering attractions by area id
        category = self.request.query_params.get('category', None)
        quantity = self.request.query_params.get('quantity', None)
        product_customer = self.request.query_params.get('customer', None)
        location = self.request.query_params.get('location', None)
# Location param is for home page search bar, which is querying location properties on prodcuts and sending back matching products
# location__iexact is filtering by location string regardless of case
        if location is not None:
            products = products.filter(location__iexact=location, quantity__gte=1)

        if category is not None:
            products = products.filter(product_category__id=category, quantity__gte=1)

        if quantity is not None:
            quantity = int(quantity)
            products = products.filter(quantity__gte=1).order_by("-created_date")[:quantity]

        if product_customer is not None:
            customer_products = Customer.objects.get(user=request.auth.user).seller.all()
            products = customer_products

        serializer = ProductSerializer(products, many=True, context={'request': request})

        return Response(serializer.data)