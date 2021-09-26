from rest_framework import generics, status
from django.http import JsonResponse

from sequence_base.services import SequenceService


class StatsListView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        stats = SequenceService().get_stats()
        return JsonResponse(stats, status=status.HTTP_200_OK)
