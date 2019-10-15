"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Product, Customer, CustomerProductPreference

'''
auther: Tyler Carpenter
purpose: Allow a user to communicate with the Bangazon database to GET PUT POST and DELETE entries.
methods: all
'''

class CustomerProductPreferenceSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for order

    Arguments:
        serializers
    """


    class Meta:
        model = CustomerProductPreference
        url = serializers.HyperlinkedIdentityField(
            view_name='customerproductpreference',
            lookup_field='id'
        )
        fields = ('id', 'url', 'user', 'product', "like")
        depth = 1


class CustomerProductPreferences(ViewSet):
    """Park Areas for Kennywood Amusement Park"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized ParkArea instance
        """
        new_preference = CustomerProductPreference()
        user = Customer.objects.get(user=request.auth.user)
        product = Product.objects.get(id=request.data["product"])
        new_preference.user = user
        new_preference.product = product
        new_preference.like = request.data["like"]
        new_preference.save()

        serializer = CustomerProductPreferenceSerializer(new_preference, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for order

        Returns:
            Response -- JSON serialized order
        """
        try:
            customer_preference = CustomerProductPreference.objects.get(pk=pk)
            serializer = CustomerProductPreferenceSerializer(customer_preference, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area

        Returns:
            Response -- Empty body with 204 status code
        """
        customer_preference = CustomerProductPreference.objects.get(pk=pk)
        customer_preference.like = request.data["like"]
        customer_preference.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park are

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            customer_preference = CustomerProductPreference.objects.get(pk=pk)
            customer_preference.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except CustomerProductPreference.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to park areas resource

        Returns:
            Response -- JSON serialized list of park areas
        """
        customer_preferences = CustomerProductPreference.objects.all()

        like = self.request.query_params.get('like', None)
        if like is not None:
            customer_preferences = customer_preferences.filter(like=like)

        serializer = CustomerProductPreferenceSerializer(
            customer_preferences, many=True, context={'request': request})
        return Response(serializer.data)
