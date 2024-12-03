from rest_framework.routers import SimpleRouter

from sellers.apps import SellersConfig
from sellers.views import SellerViewSet

app_name = SellersConfig.name

router = SimpleRouter()
router.register("", SellerViewSet)

urlpatterns = []
urlpatterns += router.urls
