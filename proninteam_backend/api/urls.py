from rest_framework.routers import DefaultRouter
from api.views import CollectionViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r"collections", CollectionViewSet, basename="collection")
router.register(r"payments", PaymentViewSet, basename="payment")

urlpatterns = router.urls
