from django.urls import path, include
from rest_framework import routers

from ads.views import AdViewSet, ProposalViewSet

router = routers.SimpleRouter()
router.register(r'ad', AdViewSet)
router.register(r'proposal', ProposalViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
