"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Image

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    class Meta:
        model = Image
        url = serializers.HyperlinkedIdentityField(
            view_name='image',
            lookup_field='id'
        )
        fields = ('id', 'url', 'product_pic',)
        # depth = 2


class Images(ViewSet):
    """Park Areas for Kennywood Amusement Park"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Product instance
        """
        new_image = Image()
        new_image.product_pic = request.data["product_pic"]

        new_image.save()

        serializer = ImageSerializer(new_image, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            image = Image.objects.get(pk=pk)
            serializer = ImageSerializer(image, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area attraction

        Returns:
            Response -- Empty body with 204 status code
        """
        image = Image.objects.get(pk=pk)
        image.product_pic = request.data["product_pic"]
        image.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park are

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            image = Image.objects.get(pk=pk)
            image.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Image.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to park attractions resource

        Returns:
            Response -- JSON serialized list of park attractions
        """
        images = Image.objects.all()

        # Support filtering attractions by area id
        # area = self.request.query_params.get('area', None)
        # if area is not None:
        #     attractions = attractions.filter(area__id=area)

        serializer = ImageSerializer(
            images, many=True, context={'request': request})
        return Response(serializer.data)
