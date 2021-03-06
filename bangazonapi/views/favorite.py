from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Customer, Favorite
from .customer import CustomerSerializer
from .product import ProductSerializer





class FavoriteCustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for customers
    Author: Dustin Hobson

    Arguments:
        serializers
    """
    products = ProductSerializer(many=True)
    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field = 'id'

        )
        fields = ('id', 'products', 'user')
        depth = 1

"""
   Author: Mary West
   Methods: GET, POST
"""

"""View module for handling requests about park areas"""

class FavoriteSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    seller = FavoriteCustomerSerializer(many=False)
    class Meta:
        model = Favorite
        url = serializers.HyperlinkedIdentityField(
            view_name='favorite',
            lookup_field='id'
        )
        fields = ('id', 'url', 'seller')
        depth = 2

class Favorites(ViewSet):
    """Park Areas for Kennywood Amusement Park"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized product category instance
        """
        new_favorite = Favorite()
        customer = Customer.objects.get(user=request.auth.user)
        new_favorite.customer = customer

        seller = Customer.objects.get(pk=request.data["seller_id"])
        new_favorite.seller = seller
        new_favorite.save()

        serializer = FavoriteSerializer(new_favorite, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            single_favorite = Favorite.objects.get(pk=pk)
            serializer = FavoriteSerializer(single_favorite, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):
        """Handle GET requests to park Ratings resource

        Returns:
            Response -- JSON serialized list of park Ratings
        """
        customer = Customer.objects.get(user=request.auth.user)
        sellers_i_love = Favorite.objects.filter(customer=customer)

        serializer = FavoriteSerializer(
            sellers_i_love, many=True, context={'request': request})
        return Response(serializer.data)
