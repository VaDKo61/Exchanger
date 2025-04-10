from django.http import HttpResponseForbidden
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from ads.models import Ad, ExchangeProposal
from ads.pagination import StandardResultsSetPagination
from ads.serializers import AdSerializer, ProposalSerializer, ProposalUpdateSerializer


class AdViewSet(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    queryset = Ad.objects.all().order_by('id')
    serializer_class = AdSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('title', 'description')
    filterset_fields = ('category', 'condition')

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user_id != request.user.id:
            return HttpResponseForbidden('You are not the author')
        else:
            return super().update(request, *args, **kwargs)


class ProposalViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      GenericViewSet):
    queryset = ExchangeProposal.objects.all().order_by('id')
    serializer_class = ProposalSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['ad_sender', 'ad_receiver', 'status']

    def get_serializer_class(self):
        if self.action == 'update':
            return ProposalUpdateSerializer
        return ProposalSerializer
