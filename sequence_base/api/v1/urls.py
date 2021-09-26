from django.urls import path

from sequence_base.api.v1.views import SequenceCreateView, StatsListView

urlpatterns = [
    path('sequence/', SequenceCreateView.as_view(), name="sequence"),
    path('stats', StatsListView.as_view(), name="stats"),
]
