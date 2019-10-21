from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Customer
from django.contrib.auth.models import User
from .user import UserSerializer



class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    # """JSON serializer for customers
    # Author: Dustin Hobson

    # Arguments:
    #     serializers
    # """
    # Depth of one allows user object to be seen on Customer
    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field = 'id'

        )
        fields = ('id', 'url', 'user', 'phone_number', 'address', 'avg_rating', 'full_name')
        depth = 1


class Customers(ViewSet):
    # """Customers for Bangazon
    # Author: Dustin Hobson
    # Purpose: Allow a user to communicate with the Bangazon database to GET PUT POST and DELETE Customers.
    # Methods: GET PUT(id) POST
    # """

    def create(self, request):
        # """Handle POST operations
        # Author: Dustin Hobson
        # Purpose: Allow a user to communicate with the Bangazon database to create new customer
        # Methods:  POST
        # Returns:
        #     Response -- JSON serialized Customer instance
        # """
        new_customer = Customer()
        new_customer.phone_number = request.data["phone_number"]
        new_customer.address = request.data["address"]
        # Grab the Customer object based on the user ID
        # This + User view allows you to see the entire user object on the Customer instance
        user = Customer.objects.get(user=request.auth.user)
        new_customer.user = user

        new_customer.save()
        serializer = CustomerSerializer(new_customer, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        # """Handle GET requests for single customer
        # Author: Dustin Hobson
        # Purpose: Allow a user to communicate with the Bangazon database to retrieve  customer
        # Methods:  GET
        # Returns:
        #     Response -- JSON serialized customer instance
        # """
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        # """Handle PUT requests for a customer
        # Author: Dustin Hobson
        # Purpose: Allow a user to communicate with the Bangazon database to update  customer's 'is_active property
        # Methods:  PUT
        # Returns:
        #     Response -- Empty body with 204 status code
        # """
        user = User.objects.get(pk=request.auth.user.id)
        user.last_name = request.data["last_name"]
        user.save()

        customer = Customer.objects.get(user=user)
        customer.address = request.data["address"]
        customer.phone_number = request.data["phone_number"]
        customer.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def list(self, request):
        # """Handle GET requests to customers resource

        # Author: Dustin Hobson
        # Purpose: Allow a user to communicate with the Bangazon database to list Customers        Methods:  GET
        # Returns:
        #     Response -- JSON serialized list of park areas
        # """
        customers = Customer.objects.all()

        name = self.request.query_params.get('name', None)

        if name is not None:
            customers = customers.filter(user__first_name__iexact=name)

        serializer = CustomerSerializer(customers, many=True, context={'request': request})

        return Response(serializer.data)