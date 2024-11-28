from rest_framework.routers import SimpleRouter

from products.apps import ProductsConfig
from products.views import ProductViewSet

app_name = ProductsConfig.name

router = SimpleRouter()
router.register("", ProductViewSet)

urlpatterns = []
urlpatterns += router.urls
