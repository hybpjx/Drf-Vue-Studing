from rest_framework.routers import DefaultRouter
from .views import StuApiViewSet

router = DefaultRouter()

router.register(prefix="stu", viewset=StuApiViewSet, basename="stu")

urlpatterns = [
              ] + router.urls
