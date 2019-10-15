"""
   Author: Mary West
   Methods: GET, POST
"""

"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Customer, Favorite


class FavoriteSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    class Meta:
        model = Favorite
        url = serializers.HyperlinkedIdentityField(
            view_name='favorite',
            lookup_field='id'
        )
        fields = ('id', 'url', 'customer', 'seller')
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
        new_favorite.customer = seller
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
        favorite = Favorite.objects.all()

        serializer = FavoriteSerializer(
            favorite, many=True, context={'request': request})
        return Response(serializer.data)
