from rest_framework.routers import DefaultRouter
from api.views import CollectionViewSet, PaymentViewSet, UserViewSet

router = DefaultRouter()
router.register(r"collections", CollectionViewSet, basename="collection")
router.register(r"payments", PaymentViewSet, basename="payment")
router.register(r"users", UserViewSet, basename="users")

urlpatterns = router.urls
