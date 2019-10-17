"""
   Author: Danny Barker
   Purpose: To convert rating data to json
   Methods: GET, POST
"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Rating
from bangazonapi.models import Customer
from bangazonapi.models import Product


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    class Meta:
        model = Rating
        url = serializers.HyperlinkedIdentityField(
            view_name='Rating',
            lookup_field='id'
        )
        fields = ('id', 'url', 'customer', 'product', 'score')
        depth = 2


class Ratings(ViewSet):

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized product category instance
        """
        new_rating = Rating()
        customer = Customer.objects.get(user=request.auth.user)
        new_rating.customer = customer
        product = Product.objects.get(pk=request.data["product_id"])
        new_rating.product = product
        new_rating.recommender = request.data["score"]
        new_rating.save()

        serializer = RatingSerializer(new_rating, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            category = Rating.objects.get(pk=pk)
            serializer = RatingSerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to park Ratings resource

        Returns:
            Response -- JSON serialized list of park Ratings
        """
        rating = Rating.objects.all()

        serializer = RatingSerializer(
            rating, many=True, context={'request': request})
        return Response(serializer.data)