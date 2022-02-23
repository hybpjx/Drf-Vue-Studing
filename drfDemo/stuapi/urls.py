from rest_framework.routers import DefaultRouter
from .views import StuApiViewSet

router = DefaultRouter() # 可处理路由的路由器

router.register(prefix="stu", viewset=StuApiViewSet, basename="stu")

# 路由列表
urlpatterns = [
              ] + router.urls
