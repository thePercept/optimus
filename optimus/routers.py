from rest_framework import routers
from api.views import DealViewSet

router = routers.SimpleRouter()
router.register(r'deals',DealViewSet)