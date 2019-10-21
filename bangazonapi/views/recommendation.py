"""
   Author: Danny Barker
   Purpose: To convert recommendation data to json
   Methods: GET, POST
"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Recommendation
from bangazonapi.models import Customer
from bangazonapi.models import Product


class RecommendationSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    class Meta:
        model = Recommendation
        url = serializers.HyperlinkedIdentityField(
            view_name='recommendation',
            lookup_field='id'
        )
        fields = ('id', 'url', 'customer', 'product', 'recommender', 'is_shown')
        depth = 2


class Recommendations(ViewSet):

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized product category instance
        """
        new_recommendation = Recommendation()
        customer = Customer.objects.get(pk=request.data["customer_id"])
        new_recommendation.customer = customer
        product = Product.objects.get(pk=request.data["product_id"])
        new_recommendation.product = product
        recommender = Customer.objects.get(user=request.auth.user)
        new_recommendation.recommender = recommender
        new_recommendation.save()

        serializer = RecommendationSerializer(new_recommendation, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            category = Recommendation.objects.get(pk=pk)
            serializer = RecommendationSerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to park Recommendations resource

        Returns:
            Response -- JSON serialized list of park Recommendations
        """
        recommendation = Recommendation.objects.all()
        user = self.request.query_params.get('user', None)

        if user is not None:
            customer = Customer.objects.get(user=request.auth.user)
            recommendation = recommendation.filter(customer=customer)

        serializer = RecommendationSerializer(
            recommendation, many=True, context={'request': request})
        return Response(serializer.data)