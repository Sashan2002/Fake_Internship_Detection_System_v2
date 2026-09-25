from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.advertisements.models import Advertisement
from apps.advertisements.serializers import AdvertisementSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def create_advertisement(request):
    serializer = AdvertisementSerializer(data=request.data)
    if not serializer.is_valid():
        errors = [str(e) for field_errors in serializer.errors.values() for e in field_errors]
        return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
    advertisement = serializer.save()
    return Response({"advertisement_id": advertisement.id}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_advertisement(request, advertisement_id):
    try:
        advertisement = Advertisement.objects.get(pk=advertisement_id)
    except Advertisement.DoesNotExist:
        return Response({"errors": ["Advertisement not found"]}, status=404)
    return Response(AdvertisementSerializer(advertisement).data, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])
def list_for_user(request, user_id):
    advertisements = Advertisement.objects.filter(user_id=user_id)
    return Response(AdvertisementSerializer(advertisements, many=True).data, status=200)
