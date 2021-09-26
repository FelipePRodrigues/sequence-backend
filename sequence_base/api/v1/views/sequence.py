from django.http import JsonResponse
from rest_framework import generics, status

from sequence_base.api.v1.serializers import SequenceCreateSerializer
from sequence_base.services import SequenceService


class SequenceCreateView(generics.CreateAPIView):
    serializer_class = SequenceCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = SequenceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        is_valid = SequenceService().is_valid_sequence(serializer.data.get('letters'))
        return JsonResponse({"is_valid": is_valid}, status=status.HTTP_200_OK)
